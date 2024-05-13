import json
from abc import abstractmethod

from bs4 import BeautifulSoup

from Constants.constants import Constants
from Processor.processor import Processor
from Utility.sanitizer import JsonSanitizer


class HtmlConverter:
    converted_result = None
    json_result = None
    sanitized_json = None
    json_dumps = None

    def __init__(self, html_file, html_string, base_url, carousels):
        self.html_file = html_file
        self.html_string = html_string
        self.base_url = base_url
        self.carousels = carousels

    @abstractmethod
    def convert(self):
        pass

    def initiate_conversion(self):
        self.converted_result = FileHtmlConverter.convert(
            self) if self.html_file else StringHtmlConverter.convert(self)
        return self

    def load(self):
        self.json_result = json.loads(self.converted_result, strict=False)
        return self

    def sanitize(self):
        json_sanitizer = JsonSanitizer()
        self.sanitized_json = json_sanitizer.sanitize(self.json_result)
        return self

    def dump(self):
        self.json_dumps = json.dumps(self.sanitized_json, indent=4)
        return self

    def build_json_ld_result(self, converted_json_ld):
        json_output = Constants.RICH_CONTENT_JSON_LD_START_TEMPLATE + ''.join(
            converted_json_ld) + Constants.RICH_CONTENT_JSON_LD_END_TEMPLATE
        json_result = json_output.replace(',]', ']')
        return json_result


class FileHtmlConverter(HtmlConverter):

    def convert(self):
        converted_json_ld = []
        with open(self.html_file, 'r') as html_file:
            soup = BeautifulSoup(html_file, Constants.HTML_PARSER)
            for section in self.carousels:
                processor = Processor(soup, section, self.base_url,
                                      self.carousels)
                converted_json_ld.append(processor.process_section())
        return self.build_json_ld_result(converted_json_ld)


class StringHtmlConverter(HtmlConverter):

    def convert(self):
        converted_json_ld = []
        soup = BeautifulSoup(self.html_string, Constants.HTML_PARSER)
        for section in self.carousels:
            processor = Processor(soup, section, self.base_url, self.carousels)
            converted_json_ld.append(processor.process_section())
        return self.build_json_ld_result(converted_json_ld)
