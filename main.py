import argparse
import re
from pathlib import Path

import frontmatter
import pypandoc
from markdown_pdf import MarkdownPdf, Section

PAGE_BREAK = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```'


def join_title_to_text(title: str, text: str) -> str:
    joined = title + text
    return joined


def get_all_filenames(directory: Path) -> list[dict]:
    all_names = []
    for entry in directory.iterdir():
        if entry.suffix == ".md":
            chapter_name = entry.name[:-3]
            chapter_number = get_chapter_number(chapter_name)
            all_names.append(
                {
                    "chapter number": chapter_number,
                    "chapter name": f"# {chapter_name} \n \n",
                    "chapter path": entry,
                }
            )
    sorted_filenames = sorted(all_names, key=lambda d: d["chapter number"])
    return sorted_filenames


def get_chapter_number(chapter_name):
    match = re.search(r"Chapter (\d+)", chapter_name)
    if match:
        chapter_number = int(match.group(1))
    elif chapter_name == "Epilogue":
        # Arbitrary number so Epilogue is always last
        chapter_number = 1000
    else:
        # If I named another last chapter differently for dramatic
        # reasons it should go before epilogue
        chapter_number = 500
    return chapter_number


def compile_to_pdf(directory: Path, book_name: str) -> None:
    """Takes a list of files in a directory, orders them by chapter number,
    and joins them into a single pdf
    """
    pdf = MarkdownPdf(toc_level=2, optimize=True)

    for file in get_all_filenames(directory):
        with open(file["chapter path"], encoding="utf-8") as f:
            raw_text = frontmatter.load(f)
            processed_text = join_title_to_text(file["chapter name"], raw_text.content)
            chapter = Section(processed_text)
            pdf.add_section(chapter)
    pdf.save(f"compiled_books/{book_name}.pdf")


def compile_to_word(directory: Path, book_name: str) -> None:
    separator = f"\n\n{PAGE_BREAK}\n\n"
    full_text = ""
    for file in get_all_filenames(directory):
        with open(file["chapter path"], encoding="utf-8") as f:
            raw_text = frontmatter.load(f)
            processed_text = join_title_to_text(file["chapter name"], raw_text.content)
            full_text = full_text + processed_text + separator
    pypandoc.convert_text(
        full_text,
        to="docx",
        format="markdown",
        outputfile=f"compiled_books/{book_name}.docx",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Random CSV Data")
    parser.add_argument("book_path", type=Path)
    parser.add_argument("book_name", type=str)
    parser.add_argument("-f", "--format", type=str, default="pdf")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    if args.format == "pdf":
        compile_to_pdf(directory=args.book_path, book_name=args.book_name)
    elif args.format == "docx":
        compile_to_word(directory=args.book_path, book_name=args.book_name)
    else:
        print("Unrecognised format, must be either pdf or docx")
