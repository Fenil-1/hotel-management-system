import mysql.connector

# GLOBAL VARIABLES DECLARATION
myConnection = None
userName = ""
password = ""
roomrent = 0
restaurentbill = 0
gamingbill = 0
fashionbill = 0
totalAmount = 0
cid = ""

def MYSQLconnectionCheck():
    global myConnection, userName, password
    userName = input("Enter MySQL server username: ").strip()
    password = input("Enter MySQL server password: ").strip()

    try:
        myConnection = mysql.connector.connect(
            host="localhost",
            user=userName,
            passwd=password,
            auth_plugin='mysql_native_password'
        )

        if myConnection:
            print("MySQL connection established successfully.")
            cursor = myConnection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS HMS")
            cursor.execute("COMMIT")
            cursor.close()
            return myConnection
        else:
            print("Error establishing MySQL connection. Check username and password.")
    except Exception as e:
        print(f"Error: {e}")
        print("Error establishing MySQL connection. Check username and password.")

def MYSQLconnection():
    global myConnection, userName, password
    try:
        myConnection = mysql.connector.connect(
            host="localhost",
            user=userName,
            passwd=password,
            database="HMS",
            auth_plugin='mysql_native_password'
        )
        if myConnection:
            return myConnection
        else:
            print("Error establishing MySQL connection!")
            return None
    except Exception as e:
        print(f"Error: {e}")
        print("Error establishing MySQL connection!")
        return None

def searchCustomer():
    global cid
    if myConnection:
        cursor = myConnection.cursor()
        cid = input("Enter customer ID: ").strip()
        sql = "SELECT * FROM C_DETAILS WHERE CID = %s"
        cursor.execute(sql, (cid,))
        data = cursor.fetchall()
        cursor.close()
        
        if data:
            print(data)
            return True
        else:
            print("Record not found. Try again!")
            return False
    else:
        print("MySQL connection not established. Please try again!")
        return False

def userEntry():
    global cid
    if myConnection:
        cursor = myConnection.cursor()
        createTable = '''
            CREATE TABLE IF NOT EXISTS C_DETAILS(
                CID VARCHAR(20),
                C_NAME VARCHAR(30),
                C_ADDRESS VARCHAR(30),
                C_AGE VARCHAR(30),
                C_COUNTRY VARCHAR(30),
                P_NO VARCHAR(30),
                C_EMAIL VARCHAR(30)
            )
        '''
        cursor.execute(createTable)

        cid = input("Enter customer ID: ").strip()
        name = input("Enter customer name: ").strip()
        address = input("Enter customer address: ").strip()
        age = input("Enter customer age: ").strip()
        nationality = input("Enter customer country: ").strip()
        phoneno = input("Enter customer phone number: ").strip()
        email = input("Enter customer email: ").strip()

        sql = "INSERT INTO C_DETAILS VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (cid, name, address, age, nationality, phoneno, email)
        cursor.execute(sql, values)
        cursor.execute("COMMIT")
        cursor.close()
        
        print("New customer entered into the system successfully!")
    else:
        print("Error establishing MySQL connection!")

def bookingRecord():
    if searchCustomer():
        if myConnection:
            cursor = myConnection.cursor()
            createTable = '''
                CREATE TABLE IF NOT EXISTS BOOKING_RECORD(
                    CID VARCHAR(20),
                    CHECK_IN DATE,
                    CHECK_OUT DATE
                )
            '''
            cursor.execute(createTable)

            checkin = input("Enter check-in date (YYYY-MM-DD): ").strip()
            checkout = input("Enter check-out date (YYYY-MM-DD): ").strip()

            sql = "INSERT INTO BOOKING_RECORD VALUES (%s, %s, %s)"
            values = (cid, checkin, checkout)
            cursor.execute(sql, values)
            cursor.execute("COMMIT")
            cursor.close()
            
            print("Check-in and check-out entry made successfully!")
        else:
            print("Error establishing MySQL connection!")
    else:
        print("Customer not found!")

