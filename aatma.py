import json
import os

MEMORY_FILE = os.path.join("data", "memory.json")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memories):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2, ensure_ascii=False)

def add_memory(summary):
    memories = load_memory()
    memories.append(summary)
    save_memory(memories)

def get_relevant_memories():
# simple version: return last 3 summaries
    memories = load_memory()
    last = memories[-3:]
    return "\n".join(last)

def get_last_memories(n=3):
    memories = load_memory()
    return memories[-n:]