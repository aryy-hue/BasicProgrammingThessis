import mysql.connector
import re
import matplotlib.pyplot as plt
import os
from prettytable import PrettyTable
import numpy as np
import pandas as pd

# --------------------------------------------Validation--------------------------------------------
def validate_email(email):
    # Define a simple email validation pattern
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_pattern, email)
# --------------------------------------------Connection--------------------------------------------
def register_user(name, email, password, birth_date, role):
    if not validate_email(email):
        print('Invalid email address.')
        return

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO users (name, email, password, birth_date, role)
    VALUES (%s, %s, %s, %s, %s)
    '''
    values = (name, email, password, birth_date, role)
    cursor.execute(insert_query, values)

    connection.commit()
    connection.close()

def register_publisher(name, email, password, date_added):
    if not validate_email(email):
        print('Invalid email address.')
        return

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO publishers (name, email, password, date_added)
    VALUES (%s, %s, %s, %s)
    '''
    values = (name, email, password, date_added)
    cursor.execute(insert_query, values)

    connection.commit()
    connection.close()

def login(email, password):
    if not validate_email(email):
        print('Invalid email address.')
        return None  # Return None if email is invalid

    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )

    cursor = connection.cursor()

    # Check login for users (including 'admin' role)
    select_user_query = '''
    SELECT * FROM users
    WHERE email = %s AND password = %s AND (role = 'user' OR role = 'admin')
    '''
    user_values = (email, password)
    cursor.execute(select_user_query, user_values)
    user = cursor.fetchone()

    if user:
        connection.close()
        return user + ('user',) if 'user' in user else user + ('admin',)  # Add 'user' or 'admin' as the role and return the user information

    # Check login for publishers
    select_publisher_query = '''
    SELECT * FROM publishers
    WHERE email = %s AND password = %s
    '''
    publisher_values = (email, password)
    cursor.execute(select_publisher_query, publisher_values)
    publisher = cursor.fetchone()

    if publisher:
        connection.close()
        return publisher + ('publisher',)  # Add 'publisher' as the role and return the publisher information

    # If no user or publisher is found
    connection.close()
    return None

def home_page(user_name):
    print(f'Welcome, {user_name}! This is your home page.')

# --------------------------------------------GAME PAGE--------------------------------------------
def add_game(title, release_date, price):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO game (title, release_date, price)
    VALUES (%s, %s, %s)
    '''
    values = (title, release_date, price)
    cursor.execute(insert_query, values)
    connection.commit()
    connection.close()

def show_games():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    select_query = '''
    SELECT * FROM game
    '''
    cursor.execute(select_query)
    rows = cursor.fetchall()

    if not rows:
        print("Tidak ada data.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Title", "Release Date", "Price"]

        for row in rows:
            table.add_row(row)

        print(table)

    connection.close()

def update_game(id_game,title, release_date, price):
    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    update_query='''UPDATE game SET title=%s, release_date=%s, price=%s WHERE id_game=%s'''
    values = (title, release_date, price ,id_game)
    cursor.execute(update_query, values)
    connection.commit()
    connection.close()

def delete_game(id_game):
    connection=mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    delete_query='''DELETE FROM game WHERE id_game=%s'''
    values = (id_game,)
    cursor.execute(delete_query, values)
    connection.commit()
    connection.close()
    
def search_game():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    print('*---------Search Game---------*')
    search_term = input('Enter the title or any keyword to search: ')

    search_query = '''
    SELECT * FROM game
    WHERE title LIKE %s OR release_date LIKE %s
    '''
    values = (f"%{search_term}%", f"%{search_term}%")

    cursor.execute(search_query, values)
    rows = cursor.fetchall()

    if not rows:
        print("No matching games found.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Title", "Release Date", "Price"]

        for row in rows:
            table.add_row(row)

        print(table)

    connection.close()
    
def game_management():
    while True:
        print('*---------Game Management---------*')
        print('|    1. Show Games                |')
        print('|    2. Add Game                  |')
        print('|    3. Update Game               |')
        print('|    4. Delete Game               |')
        print('|    5. Search Game               |')
        print('|    6. Exit                      |')
        print('*---------------------------------*')
        choice = int(input('Enter your choice: '))

        if choice == 1:
            print('*---------Showing All Games---------*')
            show_games()
        elif choice == 2:
            print('*---------Add New Game---------*')
            title = input('Enter the title: ')
            release_date = input('Enter the release date(YY-MM-DD): ')
            price = input('Enter the price: ')
            add_game(title, release_date, price)
            print('Game added successfully!')
            
        elif choice == 3:
            print('Update Game...')
            id_game = input('Enter the id_game: ')
            title = input('Enter the title: ')
            release_date = input('Enter the release date(YY-MM-DD): ')
            price = input('Enter the price: ')
            update_game(id_game,title, release_date, price)
            print('Game updated successfully!')
            
        elif choice == 4:
            print('Deleting a game...')
            id_game = input('Enter the id_game: ')
            delete_game(id_game)
            
        elif choice == 5:
            print('Searching for a game...')
            search_game()
            
        elif choice == 6:
            break
        else:
            print('Invalid choice. Please try again.')
# --------------------------------------------Publisher Page--------------------------------------------
def show_publishers():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    select_query = '''
    SELECT * FROM publishers
    '''
    cursor.execute(select_query)
    rows = cursor.fetchall()

    if not rows:
        print("Tidak ada data.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Email", "Password", "Date Added"]

        for row in rows:
            table.add_row(row)

        print(table)

    connection.close()


def add_publisher(name, email , password , date_added):
    if not validate_email(email):
        print('Invalid email address.')
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO publishers (name, email, password, date_added)
    VALUES (%s, %s, %s, %s)
    '''
    values = (name, email, password, date_added)
    cursor.execute(insert_query, values)
    connection.commit()
    connection.close()

