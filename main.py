import frontmatter
import re
import sys
from markdown_pdf import MarkdownPdf, Section
from pathlib import Path


def join_title_to_text(title: str, text: str) -> str:
    joined = title + text
    return joined


def get_all_filenames(directory: Path) -> list[dict]:
    all_names = []
    for entry in directory.iterdir():
        if entry.suffix == ".md":
            chapter_name = entry.name[:-3]
            chapter_number = get_chapter_number(chapter_name)
            all_names.append({
                "chapter number": chapter_number,
                "chapter name": f"# {chapter_name} \n \n",
                "chapter path": entry})
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


def compile_to_book(directory: Path, book_name: str) -> None:
    """Takes a list of files in a directory, orders them by chapter number,
    and joins them into a single pdf
    """
    pdf = MarkdownPdf(toc_level=2, optimize=True)

    for file in get_all_filenames(directory):
        with open(file["chapter path"], encoding="utf-8") as f:
            raw_text = frontmatter.load(f)
            processed_text = join_title_to_text(file["chapter name"],
                                                raw_text.content)
            chapter = Section(processed_text)
            pdf.add_section(chapter)
    pdf.save(f"compiled_books/{book_name}.pdf")


if __name__ == "__main__":
    compile_to_book(directory=Path(sys.argv[1]), book_name=sys.argv[2])
