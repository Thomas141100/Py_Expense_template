import ast
import csv
from PyInquirer import prompt

from user import get_users

debt_pay_questions = [
    {
        "type":"list",
        "name":"payer",
        "message":"Debt Paid - Payer: ",
        "choices": get_users(),
    },
    {
        "type":"list",
        "name":"debtor",
        "message":"Debt Paid - Debtor: ",
        "choices": get_users(),
    }
]

def debt_paid(owes):
    infos = prompt(debt_pay_questions)
    debt = owes[infos['payer']][infos['debtor']]

    # If there us no debt, ask again
    if debt == 0:
        print("There is no debt between these two users")
        return debt_paid(owes)

    # If there is a debt, display the dept paid
    else:
        print(f"{infos['payer']} paid {infos['debtor']} {debt}€")

    # Update the debt
    with open("expense_report.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow([debt, "Debt Paid", infos['payer'], infos['debtor']])
    return True


# Get users and synthesise who owes who
def status():
    users = get_users()
    # Get all expenses
    with open("expense_report.csv", 'r') as f:
        reader = csv.reader(f)
        expenses = [row for row in reader]

    # Create a dict with all users and their balance
    debts = {user:0 for user in users}

    # For each expense, update the debt to the user who paid
    for expense in expenses:
        amount = float(expense[0])
        spender = expense[2]
        participants = expense[3:]
        for participant in participants:
            debts[spender] -= amount / len(participants)
            debts[participant] += amount / len(participants)
    
    # Compute who owes who
    owes = {user:{user:0 for user in users} for user in users}
    while (True):
        # Get the user who owes the most
        max_debt = max(debts, key=debts.get)
        # If he doesn't owe anything, stop
        if debts[max_debt] <= 0:
            break
        # Get the user who is owed the most
        max_credit = max(debts, key=lambda x: -debts[x])
        # If he doesn't owe anything, stop
        if debts[max_credit] >= 0:
            break
        # Compute the amount to pay
        amount = min(-debts[max_debt], debts[max_credit])
        # Update the debts
        debts[max_debt] += amount
        debts[max_credit] -= amount
        # Update the owes
        owes[max_debt][max_credit] -= amount
    
    # Print the status
    print("Status:")
    for user in owes:
        print(f"{user} owes:")
        owes_money = False
        for debtor in owes[user]:
            if owes[user][debtor] > 0:
                owes_money = True
                print(f"\t{owes[user][debtor]}€ to {debtor} ")
        if not owes_money:
            print("\tNothing")
    
    # Ask if a debt has been paid
    answer = prompt([{
        "type":"confirm",
        "name":"debt_paid",
        "message":"Has a debt been paid ?",
        "default":True
    }])

    if answer['debt_paid']:
        debt_paid(owes)
