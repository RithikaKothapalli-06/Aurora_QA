from utils import clean_text, extract_name, extract_number, extract_date_from_text

SIMILARITY_THRESHOLD = 0.25


# ---------------------------------------------------------
# CLASSIFY QUESTION TYPE
# ---------------------------------------------------------

def classify_question(question: str):
    q = question.lower()

    if "how many" in q:
        return "count"

    if "when" in q:
        return "date"

    if "favorite" in q or "favourite" in q:
        return "favorites"

    if "trip" in q or "travel" in q or "going to" in q:
        return "travel"

    return "generic"


# ---------------------------------------------------------
# REASONING ENGINE
# ---------------------------------------------------------

def generate_answer(question, similar_messages):

    # No results
    if not similar_messages:
        return "I couldn't find any information related to that."

    top = similar_messages[0]
    score = top.get("score", 0)

    # Avoid hallucinations
    if score < SIMILARITY_THRESHOLD:
        return "I couldn't find any relevant information in the data."

    message_text = clean_text(top.get("text", ""))

    name = extract_name(question)
    name = name.capitalize() if name else "They"

    qtype = classify_question(question)

    # ---------------- COUNT ----------------
    if qtype == "count":
        number = extract_number(message_text)
        if number:
            return f"{name} has {number}."
        return f"I could not find a clear count for {name}."

    # ---------------- DATE ----------------
    if qtype == "date":
        date = extract_date_from_text(message_text)
        if date:
            return f"{name} is planning this on {date}."
        return f"I could not find any date mentioned for {name}."

    # --------------- FAVORITES --------------
    if qtype == "favorites":
        words = message_text.split()
        favs = [w for w in words if w.istitle()]
        if favs:
            return f"{name}'s favorites include: {', '.join(favs)}."
        return f"I couldn't identify specific favorites for {name}."

    # ---------------- TRAVEL ----------------
    if qtype == "travel":
        words = message_text.split()
        places = [w for w in words if w.istitle()]
        if places:
            return f"{name} is planning a trip to {places[0]}."
        return f"I couldn't find clear travel information for {name}."

    # ---------------- GENERIC ----------------
    return message_text
