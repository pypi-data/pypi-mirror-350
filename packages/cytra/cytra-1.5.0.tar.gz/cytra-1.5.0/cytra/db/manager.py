import os
from os.path import exists
from urllib.parse import urlparse

from sqlalchemy import create_engine


class DatabaseManagerAbstract(object):
    def __init__(self, engine_kwargs, admin_engine_kwargs=None):
        self.db_url = engine_kwargs["url"]
        self.db_name = urlparse(self.db_url).path.lstrip("/")
        if admin_engine_kwargs:
            self.engine = create_engine(**admin_engine_kwargs)
        else:
            self.engine = create_engine(**engine_kwargs)

    def __enter__(self):
        self.connection = self.engine.connect()
        self.connection.execute("commit")
        return self

    def __exit__(self, *args):
        self.engine.dispose()

    def create_database_if_not_exists(self):
        if not self.database_exists():
            self.create_database()

    def database_exists(self):  # pragma: no cover
        raise NotImplementedError()

    def create_database(self):  # pragma: no cover
        raise NotImplementedError()

    def drop_database(self):  # pragma: no cover
        raise NotImplementedError()


class SqliteManager(DatabaseManagerAbstract):
    """
    SQLite database manager
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = self.db_url.replace("sqlite:///", "")

    def database_exists(self):
        return exists(self.filename)

    def create_database(self):
        if self.database_exists():
            raise RuntimeError(
                "The file is already exists: %s" % self.filename
            )
        open(self.filename, "a").close()

    def drop_database(self):
        os.remove(self.filename)


class MysqlManager(DatabaseManagerAbstract):
    """
    MySQL database manager
    """

    def database_exists(self):
        r = self.connection.execute(f"SHOW DATABASES LIKE '{self.db_name}'")
        try:
            ret = r.cursor.fetchall()
            return len(ret) > 0
        finally:
            r.cursor.close()

    def create_database(self):
        self.connection.execute(f"CREATE DATABASE {self.db_name}")
        self.connection.execute("commit")

    def drop_database(self):
        self.connection.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        self.connection.execute("commit")


class PostgresManager(DatabaseManagerAbstract):
    def database_exists(self):
        r = self.connection.execute(
            f"SELECT 1 FROM pg_database WHERE datname = '{self.db_name}'"
        )
        try:
            ret = r.cursor.fetchall()
            return ret
        finally:
            r.cursor.close()

    def create_database(self):
        self.connection.execute(f"CREATE DATABASE {self.db_name}")
        self.connection.execute("commit")

    def drop_database(self):
        self.connection.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        self.connection.execute("commit")


class DatabaseManager(DatabaseManagerAbstract):
    """
    Some operations to manage database
    """

    def __new__(cls, engine_kwargs, admin_engine_kwargs=None):
        url = engine_kwargs["url"]
        if url.startswith("sqlite"):
            manager_class = SqliteManager
        elif url.startswith("postgres"):
            manager_class = PostgresManager
        elif url.startswith("mysql"):
            manager_class = MysqlManager
        else:
            raise ValueError("Unsupported database uri: %s" % url)

        return manager_class(engine_kwargs, admin_engine_kwargs)
