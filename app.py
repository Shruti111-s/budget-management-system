from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
import os

app = Flask(__name__)
FILENAME = 'transactions.csv'

def load_transactions():
    try:
        with open(FILENAME, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

def save_transactions(transactions):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['date', 'type', 'category', 'amount', 'description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

def add_transaction_to_file(transaction):
    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transaction = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': request.form['type'],
            'category': request.form['category'],
            'amount': request.form['amount'],
            'description': request.form['description']
        }
        add_transaction_to_file(transaction)
        return redirect('/')

    transactions = load_transactions()
    income = sum(float(t['amount']) for t in transactions if t['type'] == 'income')
    expense = sum(float(t['amount']) for t in transactions if t['type'] == 'expense')
    balance = income - expense

    return render_template('index.html',
                           transactions=transactions,
                           income=income,
                           expense=expense,
                           balance=balance)

if __name__ == '__main__':
    app.run(debug=True)
