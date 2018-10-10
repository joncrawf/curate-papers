import os

from paper_downloader import PaperDownloader
from section import Section
from string_utils import orange, sanitise_string

PAPERS_DIRECTORY = 'papers'
BIBTEX_DIRECTORY = 'bibtex'

# pylint: disable=too-many-instance-attributes
# These attributes should be set here (possibly should add accessors for
# the attribtues needed, but this is okay for now

class Paper:

    PUBLISHER_PDF_CONVERTERS = {
        'arxiv':      lambda url: url.replace('abs', 'pdf'),
        'openreview': lambda url: url.replace('forum', 'pdf')
    }

    def __init__(self, info):
        self.title = info.get('title', '').strip()
        self.publisher = info.get('publisher', 'pdf')
        self.url = info.get('url', '')
        self.pdf_url = Paper.get_pdf_url_from_url(self.url, self.publisher)
        self.section = info.get('section', Section())
        self.filename = Paper.get_filename_from_title(self.title,
                                                      self.section.name,
                                                      PAPERS_DIRECTORY,
                                                      'pdf')
        self.bibtex_filename = Paper.get_filename_from_title(self.title,
                                                             self.section.name,
                                                             BIBTEX_DIRECTORY,
                                                             'bib')
        self.notes_path = info.get('notes_path')
        self.changed = info.get('changed', False)
        self.is_read = info.get('is_read', False)
        self.tags = info.get('tags')
        if self.tags:
            self.tags = self.tags.split(';')

    @staticmethod
    def get_filename_from_title(title, section_name, folder, filetype):
        sanitised_filename = sanitise_string(title)
        sanitised_section = sanitise_string(section_name)
        return os.path.join(folder, sanitised_section,
                            "{}.{}".format(sanitised_filename, filetype))

    @staticmethod
    def get_pdf_url_from_url(url, publisher):
        publisher = publisher.lower().strip()
        if publisher in Paper.PUBLISHER_PDF_CONVERTERS:
            url = Paper.PUBLISHER_PDF_CONVERTERS[publisher](url)
        return url


    def short(self):
        return "{} [[{}]({})]".format(self.title, self.publisher, self.url)


    def __repr__(self):
        if self.notes_path:
            output = "[{}]({})".format(self.title, self.notes_path)
        else:
            output = self.title

        output = "{} [[{}]({})]".format(output, self.publisher, self.pdf_url)

        if PaperDownloader.is_downloaded(self.filename):
            output = "{} ~> {}".format(output, self.filename)
        if self.tags:
            output = "{} [{}]".format(output, ";".join(self.tags))
        if not PaperDownloader.is_downloaded(self.filename):
            output = "{} {}".format(output, orange("[to download]"))
        if self.changed:
            output = "{} {}".format(output, orange("[changed]"))
        if not self.is_read:
            output = "{} {}".format(output, orange("[to read]"))

        return output
