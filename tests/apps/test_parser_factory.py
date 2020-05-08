from ATE.apps.masterApp.parameter_parser import parser_factory
from ATE.apps.masterApp.parameter_parser.xml_parameter_parser import XmlParameterParser
from ATE.apps.masterApp.parameter_parser.filesystem_data_source import FileSystemDataSource


class TestParserFactory:

    def test_create_parser_yields_xml_parser_for_xmlmicronas(self):
        jobformat = 'xml.micronas'
        parser = parser_factory.CreateParser(jobformat)

        assert(type(parser) is XmlParameterParser)

    def test_create_parser_yields_none_for_unknown_value(self):
        jobformat = 'empty'
        parser = parser_factory.CreateParser(jobformat)

        assert(parser is None)

    def test_create_datasource_yields_filesystemdatasource_for_filesystem(self):
        config = {'jobsource': 'filesystem',
                  'filesystemdatasource.path': '.',
                  'filesystemdatasource.jobpattern': 'job'}
        parser = None
        datasource = parser_factory.CreateDataSource("somejob", config, parser)

        assert(type(datasource) is FileSystemDataSource)

    def test_create_datasource_yields_filesystemdatasource_for_unkown_value(self):
        config = {'jobsource': 'gremlins'}
        parser = None
        datasource = parser_factory.CreateDataSource("somejob", config, parser)

        assert(datasource is None)

    def test_read_data_from_xml_file_file_does_not_exist(self):
        config = {'jobsource': 'filesystem',
                  'jobformat': 'xml.micronas',
                  'filesystemdatasource.path': './tests/apps',
                  'filesystemdatasource.jobpattern': 'ddd.xml'}

        parser = parser_factory.CreateParser(config['jobformat'])
        datasource = parser_factory.CreateDataSource("306426001", config, parser)
        assert(type(datasource) is FileSystemDataSource)
        data = datasource.retrieve_data()
        assert(data is None)

    def test_read_data_from_xml_file_wrong_lot_number(self):
        config = {'jobsource': 'filesystem',
                  'jobformat': 'xml.micronas',
                  'filesystemdatasource.path': './tests/apps',
                  'filesystemdatasource.jobpattern': 'le306426001.xml'}

        parser = parser_factory.CreateParser(config['jobformat'])
        datasource = parser_factory.CreateDataSource("11111111", config, parser)
        assert(type(datasource) is FileSystemDataSource)
        data = datasource.retrieve_data()
        assert(data is not None)
        verify_result = datasource.verify_data(data)
        assert(verify_result is False)

    def test_read_data_from_xml_file_device_id_does_not_match(self):
        config = {'device_id': 'SCT_2121',
                  'jobsource': 'filesystem',
                  'jobformat': 'xml.micronas',
                  'filesystemdatasource.path': './tests/apps',
                  'filesystemdatasource.jobpattern': 'le306426001.xml'}

        parser = parser_factory.CreateParser(config['jobformat'])
        datasource = parser_factory.CreateDataSource("306426001", config, parser)
        assert(type(datasource) is FileSystemDataSource)
        data = datasource.retrieve_data()
        assert(data is not None)
        verify_result = datasource.verify_data(data)
        assert(verify_result is False)

    def test_read_data_from_xml_file_valid_data(self):
        config = {'device_id': 'SCT-81',
                  'jobsource': 'filesystem',
                  'jobformat': 'xml.micronas',
                  'filesystemdatasource.path': './tests/apps',
                  'filesystemdatasource.jobpattern': 'le306426001.xml',
                  'Handler': 'HTO92-20F',
                  'Environment': 'F1'}

        parser = parser_factory.CreateParser(config['jobformat'])
        print(parser)
        datasource = parser_factory.CreateDataSource("306426001", config, parser)
        assert(type(datasource) is FileSystemDataSource)
        data = datasource.retrieve_data()
        assert(data is not None)
        verify_result = datasource.verify_data(data)
        assert(verify_result is True)

    def test_read_data_from_xml_file_invalid_handler_id(self):
        config = {'device_id': 'SCT-81',
                  'jobsource': 'filesystem',
                  'jobformat': 'xml.micronas',
                  'filesystemdatasource.path': './tests/apps',
                  'filesystemdatasource.jobpattern': 'le306426001.xml',
                  'Handler': 'invalid',
                  'Environment': 'F1'}

        parser = parser_factory.CreateParser(config['jobformat'])
        print(parser)
        datasource = parser_factory.CreateDataSource("306426001", config, parser)
        assert(type(datasource) is FileSystemDataSource)
        data = datasource.retrieve_data()
        assert(data is not None)
        verify_result = datasource.verify_data(data)
        assert(verify_result is False)
