# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 11:14:33 2024

@author: madava kripa
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os



# Check if the Excel file exists, and load or create it
def load_data():
    if os.path.exists('expenses.xlsx'):
        return pd.read_excel('expenses.xlsx', parse_dates=['Date'])
    else:
        # If the file doesn't exist, create a new DataFrame with the necessary columns
        return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def save_data(df):
    df.to_excel('expenses.xlsx', index=False)
    
def load_budget_data():
    if os.path.exists('budget_data.xlsx'):
        budget_df = pd.read_excel('budget_data.xlsx', index_col=0)
        return {
            "income": budget_df.loc['Income', 'Amount'],
            "savings": budget_df.loc['Savings', 'Amount'],
            
        }
    else:
        return {}

    
def save_budget_data(budget_data):
    budget_df = pd.DataFrame({
        'Amount': [
            budget_data['income'],
            budget_data['savings'],
            
        ]
    }, index=['Income', 'Savings'])
    


# Create main application window
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Expense Tracker")
        self.root.geometry("1000x600")
        self.df = load_data()
        self.budget_data = load_budget_data()  # Load saved budget data
     

        self.category_list = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Medical' , 'Others']
        
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

        ttk.Label(self.input_frame, text="Amount (₹):", background='#f5f5f5').grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Category:", background='#f5f5f5').grid(row=0, column=2, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(self.input_frame, values=self.category_list, state="readonly")
        self.category_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.category_combobox.set(self.category_list[0])

        ttk.Label(self.input_frame, text="Description:", background='#f5f5f5').grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.input_frame)
        self.description_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky='ew')

        self.add_expense_button = ttk.Button(self.input_frame, text="Add Expense", command=self.add_expense, style="TButton")
        self.add_expense_button.grid(row=2, column=2, columnspan=4, pady=10)

        self.give_advice_button = ttk.Button(self.input_frame, text="Give Advice", command=self.give_advice, style="TButton")
        self.give_advice_button.grid(row=2, column=0, columnspan=4, pady=10)
        
        
        ttk.Label(self.input_frame, text="Income (₹):", background='#f5f5f5').grid(row=3, column=0, padx=5, pady=5)
        self.income_entry = ttk.Entry(self.input_frame)
        self.income_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Savings (₹):", background='#f5f5f5').grid(row=3, column=2, padx=5, pady=5)
        self.savings_entry = ttk.Entry(self.input_frame)
        self.savings_entry.grid(row=3, column=3, padx=5, pady=5)

        # Button to save Income and Savings
        self.save_budget_button = ttk.Button(self.input_frame, text="Save Budget Info", command=self.save_budget_info)
        self.save_budget_button.grid(row=4, column=0, columnspan=4, pady=10)
        
 
        # Table Frame
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill='both', expand=True)

        self.table = ttk.Treeview(self.table_frame, columns=('Date', 'Category', 'Amount', 'Description'), show='headings', height=10)
        self.table.heading('Date', text='Date')
        self.table.heading('Category', text='Category')
        self.table.heading('Amount', text='Amount (₹)')
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
    
    def save_budget_info(self):
        # Collect the values for Income and Savings
        income = self.income_entry.get()
        savings = self.savings_entry.get()

        if not income or not savings:
            messagebox.showerror("Missing Data", "Income and Savings are required fields.")
            return

        try:
            income = float(income)
            savings = float(savings)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for Income and Savings.")
            return

        # Update the budget data
        self.budget_data["income"] = income
        self.budget_data["savings"] = savings

        # Save the budget data to Excel
        save_budget_data(self.budget_data)

        messagebox.showinfo("Success", "Budget Info (Income and Savings) saved successfully!")

    def show_graph(self):
        if self.df.empty:
            messagebox.showwarning("No Data", "There are no expenses to display.")
            return

        fig, ax = plt.subplots(figsize=(6,5))

        # Group by category and sum the amounts
        grouped_data = self.df.groupby('Category')['Amount'].sum().reset_index()

        # Create bar chart
        ax.bar(grouped_data['Category'], grouped_data['Amount'], color='skyblue')

        ax.set_xlabel('Category')
        ax.set_ylabel('Amount (₹)')
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
        self.close_button.pack(pady=10)

    def close_graph(self, canvas):
        canvas.get_tk_widget().destroy()
        self.close_button.destroy()  # Remove the close button after the graph is closed
        self.close_button = None  # Reset the button variable to avoid redundant buttons
    def give_advice(self):
        if self.df.empty:
            messagebox.showinfo("Advice", "You have no recorded expenses to analyze.")
            return

    # Calculate total spending by category
        category_spending = self.df.groupby('Category')['Amount'].sum().reset_index()
        advice = ""

       # Retrieve the budget information (income and savings)
        income = self.budget_data.get('income', 0)
        savings = self.budget_data.get('savings', 0)
    
    # Check if income and savings data exists, otherwise provide a basic threshold
        if income == 0:
           messagebox.showwarning("Missing Budget Info", "Income is not set. Please set your income to get more accurate advice.")
           return
    
    # Dynamic thresholds based on income or savings
        for _, row in category_spending.iterrows():
             category_name = row['Category']
             amount_spent = row['Amount']
        
        # Set a default threshold
             threshold = 50000 # Default to 15000 for categories like Medical, Utilities, etc.

        # Dynamic threshold based on category
             if category_name in ['Entertainment', 'Food', 'Transport']:
               threshold = income * 0.05  # 5% of income for discretionary categories like Entertainment, Food, etc.
             elif category_name in ['Medical', 'Utilities']:
                 threshold = savings * 0.2 if savings > 0 else 20000  # 20% of savings for medical/utility expenses or a fixed amount

        # Provide advice if the spending exceeds the threshold
             if amount_spent > threshold:
               advice += f"\nYou are spending a lot on {category_name}. Consider reviewing your expenses in this category."

    # If there's no significant overspending, provide some general advice
        if not advice:
              advice = "Your spending is within reasonable limits based on your income and savings."

    # Show the advice in a messagebox
        messagebox.showinfo("Expense Advice", advice)

    
 
# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
