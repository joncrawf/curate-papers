from string_utils import get_uppercase_characters

class PaperParser():

    def __init__(self, paper_checks):
        self.paper_checks = paper_checks


    @staticmethod
    def fuzzy_paper_name_match(paper_name, searched_names,
                               fuzzy_paper_name_match_percent):
        for searched_name in searched_names.split(';'):
            paper_name_words = [x.lower().replace(':', '') for x in paper_name.split(' ')]
            searched_name_words = [x.lower().replace(':', '') for x in searched_name.split(' ')]
            percent_match = 2.0 * len(set(paper_name_words) & set(searched_name_words)) \
                            / (len(paper_name_words) + len(searched_name_words)) \
                            > fuzzy_paper_name_match_percent

            acronym_match = False
            if len(searched_name_words) == 1:
                paper_name_acronym = get_uppercase_characters(paper_name)
                acronym_match = searched_name == paper_name_acronym

            if percent_match or acronym_match:
                return True
        return False


    @staticmethod
    def check_tags(paper_tags, searched_tags):
        return set(searched_tags.split(';')).issubset(paper_tags)


    def parse_papers(self, papers):
        for option, check in self.paper_checks.items():
            if option:
                papers = [paper for paper in papers
                          if check(paper, option)]
        return papers
