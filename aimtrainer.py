import tkinter as tk
import random
import time
class AimTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Aim Trainer")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='light gray')
        self.canvas.pack()
        
        self.start_button = tk.Button(root, text="Начать тренировку", command=self.start_training)
        self.start_button.pack()
        
        self.targets = []
        self.reaction_times = []
        self.current_target = None
        self.training_running = False
        self.start_time = 0
        self.clicks = 0
        self.best_time = float('inf')
    def start_training(self):
        self.training_running = True
        self.start_button.pack_forget()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.start_time = time.time()
        self.clicks = 0
        self.reaction_times = []
        self.best_time = float('inf')
        self.spawn_target()
    def spawn_target(self):
        if not self.training_running:
            return
        x = random.randint(50, self.canvas.winfo_width() - 50)
        y = random.randint(50, self.canvas.winfo_height() - 50)
        self.current_target = self.canvas.create_oval(x-25, y-25, x+25, y+25, fill='red')
        self.target_start_time = time.time()
    def on_canvas_click(self, event):
        if self.current_target:
            click_time = time.time()
            reaction_time = click_time - self.target_start_time
            self.reaction_times.append(reaction_time)
            if reaction_time < self.best_time:
                self.best_time = reaction_time
            self.clicks += 1
            self.canvas.delete(self.current_target)
            self.current_target = None
            self.spawn_target()
    def stop_training(self):
        self.training_running = False
        self.canvas.unbind("<Button-1>")
        end_time = time.time()
        total_time = end_time - self.start_time
        average_time = sum(self.reaction_times) / len(self.reaction_times) if self.reaction_times else 0
        self.show_statistics(total_time, average_time, self.clicks, self.best_time)
        self.start_button.pack()
        
    def show_statistics(self, total_time, average_time, clicks, best_time):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика")
        tk.Label(stats_window, text=f"Всего времени: {total_time:.2f} секунд").pack()
        tk.Label(stats_window, text=f"Среднее время реакции: {average_time:.2f} секунд").pack()
        tk.Label(stats_window, text=f"Количество кликов: {clicks}").pack()
        tk.Label(stats_window, text=f"Лучшее время: {best_time:.2f} секунд").pack()
if __name__ == "__main__":
    root = tk.Tk()
    app = AimTrainer(root)
    root.mainloop()