def update_publisher(id_publisher, name, email , password , date_added):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    update_query = '''
    UPDATE publishers
    SET name=%s, email=%s, password=%s, date_added=%s
    WHERE id_publisher=%s
    '''
    values = (name, email, password, date_added, id_publisher)
    cursor.execute(update_query, values)
    connection.commit()
    connection.close()

def delete_publisher(id_publisher):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    delete_query = '''
    DELETE FROM publishers
    WHERE id_publisher=%s
    '''
    values = (id_publisher,)
    cursor.execute(delete_query, values)
    connection.commit()
    connection.close()

def search_publisher():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    print('*---------Search Game---------*')
    search_term = input('Enter the title or any keyword to search: ')

    search_query = '''
    SELECT * FROM publishers
    WHERE name LIKE %s OR date_added LIKE %s
    '''
    values = (f"%{search_term}%", f"%{search_term}%")

    cursor.execute(search_query, values)
    rows = cursor.fetchall()

    if not rows:
        print("No matching games found.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Email", "Password", "Date Added"]

        for row in rows:
            table.add_row(row)

        print(table)

    connection.close()

def publisher_management():
    while True:
        print('*---------Publisher Management---------*')
        print('|    1. Show Publishers                |')
        print('|    2. Add Publisher                  |')
        print('|    3. Update Publisher               |')
        print('|    4. Delete Publisher               |')
        print('|    5. Search Publisher               |')
        print('|    6. Exit                           |')
        print('*--------------------------------------*')
        choice = int(input('Enter your choice: '))

        if choice == 1:
            print('*--------Show Publishers---------*')
            show_publishers()
        elif choice == 2:
            print('*---------Add New Publisher---------*')
            name = input('Enter the name: ')
            email = input('Enter the email: ')
            password = input('Enter the password: ')
            date_added = input('Enter the date_added(YY-MM-DD): ')
            add_publisher(name, email, password, date_added)
            print('Publisher added successfully!')
            
        elif choice == 3:
            print('*--------Update Publisher---------*')
            id_publisher = input('Enter the id_publisher: ')
            name = input('Enter the name: ')
            email = input('Enter the email: ')
            password = input('Enter the password: ')
            date_added = input('Enter the date_added(YY-MM-DD): ')
            update_publisher(id_publisher, name, email, password, date_added)
            print('Publisher updated successfully!')
            
        elif choice == 4:
            print('*--------Delete Publisher---------*')
            id_publisher = input('Enter the id_publisher: ')
            delete_publisher(id_publisher)
            print('Publisher deleted successfully!')
        elif choice == 5:
            print('*--------Search Publisher---------*')
            search_publisher()
        elif choice == 6:
            break
        else:
            print('Invalid choice. Please try again.')
            
