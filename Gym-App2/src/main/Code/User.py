import tkinter as tk
from tkinter import messagebox

def submit():
    name = name_entry.get()
    height = height_entry.get()
    weight = weight_entry.get()
    goal = goal_var.get()
    vegetarian = "Yes" if vegetarian_var.get() else "No"
    restrictions = restrictions_entry.get()

    info = f"Name: {name}\nHeight: {height} cm\nWeight: {weight} kg\nGoal: {goal}\nVegetarian: {vegetarian}\nRestrictions: {restrictions}"
    messagebox.showinfo("User Info", info)

# Create window
root = tk.Tk()
root.title("User Info Form")
root.geometry("300x400")

# Name
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Height
tk.Label(root, text="Height (cm)").pack()
height_entry = tk.Entry(root)
height_entry.pack()

# Weight
tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

# Goal
tk.Label(root, text="Fitness Goal").pack()
goal_var = tk.StringVar(value="Bulk")
tk.Radiobutton(root, text="Bulk", variable=goal_var, value="Bulk").pack()
tk.Radiobutton(root, text="Cut", variable=goal_var, value="Cut").pack()

# Vegetarian
vegetarian_var = tk.BooleanVar()
tk.Checkbutton(root, text="Are you vegetarian?", variable=vegetarian_var).pack()

# Restrictions
tk.Label(root, text="Any dietary restrictions?").pack()
restrictions_entry = tk.Entry(root)
restrictions_entry.pack()

# Submit Button
tk.Button(root, text="Submit", command=submit).pack(pady=10)

root.mainloop()
