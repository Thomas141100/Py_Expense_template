import csv
from PyInquirer import prompt
user_questions = [
    {
        "type":"input",
        "name":"name",
        "message":"New User - Name: ",
    },
]

def add_user():
    # This function should create a new user, asking for its name
    infos = prompt(user_questions)

    with open("users.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(infos.values())
    return

# Get all users from the file
def get_users():
    with open("users.csv", 'r') as f:
        reader = csv.reader(f)
        users = [row[0] for row in reader]
    return users
