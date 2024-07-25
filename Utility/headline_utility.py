from Constants.constants import Constants


class HeadlineUtility:

    def __get_font_size(self, style):
        return float(style.split('font-size:')[1].split(';')[0].strip()[:-2])

    def __is_sub_headline_class(self, tag):
        for tag_class in tag['class']:
            for delimiter in Constants.DELIMITERS:
                if tag_class.find(f'sub{delimiter}title') > 0:
                    return True
        return False

    def __check_headline_by_size(self, size, min_size, max_size):
        if min_size <= size < max_size:
            return True
        else:
            return False

    def __is_headline_class(self, tag):
        for tag_class in tag['class']:
            if tag_class.find('title') > 0:
                for delimiter in Constants.DELIMITERS:
                    if tag_class.find(f'sub{delimiter}title') > 0:
                        return False
                return True
        return False

    def __is_headline(self, tag, is_parent=False):
        # Check if current tag is headline if it's in headline tags.
        if not is_parent and (tag.name in Constants.HEADLINE_TAGS
                              or (tag.has_attr('class')
                                  and self.__is_headline_class(tag))):
            return True

        # Check if current tag is headline by comparing size.
        if tag.has_attr('style') and tag['style']:
            style = tag['style']
            if 'font-size' in style:
                return self.__check_headline_by_size(
                    size=self.__get_font_size(style),
                    min_size=Constants.MIN_HEADLINE_SIZE, max_size=float('inf'))
        return None

    def is_headline(self, tag):
        # Check if current tag is headline.
        if self.__is_headline(tag):
            return True

        # Check if parent tag is a headline tag.
        for sub_tag in tag.parents:
            is_headline_result = self.__is_headline(sub_tag,
                                                    is_parent=True)
            if is_headline_result is not None:
                return is_headline_result
        return False

    def is_sub_headline(self, tag):
        # Check if current tag is headline.
        if tag.name in Constants.SUB_HEADLINE_TAGS:
            return True

        # Check if single line with strong tag exists.
        # Ref: https://beautiful-soup-4.readthedocs.io/en/latest/#going-up
        if tag.name == 'strong' and len(tag.parent) == 1:
            return True

        # Check if tag class is subtitle.
        if tag.has_attr('class') and self.__is_sub_headline_class(tag):
            return True

        # Check if current tag is sub headline by comparing size.
        if tag.has_attr('style') and tag['style']:
            style = tag['style']
            if 'font-size' in style:
                return self.__check_headline_by_size(
                    size=self.__get_font_size(style),
                    min_size=Constants.MIN_SUB_HEADLINE_SIZE,
                    max_size=Constants.MIN_HEADLINE_SIZE)
        return False
