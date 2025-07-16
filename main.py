# main.py

import os
import json
import fitz

INPUT_DIR = "input"
OUTPUT_DIR = "output"


def detect_heading_level(font_size, font_sizes_sorted):
    """
    Assigns heading level based on font size.
    This is a heuristic—refine as needed.
    """
    if font_size >= font_sizes_sorted[0]:
        return "H1"
    elif font_size >= font_sizes_sorted[1]:
        return "H2"
    else:
        return "H3"


def process_pdf(pdf_path):
    """
    Processes a single PDF file and returns structured data.
    """
    doc = fitz.open(pdf_path)

    all_font_sizes = set()
    text_blocks = []

    # Pass 1: Collect all font sizes
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        all_font_sizes.add(s["size"])

    # Sort font sizes descending
    font_sizes_sorted = sorted(all_font_sizes, reverse=True)

    outline = []

    # Pass 2: Extract headings
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        font_size = s["size"]

                        # Heuristic: longer text and small fonts = body text
                        if len(text) < 200 and font_size >= font_sizes_sorted[-1]:
                            level = detect_heading_level(font_size, font_sizes_sorted)
                            outline.append({
                                "level": level,
                                "text": text,
                                "page": page_num + 1
                            })

    # Use the largest text on the first page as title
    first_page = doc[0]
    title = ""
    max_size = 0
    for b in first_page.get_text("dict")["blocks"]:
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    if s["size"] > max_size:
                        max_size = s["size"]
                        title = s["text"].strip()

    return {
        "title": title,
        "outline": outline
    }


def main():
    """
    Main entry point.
    """
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing {filename}...")
            data = process_pdf(pdf_path)
            json_filename = filename.replace(".pdf", ".json")
            output_path = os.path.join(OUTPUT_DIR, json_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    print("Processing complete.")


if __name__ == "__main__":
    main()

