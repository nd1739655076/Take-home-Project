import json

TARGETS_TO_REMOVE = [
    "who is killed at the end of",
    "could you provide a list of the female characters in",
]

with open("data/longterm_memory.json", "r", encoding="utf-8") as f:
    memory = json.load(f)

def is_dirty(entry):
    q = entry.get("question", "").lower()
    return any(phrase in q for phrase in TARGETS_TO_REMOVE)

original_len = len(memory)
cleaned = [entry for entry in memory if not is_dirty(entry)]

with open("data/longterm_memory.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print(f"✅ Removed {original_len - len(cleaned)} entries.")
