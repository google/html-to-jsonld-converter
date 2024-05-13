class PreviewHtmlOfJsonLd:

    def __preview_headline(self, headline_text):
        return '<p style="text-align:center;font-family:Roboto;margin:12px' \
               ';font-size:18px;font-weight:700;" >{text}</p>' \
            .format(text=headline_text)

    def __preview_sub_headline(self, sub_headline_text):
        return '<p style="text-align:center;font-family:Roboto;margin:12px' \
               ';font-size:15px;font-weight:650;" >{text}</p>' \
            .format(text=sub_headline_text)

    def __preview_description(self, description_text):
        return '<p style=\"text-align:center;font-family:Roboto;margin:12px' \
               ';font-size:12px;font-weight:400;\">{text}</p>' \
            .format(text=description_text)

    def __preview_image(self, image_text):
        return '<img style=\"display:block;width:100%;margin:12px;\" src=\"{' \
               'src}\"/>'.format(src=image_text)

    def preview(self, json):
        html = []
        for showcaseBlock in json['g:showcaseBlock']:
            if 's:headline' in showcaseBlock and showcaseBlock['s:headline']:
                html.append(self.__preview_headline(headline_text=
                                                    showcaseBlock[
                                                        's:headline']))

            if 's:itemListElement' not in showcaseBlock or not \
                showcaseBlock['s:itemListElement']:
                continue

            for item in showcaseBlock['s:itemListElement']:
                # Prepare html for headline tag.
                if 's:headline' in item and item['s:headline']:
                    html.append(self.__preview_sub_headline(sub_headline_text=
                                                            item['s:headline']))

                # Prepare html for description tag.
                elif 's:description' in item and item['s:description']:
                    html.append(self.__preview_description(description_text=
                                                           item[
                                                               's:description']))

                # Prepare html for image tag.
                elif 's:image' in item and item['s:image']:
                    html.append(
                        self.__preview_image(image_text=item['s:image']))

        final_html = ''.join(html)
        return final_html
