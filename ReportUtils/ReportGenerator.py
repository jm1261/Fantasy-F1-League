###############################################################################
###############################################################################
#                            File: ReportGenerator                            #
#                             Author: Joshua Male                             #
#             Description: Helper functions for report generation             #
#                         Project: Fantasy F1 League                          #
#                              Date: 27/03/2026                               #
#                     Copyright © Joshua Male & Phil Male                     #
###############################################################################
###############################################################################

# Imports
import re
import base64
import logging

from pathlib import Path
from bs4 import BeautifulSoup, Tag

# Logging Parameters
logger = logging.getLogger(name=Path(__file__).stem)


def slugify(name: str) -> str:
    """
    Function Details
    ================
    Generate a slug from a name string, removing special characters and spaces.

    Parameters
    ----------
    name: str
        The name string to be slugified.

    Returns
    -------
    slug: str
        The slugified version of the name string.

    ---------------------------------------------------------------------------
    Update History
    ==============

    27/03/2026
    ----------
    - Initial function created.

    """
    slug = name.lower()
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug


def element_to_markdown(element: Tag) -> str:
    """
    Function Details
    ================
    Convert a BeautifulSoup Tag element to a Markdown string.

    Parameters
    ----------
    element: Tag
        The BeautifulSoup Tag element to be converted.

    Returns
    -------
    markdown: str
        The Markdown string representation of the Tag element.

    ---------------------------------------------------------------------------
    Update History
    ==============

    27/03/2026
    ----------
    - Initial function created.

    """
    if isinstance(element, str):
        return element

    tag = element.name if isinstance(element, Tag) else None

    if tag is None:
        return element.string or ""

    def clean_text(mode: Tag) -> str:
        """
        Function Details
        ================
        Remove anchor links from a BeautifulSoup Tag and return cleaned text.

        Parameters
        ----------
        mode: Tag
            The BeautifulSoup Tag from which to remove anchor links.

        Returns
        -------
        cleaned_text: str
            The text of the Tag with anchor links removed.

        -----------------------------------------------------------------------
        Update History
        ==============

        27/03/2026
        ----------
        - Initial function created.

        """
        for a in mode.find_all('a', class_='anchor-link'):
            a.decompose()
        return mode.get_text()

    if tag == 'h1':
        return ""

    if tag in ('h2', 'h3', 'h4', 'h5', 'h6'):
        return f"{'#' * int(tag[1])} {clean_text(element).strip()}\n\n"

    if tag == 'p':
        return (
            f"{''.join(element_to_markdown(c) for c in element.children)}"
            f".strip()\n\n"
        )

    if tag in ('strong', 'b'):
        return f"**{element.get_text()}**"

    if tag in ('em', 'i'):
        return f"*{element.get_text()}*"

    if tag == 'code':
        return f"`{element.get_text()}`"

    if tag == 'a':
        href = element.get('href', '')
        text = element.get_text()
        return text if href.startswith('#') else f"[{text}]({href})"

    if tag in ('ul', 'ol'):
        items = []
        for i, li in enumerate(element.find_all('li', recursive=False)):
            content = "".join(
                element_to_markdown(c) for c in li.children
            ).strip()
            items.append(
                f"{i + 1}. {content}" if tag == 'ol' else f"- {content}"
            )
        return "\n".join(items) + "\n\n"

    if tag == 'li':
        return "".join(
            element_to_markdown(c) for c in element.children
        ).strip()

    if tag == 'table':
        return table_to_markdown(table=element)

    if tag == 'br':
        return "  \n"

    if tag == 'hr':
        return "---\n\n"

    if tag == 'blockquote':
        inner = "".join(
            element_to_markdown(c) for c in element.children
        ).strip()
        return "\n".join(f"> {line}" for line in inner.splitlines()) + "\n\n"

    if tag == 'pre':
        code = element.find('code')
        content = code.get_text() if code else element.get_text()
        return f"```\n{content}\n```\n\n"

    return "".join(element_to_markdown(c) for c in element.children)


