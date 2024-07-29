class Constants:
    # HTML Constants:
    IMG_TAG = 'img'
    LIST_TAG = 'li'
    MIN_HEADLINE_SIZE = 14
    MIN_SUB_HEADLINE_SIZE = 10
    MAX_JSON_LD_LENGTH = 20
    MAXIMUM_IMAGE_HEIGHT = 16000
    DELIMITERS = ['-', '_', '~']
    HEADLINE_TAGS = ['h1', 'h2', 'h3']
    SUB_HEADLINE_TAGS = ['h4', 'h5', 'h6']
    META_TAGS = ['br', 'p', 'div', 'tr', 'li']
    BLACKLISTED_TAGS = ['style', 'script', 'a', 'form', 'iframe', 'i', 'audio',
                        'button', 'input', 'keygen', 'select', 'textarea',
                        'hide']
    TEXT_TAGS = ['p', 'strong', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                 'font', 'div']
    FILTER_TAGS = ['displaynone', 'df-zoom-help', 'xans-product-relation']
    CAROUSELS = ['prdDetail', 'prdInfo', 'prdReview', 'prdQnA', 'prdRelated',
                 'xans-product-relation-slider-0']
    DEFAULT_CAROUSELS_TO_CONVERT = ['prdDetail', 'prdInfo']
    HTML_PARSER = 'html.parser'

    # JSON LD Template Constants:
    RICH_CONTENT_JSON_LD_START_TEMPLATE = '{\"@context\": {\"s\": ' + \
                                          '\"http://schema.org/\",\"g\": \"http://schema.googleapis.com/\"},' + \
                                          '\"@type\": \"g:Showcase\",\"g:showcaseBlock\": [{\"@type\": ' + \
                                          '\"g:ShowcaseFeatureSet\",\"s:itemListElement\": ['
    RICH_CONTENT_JSON_LD_END_TEMPLATE = ']}]}'
    HEADLINE_JSON_LD_TEMPLATE = '{{\"@type\": \"g:ShowcaseFeatureSet\",' + \
                                '\"s:headline\": \"{txt}\", \"s:itemListElement\": ['
    END_PREVIOUS_FEATURE_SET_TEMPLATE = ']},'
    SUB_HEADLINE_JSON_LD_TEMPLATE = '{{\"@type\": \"g:ShowcaseFeature\",' + \
                                    '\"s:headline\": \"{txt}\"}}'
    DESCRIPTION_JSON_LD_TEMPLATE = '{{\"@type\": \"g:ShowcaseFeature\",' + \
                                   '\"s:description\": \"{txt}\"}}'
    IMG_JSON_LD_TEMPLATE = '{{\"@type\": \"g:ShowcaseFeature\",\"s:image\": ' \
                           '\"{url}\"}}'

    # Default Output File Path Constants:
    DEFAULT_JSON_OUTPUT_FILE_PATH = 'output/result.json'
    DEFAULT_HTML_OUTPUT_FILE_PATH = 'output/result.html'
