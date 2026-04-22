# imageTOprompt

Convert images to RAG-ready prompts using Ollama vision models.

## Features
- Auto-categorize images by filename
- Retry failed images up to N times
- Skip images with no content after max retries
- Output ready for RAG pipeline

## Usage
```python
from imageTOprompt import process_category
from pathlib import Path

good_dir = Path("good/")
output = Path("prompts.jsonl")
process_category("trading", good_dir, output)
```