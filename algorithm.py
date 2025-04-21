import tkinter as tk
from tkinter import ttk
import heapq
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# TO make a task:
class Task:
    def _init_(self, pid, burst, priority):
        self.pid, self.burst, self.priority = pid, burst, priority
    def _lt_(self, other):
        return (self.burst < other.burst) or (self.burst == other.burst and self.priority > other.priority)

class SchedulerApp:
    def _init_(self, root):
        self.root = root
        self.root.title("⚡ Energy-Efficient CPU Scheduler")
        self.setup_ui()
        self.tasks = []
        
    def setup_ui(self):
        self.root.configure(bg="#7B2CBF")
        
        # Header
        self.header = tk.Frame(self.root, bg="#7B2CBF")
        # self.header.pack(pady=20)
        tk.Label(self.header, text="⚡ Energy-Efficient CPU Scheduler", font=("Arial", 18), 
                bg="#2E3440", fg="#ECEFF4").pack()
        
        # Input Section
        input_frame = tk.Frame(self.root, bg="#3B4252", padx=20, pady=10)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Task ID:", bg="#3B4252", fg="#ECEFF4").grid(row=0, column=0, sticky="e")
        self.pid_entry = tk.Entry(input_frame, width=10)
        self.pid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Burst Time:", bg="#3B4252", fg="#ECEFF4").grid(row=1, column=0, sticky="e")
        self.burst_entry = tk.Entry(input_frame, width=10)
        self.burst_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Priority (1-5):", bg="#3B4252", fg="#ECEFF4").grid(row=2, column=0, sticky="e")
        self.priority_entry = tk.Entry(input_frame, width=10)
        self.priority_entry.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = tk.Frame(self.root, bg="#2E3440")
        button_frame.pack(pady=10)
        
        button_styles = [
            ("➕ Add Task", self.add_task, "#4CAF50"),      # Fresh green
            ("⏳ Schedule Tasks", self.schedule, "#2196F3"), # Pleasant blue
            ("❌ Exit", self.root.quit, "#F44336")          # Soft red
        ]
        
        for text, command, color in button_styles:
            tk.Button(button_frame, text=text, command=command, 
                     bg=color, fg="white", font=("Arial", 10, "bold"),
                     relief="raised", padx=15).pack(side="left", padx=5)
        
        # Task Table
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 12))  # Larger font for table content
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))  # Larger font for headers
        
        self.table = ttk.Treeview(self.root, columns=("PID", "Burst", "Priority"), show="headings")
        self.table.heading("PID", text="Task ID", anchor="center")
        self.table.heading("Burst", text="Burst Time", anchor="center")
        self.table.heading("Priority", text="Priority", anchor="center")
        self.table.column("PID", width=150, anchor="center")
        self.table.column("Burst", width=150, anchor="center")
        self.table.column("Priority", width=150, anchor="center")
        self.table.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Gantt Chart
        self.figure = Figure(figsize=(10, 3), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)
        
    def add_task(self):
        try:
            pid = int(self.pid_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get())
            if priority < 1 or priority > 5:
                raise ValueError
            self.tasks.append(Task(pid, burst, priority))
            self.table.insert("", "end", values=(pid, burst, priority))
            self.pid_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
        except:
            tk.messagebox.showerror("Error", "Invalid input!")
            
    def schedule(self):
        if not self.tasks:
            tk.messagebox.showwarning("Warning", "No tasks to schedule!")
            return
            
        heapq.heapify(self.tasks)
        scheduled = []
        energy = 0
        time = 0
        gantt_data = []
        
        while self.tasks:
            task = heapq.heappop(self.tasks)
            scheduled.append(task)
            task_energy = task.burst * (1 / task.priority)
            energy += task_energy
            gantt_data.append((task.pid, time, time + task.burst))
            time += task.burst
        
        # Update Gantt Chart
        self.plot.clear()
        for i, (pid, start, end) in enumerate(gantt_data):
            self.plot.broken_barh([(start, end - start)], (i - 0.4, 0.8), facecolors='tab:blue')
            self.plot.text((start + end) / 2, i, f"P{pid}", ha='center', va='center', color='white')
        self.plot.set_title("Gantt Chart (Task Execution Timeline)")
        self.plot.set_xlabel("Time")
        self.plot.set_yticks([])
        self.canvas.draw()
        
        tk.messagebox.showinfo("Scheduling Complete", f"Total Energy: {energy:.2f}\nEfficiency: {(1 - (energy / sum(t.burst for t in scheduled))) * 100:.1f}%")
    

if _name_ == "_main_":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
