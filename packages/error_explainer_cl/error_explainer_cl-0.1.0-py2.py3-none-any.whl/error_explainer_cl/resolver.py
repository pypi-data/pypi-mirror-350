import json
import os

def load_knowledge_base():
    path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_solution(error_type: str):
    knowledge_base = load_knowledge_base()
    info = knowledge_base.get(error_type)
    if info:
        return {
            "error": error_type,
            "explanation": info["explanation"],
            "fix": info["fix"]
        }
    return None
