# Copyright (c) 2013, 2025, Oracle and/or its affiliates.
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

"""Implementing pooling of connections to MySQL servers."""
from __future__ import annotations

import queue
import random
import re
import threading

from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, NoReturn, Optional, Tuple, Type, Union
from uuid import uuid4

try:
    import dns.exception
    import dns.resolver
except ImportError:
    HAVE_DNSPYTHON = False
else:
    HAVE_DNSPYTHON = True

try:
    from .connection_cext import CMySQLConnection
except ImportError:
    CMySQLConnection = None  # type: ignore[misc]

from .connection import MySQLConnection
from .constants import CNX_POOL_ARGS, DEFAULT_CONFIGURATION
from .errors import (
    Error,
    InterfaceError,
    NotSupportedError,
    PoolError,
    ProgrammingError,
)
from .optionfiles import read_option_files

if TYPE_CHECKING:
    from .abstracts import MySQLConnectionAbstract

CONNECTION_POOL_LOCK = threading.RLock()
CNX_POOL_MAXSIZE = 32
CNX_POOL_MAXNAMESIZE = 64
CNX_POOL_NAMEREGEX = re.compile(r"[^a-zA-Z0-9._:\-*$#]")
ERROR_NO_CEXT = "MySQL Connector/Python C Extension not available"
MYSQL_CNX_CLASS: Union[type, Tuple[type, ...]] = (
    MySQLConnection if CMySQLConnection is None else (MySQLConnection, CMySQLConnection)
)

_CONNECTION_POOLS: Dict[str, MySQLConnectionPool] = {}


def _get_pooled_connection(**kwargs: Any) -> PooledMySQLConnection:
    """Return a pooled MySQL connection."""
    # If no pool name specified, generate one
    pool_name = (
        kwargs["pool_name"] if "pool_name" in kwargs else generate_pool_name(**kwargs)
    )

    if kwargs.get("use_pure") is False and CMySQLConnection is None:
        raise ImportError(ERROR_NO_CEXT)

    # Setup the pool, ensuring only 1 thread can update at a time
    with CONNECTION_POOL_LOCK:
        if pool_name not in _CONNECTION_POOLS:
            _CONNECTION_POOLS[pool_name] = MySQLConnectionPool(**kwargs)
        elif isinstance(_CONNECTION_POOLS[pool_name], MySQLConnectionPool):
            # pool_size must be the same
            check_size = _CONNECTION_POOLS[pool_name].pool_size
            if "pool_size" in kwargs and kwargs["pool_size"] != check_size:
                raise PoolError("Size can not be changed for active pools.")

    # Return pooled connection
    try:
        return _CONNECTION_POOLS[pool_name].get_connection()
    except AttributeError:
        raise InterfaceError(
            f"Failed getting connection from pool '{pool_name}'"
        ) from None


def _get_failover_connection(
    **kwargs: Any,
) -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
    """Return a MySQL connection and try to failover if needed.

    An InterfaceError is raise when no MySQL is available. ValueError is
    raised when the failover server configuration contains an illegal
    connection argument. Supported arguments are user, password, host, port,
    unix_socket and database. ValueError is also raised when the failover
    argument was not provided.

    Returns MySQLConnection instance.
    """
    config = kwargs.copy()
    try:
        failover = config["failover"]
    except KeyError:
        raise ValueError("failover argument not provided") from None
    del config["failover"]

    support_cnx_args = set(
        [
            "user",
            "password",
            "host",
            "port",
            "unix_socket",
            "database",
            "pool_name",
            "pool_size",
            "priority",
        ]
    )

    # First check if we can add all use the configuration
    priority_count = 0
    for server in failover:
        diff = set(server.keys()) - support_cnx_args
        if diff:
            arg = "s" if len(diff) > 1 else ""
            lst = ", ".join(diff)
            raise ValueError(
                f"Unsupported connection argument {arg} in failover: {lst}"
            )
        if hasattr(server, "priority"):
            priority_count += 1

        server["priority"] = server.get("priority", 100)
        if server["priority"] < 0 or server["priority"] > 100:
            raise InterfaceError(
                "Priority value should be in the range of 0 to 100, "
                f"got : {server['priority']}"
            )
        if not isinstance(server["priority"], int):
            raise InterfaceError(
                "Priority value should be an integer in the range of 0 to "
                f"100, got : {server['priority']}"
            )

    if 0 < priority_count < len(failover):
        raise ProgrammingError(
            "You must either assign no priority to any "
            "of the routers or give a priority for "
            "every router"
        )

    server_directory = {}
    server_priority_list = []
    for server in sorted(failover, key=lambda x: x["priority"], reverse=True):
        if server["priority"] not in server_directory:
            server_directory[server["priority"]] = [server]
            server_priority_list.append(server["priority"])
        else:
            server_directory[server["priority"]].append(server)

    for priority in server_priority_list:
        failover_list = server_directory[priority]
        for _ in range(len(failover_list)):
            last = len(failover_list) - 1
            index = random.randint(0, last)
            server = failover_list.pop(index)
            new_config = config.copy()
            new_config.update(server)
            new_config.pop("priority", None)
            try:
                return connect(**new_config)
            except Error:
                # If we failed to connect, we try the next server
                pass

    raise InterfaceError("Unable to connect to any of the target hosts")


