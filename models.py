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