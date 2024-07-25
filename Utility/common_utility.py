import os
import requests
import urllib.parse

from Constants.constants import Constants

from PIL import Image

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

    @staticmethod
    def is_url(url):
        return urllib.parse.urlparse(url).scheme == "https"

    @staticmethod
    def read_image(url):
        path = urllib.parse.urlparse(url).path
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        return Image.open(response.raw), os.path.splitext(path)[1]


