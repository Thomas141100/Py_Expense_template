import ast
import csv
from PyInquirer import prompt

from user import get_users

# Get users and synthesise who owes who
def status():
    users = get_users()
    # Get all expenses
    with open("expense_report.csv", 'r') as f:
        reader = csv.reader(f)
        expenses = [row for row in reader]

    # Create a dict with all users and their balance
    debts = {user:{user:0 for user in users} for user in users}

    # For each expense, update the debt to the user who paid
    for expense in expenses:
        amount = int(expense[0])
        spender = expense[2]
        participants = expense[3:]
        print(participants)
        for participant in participants:
            debts[spender][participant] -= amount / len(participants)
            debts[participant][spender] += amount / len(participants)


    # Print the status
    print("Status:")
    for user in debts:
        print(f"{user} owes:")
        owes = False
        for debtor in debts[user]:
            if debts[user][debtor] > 0:
                owes = True
                print(f"\t{debts[user][debtor]}€ to {debtor} ")
        if not owes:
            print("\tNothing")
    return
