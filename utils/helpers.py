def clean_text(text):
    return text.replace("\n", " ").strip()

def is_valid_heading(text):
    words = text.strip().split()
    return len(text) > 5 and len(words) >= 2

def extract_title(first_page_spans):
    max_size = 0
    title = ""
    for s in first_page_spans:
        if s["size"] > max_size:
            max_size = s["size"]
            title = s["text"]
    return title