def table_to_markdown(table: Tag) -> str:
    """
    Function Details
    ================
    Convert a BeautifulSoup Tag representing an HTML table into a Markdown
    table string.

    Parameters
    ----------
    table: Tag
        The BeautifulSoup Tag representing the HTML table to be converted.

    Returns
    -------
    markdown_table: str
        The Markdown string representation of the HTML table.

    ---------------------------------------------------------------------------
    Update History
    ==============

    27/03/2026
    ----------
    - Initial function created.

    """
    rows = table.find_all('tr')
    if not rows:
        return ""
    lines = []
    for i, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])
        lines.append(
            "| " + " | ".join(c.get_text(strip=True) for c in cells) + " |"
        )
        if i == 0:
            lines.append("| " + " | ".join("---" for _ in cells) + " |")
    return "\n".join(lines) + "\n\n"


def process_jupyternotebook(html_path: Path,
                            slug: str,
                            bundle_dir: Path,
                            dry_run: bool) -> tuple[str, int, str | None]:
    """
    Function Details
    ================
    Parse a Jupyter Notebook HTML file, extract markdown content and images.

    Parameters
    ----------
    html_path: Path
        The file path to the Jupyter Notebook HTML file to be processed.
    slug: str
        A slug string to be used for naming extracted images.
    bundle_dir: Path
        The directory path where extracted images should be saved.
    dry_run: bool
        A boolean flag indicating whether to perform a dry run (no file
        writing).

    Returns
    -------
    markdown_content: str
        The extracted markdown content from the Jupyter Notebook.
    image_count: int
        The number of images extracted from the Jupyter Notebook.
    first_image_filename_or_None: str | None
        The filename of the first extracted image, or None if no images were
        extracted.

    ---------------------------------------------------------------------------
    Update History
    ==============

    27/03/2026
    ----------
    - Initial function created.

    """
    html = html_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    image_counter = [0]
    first_image = None
    parts = []

    for cell in soup.find_all('div', class_='jp-Cell'):
        classes = cell.get('class', [])

        if 'jp-MarkdownCell' in classes:
            output_div = cell.find('div', class_='jp-MarkdownOutput')
            if output_div:
                for child in output_div.children:
                    if isinstance(child, Tag):
                        parts.append(element_to_markdown(element=child))

        elif 'jp-CodeCell' in classes:
            for img in cell.find_all('img'):
                src = img.get('src', '')

                if not src.startswith('data:image/'):
                    continue

                try:
                    meta, b64data = src.split(',', 1)
                    ext = meta.split(':')[1].split(';')[0].split('/')[1]
                    if ext == 'jpeg':
                        ext = 'jpg'

                except (ValueError, IndexError):
                    continue

                image_counter[0] += 1
                img_filename = f"{slug}-img-{image_counter[0]}.{ext}"

                if not dry_run:
                    (bundle_dir / img_filename).write_bytes(
                        base64.b64decode(b64data)
                    )

                if first_image is None:
                    first_image = img_filename

                parts.append(f"![]({img_filename})\n\n")

    return "".join(parts).strip(), image_counter[0], first_image


def _build_front_matter(title: str,
                        post_date: str,
                        slug: str,
                        tags: list[str],
                        authors: list[str],
                        cover: str):
    """
    Function Details
    ================
    Build a front matter string for a markdown file based on provided metadata.

    Parameters
    ----------
    title: str
        The title of the post.
    post_date: str
        The date of the post in YYYY-MM-DD format.
    slug: str
        The slug for the post, used in URLs.
    tags: list[str]
        A list of tags associated with the post.
    authors: list[str]
        A list of authors of the post.
    cover: str
        The filename of the cover image for the post.

    Returns
    -------
    front_matter: str
        A string containing the front matter formatted for a markdown file.

    ---------------------------------------------------------------------------
    Update History
    ==============

    27/03/2026
    ----------
    - Initial function created.

    """
    tags_str = ", ".join(f'"{t}"' for t in tags)
    authors_str = ", ".join(f'"{a}"' for a in authors)
    return (
        f'---\n'
        f'title: "{title}"\n'
        f'date: {post_date}T00:00:00+00:00\n'
        f'draft: false\n'
        f'slug: "{slug}"\n'
        f'tags: [{tags_str}]\n'
        f'authors: [{authors_str}]\n'
        f'cover: "{cover}"\n'
        f'---\n\n'
    )
