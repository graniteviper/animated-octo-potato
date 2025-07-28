import pdfplumber
import re
import numpy as np
from collections import defaultdict

def extract_outline_ex(pdf_path_ex):
    title_ex = ""
    headings_ex = []
    
    with pdfplumber.open(pdf_path_ex) as pdf_ex:
        
        first_page_ex = pdf_ex.pages[0]
        title_candidates_ex = []
        
        
        words_ex = first_page_ex.extract_words(
            extra_attrs=["size", "fontname"],
            keep_blank_chars=False
        )
        
        
        lines_ex = defaultdict(list)
        for word_ex in words_ex:
            top_key_ex = round(word_ex['top'])
            lines_ex[top_key_ex].append(word_ex)
        
        
        for top_ex in sorted(lines_ex.keys()):
            line_words_ex = lines_ex[top_ex]
            min_x0_ex = min(word_ex['x0'] for word_ex in line_words_ex)
            max_x1_ex = max(word_ex['x1'] for word_ex in line_words_ex)
            text_ex = " ".join(word_ex['text'] for word_ex in line_words_ex)
            avg_size_ex = np.mean([word_ex['size'] for word_ex in line_words_ex])
            
            if avg_size_ex > 20 and (min_x0_ex < 100 and max_x1_ex > first_page_ex.width - 100):
                title_candidates_ex.append((avg_size_ex, text_ex))
        
        if title_candidates_ex:
            title_candidates_ex.sort(key=lambda x_ex: x_ex[0], reverse=True)
            title_ex = title_candidates_ex[0][1]
        
        
        heading_candidates_ex = []
        for page_number_ex, page_ex in enumerate(pdf_ex.pages, start=1):
            words_ex = page_ex.extract_words(
                extra_attrs=["size", "fontname"],
                keep_blank_chars=False
            )
            
            lines_ex = defaultdict(list)
            for word_ex in words_ex:
                top_key_ex = round(word_ex['top'])
                lines_ex[top_key_ex].append(word_ex)
            
            for top_ex in sorted(lines_ex.keys()):
                line_words_ex = lines_ex[top_ex]
                min_x0_ex = min(word_ex['x0'] for word_ex in line_words_ex)
                max_x1_ex = max(word_ex['x1'] for word_ex in line_words_ex)
                text_ex = " ".join(word_ex['text'] for word_ex in line_words_ex)
                max_size_ex = max(word_ex['size'] for word_ex in line_words_ex)
                fonts_ex = [word_ex['fontname'] for word_ex in line_words_ex]
                
                if (max_size_ex > 10 and 
                    min_x0_ex > 50 and 
                    max_x1_ex < page_ex.width - 50 and
                    len(text_ex) < 200 and 
                    len(line_words_ex) < 10):
                    heading_candidates_ex.append({
                        "text": text_ex,
                        "size": max_size_ex,
                        "page": page_number_ex,
                        "y": top_ex
                    })
        
        if heading_candidates_ex:
            sizes_ex = [c_ex['size'] for c_ex in heading_candidates_ex]
            distinct_sizes_ex = sorted(set(sizes_ex), reverse=True)[:3]
            
            level_map_ex = {}
            for i_ex, size_ex in enumerate(distinct_sizes_ex):
                level_map_ex[size_ex] = f"H{i_ex+1}"
            
            current_level_ex = 0
            for candidate_ex in sorted(heading_candidates_ex, key=lambda x_ex: (x_ex['page'], x_ex['y'])):
                level_ex = level_map_ex.get(candidate_ex['size'], None)
                if level_ex:
                    level_num_ex = int(level_ex[1:])
                    if level_num_ex <= current_level_ex + 1:
                        headings_ex.append({
                            "level": level_ex,
                            "text": candidate_ex['text'],
                            "page": candidate_ex['page']
                        })
                        current_level_ex = level_num_ex
    
    return {
        "title": title_ex,
        "outline": headings_ex
    }
