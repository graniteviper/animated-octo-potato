# 🧠 Adobe Hackathon – Document Outline Extractor

This solution extracts a structured outline (title, H1, H2, H3 headings) from PDF documents using Python and PyMuPDF, packaged in a Docker container. It processes all PDFs from an input folder and generates corresponding `.json` files.

---

## 📦 How It Works

- Takes PDF files from the `/app/input` directory.
- Parses each document and detects:
  - 📌 Title
  - 📑 Headings (H1, H2, H3) with their text and page number.
- Outputs a JSON file for each PDF to `/app/output`.

 ## 💡 Summary of Logic

| Section              | Purpose                                          |
| -------------------- | ------------------------------------------------ |
| Title Extraction     | Find big, centered text at the top of first page |
| Word Grouping        | Combine words into lines using vertical position |
| Heading Detection    | Heuristics: size, length, margins                |
| Font Size Clustering | Detect top 3 sizes = H1, H2, H3                  |
| Hierarchy Validation | Enforce logical document outline order           |

Example output format:
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "History of AI", "page": 2 },
    { "level": "H3", "text": "Symbolic AI", "page": 3 }
  ]
}
```



0. Make sure you have docker installed.

    Mac: https://youtu.be/gcacQ29AjOo?si=wx9Bo0TkpyM5nMcE

    Windows: https://youtu.be/JBEUKrjbWqg?si=qLaanGPwb5vK598U

1. to build the image: `docker build --platform linux/amd64 -t mysolution:<your-tag> .`
Replace <your-tag> with any name like v1, v2, etc.
2. project-root/

    ├── Dockerfile

    ├── main.py

    ├── requirements.txt

    ├── input/

    │       ├── document1.pdf

    │       └── document2.pdf

    └── output/  ← (will be auto-created if not present)
    Place your input PDFs inside the input/ folder.

3. For windows: 
``` 
  docker run --rm `
  -v "${PWD}\input:/app/input" `
  -v "${PWD}\output:/app/output" `
  mysolution:<your-tag>
```
   b. For mac:
   ``` 
   docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolution:<your-tag>
```

4. Check the output at:

    output/

    ├── document1.json

    ├── document2.json
