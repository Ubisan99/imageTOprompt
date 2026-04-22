import json, base64, sys
from pathlib import Path
from collections import defaultdict
import requests
from .config import OLLAMA_URL, MODEL, MAX_RETRIES, CATEGORIES
from .categories import get_category

def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def is_valid(entry: dict) -> bool:
    raw = entry.get("raw", "") or entry.get("description", "") or entry.get("filename", "")
    return bool(raw and len(raw) > 5)

def generate_prompt(path: Path, cat: str, attempt: int = 0) -> dict:
    prompt = f"Analyze this image (attempt {attempt+1}). Output ONLY JSON: {{\"category\":\"{cat}\",\"filename\":\"{path.name}\",\"description\":\"<2 sentences>\",\"keywords\":[\"kw1\",\"kw2\"],\"technical\":\"<tech>\",\"purpose\":\"<use case>\"}}"
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "images": [encode_image(path)], "stream": False}, timeout=90)
        return r.json().get("response", "")
    except Exception as e:
        return json.dumps({"error": str(e)})

def process_category(category: str, good_dir: Path, output_file: Path, max_retries: int = MAX_RETRIES):
    entries = {}
    failed = defaultdict(int)
    if output_file.exists():
        for line in output_file.read_text().splitlines():
            if not line.strip(): continue
            try:
                d = json.loads(line)
                fn = d.get("filename", "")
                if fn: entries[fn] = d
                else: failed[d.get("filename","")] += 1
            except: pass
    
    results = {"valid": 0, "failed": 0}
    out_lines = []
    
    for f in sorted(good_dir.iterdir()):
        if not f.is_file(): continue
        if get_category(f.name) != category: continue
        if f.name in entries and is_valid(entries[f.name]): continue
        
        attempts = failed[f.name]
        if attempts >= max_retries: continue
        
        resp = generate_prompt(f, category, attempts)
        try: result = json.loads(resp)
        except: result = {"raw": resp}
        
        if is_valid(result):
            results["valid"] += 1
        else:
            results["failed"] += 1
        
        out_lines.append(json.dumps(result, ensure_ascii=False))
    
    output_file.write_text("\n".join(out_lines) + "\n")
    return results

def main():
    print("imageTOprompt - Smart RAG Pipeline")
    print(f"Model: {MODEL}")

if __name__ == "__main__":
    main()