def connect(
    *args: Any, **kwargs: Any
) -> Union[PooledMySQLConnection, MySQLConnectionAbstract]:
    """Creates or gets a MySQL connection object.

    In its simpliest form, `connect()` will open a connection to a
    MySQL server and return a `MySQLConnectionAbstract` subclass
    object such as `MySQLConnection` or `CMySQLConnection`.

    When any connection pooling arguments are given, for example `pool_name`
    or `pool_size`, a pool is created or a previously one is used to return
    a `PooledMySQLConnection`.

    Args:
        *args: N/A.
        **kwargs: For a complete list of possible arguments, see [1]. If no arguments
                  are given, it uses the already configured or default values.

    Returns:
        A `MySQLConnectionAbstract` subclass instance (such as `MySQLConnection` or
        `CMySQLConnection`) or a `PooledMySQLConnection` instance.

    Examples:
        A connection with the MySQL server can be established using either the
        `mysql.connector.connect()` method or a `MySQLConnectionAbstract` subclass:
        ```
        >>> from mysql.connector import MySQLConnection, HAVE_CEXT
        >>>
        >>> cnx1 = mysql.connector.connect(user='joe', database='test')
        >>> cnx2 = MySQLConnection(user='joe', database='test')
        >>>
        >>> cnx3 = None
        >>> if HAVE_CEXT:
        >>>     from mysql.connector import CMySQLConnection
        >>>     cnx3 = CMySQLConnection(user='joe', database='test')
        ```

    References:
        [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    """
    # DNS SRV
    dns_srv = kwargs.pop("dns_srv") if "dns_srv" in kwargs else False

    if not isinstance(dns_srv, bool):
        raise InterfaceError("The value of 'dns-srv' must be a boolean")

    if dns_srv:
        if not HAVE_DNSPYTHON:
            raise InterfaceError(
                "MySQL host configuration requested DNS "
                "SRV. This requires the Python dnspython "
                "module. Please refer to documentation"
            )
        if "unix_socket" in kwargs:
            raise InterfaceError(
                "Using Unix domain sockets with DNS SRV lookup is not allowed"
            )
        if "port" in kwargs:
            raise InterfaceError(
                "Specifying a port number with DNS SRV lookup is not allowed"
            )
        if "failover" in kwargs:
            raise InterfaceError(
                "Specifying multiple hostnames with DNS SRV look up is not allowed"
            )
        if "host" not in kwargs:
            kwargs["host"] = DEFAULT_CONFIGURATION["host"]

        try:
            srv_records = dns.resolver.query(kwargs["host"], "SRV")
        except dns.exception.DNSException:
            raise InterfaceError(
                f"Unable to locate any hosts for '{kwargs['host']}'"
            ) from None

        failover = []
        for srv in srv_records:
            failover.append(
                {
                    "host": srv.target.to_text(omit_final_dot=True),
                    "port": srv.port,
                    "priority": srv.priority,
                    "weight": srv.weight,
                }
            )

        failover.sort(key=lambda x: (x["priority"], -x["weight"]))
        kwargs["failover"] = [
            {"host": srv["host"], "port": srv["port"]} for srv in failover
        ]

    # Option files
    if "read_default_file" in kwargs:
        kwargs["option_files"] = kwargs["read_default_file"]
        kwargs.pop("read_default_file")

    if "option_files" in kwargs:
        new_config = read_option_files(**kwargs)
        return connect(**new_config)

    # Failover
    if "failover" in kwargs:
        return _get_failover_connection(**kwargs)

    # Pooled connections
    try:
        if any(key in kwargs for key in CNX_POOL_ARGS):
            return _get_pooled_connection(**kwargs)
    except NameError:
        # No pooling
        pass

    # Use C Extension by default
    use_pure = kwargs.get("use_pure", False)
    if "use_pure" in kwargs:
        del kwargs["use_pure"]  # Remove 'use_pure' from kwargs
        if not use_pure and CMySQLConnection is None:
            raise ImportError(ERROR_NO_CEXT)

    if CMySQLConnection and not use_pure:
        return CMySQLConnection(*args, **kwargs)
    return MySQLConnection(*args, **kwargs)


def generate_pool_name(**kwargs: Any) -> str:
    """Generate a pool name

    This function takes keyword arguments, usually the connection
    arguments for MySQLConnection, and tries to generate a name for
    a pool.

    Raises PoolError when no name can be generated.

    Returns a string.
    """
    parts = []
    for key in ("host", "port", "user", "database"):
        try:
            parts.append(str(kwargs[key]))
        except KeyError:
            pass

    if not parts:
        raise PoolError("Failed generating pool name; specify pool_name")

    return "_".join(parts)


class PooledMySQLConnection:
    """Class holding a MySQL Connection in a pool

    PooledMySQLConnection is used by MySQLConnectionPool to return an
    instance holding a MySQL connection. It works like a MySQLConnection
    except for methods like close() and config().

    The close()-method will add the connection back to the pool rather
    than disconnecting from the MySQL server.

    Configuring the connection have to be done through the MySQLConnectionPool
    method set_config(). Using config() on pooled connection will raise a
    PoolError.

    Attributes:
        pool_name (str): Returns the name of the connection pool to which the
                         connection belongs.
    """

    def __init__(self, pool: MySQLConnectionPool, cnx: MySQLConnectionAbstract) -> None:
        """Constructor.

        Args:
            pool: A `MySQLConnectionPool` instance.
            cnx: A `MySQLConnectionAbstract` subclass instance.
        """
        if not isinstance(pool, MySQLConnectionPool):
            raise AttributeError("pool should be a MySQLConnectionPool")
        if not isinstance(cnx, MYSQL_CNX_CLASS):
            raise AttributeError("cnx should be a MySQLConnection")
        self._cnx_pool: MySQLConnectionPool = pool
        self._cnx: MySQLConnectionAbstract = cnx

    def __enter__(self) -> PooledMySQLConnection:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        self.close()

    def __getattr__(self, attr: Any) -> Any:
        """Calls attributes of the MySQLConnection instance"""
        return getattr(self._cnx, attr)

    def close(self) -> None:
        """Do not close, but adds connection back to pool.

        For a pooled connection, close() does not actually close it but returns it
        to the pool and makes it available for subsequent connection requests. If the
        pool configuration parameters are changed, a returned connection is closed
        and reopened with the new configuration before being returned from the pool
        again in response to a connection request.
        """
        try:
            cnx = self._cnx
            if self._cnx_pool.reset_session:
                cnx.reset_session()
        finally:
            self._cnx_pool.add_connection(cnx)
            self._cnx = None

    @staticmethod
    def config(**kwargs: Any) -> NoReturn:
        """Configuration is done through the pool.

        For pooled connections, the `config()` method raises a `PoolError`
        exception. Configuration for pooled connections should be done
        using the pool object.
        """
        raise PoolError(
            "Configuration for pooled connections should be done through the "
            "pool itself"
        )

    @property
    def pool_name(self) -> str:
        """Returns the name of the connection pool to which the connection belongs."""
        return self._cnx_pool.pool_name


