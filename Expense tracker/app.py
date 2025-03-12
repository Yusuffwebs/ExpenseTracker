from flask import Flask, render_template, request, redirect, url_for
import os
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

EXPENSES_FILE = 'expenses.txt'

def read_expenses():
    expenses = []
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as file:
            lines = file.readlines()
            expenses = [line.strip().split(',') for line in lines]
    return expenses

def write_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as file:
        for expense in expenses:
            file.write(','.join(expense) + '\n')

@app.route('/')
def index():
    expenses = read_expenses()

    monthly_expenses = defaultdict(float)
    for expense in expenses:
        category, amount, date = expense
        amount = float(amount)

        expense_date = datetime.strptime(date, "%Y-%m-%d")
        month_year = expense_date.strftime("%Y-%m")
        monthly_expenses[month_year] += amount

    sorted_months = sorted(monthly_expenses.items())

    return render_template('index.html', expenses=expenses, monthly_expenses=sorted_months)

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form.get('category')
    amount = request.form.get('amount')
    date = request.form.get('date')

    expenses = read_expenses()
    expenses.append([category, amount, date])
    write_expenses(expenses)

    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete_expense(id):
    expenses = read_expenses()

    if 0 <= id < len(expenses):
        expenses.pop(id)
        write_expenses(expenses)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
