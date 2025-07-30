import pandas as pd

from .database_engine import get_db_engine
from pancham.output_configuration import OutputConfiguration, OutputWriter

class DatabaseOutput(OutputConfiguration):

    def can_apply(self, configuration: dict):
        """
        Determines whether the provided configuration can be applied.

        This method validates if the configuration contains the necessary output
        settings for a database and ensures that all required fields are present.

        :param configuration: The configuration dictionary to validate.
                              It should include an 'output' key with a list of
                              output configurations.
        :type configuration: dict
        :return: Indicates whether the configuration can be applied.
        :rtype: bool
        :raises ValueError: If the 'database' output type is detected but the
                            required 'table' key is missing.
        """
        if not 'output' in configuration:
            return False

        db_config: dict | None = None

        for output in configuration['output']:
            if output['output_type'] == 'database':
                db_config = output
                break

        if db_config is None:
            return False

        if 'table' not in db_config:
            raise ValueError('table is required in database output configuration')

        return True

    def to_output_configuration(self, configuration: dict) -> dict:
        """
        Return the output configuration block for this object
       
        Will return:
            output_type: database
            table: Name of the table to write to
        
        :param configuration: 
        :return: 
        """
        for output in configuration['output']:
            if output['output_type'] == 'database':
                return output

        raise ValueError('Database configuration not set')

class DatabaseOutputWriter(OutputWriter):

    def write(self, data: pd.DataFrame, configuration: dict):
        """
        Write data from a pandas DataFrame to a database table using the specified
        configuration. The function optionally filters the DataFrame columns
        based on a list of column names provided in the configuration.

        :param data: A pandas DataFrame representing the data to be written
            to the database.
        :type data: pandas.DataFrame
        :param configuration: A dictionary containing configuration details
            for writing the DataFrame. Possible keys include:
            - "columns": List of column names to filter the DataFrame.
            - "table": Name of the destination database table.
        :type configuration: dict
        :return: None
        """
        if 'columns' in configuration:
            data = data[configuration['columns']]

        if 'merge_key' in configuration:
            on_missing = configuration.get('on_missing', 'ignore')
            merge_data_type = configuration.get('merge_data_type', None)
            native = configuration.get('native', None)
            merge_key = configuration['merge_key']

            for _, row in data.iterrows():
                get_db_engine().merge_row(row, configuration['table'], merge_key, on_missing, merge_data_type, native)
            return

        get_db_engine().write_df(data, configuration['table'])
