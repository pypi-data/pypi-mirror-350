import datetime
import os

import pytest

from pancham.data_frame_configuration_loader import YamlDataFrameConfigurationLoader
from pancham.runner import DEFAULT_FIELD_PARSERS, DEFAULT_OUTPUTS

class TestDataFrameConfigurationLoader:

    filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/order_configuration.yml"
    yaml_filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/yaml_order_configuration.yml"
    invalid_filename = os.path.dirname(os.path.realpath(__file__)) + "/../example/invalid_order_configuration.yml"

    def test_load_order_configuration(self):
        loader = YamlDataFrameConfigurationLoader(field_parsers=DEFAULT_FIELD_PARSERS, output_configuration=DEFAULT_OUTPUTS)

        config = loader.load(self.filename)

        assert len(config.fields) == 3
        assert config.fields[0].name == 'Order'
        assert config.fields[0].source_name == 'Order Id'
        assert config.fields[0].nullable is False
        assert config.fields[0].field_type == int

        assert config.fields[1].name == 'Date'
        assert config.fields[1].nullable is False
        assert config.fields[1].field_type == datetime.datetime

    def test_load_invalid_order_configuration(self):
        loader = YamlDataFrameConfigurationLoader(field_parsers=DEFAULT_FIELD_PARSERS, output_configuration=DEFAULT_OUTPUTS)

        with pytest.raises(ValueError):
            loader.load(self.invalid_filename)

    def test_load_order_yml_configuration(self):
        loader = YamlDataFrameConfigurationLoader(field_parsers=DEFAULT_FIELD_PARSERS, output_configuration=DEFAULT_OUTPUTS)

        config = loader.load(self.yaml_filename)

        assert config.file_type == 'yaml'
        assert config.key == 'exp'
        assert len(config.fields) == 3
        assert config.fields[0].name == 'Order'
        assert config.fields[0].source_name == 'Order Id'
        assert config.fields[0].nullable is False
        assert config.fields[0].field_type == int

        assert config.fields[1].name == 'Date'
        assert config.fields[1].nullable is False
        assert config.fields[1].field_type == datetime.datetime
