from sqlalchemy import MetaData, Table, Column, String
import pandas as pd
import os

from pancham.database.sql_file_loader import SqlFileLoader
from pancham.database.database_engine import get_db_engine, initialize_db_engine
from pancham.reporter import PrintReporter
from pancham_configuration import PanchamConfiguration

class MockConfig(PanchamConfiguration):

    @property
    def database_connection(self) -> str:
        return "sqlite:///:memory:"


class TestSqlFileLoader:

    def test_sql_read_df(self):
        initialize_db_engine(MockConfig(), PrintReporter())

        meta = MetaData()
        Table('customer', meta, Column("email", String), Column("customer_id", String))

        meta.create_all(get_db_engine().engine)

        data = pd.DataFrame({'email': ['a@example.com', 'b@example.com'], 'customer_id': ['1', '2']})

        get_db_engine().write_df(data, 'customer')

        loader = SqlFileLoader()

        test_file = os.path.dirname(os.path.realpath(__file__)) + "/../../"
        data = loader.read_file(f'{test_file}example/customer_load.sql')

        assert data.iloc[0]['id'] == '2'