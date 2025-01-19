# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 12:00:53 2025

@author: Programmer
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

# File to store expenses
FILE_NAME = "weekly_expense_tracker.xlsx"

# Initialize or load existing data
def initialize_data():
    global expense_data
    expense_data = None
    try:
        data = pd.read_excel(FILE_NAME)
    except FileNotFoundError:
        data = pd.DataFrame(columns=["Date", "Category", "Amount", "Income"])
        data.to_excel(FILE_NAME, index=False)
    return data

# Save data to Excel
def save_data(data):
    data.to_excel(FILE_NAME, index=False)

# Add income or expense

def add_entry(category, amount, is_income=False):
    try:
        amount = float(amount)
        entry = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Category": "Income" if is_income else category,
            "Amount": amount if is_income else -amount,
            "Income": amount if is_income else 0,
        }])
        global expense_data
        expense_data = pd.concat([expense_data, entry], ignore_index=True)
        save_data(expense_data)
        update_summary()

        # Clear input fields
        if not is_income:
            category_dropdown.set('')
            amount_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Entry added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

# Update summary in GUI
def update_summary():
    global expense_data
    if expense_data.empty:
        summary_var.set("No entries yet.")
        breakdown_var.set("No entries yet.")
        return
    
    total_income = expense_data["Income"].sum()
    total_expenses = expense_data["Amount"].sum()
    savings = total_income + total_expenses if not expense_data.empty else 0

    summary_var.set(f"Total Income: ₹{total_income:.2f}\nTotal Expenses: ₹{-total_expenses:.2f}\nSavings: ₹{savings:.2f}")

    breakdown = expense_data[expense_data["Category"] != "Income"]
    breakdown_summary = breakdown.groupby("Category")["Amount"].sum()
    breakdown_text = "".join(
        [f"{cat}: ₹{-amt:.2f}\n" for cat, amt in breakdown_summary.items()]
    )
    breakdown_var.set(breakdown_text)

# Generate improvement suggestions
global expense_data
def improvement_suggestions():
    global expense_data
    global expense_data
    breakdown = expense_data[expense_data["Category"] != "Income"]
    category_totals = breakdown.groupby("Category")["Amount"].sum()
    suggestions = "Consider reducing spending on:\n"

    for category, total in category_totals.items():
        if abs(total) > 0.3 * expense_data["Income"].sum():  # Example: if expense > 30% of income
            suggestions += f"- {category}: ₹{-total:.2f}\n"

    messagebox.showinfo("Suggestions", suggestions)

# GUI setup
app = tk.Tk()
app.title("Weekly Expense Tracker")
app.geometry("700x800")
app.configure(bg="#f2f9ff")

# Global variables
expense_data = None
expense_data = initialize_data()
summary_var = tk.StringVar()
breakdown_var = tk.StringVar()

# Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f2f9ff")
style.configure("TLabel", background="#f2f9ff", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
style.configure("Header.TLabel", font=("Arial", 16, "bold"), background="#004d99", foreground="#ffffff")

# Layout
frame = ttk.Frame(app, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Income Section
income_label = ttk.Label(frame, text="Add Income", style="Header.TLabel")
income_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

income_entry = ttk.Entry(frame, width=30, font=("Arial", 12))
income_entry.grid(row=1, column=0, padx=10, pady=5)

income_button = ttk.Button(
    frame, text="Add Income", command=lambda: add_entry("Income", income_entry.get(), is_income=True)
)
income_button.grid(row=1, column=1, padx=10, pady=5)

# Expense Section
expense_label = ttk.Label(frame, text="Add Expense", style="Header.TLabel")
expense_label.grid(row=2, column=0, columnspan=2, pady=20, sticky="ew")

category_label = ttk.Label(frame, text="Category:")
category_label.grid(row=3, column=0, padx=10, sticky=tk.W)

category_dropdown = ttk.Combobox(frame, width=28, font=("Arial", 12), state="readonly")
category_dropdown['values'] = ['Food', 'Utilities', 'Transport', 'Medical', 'Entertainment', 'Other']
category_dropdown.grid(row=3, column=1, padx=10, pady=5)

amount_label = ttk.Label(frame, text="Expense Amount:")
amount_label.grid(row=4, column=0, padx=10, sticky=tk.W)

amount_entry = tk.Entry(frame, width=30, font=("Arial", 12), bg="#e6f2ff", highlightbackground="#b3d9ff", highlightthickness=1)
amount_entry = ttk.Entry(frame, width=30, font=("Arial", 12))
new_amount_entry = ttk.Entry(frame, width=30, font=("Arial", 12))
new_amount_label = ttk.Label(frame, text="New Amount:")
new_amount_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
new_amount_entry.grid(row=5, column=1, padx=10, pady=5)

expense_button = ttk.Button(
    frame,
    text="Add Expense",
command=lambda: add_entry(category_dropdown.get(), amount_entry.get()),
)
expense_button.grid(row=5, column=0, columnspan=2, pady=10)

# Summary Section
summary_label = ttk.Label(frame, text="Summary", style="Header.TLabel")
summary_label.grid(row=6, column=0, columnspan=2, pady=20, sticky="ew")

summary_text = ttk.Label(frame, textvariable=summary_var, justify=tk.LEFT, font=("Arial", 12), background="#d9ecff", relief="solid")
summary_text.grid(row=7, column=0, columnspan=2, pady=10, sticky=tk.W)

breakdown_label = ttk.Label(frame, text="Expense Breakdown", style="Header.TLabel")
breakdown_label.grid(row=8, column=0, columnspan=2, pady=20, sticky="ew")

breakdown_text = ttk.Label(frame, textvariable=breakdown_var, justify=tk.LEFT, font=("Arial", 12), background="#d9ecff", relief="solid")
breakdown_text.grid(row=9, column=0, columnspan=2, pady=10, sticky=tk.W)

# Suggestions Section
suggestion_button = ttk.Button(
    frame, text="Get Improvement Suggestions", command=improvement_suggestions
)
suggestion_button.grid(row=10, column=0, columnspan=2, pady=20)

# Initialize summary
def init():
    update_summary()

init()
app.mainloop()