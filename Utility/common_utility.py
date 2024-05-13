import os

from Constants.constants import Constants


class CommonUtility:

    @staticmethod
    def validate_args(args):
        if (not args['url'] and not args['html_file']) or \
            (not args['url'] and not args['html_string']):
            raise Exception('Invalid params provided. Use -h or --help to show '
                            'the help message.')

    # Define a custom argument type for a list of strings
    @staticmethod
    def list_of_strings(arg):
        return arg.split(',')

    # Validates for the length of the converted json ld.
    @staticmethod
    def validate_file_length(json):
        file_length = len(json) / 1024
        if file_length >= Constants.MAX_JSON_LD_LENGTH:
            raise Exception('JSON LD is too large.')

    def __store_json_ld_output(self, json_ld, file_path):
        file_name = os.path.join(os.getcwd(), file_path)
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w') as write_file:
            write_file.write(json_ld)

    def __store_html_output(self, html, file_path):
        file_name = os.path.join(os.getcwd(), file_path)
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, 'w') as write_file:
            write_file.write(html)

    def store_json_ld(self, json, file_path):
        self.__store_json_ld_output(json_ld=json, file_path=file_path)

    def store_html(self, html, file_path):
        self.__store_html_output(html=html, file_path=file_path)
