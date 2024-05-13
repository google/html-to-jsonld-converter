from abc import abstractmethod
from urllib.parse import urlparse


class Sanitizer:

    @abstractmethod
    def sanitize(self, data):
        pass


class JsonSanitizer(Sanitizer):

    def sanitize(self, json):
        # Remove any empty fields and lists from the converted json.
        showcase_blocks = json['g:showcaseBlock']
        for showcase_block in showcase_blocks:
            if 's:headline' not in showcase_block and not \
                showcase_block['s:itemListElement']:
                showcase_blocks.remove(showcase_block)
            elif 's:itemListElement' in showcase_block and not \
                showcase_block['s:itemListElement']:
                del showcase_block['s:itemListElement']
        return json


class ArgsSanitizer(Sanitizer):

    def sanitize(self, args):
        args['base_url'] = str(urlparse(args['url']).scheme) + '://' + str(
            urlparse(args['url']).netloc)
        del args['url']
        return args
