import tkinter as tk
from tkinter import ttk
from db import ActivityDB
import time
import threading

class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro con Actividades")
        self.geometry("400x300")
        self.db = ActivityDB()
        self.history_button = ttk.Button(self, text="Ver Historial", command=self.show_history)
        self.history_button.pack(pady=5)

        
        self.current_activity = tk.StringVar()
        self.timer_label = tk.Label(self, text="25:00", font=("Helvetica", 32))
        self.timer_label.pack(pady=10)

        self.activity_entry = ttk.Entry(self, textvariable=self.current_activity)
        self.activity_entry.pack(pady=5)
        self.activity_entry.insert(0, "Escribe tu actividad")

        self.start_button = ttk.Button(self, text="Iniciar Pomodoro", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.is_running = False

    def start_timer(self):
        if self.is_running:
            return
        self.is_running = True
        activity = self.current_activity.get()
        threading.Thread(target=self.run_pomodoro, args=(activity,)).start()

    def run_pomodoro(self, activity):
        seconds = 25 * 60  # 25 minutos
        while seconds > 0 and self.is_running:
            mins, secs = divmod(seconds, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.update()
            time.sleep(1)
            seconds -= 1
        self.db.add_session(activity, 25)
        self.timer_label.config(text="¡Descanso!")
        self.is_running = False

    def show_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("Historial de Actividades")
        history_window.geometry("400x300")

        records = self.db.get_all_sessions()

        text = tk.Text(history_window)
        text.pack(expand=True, fill="both")

        text.insert("end", f"{'Actividad':<20} {'Duración':<10} {'Fecha y Hora'}\n")
        text.insert("end", "-" * 60 + "\n")
        for r in records:
            text.insert("end", f"{r[0]:<20} {r[1]} min     {r[2]}\n")
