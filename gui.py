''' Tkinter GUI for the Flashcard app '''

import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
 
import models
import storage
 
# style constants
PANEL = "#ffffff"
PRIMARY = "#137e75"
MUTED = "#6b7280"
GOOD = "#10843a"
BAD = "#d33a3a"


class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard App")
        self.geometry("760x540")
        
