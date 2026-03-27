###############################################################################
###############################################################################
#                           File: ReportProcessing                            #
#                             Author: Joshua Male                             #
#             Description: Helper functions for report processing             #
#                         Project: Fantasy F1 League                          #
#                              Date: 27/03/2026                               #
#                     Copyright © Joshua Male & Phil Male                     #
###############################################################################
###############################################################################

# Imports
import InitializeReports  # noqa

import re
import sys
import base64
import logging
import argparse
import ReportUtils.ReportGenerator as gen

from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup, Tag

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def convertnotebook(notebook_path: Path,
                    date_str: str = None,
                    title: str = None,
                    tags: list[str] = None,
                    authors: list[str] = None,
                    cover_image: Path = None,
                    output_directory: Path = ".",
                    dry_run: bool = False) -> None:
    """
    Function Details
    ================
    """
    # Set defaults for mutable types
    tags = tags or ['f1', 'race-report']
    authors = authors or ['aatapex']

    html_path = Path(notebook_path)
    if not html_path.exists():
        raise FileNotFoundError(f'Error: {html_path} not found')

    slug = gen.slugify(name=html_path.stem)
    post_date = date_str or date.today().isoformat()
    title = title or slug.replace('-', ' ').title()

    bundle_name = f'{post_date}-{slug}'
    bundle_dir = Path(output_directory, bundle_name)

    logger.info(f'Input: {html_path}\nBundle Directory: {bundle_dir}')

    if not dry_run:
        bundle_dir.mkdir(parents=True, exist_ok=True)

    markdown_content, image_count, first_image = gen.process_jupyternotebook(
        html_path=html_path,
        slug=slug,
        bundle_dir=bundle_dir,
        dry_run=dry_run
    )

    cover = cover_image or first_image or ''

    if dry_run:
        logger.info(f'[dry-run] No files written')
        return

    front_matter = gen._build_front_matter(
        title=title,
        post_date=post_date,
        slug=slug,
        tags=tags,
        authors=authors,
        cover=cover
    )

    index_path = Path(bundle_dir, 'index.md')
    index_path.write_text(
        data=front_matter + markdown_content,
        encoding='utf-8'
    )
    logger.info(f'Done. Bundle ready at: {bundle_dir}')
    return bundle_dir


if __name__ == '__main__':
    root = Path().absolute()
    notebook_dir = Path(root, 'Reports', '2026')
    convertnotebook(
        notebook_path=Path(notebook_dir, '2026_Australia.html'),
        title='Australia',
        tags=['Fantasy Report', 'F1']
    )
