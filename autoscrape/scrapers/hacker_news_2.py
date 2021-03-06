from autoscrape import base_scraper


class HackerNews2(base_scraper.Scraper):

    def __init__(self, session_id):
        base_scraper.Scraper.__init__(self, session_id)

    @staticmethod
    def description():
        return "Scrapes post titles from https://news.ycombinator.com/ (saves as semicolon-separated string)"

    def run(self):
        try:
            url = "https://news.ycombinator.com/"
            self.get(url)
            elements = self.find_elements_by_class_name('storylink')
            elements_text_list = [element.text for element in elements]
            elements_as_string = ';'.join(elements_text_list)
            self.save(
                'Post Titles', 
                url,
                elements_as_string)
        except Exception as e:
            self.log(e)
        self.destroy()