class MySQLConnectionPool:
    """Class defining a pool of MySQL connections"""

    def __init__(
        self,
        pool_size: int = 5,
        pool_name: Optional[str] = None,
        pool_reset_session: bool = True,
        **kwargs: Any,
    ) -> None:
        """Constructor.

        Initialize a MySQL connection pool with a maximum number of
        connections set to `pool_size`. The rest of the keywords
        arguments, kwargs, are configuration arguments for MySQLConnection
        instances.

        Args:
            pool_name: The pool name. If this argument is not given, Connector/Python
                       automatically generates the name, composed from whichever of
                       the host, port, user, and database connection arguments are
                       given in kwargs, in that order.
            pool_size:  The pool size. If this argument is not given, the default is 5.
            pool_reset_session: Whether to reset session variables when the connection
                                is returned to the pool.
            **kwargs: Optional additional connection arguments, as described in [1].

        Examples:
            ```
            >>> dbconfig = {
            >>>     "database": "test",
            >>>     "user":     "joe",
            >>> }
            >>> cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "mypool",
            >>>                                                       pool_size = 3,
            >>>                                                       **dbconfig)
            ```

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        """
        self._pool_size: Optional[int] = None
        self._pool_name: Optional[str] = None
        self._reset_session = pool_reset_session
        self._set_pool_size(pool_size)
        self._set_pool_name(pool_name or generate_pool_name(**kwargs))
        self._cnx_config: Dict[str, Any] = {}
        self._cnx_queue: queue.Queue[MySQLConnectionAbstract] = queue.Queue(
            self._pool_size
        )
        self._config_version = uuid4()

        if kwargs:
            self.set_config(**kwargs)
            cnt = 0
            while cnt < self._pool_size:
                self.add_connection()
                cnt += 1

    @property
    def pool_name(self) -> str:
        """Returns the name of the connection pool."""
        return self._pool_name

    @property
    def pool_size(self) -> int:
        """Returns number of connections managed by the pool."""
        return self._pool_size

    @property
    def reset_session(self) -> bool:
        """Returns whether to reset session."""
        return self._reset_session

    def set_config(self, **kwargs: Any) -> None:
        """Set the connection configuration for `MySQLConnectionAbstract` subclass instances.

        This method sets the configuration used for creating `MySQLConnectionAbstract`
        subclass instances such as `MySQLConnection`. See [1] for valid
        connection arguments.

        Args:
            **kwargs: Connection arguments - for a complete list of possible
                      arguments, see [1].

        Raises:
            PoolError: When a connection argument is not valid, missing
                       or not supported by `MySQLConnectionAbstract`.

        References:
            [1]: https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        """
        if not kwargs:
            return

        with CONNECTION_POOL_LOCK:
            try:
                test_cnx = connect()
                test_cnx.config(**kwargs)
                self._cnx_config = kwargs
                self._config_version = uuid4()
            except AttributeError as err:
                raise PoolError(f"Connection configuration not valid: {err}") from err

    def _set_pool_size(self, pool_size: int) -> None:
        """Set the size of the pool

        This method sets the size of the pool but it will not resize the pool.

        Raises an AttributeError when the pool_size is not valid. Invalid size
        is 0, negative or higher than pooling.CNX_POOL_MAXSIZE.
        """
        if pool_size <= 0 or pool_size > CNX_POOL_MAXSIZE:
            raise AttributeError(
                "Pool size should be higher than 0 and lower or equal to "
                f"{CNX_POOL_MAXSIZE}"
            )
        self._pool_size = pool_size

    def _set_pool_name(self, pool_name: str) -> None:
        r"""Set the name of the pool.

        This method checks the validity and sets the name of the pool.

        Raises an AttributeError when pool_name contains illegal characters
        ([^a-zA-Z0-9._\-*$#]) or is longer than pooling.CNX_POOL_MAXNAMESIZE.
        """
        if CNX_POOL_NAMEREGEX.search(pool_name):
            raise AttributeError(f"Pool name '{pool_name}' contains illegal characters")
        if len(pool_name) > CNX_POOL_MAXNAMESIZE:
            raise AttributeError(f"Pool name '{pool_name}' is too long")
        self._pool_name = pool_name

    def _queue_connection(self, cnx: MySQLConnectionAbstract) -> None:
        """Put connection back in the queue

        This method is putting a connection back in the queue. It will not
        acquire a lock as the methods using _queue_connection() will have it
        set.

        Raises `PoolError` on errors.
        """
        if not isinstance(cnx, MYSQL_CNX_CLASS):
            raise PoolError(
                "Connection instance not subclass of MySQLConnectionAbstract"
            )

        try:
            self._cnx_queue.put(cnx, block=False)
        except queue.Full as err:
            raise PoolError("Failed adding connection; queue is full") from err

    def add_connection(self, cnx: Optional[MySQLConnectionAbstract] = None) -> None:
        """Adds a connection to the pool.

        This method instantiates a `MySQLConnection` using the configuration
        passed when initializing the `MySQLConnectionPool` instance or using
        the `set_config()` method.
        If cnx is a `MySQLConnection` instance, it will be added to the
        queue.

        Args:
            cnx: The `MySQLConnectionAbstract` subclass object to be added to
                 the pool. If this argument is missing (aka `None`), the pool
                 creates a new connection and adds it.

        Raises:
            PoolError: When no configuration is set, when no more
                       connection can be added (maximum reached) or when the connection
                       can not be instantiated.
        """
        with CONNECTION_POOL_LOCK:
            if not self._cnx_config:
                raise PoolError("Connection configuration not available")

            if self._cnx_queue.full():
                raise PoolError("Failed adding connection; queue is full")

            if not cnx:
                cnx = connect(**self._cnx_config)  # type: ignore[assignment]
                try:
                    if (
                        self._reset_session
                        and self._cnx_config["compress"]
                        and cnx.server_version < (5, 7, 3)
                    ):
                        raise NotSupportedError(
                            "Pool reset session is not supported with "
                            "compression for MySQL server version 5.7.2 "
                            "or earlier"
                        )
                except KeyError:
                    pass

                cnx.pool_config_version = self._config_version
            else:
                if not isinstance(cnx, MYSQL_CNX_CLASS):
                    raise PoolError(
                        "Connection instance not subclass of MySQLConnectionAbstract"
                    )

            self._queue_connection(cnx)

    def get_connection(self) -> PooledMySQLConnection:
        """Gets a connection from the pool.

        This method returns an PooledMySQLConnection instance which
        has a reference to the pool that created it, and the next available
        MySQL connection.

        When the MySQL connection is not connect, a reconnect is attempted.

        Returns:
            A `PooledMySQLConnection` instance.

        Raises:
            PoolError: On errors.
        """
        with CONNECTION_POOL_LOCK:
            try:
                cnx = self._cnx_queue.get(block=False)
            except queue.Empty as err:
                raise PoolError("Failed getting connection; pool exhausted") from err

            if (
                not cnx.is_connected()
                or self._config_version != cnx.pool_config_version
            ):
                cnx.config(**self._cnx_config)
                try:
                    cnx.reconnect()
                except InterfaceError:
                    # Failed to reconnect, give connection back to pool
                    self._queue_connection(cnx)
                    raise
                cnx.pool_config_version = self._config_version

            return PooledMySQLConnection(self, cnx)

    def _remove_connections(self) -> int:
        """Close all connections

        This method closes all connections. It returns the number
        of connections it closed.

        Used mostly for tests.

        Returns int.
        """
        with CONNECTION_POOL_LOCK:
            cnt = 0
            cnxq = self._cnx_queue
            while cnxq.qsize():
                try:
                    cnx = cnxq.get(block=False)
                    cnx.disconnect()
                    cnt += 1
                except queue.Empty:
                    return cnt
                except PoolError:
                    raise
                except Error:
                    # Any other error when closing means connection is closed
                    pass

            return cnt

