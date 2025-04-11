import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from collections import deque

# ------------------ Page Replacement Algorithms ------------------ #
def fifo_page_replacement(pages, frames):
    queue = deque()
    page_faults = 0
    memory_state = []

    for page in pages:
        if page not in queue:
            if len(queue) < frames:
                queue.append(page)
            else:
                queue.popleft()
                queue.append(page)
            page_faults += 1
        memory_state.append(list(queue))

    return page_faults, memory_state


def lru_page_replacement(pages, frames):
    memory = []
    page_faults = 0
    memory_state = []

    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        else:
            memory.remove(page)
            memory.append(page)
        memory_state.append(list(memory))

    return page_faults, memory_state

# ------------------ Visualization ------------------ #
def visualize_algorithm(pages, frames, algorithm):
    if algorithm == "FIFO":
        faults, memory_state = fifo_page_replacement(pages, frames)
    else:
        faults, memory_state = lru_page_replacement(pages, frames)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(f"{algorithm} Page Replacement", fontsize=14, fontweight='bold')

    for step, state in enumerate(memory_state):
        for i, page in enumerate(state):
            ax.text(step, frames - i - 1, str(page),
                    bbox=dict(facecolor='skyblue', edgecolor='black', boxstyle='round,pad=0.3'),
                    ha='center', va='center', fontsize=10)

    ax.set_xlim(-1, len(memory_state))
    ax.set_ylim(-1, frames)
    ax.set_xlabel("Step", fontsize=12)
    ax.set_ylabel("Frame Index", fontsize=12)
    ax.set_yticks(range(frames))
    ax.grid(True)
    plt.tight_layout()
    plt.show()

    return faults

# ------------------ Simulation Trigger ------------------ #
def run_simulation():
    try:
        pages = list(map(int, entry_pages.get().split()))
        frames = int(entry_frames.get())
        algorithm = algo_choice.get()

        if frames <= 0 or not pages:
            raise ValueError

        faults = visualize_algorithm(pages, frames, algorithm)
        messagebox.showinfo("Simulation Complete", f"Total Page Faults using {algorithm}: {faults}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for pages and frames!")

# ------------------ GUI Setup ------------------ #
root = tk.Tk()
root.title("Virtual Memory Simulator")
root.geometry("400x250")
root.resizable(False, False)

# Use a custom style
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("TRadiobutton", font=("Segoe UI", 10))

frame = ttk.Frame(root, padding=20)
frame.pack(fill='both', expand=True)

# Input for page string
ttk.Label(frame, text="Page Reference String:").grid(row=0, column=0, sticky='w')
entry_pages = ttk.Entry(frame, width=30)
entry_pages.grid(row=0, column=1, pady=5)

# Input for frame count
ttk.Label(frame, text="Number of Frames:").grid(row=1, column=0, sticky='w')
entry_frames = ttk.Entry(frame, width=10)
entry_frames.grid(row=1, column=1, pady=5, sticky='w')

# Algorithm selection
ttk.Label(frame, text="Choose Algorithm:").grid(row=2, column=0, sticky='w')
algo_choice = tk.StringVar(value="FIFO")
ttk.Radiobutton(frame, text="FIFO", variable=algo_choice, value="FIFO").grid(row=2, column=1, sticky='w')
ttk.Radiobutton(frame, text="LRU", variable=algo_choice, value="LRU").grid(row=3, column=1, sticky='w')

# Run Button
ttk.Button(frame, text="Run Simulation", command=run_simulation).grid(row=4, column=0, columnspan=2, pady=15)

root.mainloop()
