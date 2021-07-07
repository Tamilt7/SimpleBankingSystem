# Write your code here
import random
import sqlite3

action = 9
cards = ["4000001000000000"]
pins = ["0000"]


conn = sqlite3.connect("card.s3db")
cursor = conn.cursor()


def inscard(id1, number, pin):
    cursor.execute("INSERT INTO card (id, number, pin) \
                   VALUES (?, ?, ?)", (id1, number, pin))
    conn.commit()


def getaction():

    print("")
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    return int(input())


def getsubaction():
    print("")
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")
    return int(input())


def checkbal(id1):

    cursor.execute("SELECT balance from card where id = ?", (id1, ))
    bal = cursor.fetchall()[0][0]
    print("")
    print("Balance: " + str(bal))


def addincome(id1):

    print("")
    print("Enter income:")
    inc = int(input())

    cursor.execute("SELECT balance from card where id = ?", (id1, ))
    bal = cursor.fetchall()[0][0] + inc

    cursor.execute("UPDATE card set balance = ? where id = ?", (bal, id1))
    conn.commit()

    print("Income was added!")


def closeaccount(id1):

    print("")

    cursor.execute("DELETE from card where id = ?", (id1,))
    conn.commit()

    print("The account has been closed!")


def dotransfer(id1):

    print("")
    print("Transfer")
    print("Enter card number")
    acq_card = str(input())
    acq_acc_no = int(acq_card[:15])
    acq_checksum = int(acq_card[15])

    valid_trx = True

    if acq_checksum != getchecksum(acq_acc_no):
        print("Probably you made a mistake in the card number. Please try again!")
        valid_trx = False

    if valid_trx and acq_acc_no == id1:
        print("You can't transfer money to the same account!")
        valid_trx = False

    if valid_trx:
        cursor.execute("SELECT number from card where number = ?", (acq_card,))
        if len(cursor.fetchall()) <= 0:
            print("Such a card does not exist.")
            valid_trx = False

    if valid_trx:
        print("Enter how much money you want to transfer:")
        trx_am = int(input())

        cursor.execute("SELECT balance from card where id = ?", (id1,))
        bal = cursor.fetchall()[0][0]

        if trx_am <= bal:
            bal -= trx_am
            cursor.execute("UPDATE card set balance = ? where id = ?", (bal, id1))
            conn.commit()

            cursor.execute("SELECT balance from card where id = ?", (acq_acc_no,))
            bal = cursor.fetchall()[0][0] + trx_am
            cursor.execute("UPDATE card set balance = ? where id = ?", (bal, acq_acc_no))
            conn.commit()
            print("Success!")
        else:
            print("Not enough money!")


def logout():

    print("")
    print("You have successfully logged out!")


def createaccount():

    cursor.execute("SELECT max(id) from card")
    acc_no = cursor.fetchall()[0][0]
    if acc_no:
        acc_no += 1
    else:
        acc_no = 400000100000001

    pin = str(random.randint(0, 9999)).zfill(4)

    checksum = getchecksum(acc_no)

    card_no = str(acc_no) + str(checksum)

    inscard(acc_no, card_no, pin)

    print("")
    print("Your card has been created")
    print("Your card number:")
    print(card_no)
    print("Your card PIN:")
    print(pin)


def getchecksum(acc_no):

    ctl_no = 0
    for idx, char in enumerate(str(acc_no)):
        if idx % 2 == 0:
            if (int(char) * 2) > 9:
                ctl_no += ((int(char) * 2) - 9)
            else:
                ctl_no += (int(char) * 2)
        else:
            ctl_no += int(char)

    if (ctl_no % 10) > 0:
        return 10 - (ctl_no % 10)
    else:
        return 0


def login():
    print("")
    print("Enter your card number:")
    card_no = str(input())
    print("Enter your PIN:")
    pin = str(input())

    cursor.execute("SELECT id from card where number = ? and pin = ?",
                   (card_no, pin))
    print("")
    acc_nos = cursor.fetchall()
    if len(acc_nos) == 1:
        print("You have successfully logged in!")
        acc_no = int(acc_nos[0][0])
        sub_action = 9

        while sub_action != 0 and sub_action != 4 and sub_action != 5:
            sub_action = getsubaction()
            if sub_action == 1:
                checkbal(acc_no)
            elif sub_action == 2:
                addincome(acc_no)
            elif sub_action == 3:
                dotransfer(acc_no)
            elif sub_action == 4:
                closeaccount(acc_no)
            elif sub_action == 5:
                logout()
            else:
                return 0
    else:
        print("Wrong card number or PIN!")

    return 1


def goodbye():
    print("")
    print("Bye!")


cursor.execute("DROP TABLE card")
cursor.execute("SELECT name from sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if len(tables) <= 0:
    cursor.execute("""CREATE TABLE card
    (id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );""")
    conn.commit()

while action != 0:
    action = getaction()
    if action == 1:
        createaccount()
    elif action == 2:
        rtn = login()

        if rtn == 0:
            goodbye()
            action = 0
    else:
        goodbye()

