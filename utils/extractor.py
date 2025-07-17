import fitz
from collections import defaultdict
from .heading import detect_heading_level
from .helpers import clean_text, is_valid_heading, extract_title

def extract_text_blocks(doc):
    all_spans = []
    all_font_sizes = set()

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    text = clean_text(s["text"])
                    if not text:
                        continue
                    span = {
                        "text": text,
                        "size": s["size"],
                        "font": s["font"],
                        "flags": s["flags"],
                        "page": page_num + 1,
                        "bbox": s["bbox"]
                    }
                    all_spans.append(span)
                    all_font_sizes.add(s["size"])

    return all_spans, sorted(all_font_sizes, reverse=True)

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    spans, font_sizes_sorted = extract_text_blocks(doc)

    outline = []
    content_by_page = defaultdict(list)
    first_page_spans = []

    for span in spans:
        text = span["text"]
        size = span["size"]
        font = span["font"]
        page = span["page"]
        flags = span["flags"]

        is_bold = flags & 2 != 0 or "bold" in font.lower()
        level = detect_heading_level(size, font_sizes_sorted, font, is_bold)

        if page == 1:
            first_page_spans.append(span)

        if level and is_valid_heading(text):
            outline.append({"level": level, "text": text, "page": page})
        else:
            content_by_page[page].append(text)

    title = extract_title(first_page_spans)

    content = []
    for page_num in sorted(content_by_page.keys()):
        content.append({
            "page": page_num,
            "text": " ".join(content_by_page[page_num])
        })

    return {
        "title": title,
        "outline": outline,
        "content": content
    }
