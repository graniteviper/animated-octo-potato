import os as os_ru
import json as json_ru
from extractor import extract_outline_ex

INPUT_DIR_ru = "input"
OUTPUT_DIR_ru = "output"

if __name__ == "__main__":
    # Ensure output directory exists
    os_ru.makedirs(OUTPUT_DIR_ru, exist_ok=True)

    # Process all PDFs in input directory
    for filename_ru in os_ru.listdir(INPUT_DIR_ru):
        if filename_ru.lower().endswith(".pdf"):
            pdf_path_ru = os_ru.path.join(INPUT_DIR_ru, filename_ru)
            print(f"Processing: {filename_ru}")
            
            try:
                # Extract outline
                result_ru = extract_outline_ex(pdf_path_ru)
                
                # Save results
                json_filename_ru = f"{os_ru.path.splitext(filename_ru)[0]}.json"
                output_path_ru = os_ru.path.join(OUTPUT_DIR_ru, json_filename_ru)
                
                with open(output_path_ru, "w") as f_ru:
                    json_ru.dump(result_ru, f_ru, indent=2)
                    
                print(f"Created: {json_filename_ru}")
                
            except Exception as e_ru:
                print(f"Error processing {filename_ru}: {str(e_ru)}")

