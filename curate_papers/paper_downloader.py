import glob
import os
import requests
import scholarly

from string_utils import green, red, orange


class PaperDownloader:

    @staticmethod
    def download(paper):
        if PaperDownloader.is_downloaded(paper.filename):
            PaperDownloader.print_status(orange("Already downloaded"), paper)
        else:
            PaperDownloader.download_file(paper.pdf_url, paper.filename, paper)


    @staticmethod
    def download_file(url, filename, paper):
        PaperDownloader.print_status(green("Downloading"),
                                     paper.short(), flush=True)

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        try:
            with open(filename, 'wb') as file:
                response = requests.get(url)
                file.write(response.content)
            PaperDownloader.print_status(green("Downloaded"), paper)

        except (requests.exceptions.RequestException, requests.HTTPError):
            PaperDownloader.print_status(red("Failed to download"),
                                         paper.short())
            os.remove(filename)


    @staticmethod
    def print_status(status_message, paper, flush=False):
        if flush:
            print("{0}: {1}".format(status_message, paper), flush=flush, end='\r')
        else:
            print("{0}: {1}".format(status_message, paper))


    @staticmethod
    def is_downloaded(filename):
        return len(glob.glob(filename)) > 0


    @staticmethod
    def get_paper_bibtex(paper):
        if not PaperDownloader.is_downloaded(paper.bibtex_filename):
            try:
                pub_search = scholarly.search_pubs_query(paper.title)
                pub = next(pub_search)
            except Exception:
                PaperDownloader.print_status(red("Unable to download bibtex"),
                                             paper.short())
                return

            PaperDownloader.download_file(pub.url_scholarbib, paper.bibtex_filename, paper)
        try:
            with open(paper.bibtex_filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            PaperDownloader.print_status(red("Unable to show bibtex"),
                                         paper.short())