def roomRent():
    global cid, roomrent

    if searchCustomer():
        if myConnection:
            cursor = myConnection.cursor()
            createTable = '''
                CREATE TABLE IF NOT EXISTS ROOM_RENT(
                    CID VARCHAR(20),
                    ROOM_CHOICE INT,
                    NO_OF_DAYS INT,
                    ROOMNO INT,
                    ROOMRENT INT
                )
            '''
            cursor.execute(createTable)

            print("Available rooms:")
            print("1. Ultra Royal > 10000 Rs.")
            print("2. Royal > 5000 Rs.")
            print("3. Elite > 3500 Rs.")
            print("4. Budget > 2500 Rs.")

            roomchoice = int(input("Enter your option: ").strip())
            roomno = int(input("Enter room number: ").strip())
            noofdays = int(input("Enter number of days: ").strip())

            room_rates = {1: 10000, 2: 5000, 3: 3500, 4: 2500}
            if roomchoice in room_rates:
                roomrent = noofdays * room_rates[roomchoice]
                print(f"Room rent: Rs. {roomrent}")

                sql = "INSERT INTO ROOM_RENT VALUES (%s, %s, %s, %s, %s)"
                values = (cid, roomchoice, noofdays, roomno, roomrent)
                cursor.execute(sql, values)
                cursor.execute("COMMIT")
                cursor.close()
                
                print(f"Room booked for {noofdays} days. Total room rent: Rs. {roomrent}")
            else:
                print("Invalid option. Please try again.")
        else:
            print("Error establishing MySQL connection!")
    else:
        print("Customer not found!")

def Restaurent():
    global cid, restaurentbill

    if searchCustomer():
        if myConnection:
            cursor = myConnection.cursor()
            createTable = '''
                CREATE TABLE IF NOT EXISTS RESTAURENT(
                    CID VARCHAR(20),
                    CUISINE VARCHAR(30),
                    QUANTITY INT,
                    BILL INT
                )
            '''
            cursor.execute(createTable)

            print("Menu:")
            print("1. Vegetarian Combo > 300 Rs.")
            print("2. Non-Vegetarian Combo > 500 Rs.")
            print("3. Vegetarian & Non-Vegetarian Combo > 750 Rs.")
            
            choice_dish = int(input("Enter your choice: ").strip())
            quantity = int(input("Enter quantity: ").strip())

            dish_prices = {1: 300, 2: 500, 3: 750}
            if choice_dish in dish_prices:
                restaurentbill = quantity * dish_prices[choice_dish]
                print(f"Total bill: Rs. {restaurentbill}")

                sql = "INSERT INTO RESTAURENT VALUES (%s, %s, %s, %s)"
                values = (cid, choice_dish, quantity, restaurentbill)
                cursor.execute(sql, values)
                cursor.execute("COMMIT")
                cursor.close()
                
                print(f"Your total bill amount is: Rs. {restaurentbill}")
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Error establishing MySQL connection!")
    else:
        print("Customer not found!")

def Gaming():
    global cid, gamingbill

    if searchCustomer():
        if myConnection:
            cursor = myConnection.cursor()
            createTable = '''
                CREATE TABLE IF NOT EXISTS GAMING(
                    CID VARCHAR(20),
                    GAMES VARCHAR(30),
                    HOURS INT,
                    GAMING_BILL INT
                )
            '''
            cursor.execute(createTable)

            print("Games:")
            print("1. Table Tennis > 150 Rs./HR")
            print("2. Bowling > 100 Rs./HR")
            print("3. Snooker > 250 Rs./HR")
            print("4. VR World Gaming > 400 Rs./HR")
            print("5. Video Games > 300 Rs./HR")
            print("6. Swimming Pool Games > 350 Rs./HR")
            
            game = int(input("Enter game choice: ").strip())
            hour = int(input("Enter number of hours: ").strip())

            game_rates = {1: 150, 2: 100, 3: 250, 4: 400, 5: 300, 6: 350}
            if game in game_rates:
                gamingbill = hour * game_rates[game]
                print(f"Total gaming bill: Rs. {gamingbill}")

                sql = "INSERT INTO GAMING VALUES (%s, %s, %s, %s)"
                values = (cid, game, hour, gamingbill)
                cursor.execute(sql, values)
                cursor.execute("COMMIT")
                cursor.close()
                
                print(f"Your total gaming bill is: Rs. {gamingbill}")
            else:
                print("Invalid game choice. Please try again.")
        else:
            print("Error establishing MySQL connection!")
    else:
        print("Customer not found!")

