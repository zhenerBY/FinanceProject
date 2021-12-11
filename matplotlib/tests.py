import matplotlib.pyplot as plt

from request.request import *

CHAT_ID = 11111111


def get_balance_pie_chart(user_id: int):
    balance = get_balance(user_id)
    labels = 'Income', 'Expenses'
    sizes = [balance['balance']['inc'], balance['balance']['exp']]
    explode = (0.1, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def get_categories_type_pie_chart(user_id: int, cat_type: str):
    balance = get_categories_balance(user_id, cat_type)
    labels = []
    sizes = []
    explode = []
    for element in balance['categories']:
        labels.append(element)
        sizes.append(balance['categories'][element])
        explode.append(0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
