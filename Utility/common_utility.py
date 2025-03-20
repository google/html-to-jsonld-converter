import os
import requests

from Constants.constants import Constants
from urllib.parse import urlparse, urljoin


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

    def is_image_url_valid(self, url):
        try:
            # Check if it's a valid URL
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False

            # Send a HEAD request to check the status without downloading the whole image
            response = requests.head(url, timeout=5)  # Set a timeout

            # Check for 200 OK status
            if response.status_code == 200:
                # Optionally check the content-type to confirm it's an image
                content_type = response.headers.get('content-type')
                if content_type and content_type.startswith('image/'):
                    return True
                else:
                    return False #It's 200, but not an image.

            else:
                return False

        except requests.exceptions.RequestException:
            # Handle connection errors, timeouts, etc.
            return False
        except ValueError: #invalid url parsing
            return False
        except Exception as e: #Catch any other exception
            print(f"An unexpected error occurred: {e}")
            return False
