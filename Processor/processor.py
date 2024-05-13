from urllib.parse import urljoin

from bs4 import Comment

from Constants.constants import Constants
from Utility.headline_utility import HeadlineUtility
from Utility.html_section_cleaner import HtmlSectionCleaner


class Processor:

    def __init__(self, soup, section, base_url, carousels):
        self.soup = soup
        self.section = section
        self.base_url = base_url
        self.carousels = carousels
        self.body = ''
        self.curr_text = ''
        self.is_curr_tag_headline = False
        self.is_curr_tag_sub_headline = False

    def __process_image_tag(self, tag):
        # If tag belongs to image tag, extract the source, add baseurl to it and
        # convert it to json ld
        src = None
        if tag.has_attr('src'):
            src = tag['src']
        else:
            if tag.has_attr('ec-data-src'):
                src = tag['ec-data-src']
        if src:
            self.body += Constants.IMG_JSON_LD_TEMPLATE \
                             .format(url=urljoin(self.base_url, src)) + ','

    def __process_list_tag(self, tag):
        # If tag belongs to list tag, extract the list text and additionally
        # check if there's a repetition due to parsing multiline breaks in html.
        li_text_set = set()
        li_text_list = []
        for text in tag.findAll(string=True, recursive=False):
            if text.strip() and not isinstance(text, Comment):
                text = tag.text
                text = text.replace('"', r'\"')
                stripped_text = text.strip()
                if stripped_text not in li_text_set:
                    li_text_list.append(stripped_text)
                    li_text_set.add(stripped_text)
        self.curr_text = ''.join(li_text_list)

    def __process_text_tag(self, tag):
        # If tag belongs to text tag, extract the text and additionally check
        # if it belongs to headline or sub-headline.
        for text in tag.findAll(string=True, recursive=False):
            if text.strip() and not isinstance(text, Comment):
                text = text.replace('"', r'\"')
                self.curr_text += text.strip() + ' '
                if HeadlineUtility().is_headline(tag):
                    self.is_curr_tag_headline = True
                elif HeadlineUtility().is_sub_headline(tag):
                    self.is_curr_tag_sub_headline = True

    def __process_meta_tag(self):
        # If tag belongs to meta tag, convert all the text contents (viz.
        # headline, sub-headline, description and list text) to json ld.
        self.curr_text = self.curr_text.strip()
        if self.curr_text:
            if self.is_curr_tag_headline:
                self.body += Constants.END_PREVIOUS_FEATURE_SET_TEMPLATE \
                             + Constants.HEADLINE_JSON_LD_TEMPLATE.format(
                    txt=self.curr_text)
            elif self.is_curr_tag_sub_headline:
                self.body += Constants.SUB_HEADLINE_JSON_LD_TEMPLATE \
                                 .format(txt=self.curr_text) + ','
            else:
                self.body += Constants.DESCRIPTION_JSON_LD_TEMPLATE \
                                 .format(txt=self.curr_text) + ','

    def process_section(self):
        detail = self.soup.find(id=self.section)
        if not detail:
            return self.body

        cleaner = HtmlSectionCleaner(self.soup, self.section)
        cleaner.clean()
        for tag in detail.findChildren(recursive=True):
            # Corner cases to remove unrelated product carousels.
            unrelated_carousels = list(
                set(Constants.CAROUSELS) - set(self.carousels))
            if tag.attrs and 'id' in tag.attrs and tag.attrs[
                'id'] in unrelated_carousels:
                tag.decompose()
                continue

            if tag.name == Constants.IMG_TAG:
                self.__process_image_tag(tag)

            elif tag.name == Constants.LIST_TAG:
                self.__process_list_tag(tag)

            elif tag.name in Constants.TEXT_TAGS:
                if tag.parent and tag.parent.name == Constants.LIST_TAG:
                    continue
                self.__process_text_tag(tag)

            if tag.name in Constants.META_TAGS:
                self.__process_meta_tag()
                self.curr_text = ''
                self.is_curr_tag_headline = False
                self.is_curr_tag_sub_headline = False

        return self.body