def Fashion():
    global cid, fashionbill

    if searchCustomer():
        if myConnection:
            cursor = myConnection.cursor()
            createTable = '''
                CREATE TABLE IF NOT EXISTS FASHION(
                    CID VARCHAR(20),
                    DRESS VARCHAR(30),
                    AMOUNT INT,
                    BILL INT
                )
            '''
            cursor.execute(createTable)

            print("Fashion items:")
            print("1. Shirts > 1500 Rs.")
            print("2. T-Shirts > 300 Rs.")
            print("3. Pants > 2000 Rs.")
            print("4. Jeans > 4000 Rs.")
            print("5. Tassel Top > 500 Rs.")
            print("6. Gown > 3000 Rs.")
            print("7. Western Dress > 3000 Rs.")
            print("8. Skirts > 400 Rs.")
            print("9. Trousers > 200 Rs.")
            print("10. InnerWear > 30 Rs.")
            
            dress = int(input("Enter item number: ").strip())
            quantity = int(input("Enter quantity: ").strip())

            item_prices = {1: 1500, 2: 300, 3: 2000, 4: 4000, 5: 500, 6: 3000, 7: 3000, 8: 400, 9: 200, 10: 30}
            if dress in item_prices:
                fashionbill = quantity * item_prices[dress]
                print(f"Total bill: Rs. {fashionbill}")

                sql = "INSERT INTO FASHION VALUES (%s, %s, %s, %s)"
                values = (cid, dress, quantity, fashionbill)
                cursor.execute(sql, values)
                cursor.execute("COMMIT")
                cursor.close()
                
                print(f"Your total bill is: Rs. {fashionbill}")
            else:
                print("Invalid item number. Please try again.")
        else:
            print("Error establishing MySQL connection!")
    else:
        print("Customer not found!")

def totalAmount():
    global cid, roomrent, restaurentbill, gamingbill, fashionbill
    
    if searchCustomer():
        if myConnection:
            cursor = myConnection.cursor()
            createTable = '''
                CREATE TABLE IF NOT EXISTS TOTAL(
                    CID VARCHAR(20),
                    C_NAME VARCHAR(30),
                    ROOMRENT INT,
                    RESTAURENTBILL INT,
                    GAMINGBILL INT,
                    FASHIONBILL INT,
                    TOTALAMOUNT INT
                )
            '''
            cursor.execute(createTable)

            name = input("Enter customer name: ").strip()
            grandTotal = roomrent + restaurentbill + gamingbill + fashionbill
            sql = "INSERT INTO TOTAL VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (cid, name, roomrent, restaurentbill, gamingbill, fashionbill, grandTotal)
            cursor.execute(sql, values)
            cursor.execute("COMMIT")
            cursor.close()
            
            print("\nCustomer Billing:")
            print(f"Customer Name: {name}")
            print(f"Room Rent: Rs. {roomrent}")
            print(f"Restaurant Bill: Rs. {restaurentbill}")
            print(f"Gaming Bill: Rs. {gamingbill}")
            print(f"Fashion Bill: Rs. {fashionbill}")
            print(f"Total Amount: Rs. {grandTotal}")
        else:
            print("Error establishing MySQL connection!")
    else:
        print("Customer not found!")

def searchOldBill():
    global cid
    if searchCustomer():
        if myConnection:
            cursor = myConnection.cursor()
            sql = "SELECT * FROM TOTAL WHERE CID = %s"
            cursor.execute(sql, (cid,))
            data = cursor.fetchall()
            cursor.close()
            
            if data:
                print(data)
            else:
                print("Record not found. Try again!")
        else:
            print("Error establishing MySQL connection!")
    else:
        print("Something went wrong. Please try again!")

# Main loop
if __name__ == "__main__":
    myConnection = MYSQLconnectionCheck()
    if myConnection:
        MYSQLconnection()

        while True:
            print('''
            1. Enter Customer Details
            2. Booking Record
            3. Calculate Room Rent
            4. Calculate Restaurant Bill
            5. Calculate Gaming Bill
            6. Calculate Fashion Store Bill
            7. Display Customer Details
            8. Generate Total Bill Amount
            9. Generate Old Bill
            10. Exit
            ''')
            choice = int(input("Enter your choice: ").strip())

            if choice == 1:
                userEntry()
            elif choice == 2:
                bookingRecord()
            elif choice == 3:
                roomRent()
            elif choice == 4:
                Restaurent()
            elif choice == 5:
                Gaming()
            elif choice == 6:
                Fashion()
            elif choice == 7:
                searchCustomer()
            elif choice == 8:
                totalAmount()
            elif choice == 9:
                searchOldBill()
            elif choice == 10:
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Error establishing MySQL connection!")
