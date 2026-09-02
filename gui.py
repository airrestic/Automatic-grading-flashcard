''' Tkinter GUI for the Flashcard app '''

import random
import tkinter as tk
from tkinter import messagebox, simpledialog

import models
import storage


class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard App")
        self.geometry("760x540")
        self.show_home()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear()
        HomeScreen(self, self).pack(fill="both", expand=True, padx=20, pady=20)

    def show_manage(self):
        self.clear()
        ManageScreen(self, self).pack(fill="both", expand=True, padx=20, pady=20)

    def show_quiz_setup(self):
        self.clear()
        QuizSetupScreen(self, self).pack(fill="both", expand=True, padx=20, pady=20)

    def show_quiz(self, deck_name, randomise):
        self.clear()
        QuizScreen(self, self, deck_name, randomise).pack(fill="both", expand=True, padx=20, pady=20)

    def show_results(self, deck_name, correct, total):
        self.clear()
        ResultsScreen(self, self, deck_name, correct, total).pack(fill="both", expand=True, padx=20, pady=20)

    def show_stats(self):
        self.clear()
        StatsScreen(self, self).pack(fill="both", expand=True, padx=20, pady=20)


''' Screens for the Flashcard app '''

class HomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="Flashcard App", font=("Arial", 20, "bold")).pack(pady=20)

        tk.Button(self, text="Manage Decks", width=20, command=app.show_manage).pack(pady=5)
        tk.Button(self, text="Start Quiz", width=20, command=app.show_quiz_setup).pack(pady=5)
        tk.Button(self, text="Stats", width=20, command=app.show_stats).pack(pady=5)


class ManageScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.current_deck = None

        tk.Button(self, text="Back", command=app.show_home).pack(anchor="w", pady=5)
        tk.Label(self, text="Manage Decks", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        # Deck list & buttons
        tk.Label(self, text="Decks:").pack(anchor="w")
        self.deck_listbox = tk.Listbox(self, height=6)
        self.deck_listbox.pack(fill="x")
        self.deck_listbox.bind("<<ListboxSelect>>", self.on_select_deck)

        deck_buttons = tk.Frame(self)
        deck_buttons.pack(anchor="w", pady=5)
        tk.Button(deck_buttons, text="New Deck", command=self.new_deck).pack(side="left", padx=5)
        tk.Button(deck_buttons, text="Rename Deck", command=self.rename_deck).pack(side="left", padx=5)
        tk.Button(deck_buttons, text="Delete Deck", command=self.delete_deck).pack(side="left", padx=5)

        # Card list & buttons
        tk.Label(self, text="Cards:").pack(anchor="w", pady=(10, 0))
        self.card_listbox = tk.Listbox(self, height=6)
        self.card_listbox.pack(fill="both", expand=True)

        add_row = tk.Frame(self)
        add_row.pack(fill="x", pady=5)
        tk.Label(add_row, text="Question:").pack(side="left")
        self.question_entry = tk.Entry(add_row, width=20)
        self.question_entry.pack(side="left", padx=5)
        tk.Label(add_row, text="Answer:").pack(side="left")
        self.answer_entry = tk.Entry(add_row, width=20)
        self.answer_entry.pack(side="left", padx=5)
        tk.Button(add_row, text="Add Card", command=self.add_card).pack(side="left", padx=5)
        tk.Button(self, text="Delete Card", command=self.delete_card).pack(anchor="w", pady=5)

        self.refresh_deck_list()

    ''' Deck list helper functions '''
    
    def refresh_deck_list(self):
        self.deck_listbox.delete(0, tk.END)
        for name in storage.list_deck_names():
            self.deck_listbox.insert(tk.END, name)

    def on_select_deck(self, event):
        selection = self.deck_listbox.curselection()
        if not selection:
            return
        name = self.deck_listbox.get(selection[0])
        self.current_deck = storage.load_deck(name)
        self.refresh_card_list()

    def new_deck(self):
        name = simpledialog.askstring("New Deck", "Deck name:", parent=self)
        if not name:
            return
        if name in storage.list_deck_names():
            messagebox.showerror("Error", "A deck with that name already exists.")
            return
        storage.save_deck(models.new_deck(name))
        self.refresh_deck_list()

    def rename_deck(self):
        if not self.current_deck:
            messagebox.showerror("Error", "No deck selected.")
            return
        new_name = simpledialog.askstring(
            "Rename Deck", "New name:", initialvalue=self.current_deck["name"], parent=self
        )
        if not new_name:
            return
        storage.rename_deck(self.current_deck["name"], new_name)
        self.current_deck["name"] = new_name
        self.refresh_deck_list()

    def delete_deck(self):
        if not self.current_deck:
            messagebox.showerror("Error", "No deck selected.")
            return
        if messagebox.askyesno("Delete Deck", f'Delete "{self.current_deck["name"]}"?'):
            storage.delete_deck(self.current_deck["name"])
            self.current_deck = None
            self.refresh_deck_list()
            self.card_listbox.delete(0, tk.END)

    ''' Card list helper functions '''

    def refresh_card_list(self):
        self.card_listbox.delete(0, tk.END)
        if not self.current_deck:
            return
        for card in self.current_deck["cards"]:
            self.card_listbox.insert(tk.END, f"{card['question']} - {card['answer']}")

    def add_card(self):
        if not self.current_deck:
            messagebox.showerror("Error", "No deck selected.")
            return
        question = self.question_entry.get().strip()
        answer = self.answer_entry.get().strip()
        if not question or not answer:
            messagebox.showerror("Error", "Question and Answer cannot be empty.")
            return
        self.current_deck["cards"].append(models.new_card(question, answer))
        storage.save_deck(self.current_deck)
        self.question_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)
        self.refresh_card_list()

    def delete_card(self):
        selection = self.card_listbox.curselection()
        if not self.current_deck or not selection:
            messagebox.showerror("Error", "No card selected.")
            return
        del self.current_deck["cards"][selection[0]]
        storage.save_deck(self.current_deck)
        self.refresh_card_list()

class QuizSetupScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Button(self, text="Back", command=app.show_home).pack(anchor="w", pady=5)

        deck_names = storage.list_deck_names()
        if not deck_names:
            tk.Label(self, text="No decks available. Please create a deck first.", fg="red").pack(pady=20)
            return

        tk.Label(self, text="Select a Deck:", font=("Arial", 14)).pack(pady=10)
        self.deck_var = tk.StringVar(value=deck_names[0])
        for name in deck_names:
            tk.Radiobutton(self, text=name, variable=self.deck_var, value=name).pack(anchor="w")

        self.random_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self, text="Randomize Questions", variable=self.random_var).pack(anchor="w", pady=10)

        tk.Button(
            self, text="Start",
            command=lambda: app.show_quiz(self.deck_var.get(), self.random_var.get())
        ).pack(anchor="w")


class QuizScreen(tk.Frame):
    def __init__(self, parent, app, deck_name, randomise):
        super().__init__(parent)
        self.app = app
        self.deck = storage.load_deck(deck_name)

        self.order = list(range(len(self.deck["cards"])))
        if randomise:
            random.shuffle(self.order)

        self.position = 0
        self.correct = 0
        self.answer_shown = False

        tk.Button(self, text="Stop Quiz", command=self.finish).pack(anchor="w")
        tk.Label(self, text=f"Quiz: {deck_name}", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        if not self.order:
            tk.Label(self, text="No cards in this deck. Please add cards first.", fg="red").pack(pady=20)
            return

        self.progress_label = tk.Label(self, text="")
        self.progress_label.pack(anchor="w", pady=5)

        self.question_label = tk.Label(self, text="", font=("Arial", 14))
        self.question_label.pack(anchor="w", pady=10)

        self.answer_entry = tk.Entry(self, width=50)
        self.answer_entry.pack(anchor="w", pady=5)
        self.answer_entry.bind("<Return>", lambda event: self.submit())

        self.feedback_label = tk.Label(self, text="", font=("Arial", 12))
        self.feedback_label.pack(anchor="w", pady=5)

        self.next_button = tk.Button(self, text="Submit", command=self.submit)
        self.next_button.pack(anchor="w", pady=5)

        self.show_current_card()

    def show_current_card(self):
        if self.position >= len(self.order):
            self.finish()
            return
        card = self.deck["cards"][self.order[self.position]]
        self.progress_label.config(text=f"Card {self.position + 1} of {len(self.order)}")
        self.question_label.config(text=card["question"])
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state="normal")
        self.feedback_label.config(text="")
        self.answer_shown = False
        self.next_button.config(text="Submit", command=self.submit)
        self.answer_entry.focus_set()

    def submit(self):
        if self.answer_shown:
            return
        card = self.deck["cards"][self.order[self.position]]
        typed_answer = self.answer_entry.get().strip()
        is_correct = typed_answer.lower() == card["answer"].lower()
        models.record_answer(card, is_correct)

        if is_correct:
            self.correct += 1
            self.feedback_label.config(text="Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"Incorrect! Correct answer: {card['answer']}", fg="red")

        self.answer_shown = True
        self.answer_entry.config(state="disabled")
        self.next_button.config(text="Next", command=self.go_next)

    def go_next(self):
        self.position += 1
        self.show_current_card()

    def finish(self):
        total = min(self.position, len(self.order))
        if total > 0:
            self.deck["sessions"].append({"correct": self.correct, "total": total})
        storage.save_deck(self.deck)
        self.app.show_results(self.deck["name"], self.correct, total)


class ResultsScreen(tk.Frame):
    def __init__(self, parent, app, deck_name, correct, total):
        super().__init__(parent)

        tk.Label(self, text="Quiz Complete", font=("Arial", 16, "bold")).pack(pady=10)

        if total:
            percent = round(100 * correct / total, 1)
            tk.Label(self, text=f"{correct}/{total} correct ({percent}%)", font=("Arial", 14)).pack(pady=5)
        else:
            tk.Label(self, text="No questions were answered.", font=("Arial", 14)).pack(pady=5)

        tk.Button(self, text="Quiz Again?", command=app.show_quiz_setup).pack(anchor="w", pady=5)
        tk.Button(self, text="Home", command=app.show_home).pack(anchor="w", pady=5)


class StatsScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Button(self, text="Back", command=app.show_home).pack(anchor="w", pady=5)
        tk.Label(self, text="Stats", font=("Arial", 16, "bold")).pack(anchor="w", pady=10)

        deck_names = storage.list_deck_names()
        if not deck_names:
            tk.Label(self, text="No decks available. Please create a deck first.", fg="red").pack(pady=20)
            return

        for name in deck_names:
            deck = storage.load_deck(name)

            tk.Label(self, text=f"Deck: {name}", font=("Arial", 14)).pack(anchor="w", pady=5)

            accuracy = models.deck_accuracy(deck)
            accuracy_text = f"All time accuracy : {accuracy}%" if accuracy is not None else "No sessions yet."
            tk.Label(self, text=accuracy_text).pack(anchor="w", padx=20)

            counts = {"Easy": 0, "Medium": 0, "Hard": 0, "New": 0}
            for card in deck["cards"]:
                label = models.difficulty(card) or "New"
                counts[label] += 1

            summary = f"Cards - Easy: {counts['Easy']}, Medium: {counts['Medium']}, Hard: {counts['Hard']}, New: {counts['New']}"
            tk.Label(self, text=summary).pack(anchor="w", padx=20)