import re

BLOCKED_PATTERNS = [
    r"\bdrop\s+table\b", r"\bdelete\s+from\b", r"\btruncate\s+table\b",
    r"\binformation_schema\b", r"\bpg_catalog\b", r"\bshow\s+(databases?|tables?)\b",
    r"\bdatabase\s+schema\b", r"\bsystem\s+prompt\b", r"\bapi\s+key\b",
    r"\bdatabase\s+password\b",
]

def check_input(message: str):
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, message.lower()):
            return False, "I can't provide internal database, system, or credential information."
    return True, ""
