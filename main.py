import argparse

from Constants.constants import Constants
from Converter.html_converter import HtmlConverter
from Utility.common_utility import CommonUtility
from Utility.preview_html_of_json_ld import PreviewHtmlOfJsonLd
from Utility.sanitizer import ArgsSanitizer


def main(html_file, html_string, base_url, carousels, output_json_ld_file_path,
    output_html_file_path, *_):
    converter = HtmlConverter(html_file, html_string, base_url, carousels) \
        .initiate_conversion() \
        .load() \
        .sanitize() \
        .dump()

    CommonUtility().store_json_ld(json=converter.json_dumps,
                                  file_path=output_json_ld_file_path)

    CommonUtility().store_html(
        html=PreviewHtmlOfJsonLd().preview(json=converter.sanitized_json),
        file_path=output_html_file_path)

    CommonUtility.validate_file_length(json=converter.json_dumps)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL of the product page.')
    parser.add_argument('-f', '--html_file',
                        help='Path for the html file that needs to be converted.')
    parser.add_argument('-s', '--html_string',
                        help='Html string that needs to be converted.')
    parser.add_argument('-c', '--carousels',
                        help='[Optional] Comma separated carousels that need to be converted.',
                        type=CommonUtility.list_of_strings,
                        default=Constants.DEFAULT_CAROUSELS_TO_CONVERT)
    parser.add_argument('-j', '--output_json_ld_file_path',
                        help='Relative file path for stroing json ld result',
                        default=Constants.DEFAULT_JSON_OUTPUT_FILE_PATH)
    parser.add_argument('-p', '--output_html_file_path',
                        help='Relative file path for stroing html preview result',
                        default=Constants.DEFAULT_HTML_OUTPUT_FILE_PATH)
    args = vars(parser.parse_args())
    CommonUtility.validate_args(args=args)
    main(**ArgsSanitizer().sanitize(args=args))
