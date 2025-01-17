import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

# File to store expenses
FILE_NAME = "weekly_expense_tracker.xlsx"

# Initialize or load existing data
def initialize_data():
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
    global expense_data
    try:
        amount = float(amount)
        entry = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Category": "Income" if is_income else category,
            "Amount": amount if is_income else -amount,
            "Income": amount if is_income else 0,
        }])
        expense_data = pd.concat([expense_data, entry], ignore_index=True)
        save_data(expense_data)
        update_summary()

        # Clear input fields
        if not is_income:
            category_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

        messagebox.showinfo("Success", "Entry added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")

# Update summary in GUI
def update_summary():
    global expense_data
    total_income = expense_data["Income"].sum()
    total_expenses = expense_data["Amount"].sum()
    savings = total_income + total_expenses

    summary_var.set(f"Total Income: ${total_income:.2f}\nTotal Expenses: ${-total_expenses:.2f}\nSavings: ${savings:.2f}")

    breakdown = expense_data[expense_data["Category"] != "Income"]
    breakdown_summary = breakdown.groupby("Category")["Amount"].sum()
    breakdown_text = "".join(
        [f"{cat}: ${-amt:.2f}\n" for cat, amt in breakdown_summary.items()]
    )
    breakdown_var.set(breakdown_text)

# Generate improvement suggestions
def improvement_suggestions():
    global expense_data
    breakdown = expense_data[expense_data["Category"] != "Income"]
    category_totals = breakdown.groupby("Category")["Amount"].sum()
    suggestions = "Consider reducing spending on:\n"

    for category, total in category_totals.items():
        if abs(total) > 0.3 * expense_data["Income"].sum():  # Example: if expense > 30% of income
            suggestions += f"- {category}: ${-total:.2f}\n"

    messagebox.showinfo("Suggestions", suggestions)

# GUI setup
app = tk.Tk()
app.title("Weekly Expense Tracker")
app.geometry("500x600")

# Global variables
expense_data = initialize_data()
summary_var = tk.StringVar()
breakdown_var = tk.StringVar()

# Layout
frame = ttk.Frame(app, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Income Section
income_label = ttk.Label(frame, text="Add Income")
income_label.grid(row=0, column=0, columnspan=2, pady=5)

income_entry = ttk.Entry(frame, width=25)
income_entry.grid(row=1, column=0, padx=5)

income_button = ttk.Button(
    frame, text="Add Income", command=lambda: add_entry("Income", income_entry.get(), is_income=True)
)
income_button.grid(row=1, column=1, padx=5)

# Expense Section
expense_label = ttk.Label(frame, text="Add Expense")
expense_label.grid(row=2, column=0, columnspan=2, pady=10)

category_label = ttk.Label(frame, text="Category")
category_label.grid(row=3, column=0, padx=5)

category_entry = ttk.Entry(frame, width=25)
category_entry.grid(row=3, column=1, padx=5)

amount_label = ttk.Label(frame, text="Amount")
amount_label.grid(row=4, column=0, padx=5)

amount_entry = ttk.Entry(frame, width=25)
amount_entry.grid(row=4, column=1, padx=5)

expense_button = ttk.Button(
    frame,
    text="Add Expense",
    command=lambda: add_entry(category_entry.get(), amount_entry.get()),
)
expense_button.grid(row=5, column=0, columnspan=2, pady=10)

# Summary Section
summary_label = ttk.Label(frame, text="Summary", font=("Arial", 14))
summary_label.grid(row=6, column=0, columnspan=2, pady=10)

summary_text = ttk.Label(frame, textvariable=summary_var, justify=tk.LEFT)
summary_text.grid(row=7, column=0, columnspan=2, pady=5)

breakdown_label = ttk.Label(frame, text="Expense Breakdown", font=("Arial", 14))
breakdown_label.grid(row=8, column=0, columnspan=2, pady=10)

breakdown_text = ttk.Label(frame, textvariable=breakdown_var, justify=tk.LEFT)
breakdown_text.grid(row=9, column=0, columnspan=2, pady=5)

# Suggestions Section
suggestion_button = ttk.Button(
    frame, text="Get Improvement Suggestions", command=improvement_suggestions
)
suggestion_button.grid(row=10, column=0, columnspan=2, pady=10)

# Initialize summary
def init():
    update_summary()

init()
app.mainloop()
