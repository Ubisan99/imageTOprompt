from pathlib import Path
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:7b"
MAX_RETRIES = 3
CHUNK_SIZE = 256
CATEGORIES = {
    "trading": ["chart","graph","equity","mt5","trading","backtest","report","signal"],
    "code": ["code","programming","script","python","mql","java","cpp"],
    "ai_ml": ["ai","ml","neural","model","dataset","llm","gpt","train"],
    "cybersec": ["pentest","security","hack","exploit","vuln","injection"],
    "blockchain": ["blockchain","crypto","eth","smart","defi","token"],
    "ui": ["ui","interface","dashboard","button","layout","web","app"],
    "diagram": ["diagram","architecture","flowchart","schema","network"],
    "logo_banner": ["logo","banner","hero","brand","icon"],
    "other": []
}