from collections import defaultdict

from string_utils import get_uppercase_characters

# pylint: disable=too-few-public-methods
# Although this only contains one public method, this class is a good place for
# the equality checks and representation

class Section:

    def __init__(self, name="Unknown"):
        self.name = name
        self.short = get_uppercase_characters(name)


    def get_papers_in_section(self, papers):
        papers_in_section = []
        for paper in papers:
            if paper.section == self:
                papers_in_section.append(paper)
        return papers_in_section

    @staticmethod
    def gather_papers_by_section(papers):
        papers_by_section = defaultdict(list)
        for paper in papers:
            papers_by_section[paper.section].append(paper)
        return papers_by_section


    def __eq__(self, other):
        name_same = False
        short_same = False
        if self.name and other.name:
            name_same = self.name.lower() == other.name.lower()
        if self.short and other.short:
            short_same = self.short.lower() == other.short.lower()
        return name_same or short_same


    def __repr__(self):
        return "{} ({})".format(self.name, self.short)


    def __hash__(self):
        return hash("{}".format(self))