# --------------------------------------------User Management--------------------------------------------
def show_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()

    table = PrettyTable()
    table.field_names = ["ID", "Name", "Email", "Password", "Birth Date"]

    for row in rows:
        table.add_row(row)

    print(table)

    connection.close()
    
def add_user(name, email, password, birth_date):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    insert_query = '''
    INSERT INTO users (name, email, password, birth_date)
    VALUES (%s, %s, %s, %s)
    '''
    values = (name, email, password, birth_date)
    cursor.execute(insert_query, values)
    connection.commit()
    connection.close()


def update_user(id_user, name, email, password, birth_date):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    update_query = '''
    UPDATE users
    SET name=%s, email=%s, password=%s, birth_date=%s
    WHERE id_user=%s
    '''
    values = (name, email, password, birth_date, id_user)
    cursor.execute(update_query, values)
    connection.commit()
    connection.close()


def delete_user(id_user):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    delete_query = '''
    DELETE FROM users
    WHERE id_user=%s
    '''
    values = (id_user,)
    cursor.execute(delete_query, values)
    connection.commit()
    connection.close()

def search_user():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    print('*---------Search Game---------*')
    search_term = input('Enter the title or any keyword to search: ')

    search_query = '''
    SELECT * FROM users
    WHERE name LIKE %s OR email LIKE %s
    '''
    values = (f"%{search_term}%", f"%{search_term}%")

    cursor.execute(search_query, values)
    rows = cursor.fetchall()

    if not rows:
        print("No matching users found.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Email", "Password", "Birth Date"]

        for row in rows:
            table.add_row(row)

        print(table)
    connection.close()
    
def export_users_to_csv():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="odyssey",
        )
        cursor = connection.cursor()

        # Execute a SELECT query to fetch user data
        query = "SELECT * FROM users"
        cursor.execute(query)
        users_data = cursor.fetchall()

        # Check if there are any rows in the result set
        if not users_data:
            print("No user data to export.")
            return

        # Extract column names from the cursor description
        columns = [column[0] for column in cursor.description]

        # Create a DataFrame using pandas
        df = pd.DataFrame(users_data, columns=columns)

        # Specify the CSV file path
        csv_file_path = "users_data_pandas.csv"

        # Write DataFrame to CSV file
        df.to_csv(csv_file_path, index=False)

        print(f"User data exported to {csv_file_path} successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")
            
def display_age_statistics():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="odyssey",
        )
        cursor = connection.cursor()

        # Execute a SELECT query to fetch user birth dates
        query = "SELECT birth_date FROM users"
        cursor.execute(query)
        birth_dates = cursor.fetchall()

        # Check if there are any rows in the result set
        if not birth_dates:
            print("No user data to display statistics.")
            return

        # Extract birth dates
        birth_dates = [date[0] for date in birth_dates]

        # Convert birth dates to ages using NumPy
        current_date = np.datetime64('today')
        ages = (current_date - np.array(birth_dates, dtype='datetime64[Y]')).astype(int)

        # Display statistics
        print(f"Mean Age: {np.mean(ages):.2f} years")
        print(f"Standard Deviation of Age: {np.std(ages):.2f} years")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")        

