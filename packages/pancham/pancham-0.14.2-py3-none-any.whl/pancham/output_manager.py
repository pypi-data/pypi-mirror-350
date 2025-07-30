import pandas as pd

from .pancham_configuration import PanchamConfiguration
from .reporter import Reporter
from .data_frame_configuration import DataFrameConfiguration
from .database.database_output import DatabaseOutputWriter
from .output_configuration import OutputWriter
from .database.database_engine import initialize_db_engine

class OutputManager:

    def __init__(self, pancham_configuration: PanchamConfiguration, outputs: dict[str, OutputWriter], reporter: Reporter):
        self.pancham_configuration = pancham_configuration
        self.outputs = outputs
        self.reporter = reporter
        self.loaded_outputs: dict[str, OutputWriter] = {}

    def write_output(self, data: pd.DataFrame, configuration: DataFrameConfiguration):
        """
        Writes a DataFrame to configured outputs using specified configurations.

        This method iterates through the output configurations and writes the
        provided DataFrame to each specified output destination. The specific
        implementation of writing is determined by the retrieved writer for
        each output configuration.

        :param data: A pandas DataFrame containing the data to be written.
        :type data: pd.DataFrame
        :param configuration: Configuration object specifying the output
            destination and output settings.
        :type configuration: DataFrameConfiguration
        :return: None
        """
        for output in configuration.output:
            writer = self.__get_output(output)
            writer.write(data, output)

    def __get_output(self, output_config: dict) -> OutputWriter:
        """
        Retrieves or creates an output writer based on the specified output configuration.

        This method checks whether the requested output type is available in the predefined
        outputs or has been previously loaded. If the output type is not found, it attempts
        to initialize the output writer for the specified type (e.g., database). If the
        requested output type is not supported, an exception is raised.

        :param output_config: Configuration dictionary specifying the output type. Must
                              include the `output_type` key.
        :type output_config: dict
        :return: An instance of OutputWriter corresponding to the output type.
        :rtype: OutputWriter
        :raises ValueError: If the requested output type is not supported.
        """
        output_type = output_config['output_type']

        if output_type in self.outputs:
            return self.outputs[output_type]

        if output_type in self.loaded_outputs:
            return self.loaded_outputs[output_type]

        if output_type == 'database':
            initialize_db_engine(self.pancham_configuration, self.reporter)
            self.loaded_outputs[output_type] = DatabaseOutputWriter()
            return self.loaded_outputs[output_type]

        raise ValueError(f'Unsupported output type: {output_type}')
