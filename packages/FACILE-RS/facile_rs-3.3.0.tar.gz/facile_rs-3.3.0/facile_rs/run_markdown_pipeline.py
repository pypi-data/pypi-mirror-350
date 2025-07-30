#!/usr/bin/env python3

"""Copy the content of Markdown files to a Grav CMS repository.

Description
-----------

This script copies the content of markdown files in the PIPELINE_SOURCE to a Grav CMS repository given by GRAV_PATH.
The Grav repository is created by the Git-Sync Plugin.

The pages need to be already existing in Grav and contain a ``pipeline`` and a ``source`` field in their frontmatter.
The script will find all pages which match the provided PIPELINE and will overwrite content part of the page with the
markdown file given by source.
If source is ``codemeta.json``, the content will be added to the frontmatter entry ``codemeta`` rather than overwriting
the page content.
Twig templates digesting the metadata can be found in the file ``Twig_templates.md`` in this directory.
After running the script, the changes to the Grav CMS repository can be committed and pushed, and the Git-Sync Plugin
will update the public pages.
See openCARP citation info or code of conduct for examples.

Usage
-----

.. argparse::
    :module: facile_rs.run_markdown_pipeline
    :func: create_parser
    :prog: run_markdown_pipeline.py

"""
import json
import logging
from pathlib import Path

import frontmatter
import yaml

from .utils import cli
from .utils.grav import collect_pages

logger = logging.getLogger(__file__)


def create_parser(add_help=True):
    parser = cli.Parser(add_help=add_help)

    parser.add_argument('--grav-path', dest='GRAV_PATH', required=True,
                        help='Path to the grav repository directory.')
    parser.add_argument('--pipeline', dest='PIPELINE', required=True,
                        help='Name of the pipeline as specified in the GRAV metadata.')
    parser.add_argument('--pipeline-source', dest='PIPELINE_SOURCE', required=True,
                        help='Path to the source directory for the pipeline.')
    parser.add_argument('--log-level', dest='LOG_LEVEL', default='WARN',
                        help='Log level (ERROR, WARN, INFO, or DEBUG)')
    parser.add_argument('--log-file', dest='LOG_FILE',
                        help='Path to the log file')
    return parser


def main(args):
    # loop over the tagged pages and write the content into the files
    for page_path, page, source in collect_pages(args.GRAV_PATH, args.PIPELINE):
        source_path = Path(args.PIPELINE_SOURCE).expanduser() / source

        # read the source file
        if source_path.suffix in ['.json']:
            data = json.loads(source_path.read_text())
            if source_path.name == 'codemeta.json':
                page.metadata['codemeta'] = data
            else:
                page.metadata['items'] = data
        elif source_path.suffix in ['.yml', '.yaml']:
            page.metadata['items'] = yaml.safe_load(source_path.read_text())
        else:
            page.content = source_path.read_text()

        # write the page file
        logger.info('writing content to %s', page_path)
        page_path.write_text(frontmatter.dumps(page))


def main_deprecated():
    cli.main_deprecated(__name__)


if __name__ == "__main__":
    main_deprecated()