def user_management():
    while True:
        print('*---------User Management---------*')
        print('|    1. Show Users                |')
        print('|    2. Add User                  |')
        print('|    3. Update User               |')
        print('|    4. Delete User               |')
        print('|    5. Search User               |')
        print('|    6. Export Users to CSV       |')
        print('|    7. Age Statistics            |')  # New menu option
        print('|    8. Exit                      |')
        print('*--------------------------------*')
        choice = int(input('Enter your choice: '))

        if choice == 1:
            print('*---------Showing All Users---------*')
            show_users()
        elif choice == 2:
            print('*---------Add New User---------*')
            name = input('Enter the name: ')
            email = input('Enter the email: ')
            password = input('Enter the password: ')
            birth_date = input('Enter the Birth Date(YY-MM-DD): ')
            add_user(name, email, password, birth_date)
            print('User added successfully!')
        elif choice == 3:
            print('*--------Update User---------*')
            id_user = input('Enter the id_user: ')
            name = input('Enter the name: ')
            email = input('Enter the email: ')
            password = input('Enter the password: ')
            birth_date = input('Enter the Birth Date(YY-MM-DD): ')
            update_user(id_user, name, email, password, birth_date)
            print('User updated successfully!')
        elif choice == 4:
            print('*--------Delete User---------*')
            id_user = input('Enter the id_user: ')
            delete_user(id_user)
            print('User deleted successfully!')
        elif choice == 5:
            print('*--------Search User---------*')
            search_user()
        elif choice == 6:
            export_users_to_csv()
        elif choice == 7:
            print('*--------Age Statistics---------*')
            display_age_statistics()
        elif choice == 8:
            break
        else:
            print('Invalid choice. Please try again.')
    

# --------------------------------------------Transaction Management--------------------------------------------
def add_transaction_for_user(id_user):
    # Display available games
    print('*---------Available Games---------*')
    show_games()

    # Get user input for game selection
    id_game = input('Enter the ID of the game you want to purchase: ')

    # Check if the selected game ID is valid
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    select_game_query = '''
    SELECT * FROM game
    WHERE id_game = %s
    '''
    cursor.execute(select_game_query, (id_game,))
    selected_game = cursor.fetchone()

    if not selected_game:
        print('Invalid game ID. Please try again.')
        connection.close()
        return

    # Get the quantity of the game the user wants to purchase
    quantity = input('Enter the quantity you want to purchase: ')

    # Add the transaction
    add_transaction(id_game, id_user, selected_game[3], quantity)

    print('Transaction added successfully!')

    connection.close()
    
def show_transaction():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    select_query = '''
    SELECT * FROM transactions
    '''
    cursor.execute(select_query)
    rows = cursor.fetchall()

    if not rows:
        print("No transactions found.")
    else:
        table = PrettyTable()
        table.field_names = ["ID Transaction", "ID User", "ID Publisher", 'ID Game' , "Quantity"]

        for row in rows:
            table.add_row(row)

        print(table)

    connection.close()

