# Automatic Flashcard Grading
#### Video Demo: https://youtu.be/d67Y1DyH9TI
#### Description: 

TLDR: This python tkinter app locally stores flashcards & decks in the form of JSON files, automatically grading their difficultly level based on how often a card particular card is answered correctly or incorrectly.

The app is split into four files each with its own specific task:
###### 1) Main: 
    The main.py file is the file thats executed to run the app.

###### 2) Models:
    This file defines what a card and a deck are, and has functions to perform logic on them. 

    This includes creation of a new card which has a question, an answer, how many times its been seen (during a quiz) and how many times it was gotten wrong.
    A deck contains its name, a list of the cards, and sessions (this is neccassary for calculation of long-term accuracy in answering cards within that deck and gives a clear picture of the person's knowledge of that deck)

    It also contains functions to record the answer (adding to the number of times its been seen and whether it was wrong).

    Calculating difficult (which is only calculated after a card has been seen atleast twice) where the card is considered "Hard" if it has been answered wrong twice or more, "Medium" if it has been answered wrong once, and "Easy" if it has not been answered wrong at all.

    Deck accuracy is a percentage of the correct answers from the total questions ever answered. Sessions is used to keep track of total and correct answers throughout multiple sessions (even if the app is closed and reopened).

###### 3) Storage:
    Storage file is responsible for storing the decks, cards and their stats so the app is useable even if it closed.

    It has functions like list_deck_names which are used to get all the decks currently stored.

    Decks can be loaded, saved and deleted.

    Decks are renamed by making a copy of the deck with the new name and deleting the old deck using already establised functions of save and delete.
###### 4) GUI:
    This file is entirely responsible for the GUI of the app built using Tkinter. It uses functions from models and storage to manage cards and decks.

    The GUI has several screens. The first screen is the home screen which can be accessed from all other screens aswell. It contains buttons to manage decks, start quiz and for stats.

    The Manage Screen has the most functionality. It also the creation of new decks, renaming, and deleting. 
    You can also view existing decks and modify cards within them.

    The Quiz Setup Screen appears before a quiz starts. It allows the user to select a deck to study and also allows whether they want the questions to be randomised ie they do not appear in the order they were created & are saved.

    The Quiz Screen comes afterwards where questions appear to the user and they have to answer them. Feedback for their answer is instantly shown. The user also has options to stop the quiz whenever they want.

    The Result Screen appears when the quiz ends. It tells the user how many questions they answered and how many were correct and its perecentage aswell. With options to redo the quiz or go home.

    The Stats Screen is a separately accessible menu which provides all time stats for decks categorising them into four grades: Easy, Medium, Hard and New (ie not answered more than twice yet). 


The app stores all files locally in JSON format so its easy to import and export the quiz data to external services like quizlet. 