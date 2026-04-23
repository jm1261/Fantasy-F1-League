import argparse
import base64
import re
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, Tag


# ── Slug ──────────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    slug = name.lower()
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug


# ── HTML → Markdown (same logic as split_notebooks.py) ────────────────────────

def el_to_md(el) -> str:
    if isinstance(el, str):
        return el
    tag = el.name if isinstance(el, Tag) else None
    if tag is None:
        return el.string or ""

    def clean_text(node) -> str:
        for a in node.find_all('a', class_='anchor-link'):
            a.decompose()
        return node.get_text()

    if tag == 'h1':
        return ""
    if tag in ('h2', 'h3', 'h4', 'h5', 'h6'):
        return f"{'#' * int(tag[1])} {clean_text(el).strip()}\n\n"
    if tag == 'p':
        return f"{''.join(el_to_md(c) for c in el.children).strip()}\n\n"
    if tag in ('strong', 'b'):
        return f"**{el.get_text()}**"
    if tag in ('em', 'i'):
        return f"*{el.get_text()}*"
    if tag == 'code':
        return f"`{el.get_text()}`"
    if tag == 'a':
        href = el.get('href', '')
        text = el.get_text()
        return text if href.startswith('#') else f"[{text}]({href})"
    if tag in ('ul', 'ol'):
        items = []
        for i, li in enumerate(el.find_all('li', recursive=False)):
            content = "".join(el_to_md(c) for c in li.children).strip()
            items.append(f"{i + 1}. {content}" if tag == 'ol' else f"- {content}")
        return "\n".join(items) + "\n\n"
    if tag == 'li':
        return "".join(el_to_md(c) for c in el.children).strip()
    if tag == 'table':
        return _table_to_md(el)
    if tag == 'br':
        return "  \n"
    if tag == 'hr':
        return "---\n\n"
    if tag == 'blockquote':
        inner = "".join(el_to_md(c) for c in el.children).strip()
        return "\n".join(f"> {line}" for line in inner.splitlines()) + "\n\n"
    if tag == 'pre':
        code = el.find('code')
        return f"```\n{(code.get_text() if code else el.get_text())}\n```\n\n"
    return "".join(el_to_md(c) for c in el.children)


def _table_to_md(table: Tag) -> str:
    rows = table.find_all('tr')
    if not rows:
        return ""
    lines = []
    for i, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])
        lines.append("| " + " | ".join(c.get_text(strip=True) for c in cells) + " |")
        if i == 0:
            lines.append("| " + " | ".join("---" for _ in cells) + " |")
    return "\n".join(lines) + "\n\n"


# ── Core: parse HTML notebook ─────────────────────────────────────────────────

def process_notebook(html_path: Path, slug: str, bundle_dir: Path, dry_run: bool):
    """
    Parse notebook HTML, extract markdown and images.
    Returns (markdown_content, image_count, first_image_filename_or_None)
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
                        parts.append(el_to_md(child))

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
                    (bundle_dir / img_filename).write_bytes(base64.b64decode(b64data))

                if first_image is None:
                    first_image = img_filename

                parts.append(f"![]({img_filename})\n\n")

    return "".join(parts).strip(), image_counter[0], first_image


# ── Front matter ──────────────────────────────────────────────────────────────

def build_front_matter(title, post_date, slug, tags, authors, cover):
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


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Jupyter notebook HTML export to a Hugo page bundle"
    )
    parser.add_argument("notebook", help="Path to the notebook .html file")
    parser.add_argument("--date", help="Post date YYYY-MM-DD (default: today)")
    parser.add_argument("--title", help="Post title (default: derived from filename)")
    parser.add_argument("--tags", nargs="+", default=["f1", "race-report"],
                        help="Tags (default: f1 race-report)")
    parser.add_argument("--authors", nargs="+", default=["aatapex"],
                        help="Authors (default: aatapex)")
    parser.add_argument("--cover", help="Cover image filename (default: first extracted image)")
    parser.add_argument("--output-dir", default=".",
                        help="Where to create the bundle dir (default: current dir)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Parse and report without writing files")
    args = parser.parse_args()

    html_path = Path(args.notebook)
    if not html_path.exists():
        print(f"Error: {html_path} not found", file=sys.stderr)
        sys.exit(1)

    slug = slugify(html_path.stem)
    post_date = args.date or date.today().isoformat()
    title = args.title or slug.replace('-', ' ').title()
    output_dir = Path(args.output_dir)

    bundle_name = f"{post_date}-{slug}"
    bundle_dir = output_dir / bundle_name

    print(f"Input:      {html_path}")
    print(f"Slug:       {slug}")
    print(f"Bundle dir: {bundle_dir}")
    print(f"Date:       {post_date}")
    print(f"Title:      {title}")
    print(f"Tags:       {args.tags}")
    print(f"Authors:    {args.authors}")
    print()

    if not args.dry_run:
        bundle_dir.mkdir(parents=True, exist_ok=True)

    markdown_content, image_count, first_image = process_notebook(
        html_path, slug, bundle_dir, args.dry_run
    )

    cover = args.cover or first_image or ""

    print(f"Images extracted: {image_count}")
    print(f"Cover image:      {cover}")
    print(f"Markdown length:  {len(markdown_content):,} chars")

    if args.dry_run:
        print("\n[dry-run] No files written.")
        return

    if not markdown_content:
        print("\nWarning: no content extracted. index.md will have front matter only.")

    front_matter = build_front_matter(title, post_date, slug, args.tags, args.authors, cover)
    index_path = bundle_dir / "index.md"
    index_path.write_text(front_matter + markdown_content, encoding='utf-8')

    print(f"\nWritten:")
    print(f"  {index_path}")
    for i in range(1, image_count + 1):
        for ext in ('png', 'jpg'):
            candidate = bundle_dir / f"{slug}-img-{i}.{ext}"
            if candidate.exists():
                print(f"  {candidate}")
                break

    print(f"\nDone. Bundle ready at: {bundle_dir}")
    print(f"\nTo deploy:")
    print(f"  cp -r {bundle_dir} /var/data/hugo-ahead/site/content/posts/")


if __name__ == "__main__":
    main()
