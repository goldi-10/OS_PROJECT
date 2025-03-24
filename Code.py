import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import deque

# FIFO Page Replacement Algorithm
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

# LRU Page Replacement Algorithm
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

# Function to visualize page replacement
def visualize_algorithm(pages, frames, algorithm):
    if algorithm == "FIFO":
        faults, memory_state = fifo_page_replacement(pages, frames)
    else:
        faults, memory_state = lru_page_replacement(pages, frames)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(f"{algorithm} Page Replacement Visualization")

    for i, state in enumerate(memory_state):
        ax.scatter([i] * len(state), state, label=f"Step {i+1}")

    ax.set_xlabel("Step")
    ax.set_ylabel("Pages in Memory")
    ax.legend(loc="upper right")
    plt.show()

    return faults

# GUI Application
def run_simulation():
    try:
        pages = list(map(int, entry_pages.get().split()))
        frames = int(entry_frames.get())
        algorithm = algo_choice.get()

        if frames <= 0 or len(pages) == 0:
            raise ValueError

        faults = visualize_algorithm(pages, frames, algorithm)
        messagebox.showinfo("Results", f"Total Page Faults: {faults}")

    except ValueError:
        messagebox.showerror("Input Error", "Enter valid numbers for pages and frames!")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Virtual Memory Simulator")

tk.Label(root, text="Page Reference String (space-separated):").grid(row=0, column=0)
entry_pages = tk.Entry(root)
entry_pages.grid(row=0, column=1)

tk.Label(root, text="Number of Frames:").grid(row=1, column=0)
entry_frames = tk.Entry(root)
entry_frames.grid(row=1, column=1)

algo_choice = tk.StringVar(value="FIFO")
tk.Label(root, text="Algorithm:").grid(row=2, column=0)
tk.Radiobutton(root, text="FIFO", variable=algo_choice, value="FIFO").grid(row=2, column=1)
tk.Radiobutton(root, text="LRU", variable=algo_choice, value="LRU").grid(row=3, column=1)

tk.Button(root, text="Run Simulation", command=run_simulation).grid(row=4, columnspan=2)

root.mainloop()

