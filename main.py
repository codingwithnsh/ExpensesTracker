# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:07:41 2024

@author: PRO
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create or load expense data
def load_data():
    try:
        return pd.read_csv('expenses.csv', parse_dates=['Date'])
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def save_data(df):
    df.to_csv('expenses.csv', index=False)

# Create main application window
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Expense Tracker")
        self.root.geometry("1000x600")
        self.df = load_data()

        self.category_list = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Other']
        
        self.create_widgets()
        self.update_expenses_table()
        self.close_button = None  # Initialize close button variable

    def create_widgets(self):
        # Header
        self.header_label = ttk.Label(self.root, text="Expense Tracker", font=("Arial", 24), background='#4CAF50', foreground='white')
        self.header_label.pack(fill='x', pady=10)

        # Expense input frame (use tk.Frame instead of ttk.Frame for background color)
        self.input_frame = tk.Frame(self.root, bg='#f5f5f5')  # Use tk.Frame here without padding
        self.input_frame.pack(fill='x', padx=20, pady=20)  # Use padding with pack() method

        ttk.Label(self.input_frame, text="Amount ($):", background='#f5f5f5').grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Category:", background='#f5f5f5').grid(row=0, column=2, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(self.input_frame, values=self.category_list, state="readonly")
        self.category_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.category_combobox.set(self.category_list[0])

        ttk.Label(self.input_frame, text="Description:", background='#f5f5f5').grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.input_frame)
        self.description_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='ew')

        self.add_button = ttk.Button(self.input_frame, text="Add Expense", command=self.add_expense, style="TButton")
        self.add_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Table Frame
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill='both', expand=True)

        self.table = ttk.Treeview(self.table_frame, columns=('Date', 'Category', 'Amount', 'Description'), show='headings', height=10)
        self.table.heading('Date', text='Date')
        self.table.heading('Category', text='Category')
        self.table.heading('Amount', text='Amount ($)')
        self.table.heading('Description', text='Description')

        # Style Table Rows
        self.table.tag_configure("oddrow", background="#f9f9f9")
        self.table.tag_configure("evenrow", background="#e3e3e3")

        self.table.pack(fill='both', expand=True)

        # Create Graph Button
        self.graph_button = ttk.Button(self.root, text="Generate Expense Graph", command=self.show_graph, style="TButton")
        self.graph_button.pack(pady=10)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combobox.get()
            description = self.description_entry.get()
            date = datetime.now()

            new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
            self.df = pd.concat([self.df, new_expense], ignore_index=True)
            save_data(self.df)

            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_input_fields()
            self.update_expenses_table()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def update_expenses_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for idx, row in self.df.iterrows():
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.table.insert('', 'end', values=(row['Date'].strftime('%Y-%m-%d'), row['Category'], row['Amount'], row['Description']), tags=(tag,))

    def clear_input_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def show_graph(self):
        if self.df.empty:
            messagebox.showwarning("No Data", "There are no expenses to display.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))

        # Group by category and sum the amounts
        grouped_data = self.df.groupby('Category')['Amount'].sum().reset_index()

        # Create bar chart
        ax.bar(grouped_data['Category'], grouped_data['Amount'], color='skyblue')

        ax.set_xlabel('Category')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Expense Breakdown by Category')

        # Display the plot
        canvas = FigureCanvasTkAgg(fig, self.root)
        canvas.get_tk_widget().pack(pady=10)
        canvas.draw()

        # If there's a graph already open, destroy it first to avoid multiple buttons
        if self.close_button:
            self.close_button.destroy()

        # Add a button to close the graph
        self.close_button = ttk.Button(self.root, text="Close Graph", command=lambda: self.close_graph(canvas))
        self.close_button.pack(pady=5)

    def close_graph(self, canvas):
        canvas.get_tk_widget().destroy()
        self.close_button.destroy()  # Remove the close button after the graph is closed
        self.close_button = None  # Reset the button variable to avoid redundant buttons

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
