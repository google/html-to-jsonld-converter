from Constants.constants import Constants


class HtmlSectionCleaner:

    def __init__(self, soup, section):
        self.soup = soup
        self.section = section

    def clean(self):
        detail = self.soup.find(id=self.section)
        if detail:
            # Filter tags which are marked as do not display.
            for tag in Constants.FILTER_TAGS:
                for child in detail.findChildren(class_=tag):
                    child.decompose()

            # Filter blacklisted tags.
            for tag in detail(Constants.BLACKLISTED_TAGS):
                tag.decompose()
