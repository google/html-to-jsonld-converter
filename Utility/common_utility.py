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
        # To avoid `requests.exceptions.HTTPError: 403 Client Error: Forbidden`.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return Image.open(response.raw)

    @staticmethod
    def suffix_url(url, suffix):
        """Inserts '-resize' into a URL before the file extension."""

        parsed_url = urllib.parse.urlparse(url)

        # Handle cases where there might be query parameters or fragments
        path_parts = parsed_url.path.rsplit(".", 1)  # Split only on the last "."
        if len(path_parts) == 2:
            new_path = f"{path_parts[0]}-{suffix}.{path_parts[1]}"
        else:
            # If no extension, simply append to the end
            new_path = parsed_url.path + "-" + suffix

            # Reconstruct the URL with the modified path
        return parsed_url._replace(path=new_path).geturl()

    @staticmethod
    def resize_long_image(url):
        img = CommonUtility.read_image(url)
        width, height = img.size
        aspect_ratio = width/height
        if height > Constants.MAXIMUM_IMAGE_HEIGHT:
            resized_img = img.resize((int(aspect_ratio*Constants.MAXIMUM_IMAGE_HEIGHT), Constants.MAXIMUM_IMAGE_HEIGHT), resample=Image.Resampling.NEAREST)
            resized_url = CommonUtility.suffix_url(url, "resize")
            # host this image with new url, feel free to use `resized_url`
            #resized_img.save(resized_url)
            return resized_url
        return url