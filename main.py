import os
import json
import sys
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
from utils.extractor import process_pdf

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing {filename}...")
            try:
                data = process_pdf(pdf_path)
                json_filename = filename.replace(".pdf", ".json")
                output_path = os.path.join(OUTPUT_DIR, json_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    print("All PDFs processed.")

if __name__ == "__main__":
    main()