def add_transaction(id_game, id_user, id_publisher ,quantity):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO transactions (id_game, id_user, id_publisher,quantity)
    VALUES (%s, %s, %s, %s)
    '''
    values = (id_game, id_user, id_publisher ,quantity)
    cursor.execute(insert_query, values)
    connection.commit()
    connection.close()

def update_transaction(id_transaction, id_game, id_user, id_publisher ,quantity):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    update_query = '''
    UPDATE transactions
    SET id_game=%s, id_user=%s,  id_publisher=%s,quantity=%s
    WHERE id_transaction=%s
    '''
    values = (id_game, id_user, quantity, id_publisher ,id_transaction)
    cursor.execute(update_query, values)
    connection.commit()
    connection.close()

def delete_transaction(id_transaction):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    delete_query = '''
    DELETE FROM transactions
    WHERE id_transaction=%s
    '''
    values = (id_transaction,)
    cursor.execute(delete_query, values)
    connection.commit()
    connection.close()

def search_transaction():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    print('*---------Search Transaction---------*')
    search_term = input('Enter the ID Game, ID User, or any keyword to search: ')

    search_query = '''
    SELECT * FROM transactions
    WHERE id_game LIKE %s OR id_user LIKE %s OR quantity LIKE %s OR id_publisher LIKE %s
    '''
    values = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")

    cursor.execute(search_query, values)
    rows = cursor.fetchall()

    if not rows:
        print("No matching transactions found.")
    else:
        table = PrettyTable()
        table.field_names = ["ID Transaction", "ID User", "ID Publisher", 'ID Game' , "Quantity"]

        for row in rows:
            table.add_row(row)

        print(table)

    connection.close()

def max_value_transaction():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    select_query = '''
    SELECT MAX(quantity) FROM transactions
    '''
    cursor.execute(select_query)
    max_value = cursor.fetchone()[0]

    if max_value is not None:
        print(f"The maximum quantity in a transaction is: {max_value}")
    else:
        print("No transactions found.")

    connection.close()

def min_value_transaction():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    select_query = '''
    SELECT MIN(quantity) FROM transactions
    '''
    cursor.execute(select_query)
    min_value = cursor.fetchone()[0]

    if min_value is not None:
        print(f"The minimum quantity in a transaction is: {min_value}")
    else:
        print("No transactions found.")

    connection.close()

def average_value_transaction():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()
    select_query = '''
    SELECT AVG(quantity) FROM transactions
    '''
    cursor.execute(select_query)
    avg_value = cursor.fetchone()[0]

    if avg_value is not None:
        print(f"The average quantity in transactions is: {avg_value}")
    else:
        print("No transactions found.")

    connection.close()

def transaction_visualization():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    select_query = '''
    SELECT t.id_publisher, p.name, AVG(t.quantity) as avg_price
    FROM transactions t
    JOIN publishers p ON t.id_publisher = p.id_publisher
    GROUP BY t.id_publisher, p.name
    ORDER BY avg_price DESC
    '''
    cursor.execute(select_query)
    results = cursor.fetchall()

    if results:
        # Extract data from results
        publishers, publisher_names, avg_prices = zip(*results)

        # Plotting the data (largest to smallest)
        plt.figure(figsize=(10, 6))
        plt.bar(publisher_names, avg_prices, color='c')
        plt.title('Average Price per Publisher (Largest to Smallest)')
        plt.xlabel('Publisher Name')
        plt.ylabel('Average Price')
        plt.xticks(rotation=45, ha='right')
        plt.show()

        # Plotting the data (smallest to largest)
        plt.figure(figsize=(10, 6))
        plt.bar(publisher_names, avg_prices, color='m')
        plt.title('Average Price per Publisher (Smallest to Largest)')
        plt.xlabel('Publisher Name')
        plt.ylabel('Average Price')
        plt.xticks(rotation=45, ha='right')
        plt.gca().invert_yaxis()  # Invert y-axis to show smallest at the top
        plt.show()
    else:
        print("No transactions found.")

    connection.close()


def transaction_management():
    while True:
        print('*---------Transaction Management--------*')
        print('|    1. Show Transaction                |')
        print('|    2. Add Transaction                 |')
        print('|    3. Update Transaction              |')
        print('|    4. Delete Transaction              |')
        print('|    5. Search Transaction              |')
        print('|    6. Max Value Transaction           |')
        print('|    7. Min Value Transaction           |')
        print('|    8. Average Transaction             |')
        print('|    9. Transaction Visualization       |')
        print('|   10. Exit                            |')
        print('*---------------------------------------*')
        choice = int(input('Enter your choice: '))

        if choice == 1:
            print('*---------Showing All Transaction---------*')
            show_transaction()
        elif choice == 2:
            print('*---------Add New Transaction---------*')
            id_game = input('Enter the id_game: ')
            id_user = input('Enter the id_user: ')
            id_publisher = input('Enter the id_publisher: ')
            quantity = input('Enter the quantity: ')
            add_transaction(id_game, id_user, id_publisher ,quantity)
            print('Transaction added successfully!')
        elif choice == 3:
            print('*--------Update Transaction---------*')
            id_transaction = input('Enter the id_transaction: ')
            id_game = input('Enter the id_game: ')
            id_user = input('Enter the id_user: ')
            id_publisher = input('Enter the id_publisher: ')
            quantity = input('Enter the quantity: ')
            update_transaction(id_transaction, id_game, id_user, quantity)
            print('Transaction updated successfully!')
        elif choice == 4:
            print('*--------Delete Transaction---------*')
            id_transaction = input('Enter the id_transaction: ')
            delete_transaction(id_transaction)
            print('Transaction deleted successfully!')
        elif choice == 5:
            print('*--------Search Transaction---------*')
            search_transaction()
        elif choice == 6:
            print('*--------Max Value Transaction---------*')
            max_value_transaction()
        elif choice == 7:
            print('*--------Min Value Transaction---------*')
            min_value_transaction()
        elif choice == 8:
            print('*--------Average Value Transaction---------*')
            average_value_transaction()
            
        elif choice == 9:
            print('*--------Transaction Visualization---------*')
            transaction_visualization()
        elif choice == 10:
            break
        else:
            print('Invalid choice. Please try again.')
            
def user_menu(id_user, email):
    while True:
        print(f'*---------------Welcome, {email}---------------*')
        print('|    1. View Profile                            |')
        print('|    2. View Games                              |')
        print('|    3. Purchase Game                           |')
        print('|    4. View Transactions                       |')
        print('|    5. Exit                                    |')
        print('*-----------------------------------------------*')

        choice = int(input('Enter your choice: '))

        if choice == 1:
            pass
        elif choice == 2:
            show_games()
        elif choice == 3:
            print('*---------Purchase Game---------*')
            add_transaction_for_user(id_user)
        elif choice == 4:
            print('*---------Showing All Transactions---------*')
            search_transaction_for_user(id_user)
        elif choice == 5:
            break
        else:
            print('Invalid choice. Please try again.')
def search_transaction_for_user(id_user):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='odyssey'
    )
    cursor = connection.cursor()

    search_query = '''
    SELECT t.id_transaction, t.id_game, g.title, t.quantity
    FROM transactions t
    JOIN game g ON t.id_game = g.id_game
    WHERE t.id_user = %s
    '''
    cursor.execute(search_query, (id_user,))
    rows = cursor.fetchall()

    if not rows:
        print("No transactions found.")
    else:
        table = PrettyTable()
        table.field_names = ["ID Transaction", "ID Game", "Game Title", "Quantity"]

        for row in rows:
            table.add_row(row)

        print(table)

    connection.close()


# --------------------------------------------Menu Page--------------------------------------------
def menu():
    
    while True:
        print('*---------------Menu Page---------------*')
        print('|    1. Game Management                 |')
        print('|    2. Publisher Management            |')
        print('|    3. Users Management                |')
        print('|    4. Transaction Management          |')
        print('|    5. Exit                            |')
        print('*---------------------------------------*')
     
        choice = int(input('Enter your choice: ')) 
        if choice == 1:
            game_management()
        elif choice == 2:
            publisher_management()
        elif choice == 3:
            user_management()
        elif choice == 4:
            transaction_management()
        elif choice == 5:
            break
        else:
            print('Invalid choice. Please try again.')
            
        
# --------------------------------------------Login Page--------------------------------------------
while True:
    print('*---------Welcome to Odyssey---------*')
    print('|    1. Login                        |')
    print('|    2. Register                     |')
    print('|    3. Exit                         |')
    print('*------------------------------------*')
    choice = int(input('Enter your choice: '))

    if choice == 1:
        print('----------Login----------')
        email = input('Enter your email: ')
        password = input('Enter your password: ')
        user = login(email, password)

        if user is not None:
            if user[-1] == 'user':
                id_user = user[0]
                user_menu(id_user, email)
            elif user[-1] == 'publisher':
                game_management()
            elif user[-1] == 'admin':
                menu()
        else:
            print('Please check your email and password and try again.')

    elif choice == 2:
        print('----------Register----------')
        print('Select role:')
        print('1. User')
        print('2. Publisher')
        role_choice = int(input('Enter your role choice: '))

        if role_choice == 1:
            name = input('Enter your name: ')
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            birth_date = input('Enter your birth date (YY-MM-DD): ')
            register_user(name, email, password, birth_date, 'user')
        elif role_choice == 2:
            name = input('Enter your name: ')
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            date_added = input('Enter your date added (YY-MM-DD): ')
            register_publisher(name, email, password, date_added)
        else:
            print('Invalid choice. Please try again.')

    elif choice == 3:
        break
    else:
            print('Invalid choice. Please try again.')    