''' Defines what a deck and a card are and the logic to be carried out on them'''

def new_card(question, answer):
    return {
        "question" : question,
        "answer": answer,
        "times_seen": 0,
        "times_wrong" : 0
    }
    
def new_deck(name):
    return {
        "name" : name,
        "cards" : [],
        "sessions" : []
    }
    
def record_answer(card, was_correct):
    card["times_seen"] += 1
    if not was_correct:
        card["times_wrong"] += 1
        
def difficulty(card):
    if card["times_seen"] < 2:
        return 0
    if card["times_wrong"] >= 2:
        return "Hard"
    if card["times_wrong"] >= 1:
        return "Medium"
    return "Easy"

def deck_accuracy(deck):
    total = sum(session["total"] for session in deck["sessions"])
    correct = sum(session["correct"] for session in deck["sessions"])
    if total == 0:
        return None
    return round(100 * correct / total, 1)