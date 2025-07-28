import os as os_m
import json as json_m
import sys as sys_m

project_root_m = os_m.path.dirname(os_m.path.abspath(__file__))
sys_m.path.insert(0, project_root_m)

from utils.extractor import process_pdf as process_pdf_m

INPUT_DIR_m = "input"
OUTPUT_DIR_m = "output"

def main_m():
    os_m.makedirs(OUTPUT_DIR_m, exist_ok=True)

    for filename_m in os_m.listdir(INPUT_DIR_m):
        if filename_m.lower().endswith(".pdf"):
            pdf_path_m = os_m.path.join(INPUT_DIR_m, filename_m)
            print(f"Processing {filename_m}...")
            try:
                data_m = process_pdf_m(pdf_path_m)
                json_filename_m = filename_m.replace(".pdf", ".json")
                output_path_m = os_m.path.join(OUTPUT_DIR_m, json_filename_m)
                with open(output_path_m, "w", encoding="utf-8") as f_m:
                    json_m.dump(data_m, f_m, indent=2, ensure_ascii=False)
            except Exception as e_m:
                print(f"Failed to process {filename_m}: {e_m}")

    print("All PDFs processed.")

if __name__ == "__main__":
    main_m()
