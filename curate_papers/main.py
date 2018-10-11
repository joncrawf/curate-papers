# Inspired by the work of @terryum https://github.com/terryum/awesome-deep-learning-papers

import argparse
import yaml

from paper_downloader import PaperDownloader
from paper_parser import PaperParser
from string_utils import red
from file_parser import FileParser
from section import Section

try:
    with open("config.yml", 'r') as file:
        CONFIG = yaml.load(file)
        REGEXES = CONFIG.get('regexes')
        PAPER_REGEXES = REGEXES.get('note')
        SECTION_REGEXES = REGEXES.get('section')
        FUZZY_PAPER_NAME_MATCH_PERCENT = CONFIG.get('fuzzy_search').get('paper_name', 0.7)
        OVERVIEW_FILE = CONFIG.get('overview', 'README.md')
        BIBFILE = CONFIG.get('bibfile', 'papers.bib')
except:
    import os
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, '../config.yml.defaults')
    with open(CONFIG_PATH, 'r') as file:
        CONFIG = yaml.load(file)
        REGEXES = CONFIG.get('regexes')
        PAPER_REGEXES = REGEXES.get('note')
        SECTION_REGEXES = REGEXES.get('section')
        FUZZY_PAPER_NAME_MATCH_PERCENT = CONFIG.get('fuzzy_search').get('paper_name', 0.7)
        OVERVIEW_FILE = CONFIG.get('overview', 'README.md')
        BIBFILE = CONFIG.get('bibfile', 'papers.bib')
    pass


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--section",
                        action="store", type=str, dest="section",
                        help='Choose papers by section.', default=None)
    parser.add_argument("-p", "--papers",
                        action="store", type=str, dest="papers",
                        help='Choose papers by paper title.', default=None)
    parser.add_argument("-t", "--tags",
                        action="store", type=str, dest="tags",
                        help='Choose papers by tag.', default=None)
    parser.add_argument("-c", "--changed",
                        action="store_true", dest="changed",
                        help='The papers that have changed.')
    parser.add_argument("-d", "--download",
                        action="store_true", dest="download",
                        help='Downloads the particular papers selected.')
    parser.add_argument("-r", "--read",
                        action="store_true", dest="to_read",
                        help='Shows the papers to read.')
    parser.add_argument("-b", "--bibtex",
                        action="store_true", dest="bibtex",
                        help='Shows the bibtex entry for the paper.')
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()
    file_parser = FileParser(SECTION_REGEXES, PAPER_REGEXES)
    papers, sections = file_parser.parse_file(OVERVIEW_FILE)

    paper_checks = {
        options.section:  lambda paper, option: paper.section == Section(option),
        options.papers:   lambda paper, option:
                          PaperParser.fuzzy_paper_name_match(paper.title, option,
                                                             FUZZY_PAPER_NAME_MATCH_PERCENT),
        options.changed:  lambda paper, option: paper.changed,
        options.tags:     lambda paper, option: PaperParser.check_tags(paper.tags, option),
        options.to_read:  lambda paper, option: not paper.is_read
    }
    papers = PaperParser(paper_checks).parse_papers(papers)

    if not papers:
        print(red("No papers match your search!"))
        return

    if options.download:
        for paper in papers:
            try:
                PaperDownloader.download(paper)
            except KeyboardInterrupt:
                print(red("Stopped download!"))
    elif options.bibtex:
        with open(BIBFILE, 'w') as file:
            for paper in papers:
                print('- {}'.format(paper))
                bibtex = PaperDownloader.get_paper_bibtex(paper)
                if bibtex:
                    file.write(bibtex)
    else:
        if options.section or options.papers or options.changed or options.to_read or options.tags:
            papers_by_section = Section.gather_papers_by_section(papers)
            for section in papers_by_section.keys():
                print('{}\n{}'.format(section,
                                      '\n'.join(['- {}'.format(paper)
                                                 for paper in papers_by_section[section]])))
        else:
            for section in sections:
                print("{} ({} papers)".format(section,
                                              len(section.get_papers_in_section(papers))))

        print("\nTags: [{}]".format(";".join(sorted(list(set([tag for paper in papers
                                                              for tag in paper.tags]))))))


if __name__ == "__main__":
    main()
