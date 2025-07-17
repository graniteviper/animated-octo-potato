def detect_heading_level(font_size, font_sizes_sorted, font_name, is_bold):
    """
    Heuristic to detect heading level based on font size and boldness.
    """
    if is_bold:
        if font_size >= font_sizes_sorted[0]:
            return "H1"
        elif font_size >= font_sizes_sorted[1]:
            return "H2"
    if font_size >= font_sizes_sorted[2]:
        return "H3"
    return None
