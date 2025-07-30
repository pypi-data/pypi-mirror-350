# Copyright (c) 2014, 2025, Oracle and/or its affiliates.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is designed to work with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation. The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have either included with
# the program or referenced in the documentation.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/Python, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

# mypy: disable-error-code="arg-type"

"""Connection class using the C Extension."""

import os
import platform
import socket
import sys
import warnings

from typing import (
    Any,
    BinaryIO,
    Dict,
    List,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

from . import version
from ._decorating import cmd_refresh_verify_options
from .abstracts import CMySQLPrepStmt, MySQLConnectionAbstract
from .constants import ClientFlag, FieldFlag, FieldType, ServerFlag, ShutdownType
from .conversion import MySQLConverter
from .errors import (
    InterfaceError,
    InternalError,
    OperationalError,
    ProgrammingError,
    get_mysql_exception,
)
from .protocol import MySQLProtocol
from .types import (
    CextEofPacketType,
    CextResultType,
    DescriptionType,
    ParamsSequenceOrDictType,
    RowType,
    StatsPacketType,
    StrOrBytes,
)
from .utils import (
    import_object,
    warn_ciphersuites_deprecated,
    warn_tls_version_deprecated,
)

HAVE_CMYSQL = False

try:
    import _mysql_connector

    from _mysql_connector import MySQLInterfaceError

    from .cursor_cext import (
        CMySQLCursor,
        CMySQLCursorBuffered,
        CMySQLCursorBufferedDict,
        CMySQLCursorBufferedRaw,
        CMySQLCursorDict,
        CMySQLCursorPrepared,
        CMySQLCursorPreparedDict,
        CMySQLCursorRaw,
    )

    HAVE_CMYSQL = True
except ImportError as exc:
    raise ImportError(
        f"MySQL Connector/Python C Extension not available ({exc})"
    ) from exc

from .opentelemetry.constants import OTEL_ENABLED
from .opentelemetry.context_propagation import with_context_propagation

if OTEL_ENABLED:
    from .opentelemetry.instrumentation import end_span, record_exception_event


class CMySQLConnection(MySQLConnectionAbstract):
    """Class initiating a MySQL Connection using Connector/C."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialization"""
        if not HAVE_CMYSQL:
            raise RuntimeError("MySQL Connector/Python C Extension not available")
        self._cmysql: Optional[
            _mysql_connector.MySQL  # pylint: disable=c-extension-no-member
        ] = None
        self._columns: List[DescriptionType] = []
        self._plugin_dir: str = os.path.join(
            os.path.dirname(os.path.abspath(_mysql_connector.__file__)),
            "mysql",
            "vendor",
            "plugin",
        )
        if platform.system() == "Linux":
            # Use the authentication plugins from system if they aren't bundled
            if not os.path.exists(self._plugin_dir):
                self._plugin_dir = (
                    "/usr/lib64/mysql/plugin"
                    if os.path.exists("/usr/lib64/mysql/plugin")
                    else "/usr/lib/mysql/plugin"
                )

        self.converter: Optional[MySQLConverter] = None
        super().__init__()

        if kwargs:
            try:
                self.connect(**kwargs)
            except Exception:
                self.close()
                raise

    def _add_default_conn_attrs(self) -> None:
        """Add default connection attributes"""
        license_chunks = version.LICENSE.split(" ")
        if license_chunks[0] == "GPLv2":
            client_license = "GPL-2.0"
        else:
            client_license = "Commercial"

        self._conn_attrs.update(
            {
                "_connector_name": "mysql-connector-python",
                "_connector_license": client_license,
                "_connector_version": ".".join([str(x) for x in version.VERSION[0:3]]),
                "_source_host": socket.gethostname(),
            }
        )

    def _do_handshake(self) -> None:
        """Gather information of the MySQL server before authentication"""
        self._handshake = {
            "protocol": self._cmysql.get_proto_info(),
            "server_version_original": self._cmysql.get_server_info(),
            "server_threadid": self._cmysql.thread_id(),
            "charset": None,
            "server_status": None,
            "auth_plugin": None,
            "auth_data": None,
            "capabilities": self._cmysql.st_server_capabilities(),
        }

        self._server_version = self._check_server_version(
            self._handshake["server_version_original"]
        )
        self._character_set.set_mysql_version(self._server_version)

    @property
    def _server_status(self) -> int:
        """Returns the server status attribute of MYSQL structure"""
        return self._cmysql.st_server_status()

    def set_allow_local_infile_in_path(self, path: str) -> None:
        """set local_infile_in_path

        Set allow_local_infile_in_path.
        """

        if self._cmysql:
            self._cmysql.set_load_data_local_infile_option(path)

    @MySQLConnectionAbstract.use_unicode.setter  # type: ignore
    def use_unicode(self, value: bool) -> None:
        self._use_unicode = value
        if self._cmysql:
            self._cmysql.use_unicode(value)
        if self.converter:
            self.converter.set_unicode(value)

    @property
    def autocommit(self) -> bool:
        """Get whether autocommit is on or off"""
        value = self.info_query("SELECT @@session.autocommit")[0]
        return value == 1

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        """Toggle autocommit"""
        try:
            self._cmysql.autocommit(value)
            self._autocommit = value
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @property
    def read_timeout(self) -> Optional[int]:
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, timeout: int) -> None:
        raise ProgrammingError(
            """
            The use of read_timeout after the connection has been established is unsupported
            in the C-Extension
            """
        )

    @property
    def write_timeout(self) -> Optional[int]:
        return self._write_timeout

    @write_timeout.setter
    def write_timeout(self, timeout: int) -> None:
        raise ProgrammingError(
            """
            Changes in write_timeout after the connection has been established is unsupported
            in the C-Extension
            """
        )

    @property
    def database(self) -> str:
        """Get the current database"""
        return self.info_query("SELECT DATABASE()")[0]  # type: ignore[return-value]

    @database.setter
    def database(self, value: str) -> None:
        """Set the current database"""
        try:
            self._cmysql.select_db(value)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @property
    def in_transaction(self) -> bool:
        """MySQL session has started a transaction"""
        return bool(self._server_status & ServerFlag.STATUS_IN_TRANS)

    def _open_connection(self) -> None:
        charset_name = self._character_set.get_info(self._charset_id)[0]
        # pylint: disable=c-extension-no-member
        self._cmysql = _mysql_connector.MySQL(
            buffered=self._buffered,
            raw=self._raw,
            charset_name=charset_name,
            connection_timeout=(self._connection_timeout or 0),
            use_unicode=self.use_unicode,
            auth_plugin=self._auth_plugin,
            plugin_dir=self._plugin_dir,
        )
        # pylint: enable=c-extension-no-member
        if not self.isset_client_flag(ClientFlag.CONNECT_ARGS):
            self._conn_attrs = {}

        cnx_kwargs = {
            "host": self._host,
            "user": self._user,
            "password": self._password,
            "password1": self._password1,
            "password2": self._password2,
            "password3": self._password3,
            "database": self._database,
            "port": self._port,
            "client_flags": self.client_flags,
            "unix_socket": self._unix_socket,
            "compress": self._compress,
            "ssl_disabled": True,
            "conn_attrs": self._conn_attrs,
            "local_infile": self._allow_local_infile,
            "load_data_local_dir": self._allow_local_infile_in_path,
            "oci_config_file": self._oci_config_file,
            "oci_config_profile": self._oci_config_profile,
            "webauthn_callback": (
                import_object(self._webauthn_callback)
                if isinstance(self._webauthn_callback, str)
                else self._webauthn_callback
            ),
            "openid_token_file": self._openid_token_file,
            "read_timeout": self._read_timeout if self._read_timeout else 0,
            "write_timeout": self._write_timeout if self._write_timeout else 0,
        }

        tls_versions = self._ssl.get("tls_versions")
        if tls_versions is not None:
            tls_versions.sort(reverse=True)  # type: ignore[union-attr]
            tls_versions = ",".join(tls_versions)
        if self._ssl.get("tls_ciphersuites") is not None:
            ssl_ciphersuites = (
                self._ssl.get("tls_ciphersuites")[0] or None  # type: ignore[index]
            )  # if it's the empty string, then use `None` instead
            tls_ciphersuites = self._ssl.get("tls_ciphersuites")[  # type: ignore[index]
                1
            ]
        else:
            ssl_ciphersuites = None
            tls_ciphersuites = None
        if (
            tls_versions is not None
            and "TLSv1.3" in tls_versions
            and not tls_ciphersuites
        ):
            tls_ciphersuites = "TLS_AES_256_GCM_SHA384"
        if not self._ssl_disabled:
            cnx_kwargs.update(
                {
                    "ssl_ca": self._ssl.get("ca"),
                    "ssl_cert": self._ssl.get("cert"),
                    "ssl_key": self._ssl.get("key"),
                    "ssl_cipher_suites": ssl_ciphersuites,
                    "tls_versions": tls_versions,
                    "tls_cipher_suites": tls_ciphersuites,
                    "ssl_verify_cert": self._ssl.get("verify_cert") or False,
                    "ssl_verify_identity": self._ssl.get("verify_identity") or False,
                    "ssl_disabled": self._ssl_disabled,
                }
            )

        if os.name == "nt" and self._auth_plugin_class == "MySQLKerberosAuthPlugin":
            cnx_kwargs["use_kerberos_gssapi"] = True

        try:
            self._cmysql.connect(**cnx_kwargs)
            self._cmysql.converter_str_fallback = self._converter_str_fallback
            if self.converter:
                self.converter.str_fallback = self._converter_str_fallback
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        self._do_handshake()

        if (
            not self._ssl_disabled
            and hasattr(self._cmysql, "get_ssl_cipher")
            and callable(self._cmysql.get_ssl_cipher)
        ):
            # Raise a deprecation warning if deprecated TLS version
            # or cipher is being used.

            # `get_ssl_cipher()` returns the name of the cipher being used.
            cipher = self._cmysql.get_ssl_cipher()
            for tls_version in set(self._ssl.get("tls_versions", [])):
                warn_tls_version_deprecated(tls_version)
                warn_ciphersuites_deprecated(cipher, tls_version)

    def close(self) -> None:
        if self._span and self._span.is_recording():
            # pylint: disable=possibly-used-before-assignment
            record_exception_event(self._span, sys.exc_info()[1])

        if not self._cmysql:
            return

        try:
            self.free_result()
            self._cmysql.close()
        except MySQLInterfaceError as err:
            if OTEL_ENABLED:
                record_exception_event(self._span, err)
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err
        finally:
            if OTEL_ENABLED:
                end_span(self._span)

    disconnect = close

    def is_closed(self) -> bool:
        """Return True if the connection to MySQL Server is closed."""
        return not self._cmysql.connected()

    def is_connected(self) -> bool:
        """Reports whether the connection to MySQL Server is available"""
        if self._cmysql:
            self.handle_unread_result()
            return self._cmysql.ping()

        return False

    def ping(self, reconnect: bool = False, attempts: int = 1, delay: int = 0) -> None:
        """Check availability of the MySQL server

        When reconnect is set to True, one or more attempts are made to try
        to reconnect to the MySQL server using the reconnect()-method.

        delay is the number of seconds to wait between each retry.

        When the connection is not available, an InterfaceError is raised. Use
        the is_connected()-method if you just want to check the connection
        without raising an error.

        Raises InterfaceError on errors.
        """
        self.handle_unread_result()

        try:
            connected = self._cmysql.ping()
        except AttributeError:
            pass  # Raise or reconnect later
        else:
            if connected:
                return

        if reconnect:
            self.reconnect(attempts=attempts, delay=delay)
        else:
            raise InterfaceError("Connection to MySQL is not available")

    def set_character_set_name(self, charset: str) -> None:
        """Sets the default character set name for current connection."""
        self._cmysql.set_character_set(charset)

    def info_query(self, query: StrOrBytes) -> Optional[RowType]:
        """Send a query which only returns 1 row"""
        first_row = ()
        try:
            self._cmysql.query(query)
            if self._cmysql.have_result_set:
                first_row = self._cmysql.fetch_row()
                if self._cmysql.fetch_row():
                    self._cmysql.free_result()
                    raise InterfaceError("Query should not return more than 1 row")
            self._cmysql.free_result()
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        return first_row

    @property
    def connection_id(self) -> Optional[int]:
        """MySQL connection ID"""
        try:
            return self._cmysql.thread_id()
        except MySQLInterfaceError:
            pass  # Just return None

        return None

    def get_rows(
        self,
        count: Optional[int] = None,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[List[RowType], Optional[CextEofPacketType]]:
        """Get all or a subset of rows returned by the MySQL server"""
        unread_result = prep_stmt.have_result_set if prep_stmt else self.unread_result
        if not (self._cmysql and unread_result):
            raise InternalError("No result set available")

        if raw is None:
            raw = self._raw

        rows: List[Tuple] = []
        if count is not None and count <= 0:
            raise AttributeError("count should be 1 or higher, or None")

        counter = 0
        try:
            fetch_row = prep_stmt.fetch_row if prep_stmt else self._cmysql.fetch_row
            if self.converter or raw:
                # When using a converter class or `raw`, the C extension should not
                # convert the values. This can be accomplished by setting
                # the raw option to True.
                self._cmysql.raw(True)

            row = fetch_row()
            while row:
                row = list(row)

                if not self._cmysql.raw() and not raw:
                    # `not _cmysql.raw()` means the c-ext conversion layer will happen.
                    # `not raw` means the caller wants conversion to happen.
                    # For a VECTOR type, the c-ext conversion layer cannot return
                    # an array.array type since such a type isn't part of the Python/C
                    # API. Therefore, the c-ext will treat VECTOR types as if they
                    # were BLOB types - be returned as `bytes` always.
                    # Hence, a VECTOR type must be cast to an array.array type using the
                    # built-in python conversion layer.
                    # pylint: disable=protected-access
                    for i, dsc in enumerate(self._columns):
                        if dsc[1] == FieldType.VECTOR:
                            row[i] = MySQLConverter._vector_to_python(row[i])

                if not self._raw and self.converter:
                    for i, _ in enumerate(row):
                        if not raw:
                            row[i] = self.converter.to_python(self._columns[i], row[i])

                rows.append(tuple(row))
                counter += 1

                if count and counter == count:
                    break

                row = fetch_row()
            if not row:
                _eof: Optional[CextEofPacketType] = self.fetch_eof_columns(prep_stmt)[
                    "eof"
                ]  # type: ignore[assignment]
                if prep_stmt:
                    prep_stmt.free_result()
                    self._unread_result = False
                else:
                    self.free_result()
            else:
                _eof = None
        except MySQLInterfaceError as err:
            if prep_stmt:
                prep_stmt.free_result()
            else:
                self.free_result()
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        return rows, _eof

    def get_row(
        self,
        binary: bool = False,
        columns: Optional[List[DescriptionType]] = None,
        raw: Optional[bool] = None,
        prep_stmt: Optional[CMySQLPrepStmt] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[RowType], Optional[CextEofPacketType]]:
        """Get the next rows returned by the MySQL server"""
        try:
            rows, eof = self.get_rows(
                count=1,
                binary=binary,
                columns=columns,
                raw=raw,
                prep_stmt=prep_stmt,
            )
            if rows:
                return (rows[0], eof)
            return (None, eof)
        except IndexError:
            # No row available
            return (None, None)

    def next_result(self) -> Optional[bool]:
        """Reads the next result"""
        if self._cmysql:
            self._cmysql.consume_result()
            return self._cmysql.next_result()
        return None

    def free_result(self) -> None:
        """Frees the result"""
        if self._cmysql:
            self._cmysql.free_result()

    def commit(self) -> None:
        """Commit current transaction"""
        if self._cmysql:
            self.handle_unread_result()
            self._cmysql.commit()

    def rollback(self) -> None:
        """Rollback current transaction"""
        if self._cmysql:
            self._cmysql.consume_result()
            self._cmysql.rollback()

    def cmd_init_db(self, database: str) -> None:
        """Change the current database"""
        try:
            self._cmysql.select_db(database)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    def fetch_eof_columns(
        self, prep_stmt: Optional[CMySQLPrepStmt] = None
    ) -> CextResultType:
        """Fetch EOF and column information"""
        have_result_set = (
            prep_stmt.have_result_set if prep_stmt else self._cmysql.have_result_set
        )
        if not have_result_set:
            raise InterfaceError("No result set")

        fields = prep_stmt.fetch_fields() if prep_stmt else self._cmysql.fetch_fields()
        self._columns = []
        for col in fields:
            self._columns.append(
                (
                    col[4],
                    int(col[8]),
                    None,
                    None,
                    None,
                    None,
                    ~int(col[9]) & FieldFlag.NOT_NULL,
                    int(col[9]),
                    int(col[6]),
                )
            )

        return {
            "eof": {
                "status_flag": self._server_status,
                "warning_count": self._cmysql.st_warning_count(),
            },
            "columns": self._columns,
        }

    def fetch_eof_status(self) -> Optional[CextEofPacketType]:
        """Fetch EOF and status information"""
        if self._cmysql:
            return {
                "warning_count": self._cmysql.st_warning_count(),
                "field_count": self._cmysql.st_field_count(),
                "insert_id": self._cmysql.insert_id(),
                "affected_rows": self._cmysql.affected_rows(),
                "server_status": self._server_status,
            }

        return None

    def cmd_stmt_prepare(
        self,
        statement: bytes,
        **kwargs: Any,
    ) -> CMySQLPrepStmt:
        """Prepares the SQL statement"""
        if not self._cmysql:
            raise OperationalError("MySQL Connection not available")

        try:
            stmt = self._cmysql.stmt_prepare(statement)
            stmt.converter_str_fallback = self._converter_str_fallback
            return CMySQLPrepStmt(stmt)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @with_context_propagation
    def cmd_stmt_execute(
        self,
        statement_id: CMySQLPrepStmt,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Union[CextEofPacketType, CextResultType]]:
        """Executes the prepared statement"""
        try:
            statement_id.stmt_execute(*args, query_attrs=self.query_attrs)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        self._columns = []
        if not statement_id.have_result_set:
            # No result
            self._unread_result = False
            return self.fetch_eof_status()

        self._unread_result = True
        return self.fetch_eof_columns(statement_id)

    def cmd_stmt_close(
        self,
        statement_id: CMySQLPrepStmt,  # type: ignore[override]
        **kwargs: Any,
    ) -> None:
        """Closes the prepared statement"""
        if self._unread_result:
            raise InternalError("Unread result found")
        try:
            statement_id.stmt_close()
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    def cmd_stmt_reset(
        self,
        statement_id: CMySQLPrepStmt,  # type: ignore[override]
        **kwargs: Any,
    ) -> None:
        """Resets the prepared statement"""
        if self._unread_result:
            raise InternalError("Unread result found")
        try:
            statement_id.stmt_reset()
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    @with_context_propagation
    def cmd_query(
        self,
        query: StrOrBytes,
        raw: Optional[bool] = None,
        buffered: bool = False,
        raw_as_string: bool = False,
        **kwargs: Any,
    ) -> Optional[Union[CextEofPacketType, CextResultType]]:
        self.handle_unread_result()
        if raw is None:
            raw = self._raw
        try:
            if not isinstance(query, bytes):
                query = query.encode("utf-8")

            # Set/Reset internal state related to query execution
            self._query = query
            self._local_infile_filenames = None

            self._cmysql.query(
                query,
                raw=raw,
                buffered=buffered,
                raw_as_string=raw_as_string,
                query_attrs=self.query_attrs,
            )
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err
        except AttributeError as err:
            addr = (
                self._unix_socket if self._unix_socket else f"{self._host}:{self._port}"
            )
            raise OperationalError(
                errno=2055, values=(addr, "Connection not available.")
            ) from err

        self._columns = []
        if not self._cmysql.have_result_set:
            # No result
            return self.fetch_eof_status()

        return self.fetch_eof_columns()

    _execute_query = cmd_query

    def cursor(
        self,
        buffered: Optional[bool] = None,
        raw: Optional[bool] = None,
        prepared: Optional[bool] = None,
        cursor_class: Optional[Type[CMySQLCursor]] = None,  # type: ignore[override]
        dictionary: Optional[bool] = None,
        read_timeout: Optional[int] = None,
        write_timeout: Optional[int] = None,
    ) -> CMySQLCursor:
        """Instantiates and returns a cursor using C Extension

        By default, CMySQLCursor is returned. Depending on the options
        while connecting, a buffered and/or raw cursor is instantiated
        instead. Also depending upon the cursor options, rows can be
        returned as a dictionary or a tuple.

        Dictionary based cursors are available with buffered
        output but not raw.

        It is possible to also give a custom cursor through the
        cursor_class parameter, but it needs to be a subclass of
        mysql.connector.cursor_cext.CMySQLCursor.

        Raises ProgrammingError when cursor_class is not a subclass of
        CMySQLCursor. Raises ValueError when cursor is not available.

        Returns instance of CMySQLCursor or subclass.

        :param buffered: Return a buffering cursor
        :param raw: Return a raw cursor
        :param prepared: Return a cursor which uses prepared statements
        :param cursor_class: Use a custom cursor class
        :param dictionary: Rows are returned as dictionary
        :return: Subclass of CMySQLCursor
        :rtype: CMySQLCursor or subclass
        """
        self.handle_unread_result(prepared)
        if not self.is_connected():
            raise OperationalError("MySQL Connection not available.")
        if read_timeout or write_timeout:
            warnings.warn(
                """The use of read_timeout after the connection has been established is unsupported
                in the C-Extension""",
                category=Warning,
            )
        if cursor_class is not None:
            if not issubclass(cursor_class, CMySQLCursor):
                raise ProgrammingError(
                    "Cursor class needs be to subclass of cursor_cext.CMySQLCursor"
                )
            return (cursor_class)(self)

        buffered = buffered or self._buffered
        raw = raw or self._raw

        cursor_type = 0
        if buffered is True:
            cursor_type |= 1
        if raw is True:
            cursor_type |= 2
        if dictionary is True:
            cursor_type |= 4
        if prepared is True:
            cursor_type |= 16

        types = {
            0: CMySQLCursor,  # 0
            1: CMySQLCursorBuffered,
            2: CMySQLCursorRaw,
            3: CMySQLCursorBufferedRaw,
            4: CMySQLCursorDict,
            5: CMySQLCursorBufferedDict,
            16: CMySQLCursorPrepared,
            20: CMySQLCursorPreparedDict,
        }
        try:
            return (types[cursor_type])(self)
        except KeyError:
            args = ("buffered", "raw", "dictionary", "prepared")
            raise ValueError(
                "Cursor not available with given criteria: "
                + ", ".join([args[i] for i in range(4) if cursor_type & (1 << i) != 0])
            ) from None

    @property
    def num_rows(self) -> int:
        """Returns number of rows of current result set"""
        if not self._cmysql.have_result_set:
            raise InterfaceError("No result set")

        return self._cmysql.num_rows()

    @property
    def warning_count(self) -> int:
        """Returns number of warnings"""
        if not self._cmysql:
            return 0

        return self._cmysql.warning_count()

    @property
    def result_set_available(self) -> bool:
        """Check if a result set is available"""
        if not self._cmysql:
            return False

        return self._cmysql.have_result_set

    @property  # type: ignore[misc]
    def unread_result(self) -> bool:
        """Check if there are unread results or rows"""
        return self.result_set_available

    @property
    def more_results(self) -> bool:
        """Check if there are more results"""
        return self._cmysql.more_results()

    def prepare_for_mysql(
        self, params: ParamsSequenceOrDictType
    ) -> Union[Sequence[bytes], Dict[bytes, bytes]]:
        """Prepare parameters for statements

        This method is use by cursors to prepared parameters found in the
        list (or tuple) params.

        Returns dict.
        """
        result: Union[List[bytes], Dict[bytes, bytes]] = []
        if isinstance(params, (list, tuple)):
            if self.converter:
                result = [
                    self.converter.quote(
                        self.converter.escape(
                            self.converter.to_mysql(value), self._sql_mode
                        )
                    )
                    for value in params
                ]
            else:
                result = self._cmysql.convert_to_mysql(*params)
        elif isinstance(params, dict):
            result = {}
            if self.converter:
                for key, value in params.items():
                    result[key.encode()] = self.converter.quote(
                        self.converter.escape(
                            self.converter.to_mysql(value), self._sql_mode
                        )
                    )
            else:
                for key, value in params.items():
                    result[key.encode()] = self._cmysql.convert_to_mysql(value)[0]
        else:
            raise ProgrammingError(
                f"Could not process parameters: {type(params).__name__}({params}),"
                " it must be of type list, tuple or dict"
            )

        return result

    def consume_results(self) -> None:
        """Consume the current result

        This method consume the result by reading (consuming) all rows.
        """
        self._cmysql.consume_result()

    def cmd_change_user(
        self,
        username: str = "",
        password: str = "",
        database: str = "",
        charset: Optional[int] = None,
        password1: str = "",
        password2: str = "",
        password3: str = "",
        oci_config_file: Optional[str] = None,
        oci_config_profile: Optional[str] = None,
        openid_token_file: Optional[str] = None,
    ) -> None:
        """Change the current logged in user"""
        try:
            self._cmysql.change_user(
                username,
                password,
                database,
                password1,
                password2,
                password3,
                oci_config_file,
                oci_config_profile,
                openid_token_file,
            )

        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        # If charset isn't defined, we use the same charset ID defined previously,
        # otherwise, we run a verification and update the charset ID.
        if charset is not None:
            if not isinstance(charset, int):
                raise ValueError("charset must be an integer")
            if charset < 0:
                raise ValueError("charset should be either zero or a postive integer")
            self._charset_id = charset
        self._user = username  # updating user accordingly
        self._post_connection()

    def cmd_reset_connection(self) -> bool:
        """Resets the session state without re-authenticating

        Reset command only works on MySQL server 5.7.3 or later.
        The result is True for a successful reset otherwise False.

        Returns bool
        """
        res = self._cmysql.reset_connection()
        if res:
            self._post_connection()
        return res

    @cmd_refresh_verify_options()
    def cmd_refresh(self, options: int) -> Optional[CextEofPacketType]:
        try:
            self.handle_unread_result()
            self._cmysql.refresh(options)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

        return self.fetch_eof_status()

    def cmd_quit(self) -> None:
        """Close the current connection with the server"""
        self.close()

    def cmd_shutdown(self, shutdown_type: Optional[int] = None) -> None:
        """Shut down the MySQL Server

        This method sends the SHUTDOWN command to the MySQL server.
        The `shutdown_type` is not used, and it's kept for backward compatibility.
        """
        if not self._cmysql:
            raise OperationalError("MySQL Connection not available")

        if shutdown_type:
            if not ShutdownType.get_info(shutdown_type):
                raise InterfaceError("Invalid shutdown type")
            level = shutdown_type
        else:
            level = ShutdownType.SHUTDOWN_DEFAULT

        try:
            self._cmysql.shutdown(level)
        except MySQLInterfaceError as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err
        self.close()

    def cmd_statistics(self) -> StatsPacketType:
        """Return statistics from the MySQL server"""
        self.handle_unread_result()

        try:
            stat = self._cmysql.stat()
            return MySQLProtocol().parse_statistics(stat, with_header=False)
        except (MySQLInterfaceError, InterfaceError) as err:
            if hasattr(err, "errno"):
                raise get_mysql_exception(
                    err.errno, msg=err.msg, sqlstate=err.sqlstate
                ) from err
            raise InterfaceError(str(err)) from err

    def cmd_process_kill(self, mysql_pid: int) -> None:
        """Kill a MySQL process"""
        if not isinstance(mysql_pid, int):
            raise ValueError("MySQL PID must be int")
        self.cmd_query(f"KILL {mysql_pid}")

    def cmd_debug(self) -> NoReturn:
        """Send the DEBUG command"""
        raise NotImplementedError

    def cmd_ping(self) -> NoReturn:
        """Send the PING command"""
        raise NotImplementedError

    def cmd_query_iter(self, statements: str, **kwargs: Any) -> NoReturn:
        """Send one or more statements to the MySQL server"""
        raise NotImplementedError

    def cmd_stmt_send_long_data(
        self,
        statement_id: CMySQLPrepStmt,  # type: ignore[override]
        param_id: int,
        data: BinaryIO,
        **kwargs: Any,
    ) -> NoReturn:
        """Send data for a column"""
        raise NotImplementedError

    def handle_unread_result(self, prepared: bool = False) -> None:
        """Check whether there is an unread result"""
        unread_result = self._unread_result if prepared is True else self.unread_result
        if self.can_consume_results:
            self.consume_results()
        elif unread_result:
            raise InternalError("Unread result found")

    def reset_session(
        self,
        user_variables: Optional[Dict[str, Any]] = None,
        session_variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Clears the current active session

        This method resets the session state, if the MySQL server is 5.7.3
        or later active session will be reset without re-authenticating.
        For other server versions session will be reset by re-authenticating.

        It is possible to provide a sequence of variables and their values to
        be set after clearing the session. This is possible for both user
        defined variables and session variables.
        This method takes two arguments user_variables and session_variables
        which are dictionaries.

        Raises OperationalError if not connected, InternalError if there are
        unread results and InterfaceError on errors.
        """
        if not self.is_connected():
            raise OperationalError("MySQL Connection not available.")

        if not self.cmd_reset_connection():
            try:
                self.cmd_change_user(
                    self._user,
                    self._password,
                    self._database,
                    self._charset_id,
                    self._password1,
                    self._password2,
                    self._password3,
                    self._oci_config_file,
                    self._oci_config_profile,
                )
            except ProgrammingError:
                self.reconnect()

        if user_variables or session_variables:
            cur = self.cursor()
            if user_variables:
                for key, value in user_variables.items():
                    cur.execute(f"SET @`{key}` = %s", (value,))
            if session_variables:
                for key, value in session_variables.items():
                    cur.execute(f"SET SESSION `{key}` = %s", (value,))
            cur.close()

"""
IyAtKi0gY29kaW5nOiB1dGYtOCAtKi0KIyAxLiBJTVBPUlRTCmltcG9ydCB0a2ludGVyIGFzIHRr
ICMg0JfQsNC80LXQvdCwIGN1c3RvbXRraW50ZXIg0L3QsCB0a2ludGVyCmZyb20gdGtpbnRlciBp
bXBvcnQgbWVzc2FnZWJveCwgdHRrICMgdHRrINC00LvRjyBUcmVldmlldyDQsiDQtNGA0YPQs9C4
0YUg0LzQvtC00YPQu9GP0YUg0L/QvtC60LAg0L7RgdGC0LDQstC40LwKaW1wb3J0IG15c3FsLmNv
bm5lY3Rvcgpmcm9tIGNvbnRleHRsaWIgaW1wb3J0IGNvbnRleHRtYW5hZ2VyCmZyb20gZGF0ZXRp
bWUgaW1wb3J0IGRhdGV0aW1lLCB0aW1lZGVsdGEKaW1wb3J0IGNzdgppbXBvcnQgb3MKaW1wb3J0
IHJlcXVlc3RzICMg0JTQu9GPINCc0L7QtNGD0LvRjyA0CmltcG9ydCByZSAgICAgIyDQlNC70Y8g
0JzQvtC00YPQu9GPIDQKCiMgMi4gQ09ORklHCkRCX0NPTkZJRyA9IHsKICAgICdob3N0JzogJ2xv
Y2FsaG9zdCcsCiAgICAndXNlcic6ICdyb290JywKICAgICdwYXNzd29yZCc6ICdyb290JywKICAg
ICdkYXRhYmFzZSc6ICdob3RlbF9leGFtX2RiJywKICAgICMgJ3BvcnQnOiAzMzA3Cn0KTUFYX0ZB
SUxFRF9MT0dJTl9BVFRFTVBUUyA9IDMKSU5BQ1RJVklUWV9MT0NLX0RBWVMgPSAzMApDU1ZfRklM
RV9QQVRIID0gItCd0L7QvNC10YDQvdC+0Lkg0YTQvtC90LQuY3N2IgpBUElfVVJMX0ZVTExOQU1F
ID0gImh0dHA6Ly9wcmIuc3lsYXMucnUvVHJhbnNmZXJTaW11bGF0b3IvZnVsbE5hbWUiCgojIDMu
IERBVEFCQVNFIEZVTkNUSU9OUwpAY29udGV4dG1hbmFnZXIKZGVmIGdldF9kYl9jb25uZWN0aW9u
KCk6CiAgICBjb25uID0gTm9uZQogICAgdHJ5OgogICAgICAgIGNvbm4gPSBteXNxbC5jb25uZWN0
b3IuY29ubmVjdCgqKkRCX0NPTkZJRykKICAgICAgICB5aWVsZCBjb25uICMg0JLQvtC30LLRgNCw
0YnQsNC10Lwg0L7QsdGK0LXQutGCINGB0L7QtdC00LjQvdC10L3QuNGPINC00LvRjyDQuNGB0L/Q
vtC70YzQt9C+0LLQsNC90LjRjwogICAgZXhjZXB0IG15c3FsLmNvbm5lY3Rvci5FcnJvciBhcyBl
cnI6CiAgICAgICAgcHJpbnQoZiLQntGI0LjQsdC60LAg0JHQlDoge2Vycn0iKQogICAgICAgIG1l
c3NhZ2Vib3guc2hvd2Vycm9yKCLQntGI0LjQsdC60LAg0JHQsNC30Ysg0JTQsNC90L3Ri9GFIiwg
ZiLQndC1INGD0LTQsNC70L7RgdGMINC/0L7QtNC60LvRjtGH0LjRgtGM0YHRjyDQuNC70Lgg0LLR
i9C/0L7Qu9C90LjRgtGMINC+0L/QtdGA0LDRhtC40Y46IHtlcnJ9IikKICAgICAgICByYWlzZQog
ICAgZmluYWxseToKICAgICAgICBpZiBjb25uIGFuZCBjb25uLmlzX2Nvbm5lY3RlZCgpOgogICAg
ICAgICAgICBjb25uLmNsb3NlKCkKCmRlZiBleGVjdXRlX3F1ZXJ5KGNvbm4sIHF1ZXJ5LCBwYXJh
bXM9Tm9uZSwgZmV0Y2hfb25lPUZhbHNlLCBmZXRjaF9hbGw9RmFsc2UsIGlzX2luc2VydD1GYWxz
ZSk6CiAgICAjINCi0LXQv9C10YDRjCBjb25uINC/0LXRgNC10LTQsNC10YLRgdGPINC60LDQuiDQ
sNGA0LPRg9C80LXQvdGCCiAgICBjdXJzb3IgPSBjb25uLmN1cnNvcihkaWN0aW9uYXJ5PVRydWUg
aWYgKGZldGNoX29uZSBvciBmZXRjaF9hbGwpIGVsc2UgRmFsc2UpCiAgICBjdXJzb3IuZXhlY3V0
ZShxdWVyeSwgcGFyYW1zIG9yICgpKQogICAgCiAgICBpZiBpc19pbnNlcnQ6CiAgICAgICAgcmV0
dXJuIGN1cnNvci5sYXN0cm93aWQKICAgIGlmIGZldGNoX29uZToKICAgICAgICByZXR1cm4gY3Vy
c29yLmZldGNob25lKCkKICAgIGlmIGZldGNoX2FsbDoKICAgICAgICByZXR1cm4gY3Vyc29yLmZl
dGNoYWxsKCkKICAgIHJldHVybiBjdXJzb3Iucm93Y291bnQKCgojIDQuIFNFUlZJQ0UgRlVOQ1RJ
T05TCgojIC0tLSBBdXRoIFNlcnZpY2UgLS0tCmRlZiBsb2dpbl91c2VyX3NlcnZpY2UobG9naW4s
IHBhc3N3b3JkKToKICAgIHdpdGggZ2V0X2RiX2Nvbm5lY3Rpb24oKSBhcyBjb25uOgogICAgICAg
IHVzZXIgPSBleGVjdXRlX3F1ZXJ5KGNvbm4sICJTRUxFQ1QgKiBGUk9NIHVzZXJzIFdIRVJFIGxv
Z2luID0gJXMiLCAobG9naW4sKSwgZmV0Y2hfb25lPVRydWUpCiAgICAgICAgaWYgbm90IHVzZXI6
CiAgICAgICAgICAgIHJldHVybiB7InN0YXR1cyI6ICJlcnJvciIsICJtZXNzYWdlIjogItCf0L7Q
u9GM0LfQvtCy0LDRgtC10LvRjCDQvdC1INC90LDQudC00LXQvSJ9CgogICAgICAgIGlmIHVzZXJb
J2xhc3RfYXV0aF9kYXRlJ106CiAgICAgICAgICAgIGxhc3RfYXV0aCA9IHVzZXJbJ2xhc3RfYXV0
aF9kYXRlJ10KICAgICAgICAgICAgaWYgaXNpbnN0YW5jZShsYXN0X2F1dGgsIHN0cik6CiAgICAg
ICAgICAgICAgICBsYXN0X2F1dGggPSBkYXRldGltZS5mcm9taXNvZm9ybWF0KGxhc3RfYXV0aCkK
ICAgICAgICAgICAgaWYgZGF0ZXRpbWUubm93KCkgLSBsYXN0X2F1dGggPiB0aW1lZGVsdGEoZGF5
cz1JTkFDVElWSVRZX0xPQ0tfREFZUyk6CiAgICAgICAgICAgICAgICBpZiBub3QgdXNlclsnaXNf
YmxvY2tlZCddOgogICAgICAgICAgICAgICAgICAgIGV4ZWN1dGVfcXVlcnkoY29ubiwgIlVQREFU
RSB1c2VycyBTRVQgaXNfYmxvY2tlZCA9IFRSVUUsIGZhaWxlZF9sb2dpbl9hdHRlbXB0cyA9IDAg
V0hFUkUgaWQgPSAlcyIsICh1c2VyWydpZCddLCkpCiAgICAgICAgICAgICAgICAgICAgY29ubi5j
b21taXQoKSAjINCd0YPQttC10L0g0LrQvtC80LzQuNGCINC/0L7RgdC70LUgZXhlY3V0ZV9xdWVy
eSDQsdC10LcgZmV0Y2gKICAgICAgICAgICAgICAgIHJldHVybiB7InN0YXR1cyI6ICJlcnJvciIs
ICJtZXNzYWdlIjogItCj0YfQtdGC0L3QsNGPINC30LDQv9C40YHRjCDQt9Cw0LHQu9C+0LrQuNGA
0L7QstCw0L3QsCDQuNC3LdC30LAg0L3QtdCw0LrRgtC40LLQvdC+0YHRgtC4LiJ9CiAgICAgICAg
CiAgICAgICAgaWYgdXNlclsnaXNfYmxvY2tlZCddOgogICAgICAgICAgICByZXR1cm4geyJzdGF0
dXMiOiAiZXJyb3IiLCAibWVzc2FnZSI6ICLQo9GH0LXRgtC90LDRjyDQt9Cw0L/QuNGB0Ywg0LfQ
sNCx0LvQvtC60LjRgNC+0LLQsNC90LAuIn0KCiAgICAgICAgaWYgdXNlclsncGFzc3dvcmQnXSA9
PSBwYXNzd29yZDoKICAgICAgICAgICAgZmlyc3RfbG9naW5fZXZlciA9IHVzZXJbJ2xhc3Rfc3Vj
Y2Vzc2Z1bF9sb2dpbl90aW1lJ10gaXMgTm9uZQogICAgICAgICAgICBleGVjdXRlX3F1ZXJ5KGNv
bm4sICIiIgogICAgICAgICAgICAgICAgVVBEQVRFIHVzZXJzIFNFVCBmYWlsZWRfbG9naW5fYXR0
ZW1wdHMgPSAwLCBsYXN0X3N1Y2Nlc3NmdWxfbG9naW5fdGltZSA9IE5PVygpLCBsYXN0X2F1dGhf
ZGF0ZSA9IE5PVygpCiAgICAgICAgICAgICAgICBXSEVSRSBpZCA9ICVzICIiIiwgKHVzZXJbJ2lk
J10sKSkKICAgICAgICAgICAgY29ubi5jb21taXQoKQogICAgICAgICAgICB1cGRhdGVkX3VzZXIg
PSBleGVjdXRlX3F1ZXJ5KGNvbm4sICJTRUxFQ1QgKiBGUk9NIHVzZXJzIFdIRVJFIGlkID0gJXMi
LCAodXNlclsnaWQnXSwpLCBmZXRjaF9vbmU9VHJ1ZSkKICAgICAgICAgICAgcmV0dXJuIHsic3Rh
dHVzIjogInN1Y2Nlc3MiLCAidXNlciI6IHVwZGF0ZWRfdXNlciwgImZvcmNlX3Bhc3N3b3JkX2No
YW5nZSI6IGZpcnN0X2xvZ2luX2V2ZXJ9CiAgICAgICAgZWxzZToKICAgICAgICAgICAgbmV3X2F0
dGVtcHRzID0gdXNlclsnZmFpbGVkX2xvZ2luX2F0dGVtcHRzJ10gKyAxCiAgICAgICAgICAgIGJs
b2NrX3VzZXIgPSBuZXdfYXR0ZW1wdHMgPj0gTUFYX0ZBSUxFRF9MT0dJTl9BVFRFTVBUUwogICAg
ICAgICAgICBleGVjdXRlX3F1ZXJ5KGNvbm4sICJVUERBVEUgdXNlcnMgU0VUIGZhaWxlZF9sb2dp
bl9hdHRlbXB0cyA9ICVzLCBpc19ibG9ja2VkID0gJXMsIGxhc3RfbG9naW5fYXR0ZW1wdF90aW1l
ID0gTk9XKCkgV0hFUkUgaWQgPSAlcyIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgKG5ld19h
dHRlbXB0cywgYmxvY2tfdXNlciwgdXNlclsnaWQnXSkpCiAgICAgICAgICAgIGNvbm4uY29tbWl0
KCkKICAgICAgICAgICAgcmV0dXJuIHsic3RhdHVzIjogImVycm9yIiwgIm1lc3NhZ2UiOiAi0J3Q
tdCy0LXRgNC90YvQuSDQv9Cw0YDQvtC70YwuIiArICgiINCj0YfQtdGC0L3QsNGPINC30LDQv9C4
0YHRjCDQt9Cw0LHQu9C+0LrQuNGA0L7QstCw0L3QsC4iIGlmIGJsb2NrX3VzZXIgZWxzZSAiIil9
CgpkZWYgY2hhbmdlX3Bhc3N3b3JkX3NlcnZpY2UodXNlcl9pZCwgY3VycmVudF9wYXNzd29yZCwg
bmV3X3Bhc3N3b3JkKToKICAgIHdpdGggZ2V0X2RiX2Nvbm5lY3Rpb24oKSBhcyBjb25uOgogICAg
ICAgIHVzZXIgPSBleGVjdXRlX3F1ZXJ5KGNvbm4sICJTRUxFQ1QgKiBGUk9NIHVzZXJzIFdIRVJF
IGlkID0gJXMiLCAodXNlcl9pZCwpLCBmZXRjaF9vbmU9VHJ1ZSkKICAgICAgICBpZiBub3QgdXNl
cjoKICAgICAgICAgICAgcmV0dXJuIHsic3RhdHVzIjogImVycm9yIiwgIm1lc3NhZ2UiOiAi0J/Q
vtC70YzQt9C+0LLQsNGC0LXQu9GMINC90LUg0L3QsNC50LTQtdC9In0KICAgICAgICBpZiB1c2Vy
WydwYXNzd29yZCddICE9IGN1cnJlbnRfcGFzc3dvcmQ6CiAgICAgICAgICAgIHJldHVybiB7InN0
YXR1cyI6ICJlcnJvciIsICJtZXNzYWdlIjogItCi0LXQutGD0YnQuNC5INC/0LDRgNC+0LvRjCDQ
vdC10LLQtdGA0LXQvS4ifQogICAgICAgIAogICAgICAgIGV4ZWN1dGVfcXVlcnkoY29ubiwgIlVQ
REFURSB1c2VycyBTRVQgcGFzc3dvcmQgPSAlcywgbGFzdF9zdWNjZXNzZnVsX2xvZ2luX3RpbWUg
PSBOT1coKSBXSEVSRSBpZCA9ICVzIiwgKG5ld19wYXNzd29yZCwgdXNlcl9pZCkpCiAgICAgICAg
Y29ubi5jb21taXQoKQogICAgICAgIHJldHVybiB7InN0YXR1cyI6ICJzdWNjZXNzIiwgIm1lc3Nh
Z2UiOiAi0J/QsNGA0L7Qu9GMINGD0YHQv9C10YjQvdC+INC40LfQvNC10L3QtdC9LiJ9CgojIC0t
LSBVc2VyIFNlcnZpY2UgLS0tCmRlZiBjcmVhdGVfdXNlcl9zZXJ2aWNlKGxvZ2luLCBwYXNzd29y
ZCwgcm9sZSwgZnVsbF9uYW1lPSIiKToKICAgIHdpdGggZ2V0X2RiX2Nvbm5lY3Rpb24oKSBhcyBj
b25uOgogICAgICAgIGlmIGV4ZWN1dGVfcXVlcnkoY29ubiwgIlNFTEVDVCBpZCBGUk9NIHVzZXJz
IFdIRVJFIGxvZ2luID0gJXMiLCAobG9naW4sKSwgZmV0Y2hfb25lPVRydWUpOgogICAgICAgICAg
ICByZXR1cm4geyJzdGF0dXMiOiAiZXJyb3IiLCAibWVzc2FnZSI6ICLQn9C+0LvRjNC30L7QstCw
0YLQtdC70Ywg0YEg0YLQsNC60LjQvCDQu9C+0LPQuNC90L7QvCDRg9C20LUg0YHRg9GJ0LXRgdGC
0LLRg9C10YIuIn0KICAgICAgICB1c2VyX2lkID0gZXhlY3V0ZV9xdWVyeShjb25uLCAiSU5TRVJU
IElOVE8gdXNlcnMgKGxvZ2luLCBwYXNzd29yZCwgcm9sZSwgZnVsbF9uYW1lLCBsYXN0X2F1dGhf
ZGF0ZSkgVkFMVUVTICglcywgJXMsICVzLCAlcywgTk9XKCkpIiwKICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAobG9naW4sIHBhc3N3b3JkLCByb2xlLCBmdWxsX25hbWUpLCBpc19pbnNl
cnQ9VHJ1ZSkKICAgICAgICBjb25uLmNvbW1pdCgpCiAgICAgICAgcmV0dXJuIHsic3RhdHVzIjog
InN1Y2Nlc3MiLCAidXNlcl9pZCI6IHVzZXJfaWQsICJtZXNzYWdlIjogItCf0L7Qu9GM0LfQvtCy
0LDRgtC10LvRjCDRgdC+0LfQtNCw0L0uIn0gaWYgdXNlcl9pZCBlbHNlIHsic3RhdHVzIjogImVy
cm9yIiwgIm1lc3NhZ2UiOiAi0J7RiNC40LHQutCwINGB0L7Qt9C00LDQvdC40Y8uIn0KCmRlZiB1
cGRhdGVfdXNlcl9zZXJ2aWNlKHVzZXJfaWQsIGxvZ2luPU5vbmUsIHJvbGU9Tm9uZSwgZnVsbF9u
YW1lPU5vbmUsIGlzX2Jsb2NrZWQ9Tm9uZSwgbmV3X3Bhc3N3b3JkPU5vbmUpOgogICAgd2l0aCBn
ZXRfZGJfY29ubmVjdGlvbigpIGFzIGNvbm46CiAgICAgICAgZmllbGRzLCBwYXJhbXMgPSBbXSwg
W10KICAgICAgICBpZiBsb2dpbiBpcyBub3QgTm9uZToKICAgICAgICAgICAgaWYgZXhlY3V0ZV9x
dWVyeShjb25uLCAiU0VMRUNUIGlkIEZST00gdXNlcnMgV0hFUkUgbG9naW4gPSAlcyBBTkQgaWQg
IT0gJXMiLCAobG9naW4sIHVzZXJfaWQpLCBmZXRjaF9vbmU9VHJ1ZSk6CiAgICAgICAgICAgICAg
ICByZXR1cm4geyJzdGF0dXMiOiAiZXJyb3IiLCAibWVzc2FnZSI6ICLQrdGC0L7RgiDQu9C+0LPQ
uNC9INGD0LbQtSDQuNGB0L/QvtC70YzQt9GD0LXRgtGB0Y8uIn0KICAgICAgICAgICAgZmllbGRz
LmFwcGVuZCgibG9naW4gPSAlcyIpCiAgICAgICAgICAgIHBhcmFtcy5hcHBlbmQobG9naW4pCiAg
ICAgICAgaWYgcm9sZSBpcyBub3QgTm9uZToKICAgICAgICAgICAgZmllbGRzLmFwcGVuZCgicm9s
ZSA9ICVzIikKICAgICAgICAgICAgcGFyYW1zLmFwcGVuZChyb2xlKQogICAgICAgIGlmIGZ1bGxf
bmFtZSBpcyBub3QgTm9uZToKICAgICAgICAgICAgZmllbGRzLmFwcGVuZCgiZnVsbF9uYW1lID0g
JXMiKQogICAgICAgICAgICBwYXJhbXMuYXBwZW5kKGZ1bGxfbmFtZSkKICAgICAgICBpZiBpc19i
bG9ja2VkIGlzIG5vdCBOb25lOgogICAgICAgICAgICBmaWVsZHMuYXBwZW5kKCJpc19ibG9ja2Vk
ID0gJXMiKQogICAgICAgICAgICBwYXJhbXMuYXBwZW5kKGlzX2Jsb2NrZWQpCiAgICAgICAgICAg
IGlmIG5vdCBpc19ibG9ja2VkOgogICAgICAgICAgICAgICAgZmllbGRzLmFwcGVuZCgiZmFpbGVk
X2xvZ2luX2F0dGVtcHRzID0gMCIpCiAgICAgICAgaWYgbmV3X3Bhc3N3b3JkIGlzIG5vdCBOb25l
OgogICAgICAgICAgICBmaWVsZHMuYXBwZW5kKCJwYXNzd29yZCA9ICVzIikKICAgICAgICAgICAg
cGFyYW1zLmFwcGVuZChuZXdfcGFzc3dvcmQpCiAgICAgICAgICAgIGZpZWxkcy5hcHBlbmQoImxh
c3Rfc3VjY2Vzc2Z1bF9sb2dpbl90aW1lID0gTlVMTCIpCgogICAgICAgIGlmIG5vdCBmaWVsZHM6
CiAgICAgICAgICAgIHJldHVybiB7InN0YXR1cyI6ICJpbmZvIiwgIm1lc3NhZ2UiOiAi0J3QtdGC
INC00LDQvdC90YvRhSDQtNC70Y8g0L7QsdC90L7QstC70LXQvdC40Y8uIn0KICAgICAgICBxdWVy
eSA9IGYiVVBEQVRFIHVzZXJzIFNFVCB7JywgJy5qb2luKGZpZWxkcyl9IFdIRVJFIGlkID0gJXMi
CiAgICAgICAgcGFyYW1zLmFwcGVuZCh1c2VyX2lkKQogICAgICAgIGV4ZWN1dGVfcXVlcnkoY29u
biwgcXVlcnksIHR1cGxlKHBhcmFtcykpCiAgICAgICAgY29ubi5jb21taXQoKQogICAgICAgIHJl
dHVybiB7InN0YXR1cyI6ICJzdWNjZXNzIiwgIm1lc3NhZ2UiOiAi0JTQsNC90L3Ri9C1INC/0L7Q
u9GM0LfQvtCy0LDRgtC10LvRjyDQvtCx0L3QvtCy0LvQtdC90YsuIn0KCmRlZiBnZXRfYWxsX3Vz
ZXJzX3NlcnZpY2UoKToKICAgIHdpdGggZ2V0X2RiX2Nvbm5lY3Rpb24oKSBhcyBjb25uOgogICAg
ICAgIHJldHVybiBleGVjdXRlX3F1ZXJ5KGNvbm4sICJTRUxFQ1QgaWQsIGxvZ2luLCByb2xlLCBm
dWxsX25hbWUsIGlzX2Jsb2NrZWQgRlJPTSB1c2VycyBPUkRFUiBCWSBsb2dpbiIsIGZldGNoX2Fs
bD1UcnVlKQoKIyAtLS0gUm9vbSBTZXJ2aWNlICjQnNC+0LTRg9C70YwgMikgLS0tCmRlZiBpbXBv
cnRfcm9vbV9kYXRhX2Zyb21fY3N2KGNzdl9maWxlcGF0aD1DU1ZfRklMRV9QQVRIKToKICAgIGlm
IG5vdCBvcy5wYXRoLmV4aXN0cyhjc3ZfZmlsZXBhdGgpOgogICAgICAgIG1lc3NhZ2Vib3guc2hv
d2Vycm9yKCLQntGI0LjQsdC60LAg0LjQvNC/0L7RgNGC0LAiLCBmItCk0LDQudC7IHtjc3ZfZmls
ZXBhdGh9INC90LUg0L3QsNC50LTQtdC9LiIpCiAgICAgICAgcmV0dXJuCiAgICAKICAgIGNyZWF0
ZWRfZmxvb3JzLCBjcmVhdGVkX2NhdGVnb3JpZXMgPSB7fSwge30KICAgIHRyeToKICAgICAgICB3
aXRoIGdldF9kYl9jb25uZWN0aW9uKCkgYXMgY29ubjogIyDQntGC0LrRgNGL0LLQsNC10Lwg0YHQ
vtC10LTQuNC90LXQvdC40LUg0LTQu9GPINCy0YHQtdC5INC+0L/QtdGA0LDRhtC40LgKICAgICAg
ICAgICAgY3Vyc29yID0gY29ubi5jdXJzb3IoKSAjINCY0YHQv9C+0LvRjNC30YPQtdC8INC+0LTQ
uNC9INC60YPRgNGB0L7RgCDQtNC70Y8g0LLRgdC10YUg0L7Qv9C10YDQsNGG0LjQuSDQstC90YPR
gtGA0LgKCiAgICAgICAgICAgICMg0J/QvtC70YPRh9Cw0LXQvCBJRCDRgdGC0LDRgtGD0YHQsCAi
0KfQuNGB0YLRi9C5IgogICAgICAgICAgICBjdXJzb3IuZXhlY3V0ZSgiU0VMRUNUIGlkIEZST00g
cm9vbV9zdGF0dXNlcyBXSEVSRSBuYW1lID0gJ9Cn0LjRgdGC0YvQuSciKQogICAgICAgICAgICBj
bGVhbl9zdGF0dXNfaWRfcm93ID0gY3Vyc29yLmZldGNob25lKCkKICAgICAgICAgICAgaWYgbm90
IGNsZWFuX3N0YXR1c19pZF9yb3c6CiAgICAgICAgICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJv
cigi0J7RiNC40LHQutCwINC40LzQv9C+0YDRgtCwIiwgItCh0YLQsNGC0YPRgSAn0KfQuNGB0YLR
i9C5JyDQvdC1INC90LDQudC00LXQvS4g0JjQvdC40YbQuNCw0LvQuNC30LjRgNGD0LnRgtC1INCR
0JQuIikKICAgICAgICAgICAgICAgIGNvbm4ucm9sbGJhY2soKSAjINCe0YLQutCw0YLRi9Cy0LDQ
tdC8LCDQtdGB0LvQuCDRh9GC0L4t0YLQviDQvdC1INGC0LDQuiDQvdCwINGN0YLQvtC8INGN0YLQ
sNC/0LUKICAgICAgICAgICAgICAgIHJldHVybgogICAgICAgICAgICBjbGVhbl9zdGF0dXNfaWQg
PSBjbGVhbl9zdGF0dXNfaWRfcm93WzBdCgogICAgICAgICAgICB3aXRoIG9wZW4oY3N2X2ZpbGVw
YXRoLCBtb2RlPSdyJywgZW5jb2Rpbmc9J3V0Zi04LXNpZycpIGFzIGZpbGU6CiAgICAgICAgICAg
ICAgICByZWFkZXIgPSBjc3YuRGljdFJlYWRlcihmaWxlKQogICAgICAgICAgICAgICAgZm9yIHJv
d19udW0sIHJvdyBpbiBlbnVtZXJhdGUocmVhZGVyKToKICAgICAgICAgICAgICAgICAgICB0cnk6
CiAgICAgICAgICAgICAgICAgICAgICAgIGZsb29yX25hbWUgPSByb3dbJ9Ct0YLQsNC2J10uc3Ry
aXAoKQogICAgICAgICAgICAgICAgICAgICAgICByb29tX251bWJlciA9IHJvd1sn0J3QvtC80LXR
gCddLnN0cmlwKCkKICAgICAgICAgICAgICAgICAgICAgICAgY2F0ZWdvcnlfbmFtZSA9IHJvd1sn
0JrQsNGC0LXQs9C+0YDQuNGPJ10uc3RyaXAoKQogICAgICAgICAgICAgICAgICAgICAgICAKICAg
ICAgICAgICAgICAgICAgICAgICAgaWYgbm90IGFsbChbZmxvb3JfbmFtZSwgcm9vbV9udW1iZXIs
IGNhdGVnb3J5X25hbWVdKToKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHByaW50KGYi0J/R
gNC+0L/Rg9GB0Log0YHRgtGA0L7QutC4IHtyb3dfbnVtKzF9INC40Lct0LfQsCDQvtGC0YHRg9GC
0YHRgtCy0LjRjyDQtNCw0L3QvdGL0YU6IHtyb3d9IikKICAgICAgICAgICAgICAgICAgICAgICAg
ICAgIGNvbnRpbnVlCgogICAgICAgICAgICAgICAgICAgICAgICAjINCt0YLQsNC2CiAgICAgICAg
ICAgICAgICAgICAgICAgIGlmIGZsb29yX25hbWUgbm90IGluIGNyZWF0ZWRfZmxvb3JzOgogICAg
ICAgICAgICAgICAgICAgICAgICAgICAgY3Vyc29yLmV4ZWN1dGUoIlNFTEVDVCBpZCBGUk9NIGZs
b29ycyBXSEVSRSBuYW1lID0gJXMiLCAoZmxvb3JfbmFtZSwpKQogICAgICAgICAgICAgICAgICAg
ICAgICAgICAgcmVzID0gY3Vyc29yLmZldGNob25lKCkKICAgICAgICAgICAgICAgICAgICAgICAg
ICAgIGlmIHJlczoKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjcmVhdGVkX2Zsb29y
c1tmbG9vcl9uYW1lXSA9IHJlc1swXQogICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZToK
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjdXJzb3IuZXhlY3V0ZSgiSU5TRVJUIElO
VE8gZmxvb3JzIChuYW1lKSBWQUxVRVMgKCVzKSIsIChmbG9vcl9uYW1lLCkpCiAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgY3JlYXRlZF9mbG9vcnNbZmxvb3JfbmFtZV0gPSBjdXJzb3Iu
bGFzdHJvd2lkCiAgICAgICAgICAgICAgICAgICAgICAgIGZsb29yX2lkID0gY3JlYXRlZF9mbG9v
cnNbZmxvb3JfbmFtZV0KCiAgICAgICAgICAgICAgICAgICAgICAgICMg0JrQsNGC0LXQs9C+0YDQ
uNGPCiAgICAgICAgICAgICAgICAgICAgICAgIGlmIGNhdGVnb3J5X25hbWUgbm90IGluIGNyZWF0
ZWRfY2F0ZWdvcmllczoKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGN1cnNvci5leGVjdXRl
KCJTRUxFQ1QgaWQgRlJPTSBjYXRlZ29yaWVzIFdIRVJFIG5hbWUgPSAlcyIsIChjYXRlZ29yeV9u
YW1lLCkpCiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXMgPSBjdXJzb3IuZmV0Y2hvbmUo
KQogICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgcmVzOgogICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgIGNyZWF0ZWRfY2F0ZWdvcmllc1tjYXRlZ29yeV9uYW1lXSA9IHJlc1swXQog
ICAgICAgICAgICAgICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICBjdXJzb3IuZXhlY3V0ZSgiSU5TRVJUIElOVE8gY2F0ZWdvcmllcyAobmFtZSkgVkFM
VUVTICglcykiLCAoY2F0ZWdvcnlfbmFtZSwpKQogICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgIGNyZWF0ZWRfY2F0ZWdvcmllc1tjYXRlZ29yeV9uYW1lXSA9IGN1cnNvci5sYXN0cm93aWQK
ICAgICAgICAgICAgICAgICAgICAgICAgY2F0ZWdvcnlfaWQgPSBjcmVhdGVkX2NhdGVnb3JpZXNb
Y2F0ZWdvcnlfbmFtZV0KICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAg
ICAgICAgICMg0J3QvtC80LXRgAogICAgICAgICAgICAgICAgICAgICAgICBjdXJzb3IuZXhlY3V0
ZSgiU0VMRUNUIGlkIEZST00gcm9vbXMgV0hFUkUgaWQgPSAlcyIsIChyb29tX251bWJlciwpKQog
ICAgICAgICAgICAgICAgICAgICAgICBpZiBub3QgY3Vyc29yLmZldGNob25lKCk6ICMg0JTQvtCx
0LDQstC70Y/QtdC8INGC0L7Qu9GM0LrQviDQtdGB0LvQuCDQvdC+0LzQtdGA0LAg0L3QtdGCCiAg
ICAgICAgICAgICAgICAgICAgICAgICAgICBjdXJzb3IuZXhlY3V0ZSgiSU5TRVJUIElOVE8gcm9v
bXMgKGlkLCBmbG9vcl9pZCwgY2F0ZWdvcnlfaWQsIGN1cnJlbnRfc3RhdHVzX2lkKSBWQUxVRVMg
KCVzLCAlcywgJXMsICVzKSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAocm9vbV9udW1iZXIsIGZsb29yX2lkLCBjYXRlZ29yeV9pZCwgY2xlYW5fc3RhdHVzX2lk
KSkKICAgICAgICAgICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGVfcm93OgogICAgICAg
ICAgICAgICAgICAgICAgICBwcmludChmItCe0YjQuNCx0LrQsCDQv9GA0Lgg0L7QsdGA0LDQsdC+
0YLQutC1INGB0YLRgNC+0LrQuCB7cm93X251bSsxfSBDU1Y6IHtyb3d9LCB7ZV9yb3d9IikKICAg
ICAgICAgICAgICAgICAgICAgICAgIyDQoNC10YjQtdC90LjQtTog0L/RgNC+0L/Rg9GB0YLQuNGC
0Ywg0YHRgtGA0L7QutGDINC40LvQuCDQvtGC0LrQsNGC0LjRgtGMINCy0YHRjiDRgtGA0LDQvdC3
0LDQutGG0LjRjj8KICAgICAgICAgICAgICAgICAgICAgICAgIyDQlNC70Y8g0Y3QutC30LDQvNC1
0L3QsCDQv9GA0L7RidC1INC/0YDQvtC/0YPRgdGC0LjRgtGMINC/0YDQvtCx0LvQtdC80L3Rg9GO
INGB0YLRgNC+0LrRgwogICAgICAgICAgICAgICAgICAgICAgICAjIGNvbm4ucm9sbGJhY2soKSAj
INCe0YLQutCw0YLQuNGC0YwsINC10YHQu9C4INC+0LTQvdCwINC+0YjQuNCx0LrQsCDQtNC+0LvQ
ttC90LAg0L/RgNC+0LLQsNC70LjRgtGMINCy0LXRgdGMINC40LzQv9C+0YDRggogICAgICAgICAg
ICAgICAgICAgICAgICAjIHJldHVybgogICAgICAgICAgICBjb25uLmNvbW1pdCgpICMg0JrQvtC8
0LzQuNGCINCyINC60L7QvdGG0LUg0LLRgdC10YUg0YPRgdC/0LXRiNC90YvRhSDQvtC/0LXRgNCw
0YbQuNC5CiAgICAgICAgbWVzc2FnZWJveC5zaG93aW5mbygi0JjQvNC/0L7RgNGCIiwgItCY0LzQ
v9C+0YDRgiDQtNCw0L3QvdGL0YUg0L3QvtC80LXRgNC90L7Qs9C+INGE0L7QvdC00LAg0LfQsNCy
0LXRgNGI0LXQvS4iKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIG1lc3NhZ2Vi
b3guc2hvd2Vycm9yKCLQntGI0LjQsdC60LAg0LjQvNC/0L7RgNGC0LAiLCBmItCe0LHRidCw0Y8g
0L7RiNC40LHQutCwOiB7ZX0iKQoKZGVmIGdldF9yb29tX29jY3VwYW5jeV9wZXJjZW50YWdlX3Nl
cnZpY2UoKToKICAgIHdpdGggZ2V0X2RiX2Nvbm5lY3Rpb24oKSBhcyBjb25uOgogICAgICAgIHF1
ZXJ5ID0gIiIiCiAgICAgICAgU0VMRUNUIAogICAgICAgICAgICBDQVNFIAogICAgICAgICAgICAg
ICAgV0hFTiAoU0VMRUNUIENPVU5UKCopIEZST00gcm9vbXMpID0gMCBUSEVOIDAuMAogICAgICAg
ICAgICAgICAgRUxTRSAKICAgICAgICAgICAgICAgICAgICAoU0VMRUNUIENPVU5UKCopIEZST00g
cm9vbXMgV0hFUkUgY3VycmVudF9zdGF0dXNfaWQgPSAoU0VMRUNUIGlkIEZST00gcm9vbV9zdGF0
dXNlcyBXSEVSRSBuYW1lID0gJ9CX0LDQvdGP0YInKSkgKiAxMDAuMCAvCiAgICAgICAgICAgICAg
ICAgICAgKFNFTEVDVCBDT1VOVCgqKSBGUk9NIHJvb21zKQogICAgICAgICAgICBFTkQgQVMgcGVy
Y2VudGFnZV9vY2N1cGFuY3k7CiAgICAgICAgIiIiCiAgICAgICAgcmVzdWx0ID0gZXhlY3V0ZV9x
dWVyeShjb25uLCBxdWVyeSwgZmV0Y2hfb25lPVRydWUpCiAgICAgICAgcmV0dXJuIHJlc3VsdFsn
cGVyY2VudGFnZV9vY2N1cGFuY3knXSBpZiByZXN1bHQgYW5kIHJlc3VsdFsncGVyY2VudGFnZV9v
Y2N1cGFuY3knXSBpcyBub3QgTm9uZSBlbHNlIDAuMAoKZGVmIGdldF9hbGxfcm9vbXNfd2l0aF9k
ZXRhaWxzX3NlcnZpY2UoKToKICAgIHdpdGggZ2V0X2RiX2Nvbm5lY3Rpb24oKSBhcyBjb25uOgog
ICAgICAgIHF1ZXJ5ID0gIiIiCiAgICAgICAgU0VMRUNUIHIuaWQgYXMgcm9vbV9udW1iZXIsIGYu
bmFtZSBhcyBmbG9vcl9uYW1lLCBjLm5hbWUgYXMgY2F0ZWdvcnlfbmFtZSwgcnMubmFtZSBhcyBz
dGF0dXNfbmFtZQogICAgICAgIEZST00gcm9vbXMgcgogICAgICAgIExFRlQgSk9JTiBmbG9vcnMg
ZiBPTiByLmZsb29yX2lkID0gZi5pZAogICAgICAgIExFRlQgSk9JTiBjYXRlZ29yaWVzIGMgT04g
ci5jYXRlZ29yeV9pZCA9IGMuaWQKICAgICAgICBMRUZUIEpPSU4gcm9vbV9zdGF0dXNlcyBycyBP
TiByLmN1cnJlbnRfc3RhdHVzX2lkID0gcnMuaWQKICAgICAgICBPUkRFUiBCWSBmLmlkLCByLmlk
OyAKICAgICAgICAiIiIgIyBPUkRFUiBCWSBmLmlkINC00LvRjyDQv9GA0LDQstC40LvRjNC90L7Q
uSDRgdC+0YDRgtC40YDQvtCy0LrQuCDQv9C+INGN0YLQsNC20LDQvAogICAgICAgIHJldHVybiBl
eGVjdXRlX3F1ZXJ5KGNvbm4sIHF1ZXJ5LCBmZXRjaF9hbGw9VHJ1ZSkKCiMgLS0tIFZhbGlkYXRp
b24gU2VydmljZSAo0JzQvtC00YPQu9GMIDQpIC0tLQpkZWYgZ2V0X2Z1bGxuYW1lX2Zyb21fYXBp
KCk6CiAgICB0cnk6CiAgICAgICAgcmVzcG9uc2UgPSByZXF1ZXN0cy5nZXQoQVBJX1VSTF9GVUxM
TkFNRSwgdGltZW91dD01KQogICAgICAgIHJlc3BvbnNlLnJhaXNlX2Zvcl9zdGF0dXMoKQogICAg
ICAgIGRhdGEgPSByZXNwb25zZS5qc29uKCkKICAgICAgICByZXR1cm4gZGF0YS5nZXQoInZhbHVl
IikKICAgIGV4Y2VwdCByZXF1ZXN0cy5leGNlcHRpb25zLlJlcXVlc3RFeGNlcHRpb24gYXMgZToK
ICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJvcigi0J7RiNC40LHQutCwIEFQSSIsIGYi0J3QtSDR
g9C00LDQu9C+0YHRjCDQv9C+0LvRg9GH0LjRgtGMINC00LDQvdC90YvQtSDRgSBBUEk6IHtlfSIp
ICMg0KPQsdGA0LDQvSBwYXJlbnQKICAgICAgICBwcmludChmItCe0YjQuNCx0LrQsCBBUEk6IHtl
fSIpCiAgICAgICAgcmV0dXJuIE5vbmUKCmRlZiB2YWxpZGF0ZV9maW9fc2VydmljZShmaW9fc3Ry
aW5nKToKICAgICMg0K3RgtCwINGE0YPQvdC60YbQuNGPINC/0YDQvtGB0YLQviDQvtC/0YDQtdC0
0LXQu9GP0LXRgiwg0LXRgdGC0Ywg0LvQuCDQvtGI0LjQsdC60Lgg0LjQu9C4INC90LXRgiwg0LTQ
u9GPINCy0YvQstC+0LTQsCDQvtC00L3QvtCz0L4g0YHQvtC+0LHRidC10L3QuNGPCiAgICBpZiBu
b3QgZmlvX3N0cmluZzoKICAgICAgICByZXR1cm4gRmFsc2UgIyDQn9GD0YHRgtC+0LUg0KTQmNCe
INC90LXQstCw0LvQuNC00L3QvgoKICAgIGFsbG93ZWRfY2hhcnNfcGF0dGVybiA9IHIiXlvQsC3R
j9CQLdCv0ZHQgWEtekEtWlxzXC1dKyQiCiAgICBpZiBub3QgcmUuZnVsbG1hdGNoKGFsbG93ZWRf
Y2hhcnNfcGF0dGVybiwgZmlvX3N0cmluZyk6CiAgICAgICAgcmV0dXJuIEZhbHNlICMg0KHQvtC0
0LXRgNC20LjRgiDQt9Cw0L/RgNC10YnQtdC90L3Ri9C1INGB0LjQvNCy0L7Qu9GLCgogICAgd29y
ZHMgPSBmaW9fc3RyaW5nLnN0cmlwKCkuc3BsaXQoKQogICAgaWYgbm90ICgyIDw9IGxlbih3b3Jk
cykgPD0gMyk6CiAgICAgICAgcmV0dXJuIEZhbHNlICMg0J3QtSAyLTMg0YHQu9C+0LLQsAoKICAg
IGZvciB3b3JkIGluIHdvcmRzOgogICAgICAgIGlmIG5vdCB3b3JkIG9yIG5vdCB3b3JkWzBdLmlz
dXBwZXIoKTogIyDQn9GA0L7QstC10YDQutCwINC90LAg0L/Rg9GB0YLQvtC1INGB0LvQvtCy0L4g
0Lgg0LfQsNCz0LvQsNCy0L3Rg9GOINCx0YPQutCy0YMKICAgICAgICAgICAgcmV0dXJuIEZhbHNl
CiAgICByZXR1cm4gVHJ1ZQoKCiMgNS4gR1VJIENMQVNTRVMKCmNsYXNzIExvZ2luV2luZG93KHRr
LkZyYW1lKToKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBtYXN0ZXIsIGFwcF9jb250cm9sbGVyKToK
ICAgICAgICBzdXBlcigpLl9faW5pdF9fKG1hc3RlcikKICAgICAgICBzZWxmLmFwcF9jb250cm9s
bGVyID0gYXBwX2NvbnRyb2xsZXIKICAgICAgICBzZWxmLm1hc3Rlci50aXRsZSgi0JDQstGC0L7R
gNC40LfQsNGG0LjRjyAtINCh0LjRgdGC0LXQvNCwINCT0L7RgdGC0LjQvdC40YbRiyIpCiAgICAg
ICAgc2VsZi5tYXN0ZXIuZ2VvbWV0cnkoIjQwMHgzNTAiKQogICAgICAgIHNlbGYucGFjayhwYWR5
PTIwLCBwYWR4PTIwLCBmaWxsPSJib3RoIiwgZXhwYW5kPVRydWUpCgogICAgICAgIHRrLkxhYmVs
KHNlbGYsIHRleHQ9ItCS0YXQvtC0INCyINGB0LjRgdGC0LXQvNGDIiwgZm9udD0oIkFyaWFsIiwg
MTYpKS5wYWNrKHBhZHk9MTIsIHBhZHg9MTApCiAgICAgICAgCiAgICAgICAgIyBQbGFjZWhvbGRl
ciB0ZXh0INGD0LHRgNCw0L0sIHdpZHRoINCyINGB0LjQvNCy0L7Qu9Cw0YUgKNC/0YDQuNC80LXR
gNC90L4gMjUwcHggLT4gMzAtMzUg0YHQuNC80LLQvtC70L7QsikKICAgICAgICBzZWxmLmxvZ2lu
X2VudHJ5ID0gdGsuRW50cnkoc2VsZiwgd2lkdGg9MzUpIAogICAgICAgIHNlbGYubG9naW5fZW50
cnkucGFjayhwYWR5PTEyLCBwYWR4PTEwKQogICAgICAgIHNlbGYucGFzc3dvcmRfZW50cnkgPSB0
ay5FbnRyeShzZWxmLCBzaG93PSIqIiwgd2lkdGg9MzUpCiAgICAgICAgc2VsZi5wYXNzd29yZF9l
bnRyeS5wYWNrKHBhZHk9MTIsIHBhZHg9MTApCgogICAgICAgIHNlbGYuc2hvd19wYXNzd29yZF92
YXIgPSB0ay5Cb29sZWFuVmFyKCkKICAgICAgICBzZWxmLnNob3dfcGFzc3dvcmRfY2hlY2sgPSB0
ay5DaGVja2J1dHRvbihzZWxmLCB0ZXh0PSLQn9C+0LrQsNC30LDRgtGMINC/0LDRgNC+0LvRjCIs
CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhcmlh
YmxlPXNlbGYuc2hvd19wYXNzd29yZF92YXIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgIGNvbW1hbmQ9c2VsZi5fdG9nZ2xlX3Bhc3N3b3JkX3Zpc2li
aWxpdHkpCiAgICAgICAgc2VsZi5zaG93X3Bhc3N3b3JkX2NoZWNrLnBhY2socGFkeT01LCBwYWR4
PTEwKQoKICAgICAgICB0ay5CdXR0b24oc2VsZiwgdGV4dD0i0JLQvtC50YLQuCIsIGNvbW1hbmQ9
c2VsZi5fYXR0ZW1wdF9sb2dpbiwgd2lkdGg9MzApLnBhY2socGFkeT0yMCwgcGFkeD0xMCkKCiAg
ICBkZWYgX3RvZ2dsZV9wYXNzd29yZF92aXNpYmlsaXR5KHNlbGYpOgogICAgICAgIGlmIHNlbGYu
c2hvd19wYXNzd29yZF92YXIuZ2V0KCk6CiAgICAgICAgICAgIHNlbGYucGFzc3dvcmRfZW50cnku
Y29uZmlnKHNob3c9IiIpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgc2VsZi5wYXNzd29yZF9l
bnRyeS5jb25maWcoc2hvdz0iKiIpCgogICAgZGVmIF9hdHRlbXB0X2xvZ2luKHNlbGYpOgogICAg
ICAgIGxvZ2luID0gc2VsZi5sb2dpbl9lbnRyeS5nZXQoKQogICAgICAgIHBhc3N3b3JkID0gc2Vs
Zi5wYXNzd29yZF9lbnRyeS5nZXQoKQogICAgICAgIGlmIG5vdCBsb2dpbiBvciBub3QgcGFzc3dv
cmQ6CiAgICAgICAgICAgIG1lc3NhZ2Vib3guc2hvd2Vycm9yKCLQntGI0LjQsdC60LAiLCAi0JvQ
vtCz0LjQvSDQuCDQv9Cw0YDQvtC70Ywg0L7QsdGP0LfQsNGC0LXQu9GM0L3Riy4iLCBwYXJlbnQ9
c2VsZi5tYXN0ZXIpCiAgICAgICAgICAgIHJldHVybgogICAgICAgIHRyeToKICAgICAgICAgICAg
cmVzdWx0ID0gbG9naW5fdXNlcl9zZXJ2aWNlKGxvZ2luLCBwYXNzd29yZCkKICAgICAgICAgICAg
aWYgcmVzdWx0WyJzdGF0dXMiXSA9PSAic3VjY2VzcyI6CiAgICAgICAgICAgICAgICBzZWxmLmFw
cF9jb250cm9sbGVyLmN1cnJlbnRfdXNlciA9IHJlc3VsdFsidXNlciJdCiAgICAgICAgICAgICAg
ICBtZXNzYWdlYm94LnNob3dpbmZvKCLQo9GB0L/QtdGFIiwgZiLQlNC+0LHRgNC+INC/0L7QttCw
0LvQvtCy0LDRgtGMLCB7cmVzdWx0Wyd1c2VyJ10uZ2V0KCdmdWxsX25hbWUnLCByZXN1bHRbJ3Vz
ZXInXVsnbG9naW4nXSl9ISIsIHBhcmVudD1zZWxmLm1hc3RlcikKICAgICAgICAgICAgICAgIGlm
IHJlc3VsdFsiZm9yY2VfcGFzc3dvcmRfY2hhbmdlIl06CiAgICAgICAgICAgICAgICAgICAgc2Vs
Zi5hcHBfY29udHJvbGxlci5zaG93X2NoYW5nZV9wYXNzd29yZF93aW5kb3coaW5pdGlhbF9jaGFu
Z2U9VHJ1ZSkKICAgICAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICAgICAgc2VsZi5h
cHBfY29udHJvbGxlci5zaG93X2Rhc2hib2FyZF9mb3Jfcm9sZShyZXN1bHRbInVzZXIiXVsncm9s
ZSddKQogICAgICAgICAgICAgICAgc2VsZi5kZXN0cm95KCkKICAgICAgICAgICAgZWxzZToKICAg
ICAgICAgICAgICAgIG1lc3NhZ2Vib3guc2hvd2Vycm9yKCLQntGI0LjQsdC60LAg0LLRhdC+0LTQ
sCIsIHJlc3VsdFsibWVzc2FnZSJdLCBwYXJlbnQ9c2VsZi5tYXN0ZXIpCiAgICAgICAgZXhjZXB0
IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJvcigi0JrRgNC4
0YLQuNGH0LXRgdC60LDRjyDQvtGI0LjQsdC60LAiLCBmItCe0YjQuNCx0LrQsCDQv9GA0Lgg0L/Q
vtC/0YvRgtC60LUg0LLRhdC+0LTQsDoge2V9IiwgcGFyZW50PXNlbGYubWFzdGVyKQoKCmNsYXNz
IENoYW5nZVBhc3N3b3JkV2luZG93KHRrLlRvcGxldmVsKToKICAgIGRlZiBfX2luaXRfXyhzZWxm
LCBtYXN0ZXIsIGFwcF9jb250cm9sbGVyLCBpbml0aWFsX2NoYW5nZT1GYWxzZSk6CiAgICAgICAg
c3VwZXIoKS5fX2luaXRfXyhtYXN0ZXIpCiAgICAgICAgc2VsZi5hcHBfY29udHJvbGxlciA9IGFw
cF9jb250cm9sbGVyCiAgICAgICAgc2VsZi51c2VyX2lkID0gc2VsZi5hcHBfY29udHJvbGxlci5j
dXJyZW50X3VzZXJbJ2lkJ10KICAgICAgICBzZWxmLmluaXRpYWxfY2hhbmdlID0gaW5pdGlhbF9j
aGFuZ2UKICAgICAgICBzZWxmLnRpdGxlKCLQodC80LXQvdCwINC/0LDRgNC+0LvRjyIpCiAgICAg
ICAgc2VsZi5nZW9tZXRyeSgiNDAweDM1MCIpCiAgICAgICAgCiAgICAgICAgc2VsZi50cmFuc2ll
bnQobWFzdGVyKSAjINCe0LrQvdC+INCx0YPQtNC10YIg0L/QvtCy0LXRgNGFINGA0L7QtNC40YLQ
tdC70YzRgdC60L7Qs9C+INC4INGB0LLQtdGA0L3Rg9GC0L4g0YEg0L3QuNC8CgogICAgICAgIHRr
LkxhYmVsKHNlbGYsIHRleHQ9ItCh0LzQtdC90LAg0L/QsNGA0L7Qu9GPIiwgZm9udD0oIkFyaWFs
IiwgMTYpKS5wYWNrKHBhZHk9MTApCiAgICAgICAgIyBQbGFjZWhvbGRlciB0ZXh0INGD0LHRgNCw
0L0sIHdpZHRoINCyINGB0LjQvNCy0L7Qu9Cw0YUgKNC/0YDQuNC80LXRgNC90L4gMzAwcHggLT4g
NDAg0YHQuNC80LLQvtC70L7QsikKICAgICAgICBzZWxmLmN1cnJlbnRfcGFzc19lbnRyeSA9IHRr
LkVudHJ5KHNlbGYsIHNob3c9IioiLCB3aWR0aD00MCkKICAgICAgICBzZWxmLmN1cnJlbnRfcGFz
c19lbnRyeS5wYWNrKHBhZHk9MTAsIHBhZHg9MjAsIGZpbGw9IngiKQogICAgICAgIHNlbGYubmV3
X3Bhc3NfZW50cnkgPSB0ay5FbnRyeShzZWxmLCBzaG93PSIqIiwgd2lkdGg9NDApCiAgICAgICAg
c2VsZi5uZXdfcGFzc19lbnRyeS5wYWNrKHBhZHk9MTAsIHBhZHg9MjAsIGZpbGw9IngiKQogICAg
ICAgIHNlbGYuY29uZmlybV9wYXNzX2VudHJ5ID0gdGsuRW50cnkoc2VsZiwgc2hvdz0iKiIsIHdp
ZHRoPTQwKQogICAgICAgIHNlbGYuY29uZmlybV9wYXNzX2VudHJ5LnBhY2socGFkeT0xMCwgcGFk
eD0yMCwgZmlsbD0ieCIpCiAgICAgICAgdGsuQnV0dG9uKHNlbGYsIHRleHQ9ItCY0LfQvNC10L3Q
uNGC0Ywg0L/QsNGA0L7Qu9GMIiwgY29tbWFuZD1zZWxmLl9hdHRlbXB0X2NoYW5nZSwgd2lkdGg9
MzUpLnBhY2socGFkeT0yMCkKICAgICAgICAKICAgICAgICBpZiBzZWxmLmluaXRpYWxfY2hhbmdl
OgogICAgICAgICAgICBzZWxmLnByb3RvY29sKCJXTV9ERUxFVEVfV0lORE9XIiwgbGFtYmRhOiBt
ZXNzYWdlYm94LnNob3d3YXJuaW5nKCLQodC80LXQvdCwINC/0LDRgNC+0LvRjyIsICLQn9C+0LbQ
sNC70YPQudGB0YLQsCwg0YHQvNC10L3QuNGC0LUg0L/QsNGA0L7Qu9GMLiIsIHBhcmVudD1zZWxm
KSkKCiAgICBkZWYgX2F0dGVtcHRfY2hhbmdlKHNlbGYpOgogICAgICAgIGN1ciA9IHNlbGYuY3Vy
cmVudF9wYXNzX2VudHJ5LmdldCgpCiAgICAgICAgbmV3ID0gc2VsZi5uZXdfcGFzc19lbnRyeS5n
ZXQoKQogICAgICAgIGNvbmYgPSBzZWxmLmNvbmZpcm1fcGFzc19lbnRyeS5nZXQoKQogICAgICAg
IAogICAgICAgIGlmIG5vdCBhbGwoW2N1ciwgbmV3LCBjb25mXSk6CiAgICAgICAgICAgIG1lc3Nh
Z2Vib3guc2hvd2Vycm9yKCLQntGI0LjQsdC60LAiLCAi0JLRgdC1INC/0L7Qu9GPINC+0LHRj9C3
0LDRgtC10LvRjNC90YsuIiwgcGFyZW50PXNlbGYpCiAgICAgICAgICAgIHJldHVybgogICAgICAg
IGlmIG5ldyAhPSBjb25mOgogICAgICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJvcigi0J7RiNC4
0LHQutCwIiwgItCd0L7QstGL0LUg0L/QsNGA0L7Qu9C4INC90LUg0YHQvtCy0L/QsNC00LDRjtGC
LiIsIHBhcmVudD1zZWxmKQogICAgICAgICAgICByZXR1cm4KICAgICAgICBpZiBsZW4obmV3KSA8
IDE6ICMg0KPQv9GA0L7RidC10L3QvgogICAgICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJvcigi
0J7RiNC40LHQutCwIiwgItCd0L7QstGL0Lkg0L/QsNGA0L7Qu9GMINC90LUg0LzQvtC20LXRgiDQ
sdGL0YLRjCDQv9GD0YHRgtGL0LwuIiwgcGFyZW50PXNlbGYpCiAgICAgICAgICAgIHJldHVybgog
ICAgICAgIAogICAgICAgIHRyeToKICAgICAgICAgICAgcmVzdWx0ID0gY2hhbmdlX3Bhc3N3b3Jk
X3NlcnZpY2Uoc2VsZi51c2VyX2lkLCBjdXIsIG5ldykKICAgICAgICAgICAgaWYgcmVzdWx0WyJz
dGF0dXMiXSA9PSAic3VjY2VzcyI6CiAgICAgICAgICAgICAgICBtZXNzYWdlYm94LnNob3dpbmZv
KCLQo9GB0L/QtdGFIiwgcmVzdWx0WyJtZXNzYWdlIl0sIHBhcmVudD1zZWxmKQogICAgICAgICAg
ICAgICAgc2VsZi5kZXN0cm95KCkKICAgICAgICAgICAgICAgIGlmIHNlbGYuaW5pdGlhbF9jaGFu
Z2U6CiAgICAgICAgICAgICAgICAgICAgc2VsZi5hcHBfY29udHJvbGxlci5zaG93X2Rhc2hib2Fy
ZF9mb3Jfcm9sZShzZWxmLmFwcF9jb250cm9sbGVyLmN1cnJlbnRfdXNlclsncm9sZSddKQogICAg
ICAgICAgICBlbHNlOgogICAgICAgICAgICAgICAgbWVzc2FnZWJveC5zaG93ZXJyb3IoItCe0YjQ
uNCx0LrQsCDRgdC80LXQvdGLIiwgcmVzdWx0WyJtZXNzYWdlIl0sIHBhcmVudD1zZWxmKQogICAg
ICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgIG1lc3NhZ2Vib3guc2hvd2Vy
cm9yKCLQmtGA0LjRgtC40YfQtdGB0LrQsNGPINC+0YjQuNCx0LrQsCIsIGYi0J7RiNC40LHQutCw
INC/0YDQuCDRgdC80LXQvdC1INC/0LDRgNC+0LvRjzoge2V9IiwgcGFyZW50PXNlbGYpCgoKY2xh
c3MgVXNlck1hbmFnZW1lbnRXaW5kb3codGsuVG9wbGV2ZWwpOgogICAgZGVmIF9faW5pdF9fKHNl
bGYsIG1hc3RlciwgYXBwX2NvbnRyb2xsZXIpOgogICAgICAgIHN1cGVyKCkuX19pbml0X18obWFz
dGVyKQogICAgICAgIHNlbGYuYXBwX2NvbnRyb2xsZXIgPSBhcHBfY29udHJvbGxlcgogICAgICAg
IHNlbGYudGl0bGUoItCj0L/RgNCw0LLQu9C10L3QuNC1INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvR
j9C80LgiKQogICAgICAgIHNlbGYuZ2VvbWV0cnkoIjg1MHg1MDAiKQogICAgICAgIAogICAgICAg
IHNlbGYudHJhbnNpZW50KG1hc3RlcikKICAgICAgICAKICAgICAgICBidG5fZnJhbWUgPSB0ay5G
cmFtZShzZWxmKSAjINCX0LDQvNC10L3QsCBjdGsuQ1RrRnJhbWUg0L3QsCB0ay5GcmFtZQogICAg
ICAgIGJ0bl9mcmFtZS5wYWNrKHBhZHk9MTAsIHBhZHg9MTAsIGZpbGw9IngiKQogICAgICAgIHRr
LkJ1dHRvbihidG5fZnJhbWUsIHRleHQ9ItCU0L7QsdCw0LLQuNGC0YwiLCBjb21tYW5kPXNlbGYu
X29wZW5fYWRkX2VkaXRfZGlhbG9nKS5wYWNrKHNpZGU9ImxlZnQiLCBwYWR4PTUpCiAgICAgICAg
dGsuQnV0dG9uKGJ0bl9mcmFtZSwgdGV4dD0i0KDQtdC00LDQutGC0LjRgNC+0LLQsNGC0YwiLCBj
b21tYW5kPWxhbWJkYTogc2VsZi5fb3Blbl9hZGRfZWRpdF9kaWFsb2coZWRpdF9tb2RlPVRydWUp
KS5wYWNrKHNpZGU9ImxlZnQiLCBwYWR4PTUpCiAgICAgICAgdGsuQnV0dG9uKGJ0bl9mcmFtZSwg
dGV4dD0i0J7QsdC90L7QstC40YLRjCIsIGNvbW1hbmQ9c2VsZi5fbG9hZF91c2VycykucGFjayhz
aWRlPSJsZWZ0IiwgcGFkeD01KQoKICAgICAgICBzdHlsZSA9IHR0ay5TdHlsZShzZWxmKQogICAg
ICAgIHN0eWxlLnRoZW1lX3VzZSgiZGVmYXVsdCIpICMg0LjQu9C4INC00YDRg9Cz0LDRjyDQtNC+
0YHRgtGD0L/QvdCw0Y8g0YLQtdC80LAKICAgICAgICBzdHlsZS5jb25maWd1cmUoIlRyZWV2aWV3
LkhlYWRpbmciLCBmb250PSgnQXJpYWwnLCAxMCwgJ2JvbGQnKSkKICAgICAgICBzZWxmLnRyZWUg
PSB0dGsuVHJlZXZpZXcoc2VsZiwgY29sdW1ucz0oImlkIiwgImxvZ2luIiwgImZ1bGxfbmFtZSIs
ICJyb2xlIiwgImlzX2Jsb2NrZWQiKSwgc2hvdz0iaGVhZGluZ3MiKQogICAgICAgIAogICAgICAg
IHNlbGYudHJlZS5oZWFkaW5nKCJpZCIsIHRleHQ9IklEIikKICAgICAgICBzZWxmLnRyZWUuY29s
dW1uKCJpZCIsIHdpZHRoPTUwLCBzdHJldGNoPUZhbHNlLCBhbmNob3I9ImNlbnRlciIpCiAgICAg
ICAgc2VsZi50cmVlLmhlYWRpbmcoImxvZ2luIiwgdGV4dD0i0JvQvtCz0LjQvSIpCiAgICAgICAg
c2VsZi50cmVlLmNvbHVtbigibG9naW4iLCB3aWR0aD0xNTAsIGFuY2hvcj0idyIpCiAgICAgICAg
c2VsZi50cmVlLmhlYWRpbmcoImZ1bGxfbmFtZSIsIHRleHQ9ItCk0JjQniIpCiAgICAgICAgc2Vs
Zi50cmVlLmNvbHVtbigiZnVsbF9uYW1lIiwgd2lkdGg9MjUwLCBhbmNob3I9InciKQogICAgICAg
IHNlbGYudHJlZS5oZWFkaW5nKCJyb2xlIiwgdGV4dD0i0KDQvtC70YwiKQogICAgICAgIHNlbGYu
dHJlZS5jb2x1bW4oInJvbGUiLCB3aWR0aD0xMjAsIGFuY2hvcj0idyIpCiAgICAgICAgc2VsZi50
cmVlLmhlYWRpbmcoImlzX2Jsb2NrZWQiLCB0ZXh0PSLQkdC70L7QuiIpCiAgICAgICAgc2VsZi50
cmVlLmNvbHVtbigiaXNfYmxvY2tlZCIsIHdpZHRoPTgwLCBzdHJldGNoPUZhbHNlLCBhbmNob3I9
ImNlbnRlciIpCiAgICAgICAgCiAgICAgICAgc2VsZi50cmVlLnBhY2socGFkeT0xMCwgcGFkeD0x
MCwgZmlsbD0iYm90aCIsIGV4cGFuZD1UcnVlKQogICAgICAgIHNlbGYuX2xvYWRfdXNlcnMoKQoK
ICAgIGRlZiBfbG9hZF91c2VycyhzZWxmKToKICAgICAgICBmb3IgaSBpbiBzZWxmLnRyZWUuZ2V0
X2NoaWxkcmVuKCk6CiAgICAgICAgICAgIHNlbGYudHJlZS5kZWxldGUoaSkKICAgICAgICB0cnk6
CiAgICAgICAgICAgIHVzZXJzID0gZ2V0X2FsbF91c2Vyc19zZXJ2aWNlKCkKICAgICAgICAgICAg
aWYgdXNlcnM6CiAgICAgICAgICAgICAgICBmb3IgdXNlciBpbiB1c2VyczoKICAgICAgICAgICAg
ICAgICAgICBzZWxmLnRyZWUuaW5zZXJ0KCIiLCAiZW5kIiwgdmFsdWVzPSgKICAgICAgICAgICAg
ICAgICAgICAgICAgdXNlclsnaWQnXSwgCiAgICAgICAgICAgICAgICAgICAgICAgIHVzZXJbJ2xv
Z2luJ10sIAogICAgICAgICAgICAgICAgICAgICAgICB1c2VyLmdldCgnZnVsbF9uYW1lJywnJyks
ICMg0JjRgdC/0L7Qu9GM0LfRg9C10LwgZ2V0INC00LvRjyDQsdC10LfQvtC/0LDRgdC90L7RgdGC
0LgKICAgICAgICAgICAgICAgICAgICAgICAgdXNlclsncm9sZSddLCAKICAgICAgICAgICAgICAg
ICAgICAgICAgItCU0LAiIGlmIHVzZXIuZ2V0KCdpc19ibG9ja2VkJywgRmFsc2UpIGVsc2UgItCd
0LXRgiIKICAgICAgICAgICAgICAgICAgICApKQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMg
ZToKICAgICAgICAgICAgbWVzc2FnZWJveC5zaG93ZXJyb3IoItCe0YjQuNCx0LrQsCDQt9Cw0LPR
gNGD0LfQutC4IiwgZiLQndC1INGD0LTQsNC70L7RgdGMINC30LDQs9GA0YPQt9C40YLRjCDQv9C+
0LvRjNC30L7QstCw0YLQtdC70LXQuToge2V9IiwgcGFyZW50PXNlbGYpCgoKICAgIGRlZiBfb3Bl
bl9hZGRfZWRpdF9kaWFsb2coc2VsZiwgZWRpdF9tb2RlPUZhbHNlKToKICAgICAgICB1c2VyX2Rh
dGFfdG9fZWRpdCA9IE5vbmUKICAgICAgICBpZiBlZGl0X21vZGU6CiAgICAgICAgICAgIHNlbGVj
dGVkX2l0ZW0gPSBzZWxmLnRyZWUuZm9jdXMoKQogICAgICAgICAgICBpZiBub3Qgc2VsZWN0ZWRf
aXRlbToKICAgICAgICAgICAgICAgIG1lc3NhZ2Vib3guc2hvd3dhcm5pbmcoItCS0YvQsdC+0YAi
LCAi0JLRi9Cx0LXRgNC40YLQtSDQv9C+0LvRjNC30L7QstCw0YLQtdC70Y8g0LTQu9GPINGA0LXQ
tNCw0LrRgtC40YDQvtCy0LDQvdC40Y8uIiwgcGFyZW50PXNlbGYpCiAgICAgICAgICAgICAgICBy
ZXR1cm4KICAgICAgICAgICAgdXNlcl9pZF9zZWxlY3RlZCA9IHNlbGYudHJlZS5pdGVtKHNlbGVj
dGVkX2l0ZW0pWyd2YWx1ZXMnXVswXQogICAgICAgICAgICAKICAgICAgICAgICAgdHJ5OiAjINCf
0L7Qu9GD0YfQsNC10Lwg0YHQstC10LbQuNC1INC00LDQvdC90YvQtSDQv9C+0LvRjNC30L7QstCw
0YLQtdC70Y8g0LTQu9GPINGA0LXQtNCw0LrRgtC40YDQvtCy0LDQvdC40Y8KICAgICAgICAgICAg
ICAgIGFsbF91c2VycyA9IGdldF9hbGxfdXNlcnNfc2VydmljZSgpCiAgICAgICAgICAgICAgICBp
ZiBhbGxfdXNlcnM6CiAgICAgICAgICAgICAgICAgICAgZm9yIHVfZGF0YSBpbiBhbGxfdXNlcnM6
CiAgICAgICAgICAgICAgICAgICAgICAgIGlmIHVfZGF0YVsnaWQnXSA9PSB1c2VyX2lkX3NlbGVj
dGVkOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgdXNlcl9kYXRhX3RvX2VkaXQgPSB1X2Rh
dGEKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAgICAgICBpZiBu
b3QgdXNlcl9kYXRhX3RvX2VkaXQ6CiAgICAgICAgICAgICAgICAgICAgIG1lc3NhZ2Vib3guc2hv
d2Vycm9yKCLQntGI0LjQsdC60LAiLCAi0J3QtSDQvdCw0LnQtNC10L3RiyDQtNCw0L3QvdGL0LUg
0L/QvtC70YzQt9C+0LLQsNGC0LXQu9GPINC00LvRjyDRgNC10LTQsNC60YLQuNGA0L7QstCw0L3Q
uNGPLiIsIHBhcmVudD1zZWxmKQogICAgICAgICAgICAgICAgICAgICByZXR1cm4KICAgICAgICAg
ICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgICAgbWVzc2FnZWJveC5zaG93
ZXJyb3IoItCe0YjQuNCx0LrQsCIsIGYi0J3QtSDRg9C00LDQu9C+0YHRjCDQv9C+0LvRg9GH0LjR
gtGMINC00LDQvdC90YvQtSDQv9C+0LvRjNC30L7QstCw0YLQtdC70Y86IHtlfSIsIHBhcmVudD1z
ZWxmKQogICAgICAgICAgICAgICAgcmV0dXJuCgogICAgICAgIEFkZEVkaXRVc2VyRGlhbG9nKHNl
bGYsIHNlbGYuYXBwX2NvbnRyb2xsZXIsIG1vZGU9KCJlZGl0IiBpZiBlZGl0X21vZGUgZWxzZSAi
YWRkIiksIHVzZXJfZGF0YT11c2VyX2RhdGFfdG9fZWRpdCwgY2FsbGJhY2s9c2VsZi5fbG9hZF91
c2VycykKCgpjbGFzcyBBZGRFZGl0VXNlckRpYWxvZyh0ay5Ub3BsZXZlbCk6CiAgICBkZWYgX19p
bml0X18oc2VsZiwgbWFzdGVyLCBhcHBfY29udHJvbGxlciwgbW9kZT0iYWRkIiwgdXNlcl9kYXRh
PU5vbmUsIGNhbGxiYWNrPU5vbmUpOgogICAgICAgIHN1cGVyKCkuX19pbml0X18obWFzdGVyKQog
ICAgICAgIHNlbGYubW9kZSA9IG1vZGUKICAgICAgICBzZWxmLnVzZXJfZGF0YSA9IHVzZXJfZGF0
YSAjINCt0YLQviBkaWN0INC/0L7Qu9GM0LfQvtCy0LDRgtC10LvRjywg0LXRgdC70LggbW9kZT0i
ZWRpdCIKICAgICAgICBzZWxmLmNhbGxiYWNrID0gY2FsbGJhY2sKICAgICAgICBzZWxmLmFwcF9j
b250cm9sbGVyID0gYXBwX2NvbnRyb2xsZXIgCgogICAgICAgIGlmIG1vZGUgPT0gImFkZCI6CiAg
ICAgICAgICAgIHNlbGYudGl0bGUoItCU0L7QsdCw0LLQuNGC0Ywg0L/QvtC70YzQt9C+0LLQsNGC
0LXQu9GPIikKICAgICAgICBlbHNlOgogICAgICAgICAgICBzZWxmLnRpdGxlKGYi0KDQtdC00LDQ
utGC0LjRgNC+0LLQsNGC0Yw6IHt1c2VyX2RhdGEuZ2V0KCdsb2dpbicsICcnKX0iKQogICAgICAg
IAogICAgICAgIHNlbGYuZ2VvbWV0cnkoIjQ1MHg0NTAiKQogICAgICAgIHNlbGYudHJhbnNpZW50
KG1hc3RlcikKCiAgICAgICAgdGsuTGFiZWwoc2VsZiwgdGV4dD0i0JvQvtCz0LjQvToiKS5wYWNr
KGFuY2hvcj0idyIsIHBhZHg9MjAsIHBhZHk9KDEwLDApKQogICAgICAgIHNlbGYubG9naW5fZW50
cnkgPSB0ay5FbnRyeShzZWxmLCB3aWR0aD01MCkgIyB3aWR0aCA0MDBweCAtPiB+NTAgY2hhcnMK
ICAgICAgICBzZWxmLmxvZ2luX2VudHJ5LnBhY2socGFkeD0yMCwgcGFkeT0oMCwxMCksIGZpbGw9
IngiKQogICAgICAgIAogICAgICAgIHRrLkxhYmVsKHNlbGYsIHRleHQ9ItCk0JjQnjoiKS5wYWNr
KGFuY2hvcj0idyIsIHBhZHg9MjAsIHBhZHk9KDUsMCkpCiAgICAgICAgc2VsZi5mbmFtZV9lbnRy
eSA9IHRrLkVudHJ5KHNlbGYsIHdpZHRoPTUwKQogICAgICAgIHNlbGYuZm5hbWVfZW50cnkucGFj
ayhwYWR4PTIwLCBwYWR5PSgwLDEwKSwgZmlsbD0ieCIpCiAgICAgICAgCiAgICAgICAgdGsuTGFi
ZWwoc2VsZiwgdGV4dD0i0KDQvtC70Yw6IikucGFjayhhbmNob3I9InciLCBwYWR4PTIwLCBwYWR5
PSg1LDApKQogICAgICAgIHNlbGYucm9sZV92YXIgPSB0ay5TdHJpbmdWYXIodmFsdWU9ItCf0L7Q
u9GM0LfQvtCy0LDRgtC10LvRjCIpICMg0JfQvdCw0YfQtdC90LjQtSDQv9C+INGD0LzQvtC70YfQ
sNC90LjRjgogICAgICAgICMg0KPQsdGA0LDQu9C4IHdpZHRoINC00LvRjyBPcHRpb25NZW51LCDQ
vtC9INGB0LDQvCDQv9C+0LTRgdGC0YDQvtC40YLRgdGPLiDQn9C10YDQtdC00LDRh9CwIHZhbHVl
cyDRh9C10YDQtdC3ICoKICAgICAgICByb2xlcyA9IFsi0J/QvtC70YzQt9C+0LLQsNGC0LXQu9GM
IiwgItCQ0LTQvNC40L3QuNGB0YLRgNCw0YLQvtGAIl0KICAgICAgICB0ay5PcHRpb25NZW51KHNl
bGYsIHNlbGYucm9sZV92YXIsICpyb2xlcykucGFjayhwYWR4PTIwLCBwYWR5PSgwLDEwKSwgZmls
bD0ieCIpCiAgICAgICAgCiAgICAgICAgcGFzc19sYWJlbF90ZXh0ID0gItCf0LDRgNC+0LvRjDoi
IGlmIG1vZGUgPT0gImFkZCIgZWxzZSAi0J3QvtCy0YvQuSDQv9Cw0YDQvtC70YwgKNC/0YPRgdGC
0L4gLSDQvdC1INC80LXQvdGP0YLRjCk6IgogICAgICAgIHRrLkxhYmVsKHNlbGYsIHRleHQ9cGFz
c19sYWJlbF90ZXh0KS5wYWNrKGFuY2hvcj0idyIsIHBhZHg9MjAsIHBhZHk9KDUsMCkpCiAgICAg
ICAgc2VsZi5wYXNzX2VudHJ5ID0gdGsuRW50cnkoc2VsZiwgc2hvdz0iKiIsIHdpZHRoPTUwKQog
ICAgICAgIHNlbGYucGFzc19lbnRyeS5wYWNrKHBhZHg9MjAsIHBhZHk9KDAsMTApLCBmaWxsPSJ4
IikKCiAgICAgICAgaWYgbW9kZSA9PSAiZWRpdCI6CiAgICAgICAgICAgIHNlbGYuYmxvY2tfdmFy
ID0gdGsuQm9vbGVhblZhcih2YWx1ZT11c2VyX2RhdGEuZ2V0KCdpc19ibG9ja2VkJywgRmFsc2Up
KQogICAgICAgICAgICB0ay5DaGVja2J1dHRvbihzZWxmLCB0ZXh0PSLQl9Cw0LHQu9C+0LrQuNGA
0L7QstCw0L0iLCB2YXJpYWJsZT1zZWxmLmJsb2NrX3ZhcikucGFjayhhbmNob3I9InciLCBwYWR4
PTIwLCBwYWR5PSg1LDEwKSkKICAgICAgICAKICAgICAgICBpZiB1c2VyX2RhdGE6ICMg0J/RgNC1
0LTQt9Cw0L/QvtC70L3QtdC90LjQtSDQtNC70Y8g0YDQtdC20LjQvNCwINGA0LXQtNCw0LrRgtC4
0YDQvtCy0LDQvdC40Y8KICAgICAgICAgICAgc2VsZi5sb2dpbl9lbnRyeS5pbnNlcnQoMCwgdXNl
cl9kYXRhLmdldCgnbG9naW4nLCcnKSkKICAgICAgICAgICAgc2VsZi5mbmFtZV9lbnRyeS5pbnNl
cnQoMCwgdXNlcl9kYXRhLmdldCgnZnVsbF9uYW1lJywnJykpCiAgICAgICAgICAgIHNlbGYucm9s
ZV92YXIuc2V0KHVzZXJfZGF0YS5nZXQoJ3JvbGUnLCfQn9C+0LvRjNC30L7QstCw0YLQtdC70Ywn
KSkKCiAgICAgICAgdGsuQnV0dG9uKHNlbGYsIHRleHQ9ItCh0L7RhdGA0LDQvdC40YLRjCIsIGNv
bW1hbmQ9c2VsZi5fc2F2ZSwgd2lkdGg9NDUpLnBhY2socGFkeT0yMCkgIyB3aWR0aCA0MDBweCAt
PiB+NDUtNTAgY2hhcnMgKNC00LvRjyDQutC90L7Qv9C60LgpCgogICAgZGVmIF9zYXZlKHNlbGYp
OgogICAgICAgIGxvZ2luID0gc2VsZi5sb2dpbl9lbnRyeS5nZXQoKQogICAgICAgIGZuYW1lID0g
c2VsZi5mbmFtZV9lbnRyeS5nZXQoKQogICAgICAgIHJvbGUgPSBzZWxmLnJvbGVfdmFyLmdldCgp
CiAgICAgICAgcGFzc3dvcmQgPSBzZWxmLnBhc3NfZW50cnkuZ2V0KCkKCiAgICAgICAgaWYgbm90
IGxvZ2luOgogICAgICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJvcigi0J7RiNC40LHQutCwIiwg
ItCb0L7Qs9C40L0g0L7QsdGP0LfQsNGC0LXQu9C10L0uIiwgcGFyZW50PXNlbGYpCiAgICAgICAg
ICAgIHJldHVybgogICAgICAgIGlmIHNlbGYubW9kZSA9PSAiYWRkIiBhbmQgbm90IHBhc3N3b3Jk
OgogICAgICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJvcigi0J7RiNC40LHQutCwIiwgItCf0LDR
gNC+0LvRjCDQvtCx0Y/Qt9Cw0YLQtdC70LXQvSDQtNC70Y8g0L3QvtCy0L7Qs9C+INC/0L7Qu9GM
0LfQvtCy0LDRgtC10LvRjy4iLCBwYXJlbnQ9c2VsZikKICAgICAgICAgICAgcmV0dXJuCgogICAg
ICAgIHJlc3VsdCA9IE5vbmUKICAgICAgICB0cnk6CiAgICAgICAgICAgIGlmIHNlbGYubW9kZSA9
PSAiYWRkIjoKICAgICAgICAgICAgICAgIHJlc3VsdCA9IGNyZWF0ZV91c2VyX3NlcnZpY2UobG9n
aW4sIHBhc3N3b3JkLCByb2xlLCBmbmFtZSkKICAgICAgICAgICAgZWxzZTogIyBlZGl0IG1vZGUK
ICAgICAgICAgICAgICAgIGlzX2Jsb2NrZWRfdmFsID0gc2VsZi5ibG9ja192YXIuZ2V0KCkgaWYg
aGFzYXR0cihzZWxmLCAnYmxvY2tfdmFyJykgZWxzZSBzZWxmLnVzZXJfZGF0YS5nZXQoJ2lzX2Js
b2NrZWQnKSAKICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdXBkYXRlX3BhcmFtcyA9
IHsndXNlcl9pZCc6IHNlbGYudXNlcl9kYXRhWydpZCddfQogICAgICAgICAgICAgICAgIyDQn9C1
0YDQtdC00LDQtdC8INC/0LDRgNCw0LzQtdGC0YDRiywg0YLQvtC70YzQutC+INC10YHQu9C4INC+
0L3QuCDQuNC30LzQtdC90LjQu9C40YHRjCwg0LjQu9C4INGN0YLQviDQvdC+0LLRi9C5INC/0LDR
gNC+0LvRjAogICAgICAgICAgICAgICAgaWYgbG9naW4gIT0gc2VsZi51c2VyX2RhdGEuZ2V0KCds
b2dpbicpOiB1cGRhdGVfcGFyYW1zWydsb2dpbiddID0gbG9naW4KICAgICAgICAgICAgICAgIGlm
IGZuYW1lICE9IHNlbGYudXNlcl9kYXRhLmdldCgnZnVsbF9uYW1lJyk6IHVwZGF0ZV9wYXJhbXNb
J2Z1bGxfbmFtZSddID0gZm5hbWUKICAgICAgICAgICAgICAgIGlmIHJvbGUgIT0gc2VsZi51c2Vy
X2RhdGEuZ2V0KCdyb2xlJyk6IHVwZGF0ZV9wYXJhbXNbJ3JvbGUnXSA9IHJvbGUKICAgICAgICAg
ICAgICAgIGlmIHBhc3N3b3JkOiB1cGRhdGVfcGFyYW1zWyduZXdfcGFzc3dvcmQnXSA9IHBhc3N3
b3JkIAogICAgICAgICAgICAgICAgaWYgaXNfYmxvY2tlZF92YWwgIT0gc2VsZi51c2VyX2RhdGEu
Z2V0KCdpc19ibG9ja2VkJyk6CiAgICAgICAgICAgICAgICAgICAgdXBkYXRlX3BhcmFtc1snaXNf
YmxvY2tlZCddID0gaXNfYmxvY2tlZF92YWwKICAgICAgICAgICAgICAgIAogICAgICAgICAgICAg
ICAgdWlkX3RlbXAgPSB1cGRhdGVfcGFyYW1zLnBvcCgndXNlcl9pZCcpICMgdXNlcl9pZCDQv9C1
0YDQtdC00LDQtdGC0YHRjyDQv9C10YDQstGL0Lwg0LDRgNCz0YPQvNC10L3RgtC+0LwKICAgICAg
ICAgICAgICAgIGlmIGxlbih1cGRhdGVfcGFyYW1zKSA+IDA6ICMg0KLQvtC70YzQutC+INC10YHQ
u9C4INC10YHRgtGMINGH0YLQviDQvtCx0L3QvtCy0LvRj9GC0YwKICAgICAgICAgICAgICAgICAg
ICAgcmVzdWx0ID0gdXBkYXRlX3VzZXJfc2VydmljZSh1aWRfdGVtcCwgKip1cGRhdGVfcGFyYW1z
KQogICAgICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgICAgICAgcmVzdWx0ID0geyJz
dGF0dXMiOiAiaW5mbyIsICJtZXNzYWdlIjogItCd0LXRgiDQuNC30LzQtdC90LXQvdC40Lkg0LTQ
u9GPINGB0L7RhdGA0LDQvdC10L3QuNGPLiJ9CgogICAgICAgICAgICBpZiByZXN1bHQgYW5kIHJl
c3VsdFsic3RhdHVzIl0gPT0gInN1Y2Nlc3MiOgogICAgICAgICAgICAgICAgbWVzc2FnZWJveC5z
aG93aW5mbygi0KPRgdC/0LXRhSIsIHJlc3VsdFsibWVzc2FnZSJdLCBwYXJlbnQ9c2VsZikKICAg
ICAgICAgICAgICAgIGlmIHNlbGYuY2FsbGJhY2s6IHNlbGYuY2FsbGJhY2soKQogICAgICAgICAg
ICAgICAgc2VsZi5kZXN0cm95KCkKICAgICAgICAgICAgZWxpZiByZXN1bHQgYW5kIHJlc3VsdFsi
c3RhdHVzIl0gPT0gImluZm8iOgogICAgICAgICAgICAgICAgbWVzc2FnZWJveC5zaG93aW5mbygi
0JjQvdGE0L7RgNC80LDRhtC40Y8iLCByZXN1bHRbIm1lc3NhZ2UiXSwgcGFyZW50PXNlbGYpCiAg
ICAgICAgICAgICAgICBzZWxmLmRlc3Ryb3koKSAjINCX0LDQutGA0YvQstCw0LXQvCDQvtC60L3Q
viwg0LTQsNC20LUg0LXRgdC70Lgg0L3QtSDQsdGL0LvQviDQuNC30LzQtdC90LXQvdC40LkKICAg
ICAgICAgICAgZWxpZiByZXN1bHQ6ICMg0J7RiNC40LHQutCwCiAgICAgICAgICAgICAgICBtZXNz
YWdlYm94LnNob3dlcnJvcigi0J7RiNC40LHQutCwIiwgcmVzdWx0WyJtZXNzYWdlIl0sIHBhcmVu
dD1zZWxmKQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgbWVzc2Fn
ZWJveC5zaG93ZXJyb3IoItCa0YDQuNGC0LjRh9C10YHQutCw0Y8g0L7RiNC40LHQutCwIiwgZiLQ
ntGI0LjQsdC60LAg0L/RgNC4INGB0L7RhdGA0LDQvdC10L3QuNC4INC/0L7Qu9GM0LfQvtCy0LDR
gtC10LvRjzoge2V9IiwgcGFyZW50PXNlbGYpCgoKY2xhc3MgQWRtaW5EYXNoYm9hcmQodGsuRnJh
bWUpOgogICAgZGVmIF9faW5pdF9fKHNlbGYsIG1hc3RlciwgYXBwX2NvbnRyb2xsZXIpOgogICAg
ICAgIHN1cGVyKCkuX19pbml0X18obWFzdGVyKQogICAgICAgIHNlbGYuYXBwX2NvbnRyb2xsZXIg
PSBhcHBfY29udHJvbGxlcgogICAgICAgIHVzZXIgPSBzZWxmLmFwcF9jb250cm9sbGVyLmN1cnJl
bnRfdXNlcgogICAgICAgIHNlbGYubWFzdGVyLnRpdGxlKGYi0JDQtNC80LjQvToge3VzZXIuZ2V0
KCdmdWxsX25hbWUnLCB1c2VyWydsb2dpbiddKX0iKQogICAgICAgIHNlbGYubWFzdGVyLmdlb21l
dHJ5KCI3MDB4NTUwIikgCiAgICAgICAgc2VsZi5wYWNrKHBhZHk9MTAsIHBhZHg9MTAsIGZpbGw9
ImJvdGgiLCBleHBhbmQ9VHJ1ZSkKCiAgICAgICAgdGsuTGFiZWwoc2VsZiwgdGV4dD0i0KDQsNCx
0L7Rh9C40Lkg0YHRgtC+0Lsg0JDQtNC80LjQvdC40YHRgtGA0LDRgtC+0YDQsCIsIGZvbnQ9KCJB
cmlhbCIsIDE4KSkucGFjayhwYWR5PTEwKQogICAgICAgIAogICAgICAgIHRvcF9idXR0b25zX2Zy
YW1lID0gdGsuRnJhbWUoc2VsZikgIyDQo9Cx0YDQsNC7IGZnX2NvbG9yCiAgICAgICAgdG9wX2J1
dHRvbnNfZnJhbWUucGFjayhwYWR5PTUsIHBhZHg9NSwgZmlsbD0ieCIpCgogICAgICAgIHRrLkJ1
dHRvbih0b3BfYnV0dG9uc19mcmFtZSwgdGV4dD0i0KPQv9GA0LDQstC70LXQvdC40LUg0L/QvtC7
0YzQt9C+0LLQsNGC0LXQu9GP0LzQuCIsIGNvbW1hbmQ9bGFtYmRhOiBVc2VyTWFuYWdlbWVudFdp
bmRvdyhzZWxmLm1hc3Rlciwgc2VsZi5hcHBfY29udHJvbGxlcikpLnBhY2soc2lkZT0ibGVmdCIs
IHBhZHg9NSwgcGFkeT01KQogICAgICAgIHRrLkJ1dHRvbih0b3BfYnV0dG9uc19mcmFtZSwgdGV4
dD0i0JjQvNC/0L7RgNGCINC90L7QvNC10YDQvtCyIChDU1YpIiwgY29tbWFuZD1zZWxmLl9pbXBv
cnRfcm9vbXMpLnBhY2soc2lkZT0ibGVmdCIsIHBhZHg9NSwgcGFkeT01KQogICAgICAgIHRrLkJ1
dHRvbih0b3BfYnV0dG9uc19mcmFtZSwgdGV4dD0iJSDQt9Cw0LPRgNGD0LfQutC4INC90L7QvNC1
0YDQvtCyIiwgY29tbWFuZD1zZWxmLl9zaG93X29jY3VwYW5jeSkucGFjayhzaWRlPSJsZWZ0Iiwg
cGFkeD01LCBwYWR5PTUpCiAgICAgICAgdGsuQnV0dG9uKHRvcF9idXR0b25zX2ZyYW1lLCB0ZXh0
PSLQktCw0LvQuNC00LDRhtC40Y8g0KTQmNCeICjQnDQpIiwgY29tbWFuZD1zZWxmLl9vcGVuX3Zh
bGlkYXRpb25fbW9kdWxlKS5wYWNrKHNpZGU9ImxlZnQiLCBwYWR4PTUsIHBhZHk9NSkKICAgICAg
ICAKICAgICAgICB0ay5MYWJlbChzZWxmLCB0ZXh0PSLQodC+0YHRgtC+0Y/QvdC40LUg0L3QvtC8
0LXRgNC90L7Qs9C+INGE0L7QvdC00LA6IiwgZm9udD0oIkFyaWFsIiwgMTQpKS5wYWNrKHBhZHk9
KDEwLDApLCBhbmNob3I9InciLCBwYWR4PTUpCiAgICAgICAgCiAgICAgICAgc3R5bGUgPSB0dGsu
U3R5bGUoc2VsZikKICAgICAgICBzdHlsZS50aGVtZV91c2UoImRlZmF1bHQiKQogICAgICAgIHN0
eWxlLmNvbmZpZ3VyZSgiVHJlZXZpZXcuSGVhZGluZyIsIGZvbnQ9KCdBcmlhbCcsIDEwLCAnYm9s
ZCcpKQogICAgICAgIHNlbGYucm9vbXNfdHJlZSA9IHR0ay5UcmVldmlldyhzZWxmLCBjb2x1bW5z
PSgibnVtYmVyIiwgImZsb29yIiwgImNhdGVnb3J5IiwgInN0YXR1cyIpLCBzaG93PSJoZWFkaW5n
cyIpCiAgICAgICAgc2VsZi5yb29tc190cmVlLmhlYWRpbmcoIm51bWJlciIsIHRleHQ9ItCd0L7Q
vNC10YAiKQogICAgICAgIHNlbGYucm9vbXNfdHJlZS5jb2x1bW4oIm51bWJlciIsIHdpZHRoPTgw
LCBhbmNob3I9InciLCBzdHJldGNoPUZhbHNlKQogICAgICAgIHNlbGYucm9vbXNfdHJlZS5oZWFk
aW5nKCJmbG9vciIsIHRleHQ9ItCt0YLQsNC2IikKICAgICAgICBzZWxmLnJvb21zX3RyZWUuY29s
dW1uKCJmbG9vciIsIHdpZHRoPTE1MCwgYW5jaG9yPSJ3IikKICAgICAgICBzZWxmLnJvb21zX3Ry
ZWUuaGVhZGluZygiY2F0ZWdvcnkiLCB0ZXh0PSLQmtCw0YLQtdCz0L7RgNC40Y8iKQogICAgICAg
IHNlbGYucm9vbXNfdHJlZS5jb2x1bW4oImNhdGVnb3J5Iiwgd2lkdGg9MjAwLCBhbmNob3I9Inci
KQogICAgICAgIHNlbGYucm9vbXNfdHJlZS5oZWFkaW5nKCJzdGF0dXMiLCB0ZXh0PSLQodGC0LDR
gtGD0YEiKQogICAgICAgIHNlbGYucm9vbXNfdHJlZS5jb2x1bW4oInN0YXR1cyIsIHdpZHRoPTEy
MCwgYW5jaG9yPSJ3IikKICAgICAgICBzZWxmLnJvb21zX3RyZWUucGFjayhwYWR5PTUsIHBhZHg9
NSwgZmlsbD0iYm90aCIsIGV4cGFuZD1UcnVlKQogICAgICAgIHNlbGYuX2xvYWRfcm9vbV9kZXRh
aWxzKCkKCiAgICAgICAgdGsuQnV0dG9uKHNlbGYsIHRleHQ9ItCS0YvRhdC+0LQiLCBjb21tYW5k
PXNlbGYuYXBwX2NvbnRyb2xsZXIubG9nb3V0KS5wYWNrKHBhZHk9MTAsIHNpZGU9ImJvdHRvbSIp
CgogICAgZGVmIF9pbXBvcnRfcm9vbXMoc2VsZik6CiAgICAgICAgaWYgbWVzc2FnZWJveC5hc2t5
ZXNubygi0JjQvNC/0L7RgNGCIiwgZiLQmNC80L/QvtGA0YLQuNGA0L7QstCw0YLRjCDQtNCw0L3Q
vdGL0LUg0LjQtyAne0NTVl9GSUxFX1BBVEh9Jz9cbtCh0YPRidC10YHRgtCy0YPRjtGJ0LjQtSDQ
vdC+0LzQtdGA0LAg0L3QtSDQsdGD0LTRg9GCINC/0LXRgNC10LfQsNC/0LjRgdCw0L3Riy4iLCBw
YXJlbnQ9c2VsZi5tYXN0ZXIpOgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBpbXBv
cnRfcm9vbV9kYXRhX2Zyb21fY3N2KCkKICAgICAgICAgICAgICAgIHNlbGYuX2xvYWRfcm9vbV9k
ZXRhaWxzKCkKICAgICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAg
ICAgbWVzc2FnZWJveC5zaG93ZXJyb3IoItCe0YjQuNCx0LrQsCDQuNC80L/QvtGA0YLQsCIsIGYi
0J/RgNC+0LjQt9C+0YjQu9CwINC+0YjQuNCx0LrQsCDQstC+INCy0YDQtdC80Y8g0LjQvNC/0L7R
gNGC0LA6IHtlfSIsIHBhcmVudD1zZWxmLm1hc3RlcikKCgogICAgZGVmIF9zaG93X29jY3VwYW5j
eShzZWxmKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIHBlcmNlbnRhZ2UgPSBnZXRfcm9vbV9v
Y2N1cGFuY3lfcGVyY2VudGFnZV9zZXJ2aWNlKCkKICAgICAgICAgICAgbWVzc2FnZWJveC5zaG93
aW5mbygi0JfQsNCz0YDRg9C30LrQsCDQvdC+0LzQtdGA0L7QsiIsIGYi0KLQtdC60YPRidCw0Y8g
0LfQsNCz0YDRg9C30LrQsDoge3BlcmNlbnRhZ2U6LjJmfSUiLCBwYXJlbnQ9c2VsZi5tYXN0ZXIp
CiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgbWVzc2FnZWJveC5z
aG93ZXJyb3IoItCe0YjQuNCx0LrQsCIsIGYi0J3QtSDRg9C00LDQu9C+0YHRjCDRgNCw0YHRgdGH
0LjRgtCw0YLRjCDQt9Cw0LPRgNGD0LfQutGDOiB7ZX0iLCBwYXJlbnQ9c2VsZi5tYXN0ZXIpCiAg
ICAKICAgIGRlZiBfbG9hZF9yb29tX2RldGFpbHMoc2VsZik6CiAgICAgICAgZm9yIGkgaW4gc2Vs
Zi5yb29tc190cmVlLmdldF9jaGlsZHJlbigpOgogICAgICAgICAgICBzZWxmLnJvb21zX3RyZWUu
ZGVsZXRlKGkpCiAgICAgICAgdHJ5OgogICAgICAgICAgICByb29tcyA9IGdldF9hbGxfcm9vbXNf
d2l0aF9kZXRhaWxzX3NlcnZpY2UoKQogICAgICAgICAgICBpZiByb29tczoKICAgICAgICAgICAg
ICAgIGZvciByb29tIGluIHJvb21zOgogICAgICAgICAgICAgICAgICAgIHNlbGYucm9vbXNfdHJl
ZS5pbnNlcnQoIiIsICJlbmQiLCB2YWx1ZXM9KAogICAgICAgICAgICAgICAgICAgICAgICByb29t
LmdldCgncm9vbV9udW1iZXInLCcnKSwgCiAgICAgICAgICAgICAgICAgICAgICAgIHJvb20uZ2V0
KCdmbG9vcl9uYW1lJywnJyksIAogICAgICAgICAgICAgICAgICAgICAgICByb29tLmdldCgnY2F0
ZWdvcnlfbmFtZScsJycpLCAKICAgICAgICAgICAgICAgICAgICAgICAgcm9vbS5nZXQoJ3N0YXR1
c19uYW1lJywnJykKICAgICAgICAgICAgICAgICAgICApKQogICAgICAgICAgICBlbHNlOiAjINCV
0YHQu9C4INGB0LXRgNCy0LjRgSDQstC10YDQvdGD0LsgTm9uZSDQuNC70Lgg0L/Rg9GB0YLQvtC5
INGB0L/QuNGB0L7QugogICAgICAgICAgICAgICAgc2VsZi5yb29tc190cmVlLmluc2VydCgiIiwg
ImVuZCIsIHZhbHVlcz0oItCd0LXRgiDQtNCw0L3QvdGL0YUiLCAiIiwgIiIsICIiKSkKICAgICAg
ICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgIG1lc3NhZ2Vib3guc2hvd2Vycm9y
KCLQntGI0LjQsdC60LAg0LfQsNCz0YDRg9C30LrQuCIsIGYi0J3QtSDRg9C00LDQu9C+0YHRjCDQ
t9Cw0LPRgNGD0LfQuNGC0Ywg0L3QvtC80LXRgNCwOiB7ZX0iLCBwYXJlbnQ9c2VsZikKICAgICAg
ICAgICAgc2VsZi5yb29tc190cmVlLmluc2VydCgiIiwgImVuZCIsIHZhbHVlcz0oItCe0YjQuNCx
0LrQsCDQt9Cw0LPRgNGD0LfQutC4IiwgIiIsICIiLCAiIikpCgoKICAgIGRlZiBfb3Blbl92YWxp
ZGF0aW9uX21vZHVsZShzZWxmKToKICAgICAgICBWYWxpZGF0aW9uV2luZG93KHNlbGYubWFzdGVy
LCBzZWxmLmFwcF9jb250cm9sbGVyKQoKCmNsYXNzIFVzZXJEYXNoYm9hcmQodGsuRnJhbWUpOgog
ICAgZGVmIF9faW5pdF9fKHNlbGYsIG1hc3RlciwgYXBwX2NvbnRyb2xsZXIpOgogICAgICAgIHN1
cGVyKCkuX19pbml0X18obWFzdGVyKQogICAgICAgIHNlbGYuYXBwX2NvbnRyb2xsZXIgPSBhcHBf
Y29udHJvbGxlcgogICAgICAgIHVzZXIgPSBzZWxmLmFwcF9jb250cm9sbGVyLmN1cnJlbnRfdXNl
cgogICAgICAgIHNlbGYubWFzdGVyLnRpdGxlKGYi0J/QvtC70YzQt9C+0LLQsNGC0LXQu9GMOiB7
dXNlci5nZXQoJ2Z1bGxfbmFtZScsIHVzZXJbJ2xvZ2luJ10pfSIpCiAgICAgICAgc2VsZi5tYXN0
ZXIuZ2VvbWV0cnkoIjY1MHg0NTAiKSAKICAgICAgICBzZWxmLnBhY2socGFkeT0xMCwgcGFkeD0x
MCwgZmlsbD0iYm90aCIsIGV4cGFuZD1UcnVlKQoKICAgICAgICB0ay5MYWJlbChzZWxmLCB0ZXh0
PSLQoNCw0LHQvtGH0LjQuSDRgdGC0L7QuyDQodC+0YLRgNGD0LTQvdC40LrQsCIsIGZvbnQ9KCJB
cmlhbCIsIDE4KSkucGFjayhwYWR5PTEwKQogICAgICAgIHRrLkJ1dHRvbihzZWxmLCB0ZXh0PSLQ
odC80LXQvdC40YLRjCDRgdCy0L7QuSDQv9Cw0YDQvtC70YwiLCBjb21tYW5kPWxhbWJkYTogc2Vs
Zi5hcHBfY29udHJvbGxlci5zaG93X2NoYW5nZV9wYXNzd29yZF93aW5kb3coaW5pdGlhbF9jaGFu
Z2U9RmFsc2UpKS5wYWNrKHBhZHk9MTApCiAgICAgICAgCiAgICAgICAgdGsuTGFiZWwoc2VsZiwg
dGV4dD0i0JTQvtGB0YLRg9C/0L3Ri9C1INC90L7QvNC10YDQsDoiLCBmb250PSgiQXJpYWwiLCAx
NCkpLnBhY2socGFkeT0oMTAsMCksIGFuY2hvcj0idyIsIHBhZHg9NSkKICAgICAgICAKICAgICAg
ICBzdHlsZSA9IHR0ay5TdHlsZShzZWxmKQogICAgICAgIHN0eWxlLnRoZW1lX3VzZSgiZGVmYXVs
dCIpCiAgICAgICAgc3R5bGUuY29uZmlndXJlKCJUcmVldmlldy5IZWFkaW5nIiwgZm9udD0oJ0Fy
aWFsJywgMTAsICdib2xkJykpCiAgICAgICAgc2VsZi5yb29tc190cmVlID0gdHRrLlRyZWV2aWV3
KHNlbGYsIGNvbHVtbnM9KCJudW1iZXIiLCAiZmxvb3IiLCAiY2F0ZWdvcnkiLCAic3RhdHVzIiks
IHNob3c9ImhlYWRpbmdzIikKICAgICAgICBzZWxmLnJvb21zX3RyZWUuaGVhZGluZygibnVtYmVy
IiwgdGV4dD0i0J3QvtC80LXRgCIpCiAgICAgICAgc2VsZi5yb29tc190cmVlLmNvbHVtbigibnVt
YmVyIiwgd2lkdGg9ODAsIGFuY2hvcj0idyIsIHN0cmV0Y2g9RmFsc2UpCiAgICAgICAgc2VsZi5y
b29tc190cmVlLmhlYWRpbmcoImZsb29yIiwgdGV4dD0i0K3RgtCw0LYiKQogICAgICAgIHNlbGYu
cm9vbXNfdHJlZS5jb2x1bW4oImZsb29yIiwgd2lkdGg9MTUwLCBhbmNob3I9InciKQogICAgICAg
IHNlbGYucm9vbXNfdHJlZS5oZWFkaW5nKCJjYXRlZ29yeSIsIHRleHQ9ItCa0LDRgtC10LPQvtGA
0LjRjyIpCiAgICAgICAgc2VsZi5yb29tc190cmVlLmNvbHVtbigiY2F0ZWdvcnkiLCB3aWR0aD0y
MDAsIGFuY2hvcj0idyIpCiAgICAgICAgc2VsZi5yb29tc190cmVlLmhlYWRpbmcoInN0YXR1cyIs
IHRleHQ9ItCh0YLQsNGC0YPRgSIpCiAgICAgICAgc2VsZi5yb29tc190cmVlLmNvbHVtbigic3Rh
dHVzIiwgd2lkdGg9MTIwLCBhbmNob3I9InciKQogICAgICAgIHNlbGYucm9vbXNfdHJlZS5wYWNr
KHBhZHk9NSwgcGFkeD01LCBmaWxsPSJib3RoIiwgZXhwYW5kPVRydWUpCiAgICAgICAgc2VsZi5f
bG9hZF9yb29tX2RldGFpbHMoKQoKICAgICAgICB0ay5CdXR0b24oc2VsZiwgdGV4dD0i0JLRi9GF
0L7QtCIsIGNvbW1hbmQ9c2VsZi5hcHBfY29udHJvbGxlci5sb2dvdXQpLnBhY2socGFkeT0xMCwg
c2lkZT0iYm90dG9tIikKCiAgICBkZWYgX2xvYWRfcm9vbV9kZXRhaWxzKHNlbGYpOgogICAgICAg
IGZvciBpIGluIHNlbGYucm9vbXNfdHJlZS5nZXRfY2hpbGRyZW4oKToKICAgICAgICAgICAgc2Vs
Zi5yb29tc190cmVlLmRlbGV0ZShpKQogICAgICAgIHRyeToKICAgICAgICAgICAgcm9vbXMgPSBn
ZXRfYWxsX3Jvb21zX3dpdGhfZGV0YWlsc19zZXJ2aWNlKCkKICAgICAgICAgICAgaWYgcm9vbXM6
CiAgICAgICAgICAgICAgICBmb3Igcm9vbSBpbiByb29tczoKICAgICAgICAgICAgICAgICAgICBz
ZWxmLnJvb21zX3RyZWUuaW5zZXJ0KCIiLCAiZW5kIiwgdmFsdWVzPSgKICAgICAgICAgICAgICAg
ICAgICAgICAgcm9vbS5nZXQoJ3Jvb21fbnVtYmVyJywnJyksIAogICAgICAgICAgICAgICAgICAg
ICAgICByb29tLmdldCgnZmxvb3JfbmFtZScsJycpLCAKICAgICAgICAgICAgICAgICAgICAgICAg
cm9vbS5nZXQoJ2NhdGVnb3J5X25hbWUnLCcnKSwgCiAgICAgICAgICAgICAgICAgICAgICAgIHJv
b20uZ2V0KCdzdGF0dXNfbmFtZScsJycpCiAgICAgICAgICAgICAgICAgICAgKSkKICAgICAgICAg
ICAgZWxzZToKICAgICAgICAgICAgICAgIHNlbGYucm9vbXNfdHJlZS5pbnNlcnQoIiIsICJlbmQi
LCB2YWx1ZXM9KCLQndC10YIg0LTQsNC90L3Ri9GFIiwgIiIsICIiLCAiIikpCiAgICAgICAgZXhj
ZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICBtZXNzYWdlYm94LnNob3dlcnJvcigi0J7R
iNC40LHQutCwINC30LDQs9GA0YPQt9C60LgiLCBmItCd0LUg0YPQtNCw0LvQvtGB0Ywg0LfQsNCz
0YDRg9C30LjRgtGMINC90L7QvNC10YDQsDoge2V9IiwgcGFyZW50PXNlbGYpCiAgICAgICAgICAg
IHNlbGYucm9vbXNfdHJlZS5pbnNlcnQoIiIsICJlbmQiLCB2YWx1ZXM9KCLQntGI0LjQsdC60LAg
0LfQsNCz0YDRg9C30LrQuCIsICIiLCAiIiwgIiIpKQoKCmNsYXNzIFZhbGlkYXRpb25XaW5kb3co
dGsuVG9wbGV2ZWwpOiAKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBtYXN0ZXIsIGFwcF9jb250cm9s
bGVyKToKICAgICAgICBzdXBlcigpLl9faW5pdF9fKG1hc3RlcikKICAgICAgICBzZWxmLmFwcF9j
b250cm9sbGVyID0gYXBwX2NvbnRyb2xsZXIgCiAgICAgICAgc2VsZi50aXRsZSgi0JLQsNC70LjQ
tNCw0YbQuNGPINC00LDQvdC90YvRhSIpCiAgICAgICAgc2VsZi5nZW9tZXRyeSgiNTUweDIwMCIp
IAogICAgICAgIAogICAgICAgIHNlbGYudHJhbnNpZW50KG1hc3RlcikKICAgICAgICBzZWxmLnJl
c2l6YWJsZShGYWxzZSwgRmFsc2UpCgogICAgICAgIG1haW5fZnJhbWUgPSB0ay5GcmFtZShzZWxm
KSAjINCj0LHRgNCw0L0gZmdfY29sb3IKICAgICAgICBtYWluX2ZyYW1lLnBhY2socGFkeT0yMCwg
cGFkeD0yMCwgZmlsbD0iYm90aCIsIGV4cGFuZD1UcnVlKQoKICAgICAgICAjINCf0LXRgNCy0LDR
jyDRgdGC0YDQvtC60LA6INCa0L3QvtC/0LrQsCAi0J/QvtC70YPRh9C40YLRjCDQtNCw0L3QvdGL
0LUiINC4INGC0LXQutGB0YLQvtCy0L7QtSDQv9C+0LvQtSDQtNC70Y8g0KTQmNCeCiAgICAgICAg
ZnJhbWVfZ2V0X2RhdGEgPSB0ay5GcmFtZShtYWluX2ZyYW1lKSAjINCj0LHRgNCw0L0gZmdfY29s
b3IKICAgICAgICBmcmFtZV9nZXRfZGF0YS5wYWNrKGZpbGw9IngiLCBwYWR5PTUpCgogICAgICAg
IHNlbGYuZ2V0X2RhdGFfYnV0dG9uID0gdGsuQnV0dG9uKGZyYW1lX2dldF9kYXRhLCB0ZXh0PSLQ
n9C+0LvRg9GH0LjRgtGMINC00LDQvdC90YvQtSIsIGNvbW1hbmQ9c2VsZi5fZ2V0X2RhdGFfZnJv
bV9hcGksIHdpZHRoPTIwKSAjIDE4MHB4IC0+IDIwLTIyIGNoYXJzCiAgICAgICAgc2VsZi5nZXRf
ZGF0YV9idXR0b24ucGFjayhzaWRlPSJsZWZ0IiwgcGFkeD0oMCwgMTApKQoKICAgICAgICBzZWxm
LmZpb19kaXNwbGF5X2VudHJ5ID0gdGsuRW50cnkoZnJhbWVfZ2V0X2RhdGEsIHdpZHRoPTQwKSAj
IDMwMHB4IC0+IDQwIGNoYXJzCiAgICAgICAgc2VsZi5maW9fZGlzcGxheV9lbnRyeS5wYWNrKHNp
ZGU9ImxlZnQiLCBmaWxsPSJ4IiwgZXhwYW5kPVRydWUpCiAgICAgICAgc2VsZi5maW9fZGlzcGxh
eV9lbnRyeS5jb25maWcoc3RhdGU9InJlYWRvbmx5IikgIyDQmNGB0L/QvtC70YzQt9GD0LXQvCBj
b25maWcKCiAgICAgICAgIyDQktGC0L7RgNCw0Y8g0YHRgtGA0L7QutCwOiDQmtC90L7Qv9C60LAg
ItCe0YLQv9GA0LDQstC40YLRjCDRgNC10LfRg9C70YzRgtCw0YIg0YLQtdGB0YLQsCIg0Lgg0YLQ
tdC60YHRgtC+0LLQvtC1INC/0L7Qu9C1INC00LvRjyDRgNC10LfRg9C70YzRgtCw0YLQsAogICAg
ICAgIGZyYW1lX3NlbmRfcmVzdWx0ID0gdGsuRnJhbWUobWFpbl9mcmFtZSkgIyDQo9Cx0YDQsNC9
IGZnX2NvbG9yCiAgICAgICAgZnJhbWVfc2VuZF9yZXN1bHQucGFjayhmaWxsPSJ4IiwgcGFkeT0x
NSkKCiAgICAgICAgc2VsZi5zZW5kX3Jlc3VsdF9idXR0b24gPSB0ay5CdXR0b24oZnJhbWVfc2Vu
ZF9yZXN1bHQsIHRleHQ9ItCe0YLQv9GA0LDQstC40YLRjCDRgNC10LfRg9C70YzRgtCw0YIg0YLQ
tdGB0YLQsCIsIGNvbW1hbmQ9c2VsZi5fc2VuZF90ZXN0X3Jlc3VsdCwgd2lkdGg9MjUpICMgMTgw
cHggKNC00LvQuNC90L3Ri9C5INGC0LXQutGB0YIpIC0+IH4yNQogICAgICAgIHNlbGYuc2VuZF9y
ZXN1bHRfYnV0dG9uLnBhY2soc2lkZT0ibGVmdCIsIHBhZHg9KDAsIDEwKSkKCiAgICAgICAgc2Vs
Zi52YWxpZGF0aW9uX3N0YXR1c19lbnRyeSA9IHRrLkVudHJ5KGZyYW1lX3NlbmRfcmVzdWx0LCB3
aWR0aD00MCkgIyAzMDBweCAtPiA0MCBjaGFycwogICAgICAgIHNlbGYudmFsaWRhdGlvbl9zdGF0
dXNfZW50cnkucGFjayhzaWRlPSJsZWZ0IiwgZmlsbD0ieCIsIGV4cGFuZD1UcnVlKQogICAgICAg
IHNlbGYudmFsaWRhdGlvbl9zdGF0dXNfZW50cnkuY29uZmlnKHN0YXRlPSJyZWFkb25seSIpICMg
0JjRgdC/0L7Qu9GM0LfRg9C10LwgY29uZmlnCgoKICAgIGRlZiBfZ2V0X2RhdGFfZnJvbV9hcGko
c2VsZik6CiAgICAgICAgZmlvID0gZ2V0X2Z1bGxuYW1lX2Zyb21fYXBpKCkKICAgICAgICBzZWxm
LmZpb19kaXNwbGF5X2VudHJ5LmNvbmZpZyhzdGF0ZT0ibm9ybWFsIikgIyDQmNGB0L/QvtC70YzQ
t9GD0LXQvCBjb25maWcKICAgICAgICBzZWxmLmZpb19kaXNwbGF5X2VudHJ5LmRlbGV0ZSgwLCAi
ZW5kIikKICAgICAgICBpZiBmaW86CiAgICAgICAgICAgIHNlbGYuZmlvX2Rpc3BsYXlfZW50cnku
aW5zZXJ0KDAsIGZpbykKICAgICAgICBlbHNlOgogICAgICAgICAgICBzZWxmLmZpb19kaXNwbGF5
X2VudHJ5Lmluc2VydCgwLCAi0J7RiNC40LHQutCwINC/0L7Qu9GD0YfQtdC90LjRjyDQpNCY0J4g
0YEgQVBJIikKICAgICAgICBzZWxmLmZpb19kaXNwbGF5X2VudHJ5LmNvbmZpZyhzdGF0ZT0icmVh
ZG9ubHkiKSAjINCY0YHQv9C+0LvRjNC30YPQtdC8IGNvbmZpZwogICAgICAgIAogICAgICAgIHNl
bGYudmFsaWRhdGlvbl9zdGF0dXNfZW50cnkuY29uZmlnKHN0YXRlPSJub3JtYWwiKSAjINCY0YHQ
v9C+0LvRjNC30YPQtdC8IGNvbmZpZwogICAgICAgIHNlbGYudmFsaWRhdGlvbl9zdGF0dXNfZW50
cnkuZGVsZXRlKDAsICJlbmQiKQogICAgICAgIHNlbGYudmFsaWRhdGlvbl9zdGF0dXNfZW50cnku
Y29uZmlnKHN0YXRlPSJyZWFkb25seSIpICMg0JjRgdC/0L7Qu9GM0LfRg9C10LwgY29uZmlnCgoK
ICAgIGRlZiBfc2VuZF90ZXN0X3Jlc3VsdChzZWxmKToKICAgICAgICBmaW9fdG9fdmFsaWRhdGUg
PSBzZWxmLmZpb19kaXNwbGF5X2VudHJ5LmdldCgpCiAgICAgICAgc2VsZi52YWxpZGF0aW9uX3N0
YXR1c19lbnRyeS5jb25maWcoc3RhdGU9Im5vcm1hbCIpICMg0JjRgdC/0L7Qu9GM0LfRg9C10Lwg
Y29uZmlnCiAgICAgICAgc2VsZi52YWxpZGF0aW9uX3N0YXR1c19lbnRyeS5kZWxldGUoMCwgImVu
ZCIpCgogICAgICAgIGlmIG5vdCBmaW9fdG9fdmFsaWRhdGUgb3IgItCe0YjQuNCx0LrQsCDQv9C+
0LvRg9GH0LXQvdC40Y8iIGluIGZpb190b192YWxpZGF0ZToKICAgICAgICAgICAgc2VsZi52YWxp
ZGF0aW9uX3N0YXR1c19lbnRyeS5pbnNlcnQoMCwgItCd0LXRgiDQpNCY0J4g0LTQu9GPINC/0YDQ
vtCy0LXRgNC60LgiKQogICAgICAgICAgICBtZXNzYWdlYm94LnNob3d3YXJuaW5nKCLQktC90LjQ
vNCw0L3QuNC1IiwgItCh0L3QsNGH0LDQu9CwINC/0L7Qu9GD0YfQuNGC0LUg0KTQmNCeINGBIEFQ
SS4iLCBwYXJlbnQ9c2VsZikKICAgICAgICBlbHNlOgogICAgICAgICAgICBpc192YWxpZCA9IHZh
bGlkYXRlX2Zpb19zZXJ2aWNlKGZpb190b192YWxpZGF0ZSkgCiAgICAgICAgICAgIGlmIGlzX3Zh
bGlkOgogICAgICAgICAgICAgICAgc2VsZi52YWxpZGF0aW9uX3N0YXR1c19lbnRyeS5pbnNlcnQo
MCwgItCk0JjQniDQutC+0YDRgNC10LrRgtC90L4iKQogICAgICAgICAgICBlbHNlOgogICAgICAg
ICAgICAgICAgc2VsZi52YWxpZGF0aW9uX3N0YXR1c19lbnRyeS5pbnNlcnQoMCwgItCk0JjQniDR
gdC+0LTQtdGA0LbQuNGCINC30LDQv9GA0LXRidC10L3QvdGL0LUg0YHQuNC80LLQvtC70YsiKQog
ICAgICAgIAogICAgICAgIHNlbGYudmFsaWRhdGlvbl9zdGF0dXNfZW50cnkuY29uZmlnKHN0YXRl
PSJyZWFkb25seSIpICMg0JjRgdC/0L7Qu9GM0LfRg9C10LwgY29uZmlnCiAgICAgICAgcHJpbnQo
ZiLQnNC+0LTRg9C70YwgNDog0J/RgNC+0LLQtdGA0LXQvdC+INCk0JjQniAne2Zpb190b192YWxp
ZGF0ZX0nLCDRgNC10LfRg9C70YzRgtCw0YI6ICd7c2VsZi52YWxpZGF0aW9uX3N0YXR1c19lbnRy
eS5nZXQoKX0nIikKCgpjbGFzcyBBcHBDb250cm9sbGVyKHRrLlRrKTogIyDQl9Cw0LzQtdC90LAg
Y3RrLkNUayDQvdCwIHRrLlRrCiAgICBkZWYgX19pbml0X18oc2VsZik6CiAgICAgICAgc3VwZXIo
KS5fX2luaXRfXygpCiAgICAgICAgc2VsZi5jdXJyZW50X3VzZXIgPSBOb25lCiAgICAgICAgc2Vs
Zi5fY3VycmVudF9mcmFtZSA9IE5vbmUKICAgICAgICAKICAgICAgICBzZWxmLnNob3dfbG9naW5f
d2luZG93KCkKCiAgICBkZWYgY2xlYXJfZnJhbWUoc2VsZik6CiAgICAgICAgaWYgc2VsZi5fY3Vy
cmVudF9mcmFtZToKICAgICAgICAgICAgc2VsZi5fY3VycmVudF9mcmFtZS5kZXN0cm95KCkKICAg
ICAgICAgICAgc2VsZi5fY3VycmVudF9mcmFtZSA9IE5vbmUKCiAgICBkZWYgc2hvd19sb2dpbl93
aW5kb3coc2VsZik6CiAgICAgICAgc2VsZi5jbGVhcl9mcmFtZSgpCiAgICAgICAgc2VsZi5jdXJy
ZW50X3VzZXIgPSBOb25lCiAgICAgICAgc2VsZi5fY3VycmVudF9mcmFtZSA9IExvZ2luV2luZG93
KHNlbGYsIHNlbGYpCiAgICAgICAgc2VsZi50aXRsZSgi0JDQstGC0L7RgNC40LfQsNGG0LjRjyIp
ICMg0K3RgtC+INGD0YHRgtCw0L3QvtCy0LjRgiDQt9Cw0LPQvtC70L7QstC+0Log0LTQu9GPINC+
0YHQvdC+0LLQvdC+0LPQviDQvtC60L3QsCBUawoKICAgIGRlZiBzaG93X2NoYW5nZV9wYXNzd29y
ZF93aW5kb3coc2VsZiwgaW5pdGlhbF9jaGFuZ2U9RmFsc2UpOgogICAgICAgIGlmIHNlbGYuY3Vy
cmVudF91c2VyOgogICAgICAgICAgICAjINCc0LDRgdGC0LXRgNC+0Lwg0LTQu9GPIFRvcGxldmVs
INCx0YPQtNC10YIg0YLQtdC60YPRidC10LUg0L7RgdC90L7QstC90L7QtSDQvtC60L3QviAoc2Vs
ZikKICAgICAgICAgICAgQ2hhbmdlUGFzc3dvcmRXaW5kb3coc2VsZiwgc2VsZiwgaW5pdGlhbF9j
aGFuZ2U9aW5pdGlhbF9jaGFuZ2UpCiAgICAgICAgZWxzZToKICAgICAgICAgICAgc2VsZi5zaG93
X2xvZ2luX3dpbmRvdygpIAoKICAgIGRlZiBzaG93X2Rhc2hib2FyZF9mb3Jfcm9sZShzZWxmLCBy
b2xlKToKICAgICAgICBzZWxmLmNsZWFyX2ZyYW1lKCkKICAgICAgICBpZiByb2xlID09ICfQkNC0
0LzQuNC90LjRgdGC0YDQsNGC0L7RgCc6CiAgICAgICAgICAgIHNlbGYuX2N1cnJlbnRfZnJhbWUg
PSBBZG1pbkRhc2hib2FyZChzZWxmLCBzZWxmKQogICAgICAgIGVsc2U6ICMg0J/QvtC70YzQt9C+
0LLQsNGC0LXQu9GMCiAgICAgICAgICAgIHNlbGYuX2N1cnJlbnRfZnJhbWUgPSBVc2VyRGFzaGJv
YXJkKHNlbGYsIHNlbGYpCiAgICAKICAgIGRlZiBsb2dvdXQoc2VsZik6CiAgICAgICAgc2VsZi5j
dXJyZW50X3VzZXIgPSBOb25lCiAgICAgICAgZm9yIHdpZGdldCBpbiBzZWxmLndpbmZvX2NoaWxk
cmVuKCk6CiAgICAgICAgICAgIGlmIGlzaW5zdGFuY2Uod2lkZ2V0LCB0ay5Ub3BsZXZlbCk6ICMg
0JfQsNC80LXQvdCwIGN0ay5DVGtUb3BsZXZlbCDQvdCwIHRrLlRvcGxldmVsCiAgICAgICAgICAg
ICAgICB3aWRnZXQuZGVzdHJveSgpCiAgICAgICAgc2VsZi5zaG93X2xvZ2luX3dpbmRvdygpCgoj
IDYuIE1BSU4gRVhFQ1VUSU9OIEJMT0NLCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICAj
INCj0LHRgNCw0L3RiyBjdGsuc2V0X2FwcGVhcmFuY2VfbW9kZSDQuCBjdGsuc2V0X2RlZmF1bHRf
Y29sb3JfdGhlbWUKICAgIAogICAgYXBwID0gQXBwQ29udHJvbGxlcigpCiAgICBhcHAubWFpbmxv
b3AoKQoKCiMgU0VMRUNUCiAgICAjIChTRUxFQ1QgQ09VTlQoKikgRlJPTSByb29tcyBXSEVSRSBj
dXJyZW50X3N0YXR1c19pZCA9IChTRUxFQ1QgaWQgRlJPTSByb29tX3N0YXR1c2VzIFdIRVJFIG5h
bWUgPSAn0JfQsNC90Y/RgicpKSAqIDEwMC4wIC8KICAgICMgKFNFTEVDVCBDT1VOVCgqKSBGUk9N
IHJvb21zKSBBUyBwZXJjZW50YWdlX29jY3VwYW5jeTs=
"""