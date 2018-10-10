import re
import codecs
import git
from git import Repo

from paper import Paper
from section import Section


class FileParser:

    def __init__(self, section_regexes, paper_regexes):
        self.section_regexes = section_regexes
        self.paper_regexes = paper_regexes


    @staticmethod
    def check_all_regexes(regexes, line):
        for regex in regexes:
            result = re.search(regex, line)
            if result:
                return result


    def get_changed_papers_titles(self):
        try:
            repo = Repo('.')
            changed_papers_titles = []
            for file in repo.git.diff(repo.head.commit.tree).splitlines():
                if re.match(r"^\+-", file):
                    result = FileParser.check_all_regexes(self.paper_regexes, file[1:])
                    if result:
                        changed_papers_titles.append(result.groups()[1])
            return changed_papers_titles
        except git.InvalidGitRepositoryError:
            return []


    @staticmethod
    def is_read(reading_tag):
        if reading_tag.isspace():
            return False
        return True


    def parse_file(self, filename):
        with codecs.open(filename, encoding='utf-8', mode='r',
                         buffering=1, errors='strict') as file:

            sections = []
            papers = []
            changed_papers_titles = self.get_changed_papers_titles()
            current_section = None

            for line in file.read().splitlines():
                section_details = FileParser.check_all_regexes(self.section_regexes, line)
                if section_details:
                    section_details_dict = section_details.groupdict()
                    current_section = Section(section_details_dict['name'])
                    sections.append(current_section)
                else:
                    details = FileParser.check_all_regexes(self.paper_regexes, line)
                    if details:
                        paper_details = details.groupdict()
                        paper_title = paper_details['title']
                        papers.append(Paper({
                            'title':      paper_title,
                            'publisher':  paper_details['publisher'],
                            'url':        paper_details['url'],
                            'section':    current_section,
                            'notes_path': paper_details.get('notes_path'),
                            'changed':    paper_title in changed_papers_titles,
                            'is_read':    FileParser.is_read(paper_details['read']),
                            'tags':       paper_details.get('tags')}))

        return papers, sections
