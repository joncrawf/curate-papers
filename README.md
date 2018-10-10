## curate-papers

A tool for the curation of papers, and their associated notes. This will provide
a means for notes about the papers to be easily stored, and for papers to be
associated with each other.

## Intended usage

- List papers (need to read/already read/discussion topics).
  - Provide a means of grouping/tagging papers to form associations across paper
    types.
- Provide a place for notes to be linked with the papers.
- Allow for easy collection of bibtex entries for use in further citations.

## Current usage

```

usage: main.py [-h] [-s SECTION] [-p PAPERS] [-t TAGS] [-c] [-d] [-r] [-b]

optional arguments:
  -h, --help            show this help message and exit
  -s SECTION, --section SECTION
                        Choose papers by section.
  -p PAPERS, --papers PAPERS
                        Choose papers by paper title.
  -t TAGS, --tags TAGS  Choose papers by tag.
  -c, --changed         The papers that have changed.
  -d, --download        Downloads the particular papers selected.
  -r, --read            Shows the papers to read.
  -b, --bibtex          Shows the bibtex entry for the paper.

```

## Suggestions

If you have any suggestions over the features you would like to see in this
tool, or find any bugs within the code, please submit an issue.