if True is False:
    # -*- coding: utf-8 -*-
    # 1. IMPORTS
    import customtkinter as ctk
    from tkinter import messagebox, ttk # ttk для Treeview в других модулях пока оставим
    import mysql.connector
    from contextlib import contextmanager
    from datetime import datetime, timedelta
    import csv
    import os
    import requests # Для Модуля 4
    import re     # Для Модуля 4

    # 2. CONFIG
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'hotel_exam_db',
        # 'port': 3307
    }
    MAX_FAILED_LOGIN_ATTEMPTS = 3
    INACTIVITY_LOCK_DAYS = 30
    CSV_FILE_PATH = "Номерной фонд.csv"
    API_URL_FULLNAME = "http://prb.sylas.ru/TransferSimulator/fullName"

    # 3. DATABASE FUNCTIONS
    @contextmanager
    def get_db_connection():
        conn = None
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            yield conn # Возвращаем объект соединения для использования
        except mysql.connector.Error as err:
            print(f"Ошибка БД: {err}")
            messagebox.showerror("Ошибка Базы Данных", f"Не удалось подключиться или выполнить операцию: {err}")
            raise
        finally:
            if conn and conn.is_connected():
                conn.close()

    def execute_query(conn, query, params=None, fetch_one=False, fetch_all=False, is_insert=False):
        # Теперь conn передается как аргумент
        cursor = conn.cursor(dictionary=True if (fetch_one or fetch_all) else False)
        cursor.execute(query, params or ())
        
        if is_insert:
            return cursor.lastrowid
        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        return cursor.rowcount


    # 4. SERVICE FUNCTIONS

    # --- Auth Service ---
    def login_user_service(login, password):
        with get_db_connection() as conn:
            user = execute_query(conn, "SELECT * FROM users WHERE login = %s", (login,), fetch_one=True)
            if not user:
                return {"status": "error", "message": "Пользователь не найден"}

            if user['last_auth_date']:
                last_auth = user['last_auth_date']
                if isinstance(last_auth, str):
                    last_auth = datetime.fromisoformat(last_auth)
                if datetime.now() - last_auth > timedelta(days=INACTIVITY_LOCK_DAYS):
                    if not user['is_blocked']:
                        execute_query(conn, "UPDATE users SET is_blocked = TRUE, failed_login_attempts = 0 WHERE id = %s", (user['id'],))
                        conn.commit() # Нужен коммит после execute_query без fetch
                    return {"status": "error", "message": "Учетная запись заблокирована из-за неактивности."}
            
            if user['is_blocked']:
                return {"status": "error", "message": "Учетная запись заблокирована."}

            if user['password'] == password:
                first_login_ever = user['last_successful_login_time'] is None
                execute_query(conn, """
                    UPDATE users SET failed_login_attempts = 0, last_successful_login_time = NOW(), last_auth_date = NOW()
                    WHERE id = %s """, (user['id'],))
                conn.commit()
                updated_user = execute_query(conn, "SELECT * FROM users WHERE id = %s", (user['id'],), fetch_one=True)
                return {"status": "success", "user": updated_user, "force_password_change": first_login_ever}
            else:
                new_attempts = user['failed_login_attempts'] + 1
                block_user = new_attempts >= MAX_FAILED_LOGIN_ATTEMPTS
                execute_query(conn, "UPDATE users SET failed_login_attempts = %s, is_blocked = %s, last_login_attempt_time = NOW() WHERE id = %s",
                            (new_attempts, block_user, user['id']))
                conn.commit()
                return {"status": "error", "message": "Неверный пароль." + (" Учетная запись заблокирована." if block_user else "")}

    def change_password_service(user_id, current_password, new_password):
        with get_db_connection() as conn:
            user = execute_query(conn, "SELECT * FROM users WHERE id = %s", (user_id,), fetch_one=True)
            if not user:
                return {"status": "error", "message": "Пользователь не найден"}
            if user['password'] != current_password:
                return {"status": "error", "message": "Текущий пароль неверен."}
            
            execute_query(conn, "UPDATE users SET password = %s, last_successful_login_time = NOW() WHERE id = %s", (new_password, user_id))
            conn.commit()
            return {"status": "success", "message": "Пароль успешно изменен."}

    # --- User Service ---
    def create_user_service(login, password, role, full_name=""):
        with get_db_connection() as conn:
            if execute_query(conn, "SELECT id FROM users WHERE login = %s", (login,), fetch_one=True):
                return {"status": "error", "message": "Пользователь с таким логином уже существует."}
            user_id = execute_query(conn, "INSERT INTO users (login, password, role, full_name, last_auth_date) VALUES (%s, %s, %s, %s, NOW())",
                                    (login, password, role, full_name), is_insert=True)
            conn.commit()
            return {"status": "success", "user_id": user_id, "message": "Пользователь создан."} if user_id else {"status": "error", "message": "Ошибка создания."}

    def update_user_service(user_id, login=None, role=None, full_name=None, is_blocked=None, new_password=None):
        with get_db_connection() as conn:
            fields, params = [], []
            if login is not None:
                if execute_query(conn, "SELECT id FROM users WHERE login = %s AND id != %s", (login, user_id), fetch_one=True):
                    return {"status": "error", "message": "Этот логин уже используется."}
                fields.append("login = %s")
                params.append(login)
            if role is not None:
                fields.append("role = %s")
                params.append(role)
            if full_name is not None:
                fields.append("full_name = %s")
                params.append(full_name)
            if is_blocked is not None:
                fields.append("is_blocked = %s")
                params.append(is_blocked)
                if not is_blocked:
                    fields.append("failed_login_attempts = 0")
            if new_password is not None:
                fields.append("password = %s")
                params.append(new_password)
                fields.append("last_successful_login_time = NULL")

            if not fields:
                return {"status": "info", "message": "Нет данных для обновления."}
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
            params.append(user_id)
            execute_query(conn, query, tuple(params))
            conn.commit()
            return {"status": "success", "message": "Данные пользователя обновлены."}

    def get_all_users_service():
        with get_db_connection() as conn:
            return execute_query(conn, "SELECT id, login, role, full_name, is_blocked FROM users ORDER BY login", fetch_all=True)

    # --- Room Service (Модуль 2) ---
    def import_room_data_from_csv(csv_filepath=CSV_FILE_PATH):
        if not os.path.exists(csv_filepath):
            messagebox.showerror("Ошибка импорта", f"Файл {csv_filepath} не найден.")
            return
        
        created_floors, created_categories = {}, {}
        try:
            with get_db_connection() as conn: # Открываем соединение для всей операции
                cursor = conn.cursor() # Используем один курсор для всех операций внутри

                # Получаем ID статуса "Чистый"
                cursor.execute("SELECT id FROM room_statuses WHERE name = 'Чистый'")
                clean_status_id_row = cursor.fetchone()
                if not clean_status_id_row:
                    messagebox.showerror("Ошибка импорта", "Статус 'Чистый' не найден. Инициализируйте БД.")
                    conn.rollback() # Откатываем, если что-то не так на этом этапе
                    return
                clean_status_id = clean_status_id_row[0]

                with open(csv_filepath, mode='r', encoding='utf-8-sig') as file:
                    reader = csv.DictReader(file)
                    for row_num, row in enumerate(reader):
                        try:
                            floor_name = row['Этаж'].strip()
                            room_number = row['Номер'].strip()
                            category_name = row['Категория'].strip()
                            
                            if not all([floor_name, room_number, category_name]):
                                print(f"Пропуск строки {row_num+1} из-за отсутствия данных: {row}")
                                continue

                            # Этаж
                            if floor_name not in created_floors:
                                cursor.execute("SELECT id FROM floors WHERE name = %s", (floor_name,))
                                res = cursor.fetchone()
                                if res:
                                    created_floors[floor_name] = res[0]
                                else:
                                    cursor.execute("INSERT INTO floors (name) VALUES (%s)", (floor_name,))
                                    created_floors[floor_name] = cursor.lastrowid
                            floor_id = created_floors[floor_name]

                            # Категория
                            if category_name not in created_categories:
                                cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
                                res = cursor.fetchone()
                                if res:
                                    created_categories[category_name] = res[0]
                                else:
                                    cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
                                    created_categories[category_name] = cursor.lastrowid
                            category_id = created_categories[category_name]
                            
                            # Номер
                            cursor.execute("SELECT id FROM rooms WHERE id = %s", (room_number,))
                            if not cursor.fetchone(): # Добавляем только если номера нет
                                cursor.execute("INSERT INTO rooms (id, floor_id, category_id, current_status_id) VALUES (%s, %s, %s, %s)",
                                            (room_number, floor_id, category_id, clean_status_id))
                        except Exception as e_row:
                            print(f"Ошибка при обработке строки {row_num+1} CSV: {row}, {e_row}")
                            # Решение: пропустить строку или откатить всю транзакцию?
                            # Для экзамена проще пропустить проблемную строку
                            # conn.rollback() # Откатить, если одна ошибка должна провалить весь импорт
                            # return
                conn.commit() # Коммит в конце всех успешных операций
            messagebox.showinfo("Импорт", "Импорт данных номерного фонда завершен.")
        except Exception as e:
            messagebox.showerror("Ошибка импорта", f"Общая ошибка: {e}")

    def get_room_occupancy_percentage_service():
        with get_db_connection() as conn:
            query = """
            SELECT 
                CASE 
                    WHEN (SELECT COUNT(*) FROM rooms) = 0 THEN 0.0
                    ELSE 
                        (SELECT COUNT(*) FROM rooms WHERE current_status_id = (SELECT id FROM room_statuses WHERE name = 'Занят')) * 100.0 /
                        (SELECT COUNT(*) FROM rooms)
                END AS percentage_occupancy;
            """
            result = execute_query(conn, query, fetch_one=True)
            return result['percentage_occupancy'] if result and result['percentage_occupancy'] is not None else 0.0

    def get_all_rooms_with_details_service():
        with get_db_connection() as conn:
            query = """
            SELECT r.id as room_number, f.name as floor_name, c.name as category_name, rs.name as status_name
            FROM rooms r
            LEFT JOIN floors f ON r.floor_id = f.id
            LEFT JOIN categories c ON r.category_id = c.id
            LEFT JOIN room_statuses rs ON r.current_status_id = rs.id
            ORDER BY f.id, r.id; 
            """ # ORDER BY f.id для правильной сортировки по этажам
            return execute_query(conn, query, fetch_all=True)

    # --- Validation Service (Модуль 4) ---
    def get_fullname_from_api():
        try:
            response = requests.get(API_URL_FULLNAME, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("value")
        except requests.exceptions.RequestException as e:
            # messagebox.showerror("Ошибка API", f"Не удалось получить данные с API: {e}", parent=ctk.CTk()) # Parent может быть проблемой если окна нет
            print(f"Ошибка API: {e}")
            return None

    def validate_fio_service(fio_string):
        # Эта функция просто определяет, есть ли ошибки или нет, для вывода одного сообщения
        if not fio_string:
            return False # Пустое ФИО невалидно

        allowed_chars_pattern = r"^[а-яА-ЯёЁa-zA-Z\s\-]+$"
        if not re.fullmatch(allowed_chars_pattern, fio_string):
            return False # Содержит запрещенные символы

        words = fio_string.strip().split()
        if not (2 <= len(words) <= 3):
            return False # Не 2-3 слова

        for word in words:
            if not word or not word[0].isupper(): # Проверка на пустое слово и заглавную букву
                return False
        return True


    # 5. GUI CLASSES

    class LoginWindow(ctk.CTkFrame):
        def __init__(self, master, app_controller):
            super().__init__(master)
            self.app_controller = app_controller
            self.master.title("Авторизация - Система Гостиницы")
            self.master.geometry("400x350")
            self.pack(pady=20, padx=20, fill="both", expand=True)

            ctk.CTkLabel(self, text="Вход в систему", font=("Arial", 16)).pack(pady=12, padx=10)
            self.login_entry = ctk.CTkEntry(self, placeholder_text="Логин", width=250)
            self.login_entry.pack(pady=12, padx=10)
            self.password_entry = ctk.CTkEntry(self, placeholder_text="Пароль", show="*", width=250)
            self.password_entry.pack(pady=12, padx=10)

            self.show_password_var = ctk.BooleanVar()
            self.show_password_check = ctk.CTkCheckBox(self, text="Показать пароль",
                                                    variable=self.show_password_var,
                                                    command=self._toggle_password_visibility)
            self.show_password_check.pack(pady=5, padx=10)

            ctk.CTkButton(self, text="Войти", command=self._attempt_login, width=250).pack(pady=20, padx=10)

        def _toggle_password_visibility(self):
            if self.show_password_var.get():
                self.password_entry.configure(show="")
            else:
                self.password_entry.configure(show="*")

        def _attempt_login(self):
            login = self.login_entry.get()
            password = self.password_entry.get()
            if not login or not password:
                messagebox.showerror("Ошибка", "Логин и пароль обязательны.", parent=self.master)
                return
            try:
                result = login_user_service(login, password)
                if result["status"] == "success":
                    self.app_controller.current_user = result["user"]
                    messagebox.showinfo("Успех", f"Добро пожаловать, {result['user'].get('full_name', result['user']['login'])}!", parent=self.master)
                    if result["force_password_change"]:
                        self.app_controller.show_change_password_window(initial_change=True)
                    else:
                        self.app_controller.show_dashboard_for_role(result["user"]['role'])
                    self.destroy()
                else:
                    messagebox.showerror("Ошибка входа", result["message"], parent=self.master)
            except Exception as e:
                messagebox.showerror("Критическая ошибка", f"Ошибка при попытке входа: {e}", parent=self.master)


    class ChangePasswordWindow(ctk.CTkToplevel):
        def __init__(self, master, app_controller, initial_change=False):
            super().__init__(master)
            self.app_controller = app_controller
            self.user_id = self.app_controller.current_user['id']
            self.initial_change = initial_change
            self.title("Смена пароля")
            self.geometry("400x350")
            
            self.transient(master)

            ctk.CTkLabel(self, text="Смена пароля", font=("Arial", 16)).pack(pady=10)
            self.current_pass_entry = ctk.CTkEntry(self, placeholder_text="Текущий пароль", show="*", width=300)
            self.current_pass_entry.pack(pady=10, padx=20, fill="x")
            self.new_pass_entry = ctk.CTkEntry(self, placeholder_text="Новый пароль", show="*", width=300)
            self.new_pass_entry.pack(pady=10, padx=20, fill="x")
            self.confirm_pass_entry = ctk.CTkEntry(self, placeholder_text="Подтвердите новый пароль", show="*", width=300)
            self.confirm_pass_entry.pack(pady=10, padx=20, fill="x")
            ctk.CTkButton(self, text="Изменить пароль", command=self._attempt_change, width=300).pack(pady=20)
            
            if self.initial_change:
                self.protocol("WM_DELETE_WINDOW", lambda: messagebox.showwarning("Смена пароля", "Пожалуйста, смените пароль.", parent=self))

        def _attempt_change(self):
            cur = self.current_pass_entry.get()
            new = self.new_pass_entry.get()
            conf = self.confirm_pass_entry.get()
            
            if not all([cur, new, conf]):
                messagebox.showerror("Ошибка", "Все поля обязательны.", parent=self)
                return
            if new != conf:
                messagebox.showerror("Ошибка", "Новые пароли не совпадают.", parent=self)
                return
            if len(new) < 1: # Упрощено
                messagebox.showerror("Ошибка", "Новый пароль не может быть пустым.", parent=self)
                return
            
            try:
                result = change_password_service(self.user_id, cur, new)
                if result["status"] == "success":
                    messagebox.showinfo("Успех", result["message"], parent=self)
                    self.destroy()
                    if self.initial_change:
                        self.app_controller.show_dashboard_for_role(self.app_controller.current_user['role'])
                else:
                    messagebox.showerror("Ошибка смены", result["message"], parent=self)
            except Exception as e:
                messagebox.showerror("Критическая ошибка", f"Ошибка при смене пароля: {e}", parent=self)


    class UserManagementWindow(ctk.CTkToplevel):
        # ... (код этого класса остается почти таким же, как в предыдущей версии, только вызовы сервисов теперь без conn)
        def __init__(self, master, app_controller):
            super().__init__(master)
            self.app_controller = app_controller
            self.title("Управление пользователями")
            self.geometry("850x500")
            
            self.transient(master)
            
            btn_frame = ctk.CTkFrame(self)
            btn_frame.pack(pady=10, padx=10, fill="x")
            ctk.CTkButton(btn_frame, text="Добавить", command=self._open_add_edit_dialog).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="Редактировать", command=lambda: self._open_add_edit_dialog(edit_mode=True)).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="Обновить", command=self._load_users).pack(side="left", padx=5)

            style = ttk.Style(self)
            style.theme_use("default") # или другая доступная тема
            style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
            self.tree = ttk.Treeview(self, columns=("id", "login", "full_name", "role", "is_blocked"), show="headings")
            
            self.tree.heading("id", text="ID")
            self.tree.column("id", width=50, stretch=False, anchor="center")
            self.tree.heading("login", text="Логин")
            self.tree.column("login", width=150, anchor="w")
            self.tree.heading("full_name", text="ФИО")
            self.tree.column("full_name", width=250, anchor="w")
            self.tree.heading("role", text="Роль")
            self.tree.column("role", width=120, anchor="w")
            self.tree.heading("is_blocked", text="Блок")
            self.tree.column("is_blocked", width=80, stretch=False, anchor="center")
            
            self.tree.pack(pady=10, padx=10, fill="both", expand=True)
            self._load_users()

        def _load_users(self):
            for i in self.tree.get_children():
                self.tree.delete(i)
            try:
                users = get_all_users_service()
                if users:
                    for user in users:
                        self.tree.insert("", "end", values=(
                            user['id'], 
                            user['login'], 
                            user.get('full_name',''), # Используем get для безопасности
                            user['role'], 
                            "Да" if user.get('is_blocked', False) else "Нет"
                        ))
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить пользователей: {e}", parent=self)


        def _open_add_edit_dialog(self, edit_mode=False):
            user_data_to_edit = None
            if edit_mode:
                selected_item = self.tree.focus()
                if not selected_item:
                    messagebox.showwarning("Выбор", "Выберите пользователя для редактирования.", parent=self)
                    return
                user_id_selected = self.tree.item(selected_item)['values'][0]
                
                try: # Получаем свежие данные пользователя для редактирования
                    all_users = get_all_users_service()
                    if all_users:
                        for u_data in all_users:
                            if u_data['id'] == user_id_selected:
                                user_data_to_edit = u_data
                                break
                    if not user_data_to_edit:
                        messagebox.showerror("Ошибка", "Не найдены данные пользователя для редактирования.", parent=self)
                        return
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось получить данные пользователя: {e}", parent=self)
                    return

            AddEditUserDialog(self, self.app_controller, mode=("edit" if edit_mode else "add"), user_data=user_data_to_edit, callback=self._load_users)


    class AddEditUserDialog(ctk.CTkToplevel):
        # ... (код этого класса остается почти таким же, как в предыдущей версии, только вызовы сервисов теперь без conn)
        def __init__(self, master, app_controller, mode="add", user_data=None, callback=None):
            super().__init__(master)
            self.mode = mode
            self.user_data = user_data # Это dict пользователя, если mode="edit"
            self.callback = callback
            self.app_controller = app_controller # Не использовался, но может пригодиться

            if mode == "add":
                self.title("Добавить пользователя")
            else:
                self.title(f"Редактировать: {user_data.get('login', '')}")
            
            self.geometry("450x450")
            
            self.transient(master)

            ctk.CTkLabel(self, text="Логин:").pack(anchor="w", padx=20, pady=(10,0))
            self.login_entry = ctk.CTkEntry(self, width=400)
            self.login_entry.pack(padx=20, pady=(0,10))
            
            ctk.CTkLabel(self, text="ФИО:").pack(anchor="w", padx=20, pady=(5,0))
            self.fname_entry = ctk.CTkEntry(self, width=400)
            self.fname_entry.pack(padx=20, pady=(0,10))
            
            ctk.CTkLabel(self, text="Роль:").pack(anchor="w", padx=20, pady=(5,0))
            self.role_var = ctk.StringVar(value="Пользователь") # Значение по умолчанию
            ctk.CTkOptionMenu(self, variable=self.role_var, values=["Пользователь", "Администратор"], width=400).pack(padx=20, pady=(0,10))
            
            pass_label_text = "Пароль:" if mode == "add" else "Новый пароль (пусто - не менять):"
            ctk.CTkLabel(self, text=pass_label_text).pack(anchor="w", padx=20, pady=(5,0))
            self.pass_entry = ctk.CTkEntry(self, show="*", width=400)
            self.pass_entry.pack(padx=20, pady=(0,10))

            if mode == "edit":
                self.block_var = ctk.BooleanVar(value=user_data.get('is_blocked', False))
                ctk.CTkCheckBox(self, text="Заблокирован", variable=self.block_var).pack(anchor="w", padx=20, pady=(5,10))
            
            if user_data: # Предзаполнение для режима редактирования
                self.login_entry.insert(0, user_data.get('login',''))
                self.fname_entry.insert(0, user_data.get('full_name',''))
                self.role_var.set(user_data.get('role','Пользователь'))

            ctk.CTkButton(self, text="Сохранить", command=self._save, width=400).pack(pady=20)

        def _save(self):
            login = self.login_entry.get()
            fname = self.fname_entry.get()
            role = self.role_var.get()
            password = self.pass_entry.get()

            if not login:
                messagebox.showerror("Ошибка", "Логин обязателен.", parent=self)
                return
            if self.mode == "add" and not password:
                messagebox.showerror("Ошибка", "Пароль обязателен для нового пользователя.", parent=self)
                return

            result = None
            try:
                if self.mode == "add":
                    result = create_user_service(login, password, role, fname)
                else: # edit mode
                    is_blocked_val = self.block_var.get() if hasattr(self, 'block_var') else self.user_data.get('is_blocked') 
                    
                    update_params = {'user_id': self.user_data['id']}
                    # Передаем параметры, только если они изменились, или это новый пароль
                    if login != self.user_data.get('login'): update_params['login'] = login
                    if fname != self.user_data.get('full_name'): update_params['full_name'] = fname
                    if role != self.user_data.get('role'): update_params['role'] = role
                    if password: update_params['new_password'] = password 
                    if is_blocked_val != self.user_data.get('is_blocked'):
                        update_params['is_blocked'] = is_blocked_val
                    
                    uid_temp = update_params.pop('user_id') # user_id передается первым аргументом
                    if len(update_params) > 0: # Только если есть что обновлять
                        result = update_user_service(uid_temp, **update_params)
                    else:
                        result = {"status": "info", "message": "Нет изменений для сохранения."}

                if result and result["status"] == "success":
                    messagebox.showinfo("Успех", result["message"], parent=self)
                    if self.callback: self.callback()
                    self.destroy()
                elif result and result["status"] == "info":
                    messagebox.showinfo("Информация", result["message"], parent=self)
                    self.destroy() # Закрываем окно, даже если не было изменений
                elif result: # Ошибка
                    messagebox.showerror("Ошибка", result["message"], parent=self)
            except Exception as e:
                messagebox.showerror("Критическая ошибка", f"Ошибка при сохранении пользователя: {e}", parent=self)


    class AdminDashboard(ctk.CTkFrame):
        # ... (код этого класса остается почти таким же, как в предыдущей версии, только вызовы сервисов теперь без conn)
        def __init__(self, master, app_controller):
            super().__init__(master)
            self.app_controller = app_controller
            user = self.app_controller.current_user
            self.master.title(f"Админ: {user.get('full_name', user['login'])}")
            self.master.geometry("700x550") # Увеличил высоту для таблицы
            self.pack(pady=10, padx=10, fill="both", expand=True)

            ctk.CTkLabel(self, text="Рабочий стол Администратора", font=("Arial", 18)).pack(pady=10)
            
            top_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
            top_buttons_frame.pack(pady=5, padx=5, fill="x")

            ctk.CTkButton(top_buttons_frame, text="Управление пользователями", command=lambda: UserManagementWindow(self.master, self.app_controller)).pack(side="left", padx=5, pady=5)
            ctk.CTkButton(top_buttons_frame, text="Импорт номеров (CSV)", command=self._import_rooms).pack(side="left", padx=5, pady=5)
            ctk.CTkButton(top_buttons_frame, text="% загрузки номеров", command=self._show_occupancy).pack(side="left", padx=5, pady=5)
            ctk.CTkButton(top_buttons_frame, text="Валидация ФИО (М4)", command=self._open_validation_module).pack(side="left", padx=5, pady=5)
            
            ctk.CTkLabel(self, text="Состояние номерного фонда:", font=("Arial", 14)).pack(pady=(10,0), anchor="w", padx=5)
            
            style = ttk.Style(self)
            style.theme_use("default")
            style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
            self.rooms_tree = ttk.Treeview(self, columns=("number", "floor", "category", "status"), show="headings")
            self.rooms_tree.heading("number", text="Номер")
            self.rooms_tree.column("number", width=80, anchor="w", stretch=False)
            self.rooms_tree.heading("floor", text="Этаж")
            self.rooms_tree.column("floor", width=150, anchor="w")
            self.rooms_tree.heading("category", text="Категория")
            self.rooms_tree.column("category", width=200, anchor="w")
            self.rooms_tree.heading("status", text="Статус")
            self.rooms_tree.column("status", width=120, anchor="w")
            self.rooms_tree.pack(pady=5, padx=5, fill="both", expand=True)
            self._load_room_details()

            ctk.CTkButton(self, text="Выход", command=self.app_controller.logout).pack(pady=10, side="bottom")

        def _import_rooms(self):
            if messagebox.askyesno("Импорт", f"Импортировать данные из '{CSV_FILE_PATH}'?\nСуществующие номера не будут перезаписаны.", parent=self.master):
                try:
                    import_room_data_from_csv()
                    self._load_room_details()
                except Exception as e:
                    messagebox.showerror("Ошибка импорта", f"Произошла ошибка во время импорта: {e}", parent=self.master)


        def _show_occupancy(self):
            try:
                percentage = get_room_occupancy_percentage_service()
                messagebox.showinfo("Загрузка номеров", f"Текущая загрузка: {percentage:.2f}%", parent=self.master)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось рассчитать загрузку: {e}", parent=self.master)
        
        def _load_room_details(self):
            for i in self.rooms_tree.get_children():
                self.rooms_tree.delete(i)
            try:
                rooms = get_all_rooms_with_details_service()
                if rooms:
                    for room in rooms:
                        self.rooms_tree.insert("", "end", values=(
                            room.get('room_number',''), 
                            room.get('floor_name',''), 
                            room.get('category_name',''), 
                            room.get('status_name','')
                        ))
                else: # Если сервис вернул None или пустой список
                    self.rooms_tree.insert("", "end", values=("Нет данных", "", "", ""))
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить номера: {e}", parent=self)
                self.rooms_tree.insert("", "end", values=("Ошибка загрузки", "", "", ""))


        def _open_validation_module(self):
            ValidationWindow(self.master, self.app_controller)


    class UserDashboard(ctk.CTkFrame):
        def __init__(self, master, app_controller):
            super().__init__(master)
            self.app_controller = app_controller
            user = self.app_controller.current_user
            self.master.title(f"Пользователь: {user.get('full_name', user['login'])}")
            self.master.geometry("650x450") # Изменил размер
            self.pack(pady=10, padx=10, fill="both", expand=True)

            ctk.CTkLabel(self, text="Рабочий стол Сотрудника", font=("Arial", 18)).pack(pady=10)
            ctk.CTkButton(self, text="Сменить свой пароль", command=lambda: self.app_controller.show_change_password_window(initial_change=False)).pack(pady=10)
            
            ctk.CTkLabel(self, text="Доступные номера:", font=("Arial", 14)).pack(pady=(10,0), anchor="w", padx=5)
            
            style = ttk.Style(self)
            style.theme_use("default")
            style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
            self.rooms_tree = ttk.Treeview(self, columns=("number", "floor", "category", "status"), show="headings")
            self.rooms_tree.heading("number", text="Номер")
            self.rooms_tree.column("number", width=80, anchor="w", stretch=False)
            self.rooms_tree.heading("floor", text="Этаж")
            self.rooms_tree.column("floor", width=150, anchor="w")
            self.rooms_tree.heading("category", text="Категория")
            self.rooms_tree.column("category", width=200, anchor="w")
            self.rooms_tree.heading("status", text="Статус")
            self.rooms_tree.column("status", width=120, anchor="w")
            self.rooms_tree.pack(pady=5, padx=5, fill="both", expand=True)
            self._load_room_details()

            ctk.CTkButton(self, text="Выход", command=self.app_controller.logout).pack(pady=10, side="bottom")

        def _load_room_details(self):
            for i in self.rooms_tree.get_children():
                self.rooms_tree.delete(i)
            try:
                rooms = get_all_rooms_with_details_service()
                if rooms:
                    for room in rooms:
                        self.rooms_tree.insert("", "end", values=(
                            room.get('room_number',''), 
                            room.get('floor_name',''), 
                            room.get('category_name',''), 
                            room.get('status_name','')
                        ))
                else:
                    self.rooms_tree.insert("", "end", values=("Нет данных", "", "", ""))
            except Exception as e:
                messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить номера: {e}", parent=self)
                self.rooms_tree.insert("", "end", values=("Ошибка загрузки", "", "", ""))


    class ValidationWindow(ctk.CTkToplevel): # Модуль 4 - Упрощенный
        def __init__(self, master, app_controller):
            super().__init__(master)
            self.app_controller = app_controller # Не используется, но по структуре передаем
            self.title("Валидация данных")
            self.geometry("550x200") # Уменьшил размер
            
            self.transient(master)
            self.resizable(False, False)

            main_frame = ctk.CTkFrame(self, fg_color="transparent")
            main_frame.pack(pady=20, padx=20, fill="both", expand=True)

            # Первая строка: Кнопка "Получить данные" и текстовое поле для ФИО
            frame_get_data = ctk.CTkFrame(main_frame, fg_color="transparent")
            frame_get_data.pack(fill="x", pady=5)

            self.get_data_button = ctk.CTkButton(frame_get_data, text="Получить данные", command=self._get_data_from_api, width=180)
            self.get_data_button.pack(side="left", padx=(0, 10))

            self.fio_display_entry = ctk.CTkEntry(frame_get_data, placeholder_text="ФИО с API", width=300)
            self.fio_display_entry.pack(side="left", fill="x", expand=True)
            self.fio_display_entry.configure(state="readonly")

            # Вторая строка: Кнопка "Отправить результат теста" и текстовое поле для результата
            frame_send_result = ctk.CTkFrame(main_frame, fg_color="transparent")
            frame_send_result.pack(fill="x", pady=15)

            self.send_result_button = ctk.CTkButton(frame_send_result, text="Отправить результат теста", command=self._send_test_result, width=180)
            self.send_result_button.pack(side="left", padx=(0, 10))

            self.validation_status_entry = ctk.CTkEntry(frame_send_result, placeholder_text="Статус валидации", width=300)
            self.validation_status_entry.pack(side="left", fill="x", expand=True)
            self.validation_status_entry.configure(state="readonly")


        def _get_data_from_api(self):
            fio = get_fullname_from_api()
            self.fio_display_entry.configure(state="normal")
            self.fio_display_entry.delete(0, "end")
            if fio:
                self.fio_display_entry.insert(0, fio)
            else:
                self.fio_display_entry.insert(0, "Ошибка получения ФИО с API")
            self.fio_display_entry.configure(state="readonly")
            
            # Сразу очищаем поле результата валидации, т.к. данные новые
            self.validation_status_entry.configure(state="normal")
            self.validation_status_entry.delete(0, "end")
            self.validation_status_entry.configure(state="readonly")


        def _send_test_result(self):
            fio_to_validate = self.fio_display_entry.get()
            self.validation_status_entry.configure(state="normal")
            self.validation_status_entry.delete(0, "end")

            if not fio_to_validate or "Ошибка получения" in fio_to_validate:
                self.validation_status_entry.insert(0, "Нет ФИО для проверки")
                messagebox.showwarning("Внимание", "Сначала получите ФИО с API.", parent=self)
            else:
                is_valid = validate_fio_service(fio_to_validate) # Используем упрощенный сервис
                if is_valid:
                    self.validation_status_entry.insert(0, "ФИО корректно")
                else:
                    self.validation_status_entry.insert(0, "ФИО содержит запрещенные символы")
            
            self.validation_status_entry.configure(state="readonly")
            # Имитация "отправки" - просто выводим сообщение
            print(f"Модуль 4: Проверено ФИО '{fio_to_validate}', результат: '{self.validation_status_entry.get()}'")


    class AppController(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.current_user = None
            self._current_frame = None
            
            self.show_login_window()

        def clear_frame(self):
            if self._current_frame:
                self._current_frame.destroy()
                self._current_frame = None

        def show_login_window(self):
            self.clear_frame()
            self.current_user = None
            self._current_frame = LoginWindow(self, self)
            self.title("Авторизация")

        def show_change_password_window(self, initial_change=False):
            if self.current_user:
                ChangePasswordWindow(self, self, initial_change=initial_change)
            else:
                self.show_login_window() # Перенаправить на логин, если нет пользователя

        def show_dashboard_for_role(self, role):
            self.clear_frame()
            if role == 'Администратор':
                self._current_frame = AdminDashboard(self, self)
            else: # Пользователь
                self._current_frame = UserDashboard(self, self)
        
        def logout(self):
            self.current_user = None
            # Закрыть все дочерние окна Toplevel
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkToplevel):
                    widget.destroy()
            self.show_login_window()

    # 6. MAIN EXECUTION BLOCK
    if __name__ == "__main__":
        ctk.set_appearance_mode("System")  # Modes: "System" (стандарт), "Dark", "Light"
        ctk.set_default_color_theme("green") # Themes: "blue" (стандарт), "green", "dark-blue"
        
        app = AppController()
        app.mainloop()


    # SELECT
        # (SELECT COUNT(*) FROM rooms WHERE current_status_id = (SELECT id FROM room_statuses WHERE name = 'Занят')) * 100.0 /
        # (SELECT COUNT(*) FROM rooms) AS percentage_occupancy;