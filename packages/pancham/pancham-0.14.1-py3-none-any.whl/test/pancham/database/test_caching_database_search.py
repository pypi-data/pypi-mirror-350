from sqlalchemy import MetaData, Table, Column, String
import pandas as pd

from pancham.database.database_search_manager import get_database_search
from pancham.database.database_engine import get_db_engine, initialize_db_engine
from pancham.reporter import PrintReporter
from pancham.database.caching_database_search import CachingDatabaseSearch
from pancham_configuration import PanchamConfiguration

class MockConfig(PanchamConfiguration):

    @property
    def database_connection(self) -> str:
        return "sqlite:///:memory:"

class TestCachingDatabaseSearch:

    def test_engine_write_df(self):
        initialize_db_engine(MockConfig(), PrintReporter())

        meta = MetaData()
        Table('order0', meta, Column("email", String), Column("order_id", String))

        meta.create_all(get_db_engine().engine)

        data = pd.DataFrame({'email': ['a@example.com', 'b@example.com'], 'order_id': ['1', '2']})

        get_db_engine().write_df(data, 'order0')

        search = CachingDatabaseSearch('order0', 'email', 'order_id')

        assert search.get_mapped_id('b@example.com') == '2'
        assert search.get_mapped_id('c@example.com') is None

    def test_cast_engine_write_df(self):
        initialize_db_engine(MockConfig(), PrintReporter())

        meta = MetaData()
        Table('order2', meta, Column("email", String), Column("order_id", String))

        meta.create_all(get_db_engine().engine)

        data = pd.DataFrame({'email': ['a@example.com', 'b@example.com'], 'order_id': ['1', '2']})

        get_db_engine().write_df(data, 'order2')

        search = get_database_search('order2', 'email', 'order_id', None,'str', 'int')

        assert search.get_mapped_id('b@example.com') == 2
        assert search.get_mapped_id('c@example.com') is None

    def test_cast_filter_engine_write_df(self):
        initialize_db_engine(MockConfig(), PrintReporter())

        meta = MetaData()
        Table('order3', meta, Column("email", String), Column("order_id", String), Column("active", String))

        meta.create_all(get_db_engine().engine)

        data = pd.DataFrame({'email': ['a@example.com', 'b@example.com'], 'order_id': ['1', '2'], 'active':['N', 'Y']})

        get_db_engine().write_df(data, 'order3')

        search = get_database_search('order3', 'email', 'order_id', {'active': 'Y'},'str', 'int')

        assert search.get_mapped_id('b@example.com') == 2
        assert search.get_mapped_id('c@example.com') is None
        assert search.get_mapped_id('a@example.com') is None
