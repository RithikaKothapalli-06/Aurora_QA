import re

# ---------------------------------------
# CLEAN TEXT
# ---------------------------------------

def clean_text(t: str):
    return t.replace("\n", " ").strip()


# ---------------------------------------
# NAME EXTRACTION (very simple)
# ---------------------------------------

def extract_name(q: str):
    words = q.split()
    for w in words:
        if w.istitle():  # First letter capital
            return w
    return None


# ---------------------------------------
# EXTRACT NUMBER
# ---------------------------------------

def extract_number(text: str):
    found = re.findall(r"\b\d+\b", text)
    return found[0] if found else None


# ---------------------------------------
# EXTRACT DATE
# ---------------------------------------

def extract_date_from_text(text: str):
    # simplest date detector: 12/03, March, Monday, etc.
    months = [
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    ]

    words = text.lower().split()

    for w in words:
        if w in months:
            return w.capitalize()
        if "/" in w:
            return w

    return None
