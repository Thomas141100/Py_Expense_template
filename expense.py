import csv
from PyInquirer import prompt

from user import get_users

expense_questions = [
    {
        "type":"input",
        "name":"amount",
        "message":"New Expense - Amount: ",
        "validate": lambda answer: answer.isdigit() or "Please enter a number"
    },
    {
        "type":"input",
        "name":"label",
        "message":"New Expense - Label: ",
    },
    {
        "type":"list",
        "name":"spender",
        "message":"New Expense - Spender: ",
        "choices": get_users(),
    },
    {
        "type":"list",
        "name":"split_type",
        "message":"New Expense - Split Type: ",
        "choices": ["Even", "Custom"],
    }
]

participants_questions = [
    {
        "type":"checkbox",
        "name":"participants",
        "message":"New Expense - Participants: ",
        "choices": [{"name":user, "checked": False} for user in get_users()],
    }
]


def new_expense(*args):
    infos = prompt(expense_questions)

    # Get spender and set checked to True for him
    for user in participants_questions[0]['choices']:
        if user['name'] == infos['spender']:
            user['checked'] = True
    participants = prompt(participants_questions)

    # Writing the informations on external file might be a good idea ¯\_(ツ)_/¯
    with open("expense_report.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(list(infos.values()) + list(participants.values())[0])

    print("Expense Added !")
    return True


