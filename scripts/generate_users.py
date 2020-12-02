import random
from random import randint


#####################################################
# Used for generating fake data for the users table #
#####################################################


options_first_name = [
    "Josh",
    "Barry",
    "Elise",
    "Mary",
    "Joanna",
    "Elliot",
    "Ally",
    "Walter",
    "Saul",
    "Jessie",
    "Jesse",
    "Luke",
    "Samantha",
    "Diana",
]

options_last_name = [
    "Smith",
    "Anderson",
    "White",
    "Alderson",
    "Moss",
    "Pinkman",
    "Goodman",
    "Lyndon",
    "Plainview",
    "Johnson",
    "Williams",
    "Willson",
    "Jackson",
    "Robinson",
    "Young",
    "King",
]

options_email = ["gmail", "yahoo", "outlook"]

options_email_org = [".ca", ".com"]

for i in range(20):
    user_id = "NULL"
    first_name = ""
    last_name = ""
    email = ""
    phone_num = ""
    password = "password"
    user_type = "Regular"

    # Get first name
    first_name = random.choice(options_first_name)

    # Get last name
    last_name = random.choice(options_last_name)

    # Create email
    email = (
        first_name.lower()
        + "."
        + last_name.lower()
        + "@"
        + random.choice(options_email)
        + random.choice(options_email_org)
    )

    # Generate phone #
    phone_num = "905"
    phone_num += str(randint(1000000, 9999999))

    sql_query = "INSERT INTO users (user_id, first_name, last_name, email_address, phone_number, password, user_type)"
    sql_query += "\nVALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
        user_id,
        first_name,
        last_name,
        email,
        phone_num,
        password,
        user_type,
    )

    print(sql_query)
