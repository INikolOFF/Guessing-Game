import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import json
import os


class GuessNumberGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎯 Guess the Number")
        self.window.geometry("550x800")
        self.window.resizable(False, False)
        self.window.configure(bg="#1a1a2e")

        self.secret_number = 0
        self.attempts = 0
        self.max_range = 100
        self.best_scores = {"Easy": None, "Medium": None, "Hard": None}
        self.guess_history = []
        self.game_active = False
        self.stats_file = "guess_stats.json"

        self.load_stats()
        self.setup_ui()
        self.bind_shortcuts()

    def load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.best_scores = json.load(f)
            except:
                pass

    def save_stats(self):
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.best_scores, f)
        except:
            pass

    def bind_shortcuts(self):
        self.window.bind("<Return>", lambda e: self.make_guess())
        self.window.bind("<Control-n>", lambda e: self.start_game())
        self.window.bind("<Control-r>", lambda e: self.start_game())
        self.window.bind("<Escape>", lambda e: self.window.destroy())

    def setup_ui(self):
        header_frame = tk.Frame(self.window, bg="#16213e", height=80)
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            header_frame,
            text="🎯 GUESS THE NUMBER",
            font=("Arial", 24, "bold"),
            bg="#16213e",
            fg="#00ff88"
        ).pack(pady=20)

        main_container = tk.Frame(self.window, bg="#1a1a2e")
        main_container.pack(expand=True, fill="both", padx=20)

        difficulty_frame = tk.LabelFrame(
            main_container,
            text="🎮 Select Difficulty",
            font=("Arial", 12, "bold"),
            bg="#0f3460",
            fg="#00ff88",
            padx=20,
            pady=15
        )
        difficulty_frame.pack(pady=10, fill="x")

        self.difficulty_var = tk.StringVar(value="Medium")

        for text, value in [
            ("Easy (1–50)", "Easy"),
            ("Medium (1–100)", "Medium"),
            ("Hard (1–200)", "Hard")
        ]:
            tk.Radiobutton(
                difficulty_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                bg="#0f3460",
                fg="white",
                selectcolor="#16213e",
                font=("Arial", 10),
                command=self.update_difficulty_display
            ).pack(anchor="w", pady=3)

        self.start_btn = tk.Button(
            main_container,
            text="🚀 START NEW GAME (Ctrl+N)",
            command=self.start_game,
            font=("Arial", 14, "bold"),
            bg="#00ff88",
            fg="#1a1a2e",
            height=2,
            cursor="hand2"
        )
        self.start_btn.pack(pady=15, fill="x")

        info_frame = tk.Frame(main_container, bg="#0f3460", padx=15, pady=15)
        info_frame.pack(pady=10, fill="x")

        self.range_label = tk.Label(
            info_frame,
            text="Press START to begin!",
            bg="#0f3460",
            fg="#00ff88",
            font=("Arial", 12, "bold")
        )
        self.range_label.pack()

        self.attempts_label = tk.Label(
            info_frame,
            text="Attempts: 0",
            bg="#0f3460",
            fg="white",
            font=("Arial", 11)
        )
        self.attempts_label.pack(pady=5)

        self.best_score_label = tk.Label(
            info_frame,
            text="Best Score: -",
            bg="#0f3460",
            fg="#ffd700",
            font=("Arial", 11, "bold")
        )
        self.best_score_label.pack()

        input_frame = tk.Frame(main_container, bg="#1a1a2e")
        input_frame.pack(pady=15)

        tk.Label(
            input_frame,
            text="Your Guess:",
            bg="#1a1a2e",
            fg="white",
            font=("Arial", 11)
        ).pack()

        self.guess_entry = tk.Entry(
            input_frame,
            font=("Arial", 18, "bold"),
            justify="center",
            width=12
        )
        self.guess_entry.pack(pady=5)

        self.guess_btn = tk.Button(
            input_frame,
            text="🎲 GUESS (Enter)",
            command=self.make_guess,
            font=("Arial", 12, "bold"),
            state="disabled",
            cursor="hand2",
            bg="#4CAF50",
            fg="white"
        )
        self.guess_btn.pack(pady=10)

        progress_frame = tk.LabelFrame(
            main_container,
            text="🎯 Proximity Meter",
            font=("Arial", 12, "bold"),
            bg="#0f3460",
            fg="#00ff88",
            padx=10,
            pady=10
        )
        progress_frame.pack(pady=10, fill="x")

        self.progress_canvas = tk.Canvas(
            progress_frame,
            height=30,
            bg="#16213e",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill="x")

        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 0, 30, fill="#00ff88", outline=""
        )

        self.result_label = tk.Label(
            main_container,
            text="",
            bg="#1a1a2e",
            fg="white",
            font=("Arial", 16, "bold")
        )
        self.result_label.pack(pady=10)

        self.hint_label = tk.Label(
            main_container,
            text="",
            bg="#1a1a2e",
            fg="#aaa",
            font=("Arial", 10)
        )
        self.hint_label.pack()

        history_frame = tk.LabelFrame(
            main_container,
            text="📜 Guess History",
            font=("Arial", 12, "bold"),
            bg="#0f3460",
            fg="#00ff88",
            padx=10,
            pady=10
        )
        history_frame.pack(pady=10, fill="both", expand=True)

        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            height=8,
            font=("Courier", 12),
            bg="#16213e",
            fg="#00ff88"
        )
        self.history_text.pack(fill="both", expand=True)

    def update_difficulty_display(self):
        best = self.best_scores.get(self.difficulty_var.get())
        self.best_score_label.config(
            text=f"Best Score: {best}" if best else "Best Score: -"
        )

    def get_proximity_hint(self, difference):
        if difference == 0:
            return "🎯 PERFECT!"
        elif difference <= 3:
            return "🔥 МНОГО ГОРЕЩО!"
        elif difference <= 10:
            return "🌡️ Горещо!"
        elif difference <= 20:
            return "💨 Топло"
        elif difference <= 50:
            return "❄️ Студено"
        else:
            return "🧊 Много студено"

    def update_progress_bar(self, difference):
        max_diff = self.max_range
        proximity = max(0, 1 - (difference / max_diff))

        width = self.progress_canvas.winfo_width()
        bar_width = width * proximity

        if proximity > 0.9:
            color = "#00ff88"
        elif proximity > 0.7:
            color = "#ffd700"
        elif proximity > 0.4:
            color = "#ff9500"
        else:
            color = "#ff6b6b"

        self.progress_canvas.coords(self.progress_bar, 0, 0, bar_width, 30)
        self.progress_canvas.itemconfig(self.progress_bar, fill=color)

    def add_to_history(self, guess, result, difference):
        self.history_text.config(state="normal")
        proximity = self.get_proximity_hint(difference)
        entry = f"#{self.attempts}: {guess} → {result} | {proximity}\n"
        self.history_text.insert("1.0", entry)
        self.history_text.config(state="disabled")

    def start_game(self):
        self.attempts = 0
        self.guess_history.clear()
        self.game_active = True

        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        self.history_text.config(state="disabled")

        self.progress_canvas.coords(self.progress_bar, 0, 0, 0, 30)

        difficulty = self.difficulty_var.get()
        self.max_range = {"Easy": 50, "Medium": 100, "Hard": 200}[difficulty]
        self.secret_number = random.randint(1, self.max_range)

        self.range_label.config(text=f"Guess a number between 1 and {self.max_range}")
        self.attempts_label.config(text="Attempts: 0")
        self.result_label.config(text="Good luck! 🍀", fg="white")
        self.hint_label.config(text="")
        self.guess_btn.config(state="normal")
        self.guess_entry.config(state="normal")
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        self.update_difficulty_display()

    def make_guess(self):
        if not self.game_active:
            return

        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")
            return

        if not 1 <= guess <= self.max_range:
            messagebox.showwarning("Out of range", f"Please enter a number between 1 and {self.max_range}")
            return

        if guess in self.guess_history:
            messagebox.showinfo("Already tried", f"You already tried {guess}!")
            self.guess_entry.delete(0, tk.END)
            return

        self.guess_history.append(guess)
        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        difference = abs(guess - self.secret_number)
        self.update_progress_bar(difference)

        if guess < self.secret_number:
            result = "📈 TOO LOW"
            self.result_label.config(text=result, fg="#ff6b6b")
            self.add_to_history(guess, "Low", difference)
            proximity = self.get_proximity_hint(difference)
            self.hint_label.config(text=proximity)
        elif guess > self.secret_number:
            result = "📉 TOO HIGH"
            self.result_label.config(text=result, fg="#4ecdc4")
            self.add_to_history(guess, "High", difference)
            proximity = self.get_proximity_hint(difference)
            self.hint_label.config(text=proximity)
        else:
            self.game_active = False
            self.result_label.config(text=f"🎉 CORRECT! The number was {self.secret_number}", fg="#00ff88")
            self.hint_label.config(text=f"You won in {self.attempts} attempts!")
            self.add_to_history(guess, "✓ WIN", 0)
            self.guess_btn.config(state="disabled")
            self.guess_entry.config(state="disabled")

            diff = self.difficulty_var.get()
            current_best = self.best_scores.get(diff)

            if not current_best or self.attempts < current_best:
                self.best_scores[diff] = self.attempts
                self.save_stats()
                self.update_difficulty_display()
                messagebox.showinfo("New Record! 🏆",
                                    f"Congratulations! New best score: {self.attempts} attempts!")
            else:
                messagebox.showinfo("Victory! 🎉",
                                    f"You won in {self.attempts} attempts!\nBest score: {current_best}")

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    GuessNumberGame().run()