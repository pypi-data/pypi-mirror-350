import argparse
import json
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def pdf_to_markdown_sections(pdf_path):
    logger.info(f"Starting conversion of PDF: {pdf_path}")

    converter = DocumentConverter()

    logger.info("Converting PDF to markdown...")
    result = converter.convert(pdf_path)
    markdown_text = result.document.export_to_markdown()

    logger.info("Splitting markdown into sections...")
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(markdown_text)

    logger.info(f"Extracted {len(md_header_splits)} sections.")

    sections = []
    for doc in md_header_splits:
        sections.append({
            "header": doc.metadata.get("Header 1") or 
                      doc.metadata.get("Header 2") or 
                      doc.metadata.get("Header 3") or "Untitled",
            "content": doc.page_content
        })

    return sections




def save_json(obj, path):
    logger.info(f"Saving output to: {path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help="Path to the input PDF file")
    parser.add_argument('--output', required=True, help="Path to save the output JSON")
    args = parser.parse_args()

    sections = pdf_to_markdown_sections(args.input)
    save_json(sections, args.output)


if __name__ == "__main__":
    main()
