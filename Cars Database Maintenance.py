""""
App for database maintenance as bellow example (eg. maintenace of a database for cars).

The App is working as an RESTfull API using Comand Prompt terminal (Windows) or
any other OS terminal.

The App is using http protocol for server comunication (CRUD).

Bellow example is simulating communication with an HTTP server where a database for cars is stored
as a json file (a json object containing the details for all database existing cars).

Use the json-server to simulate the functionality of the App.



+-----------------------------------+
|       Vintage Cars Database       |
+-----------------------------------+
M E N U
=======
1. List cars
2. Add new car
3. Delete car
4. Update car
0. Exit
Enter your choice (0..4): 1
*** Database is empty ***
+-----------------------------------+
|       Vintage Cars Database       |
+-----------------------------------+
M E N U
=======
1. List cars
2. Add new car
3. Delete car
4. Update car
0. Exit
Enter your choice (0..4): 2
Car ID (empty string to exit): 1
Car brand (empty string to exit): Porsche
Car model (empty string to exit): 911
Car production year (empty string to exit): 1963
Is this car convertible? [y/n] (empty string to exit): n
+-----------------------------------+
|       Vintage Cars Database       |
+-----------------------------------+
M E N U
=======
1. List cars
2. Add new car
3. Delete car
4. Update car
0. Exit
Enter your choice (0..4): 2
Car ID (empty string to exit): 2
Car brand (empty string to exit): Ford
Car model (empty string to exit): Mustang
Car production year (empty string to exit): 1972
Is this car convertible? [y/n] (empty string to exit): y
+-----------------------------------+
|       Vintage Cars Database       |
+-----------------------------------+
M E N U
=======
1. List cars
2. Add new car
3. Delete car
4. Update car
0. Exit
Enter your choice (0..4): 1
id        | brand          | model     | production_year     | convertible    | 
1         | Porsche        | 911       | 1963                | False          | 
2         | Ford           | Mustang   | 1972                | True           | 

+-----------------------------------+
|       Vintage Cars Database       |
+-----------------------------------+
M E N U
=======
1. List cars
2. Add new car
3. Delete car
4. Update car
0. Exit
Enter your choice (0..4):  4
Car ID (empty string to exit): 2
Car brand (empty string to exit): Ford
Car model (empty string to exit): Mustang
Car production year (empty string to exit): 1973
Is this car convertible? [y/n] (empty string to exit): n
+-----------------------------------+
|       Vintage Cars Database       |
+-----------------------------------+
M E N U
=======
1. List cars
2. Add new car
3. Delete car
4. Update car
0. Exit
Enter your choice (0..4): 3
Car ID (empty string to exit): 1
Success!
Car ID (empty string to exit): 
+-----------------------------------+
|       Vintage Cars Database       |
+-----------------------------------+
M E N U
=======
1. List cars
2. Add new car
3. Delete car
4. Update car
0. Exit
Enter your choice (0..4): 0
Bye!

"""


import requests
import json

from requests.models import codes


# list used to create car tables when invoked by the user
header_names = ["id", "brand", "model", "production_year", "convertible"]
widths = [3, 20, 15, 20, 20]
sum = 0
for i in widths:
    sum += i

# with_id variable used to determine if the car ID was inputed by the user
with_id = False

# car_id variable used to store the value for car_id inputed by the user
car_id = None


# a predefined class used to create car objects for storing car properties
# inputed by the user
class Car():
    def __init__(self, id, brand, model, production_year, convertible):
        self.id = id
        self.brand = brand
        self.model = model
        self.production_year = production_year
        self.convertible = convertible


# a subclass used to encode the Python car properties into json format
class encode_Car(json.JSONEncoder):
    def default(self, car):
        if isinstance(car, Car):
            return car.__dict__
        else:
            return super().default(car)


def check_server(cid=None):
    # returns True or False;
    # when invoked without arguments simply checks if server responds;
    # invoked with car ID checks if the ID is present in the database;
    if cid == None:
        try:
            reply = requests.head("http://localhost:3000/")
            # print(reply.headers)
        except requests.exceptions.Timeout:
            return False
        except requests.RequestException:
            return False
        else:
            if reply.status_code == requests.codes.ok:
                print("Server is active!")
                return True
            else:
                print("Server is down!")
                return False
    else:
        try:
            reply = requests.get("http://localhost:3000/cars")
        except requests.exceptions.Timeout:
            print("Server is busy. Try again!")
        except requests.RequestException:
            print("Server Error!")
        else:
            if reply.status_code == requests.codes.ok:
                reply = reply.json()
                for car in reply:
                    if car["id"] == cid:
                        return True
                return False
            elif reply.status_code == requests.codes.not_found:
                print("+" + "-" * 51 + "+")
                print(
                    "| " + "The cars' database is missing from the server.".center(50) + "|")
                print("| " +
                      "It may be removed or renamed.".center(50) + "|")
                print("| " + "Contact the server's administrator".center(50) + "|")
                print("+" + "_" * 51 + "+")
                exit(1)


def print_menu():
    # prints user menu - nothing else happens here;
    print("+" + "-" * 30 + "+")
    print("|" + "Vintage Cars Database".center(30) + "|")
    print("+" + "-" * 30 + "+")
    print("M E N U")
    print("=" * 7)
    print("1. List cars")
    print("2. Add new car")
    print("3. Delete car")
    print("4. Update car")
    print("0. Exit")


def read_user_choice():
    # reads user choice and checks if it's valid;
    # returns '0', '1', '2', '3' or '4'
    global with_id, car_id
    choice = input("Enter your choice: (0...4): ").strip()
    while not choice.isdigit():
        print("Invalid input! (digits only)")
        choice = input("Enter your choice: (0...4): ").strip()
    while int(choice) not in range(0, 5):
        print("Invalid input! Try again and choose from above menu options")
        choice = input("Enter your choice: (0...4): ").strip()
        while not choice.isdigit():
            print("Invalid input! (digits only)")
            choice = input("Enter your choice: (0...4): ").strip()
    if choice != "":
        return choice
    else:
        with_id = False
        car_id = None
        main()


# print table header with column's titles
def print_header():
    # prints elegant cars table header;
    for name, width in zip(header_names, widths):
        print(name.ljust(width), end="| ")
    print()
    for width in widths:
        print("_" * width, end="| ")
    print()


def print_car(car):
    # prints one car's data in a way that fits the header;
    for name, width in zip(header_names, widths):
        print(str(car[name]).ljust(width), end="| ")
    print()


def list_cars():
    # gets all cars' data from server and prints it;
    # if the database is empty prints diagnostic messag
    # instead;
    try:
        reply = requests.get("http://localhost:3000/cars")
    except requests.exceptions.Timeout:
        print("Server is busy. Try again!")
    except requests.RequestException:
        print("Server Error!")
    else:
        if reply.status_code == requests.codes.ok:
            reply_json = reply.json()
            if reply_json:
                print_header()
                # order the cars list in ascending order
                # filtered by id
                for car in sorted(reply_json, key=lambda car: car["id"]):
                    print_car(car)
            else:
                print("*" * 3, "Database is empty", "*" * 3)
        elif reply.status_code == requests.codes.not_found:
            print("+" + "-" * 51 + "+")
            print(
                "| " + "The cars' database is missing from the server.".center(50) + "|")
            print("| " +
                  "It may be removed or renamed.".center(50) + "|")
            print("| " + "Contact the server's administrator".center(50) + "|")
            print("+" + "_" * 51 + "+")
            exit(1)


def name_is_valid(name):
    # checks if name (brand or model) is valid;
    # valid name is non-empty string containing
    # digits, letters and spaces;
    # returns True or False;
    if name.isalnum():
        return True
    else:
        return False


def enter_id():
    # allows user to enter car's ID and checks if it's valid;
    # valid ID consists of digits only;
    # returns int or None (if user enters an empty line);
    global with_id, car_id
    while not with_id:
        choice = input("Car ID (empty string to exit): ")
        choice_no_white_space = choice.replace(" ", "")
        while not choice_no_white_space.isdigit() and choice != "":
            print("""Invalid car ID (must be a number).\nTry again, please!""")
            choice = input("Car ID (empty string to exit): ")
            choice_no_white_space = choice.strip()
        # if user input nothing ("empty-string") the app will
        # go back to the main menu
        if choice == "":
            with_id = False
            car_id = None
            main()
        # if user input is valid and not empty it will return
        # the input as an integer
        if choice:
            choice = int(choice)
            with_id = True
        # if user input is an empty line (empty-space string)
        # it will not return None
        else:
            choice = None
        return choice


def enter_production_year():
    # allows user to enter car's production year and checks if it's valid;
    # valid production year is an int from range 1900..2000;
    # returns int or None  (if user enters an empty line);
    global with_id, car_id
    choice = input("Enter production year (empty string to exit): ")
    choice_no_white_space = choice.replace(" ", "")
    if choice != "" and choice != " ":
        while not choice_no_white_space.isdigit():
            print("Production year is not valid (digits only). Try again!")
            choice = input(
                "Enter production year (empty string to exit): ")
            choice_no_white_space = choice.replace(" ", "")
        while int(choice_no_white_space) not in range(1900, 2022):
            print("Production year is not valid (values of 1900...2021 only)")
            choice = input(
                "Enter production year (empty string to exit): ")
            choice_no_white_space = choice.replace(" ", "")
            while not choice_no_white_space.isdigit():
                print("Production year is not valid (digits only). Try again!")
                choice = input(
                    "Enter production year (empty string to exit): ")
                choice_no_white_space = choice.replace(" ", "")
            choice = int(choice_no_white_space)
        return choice
    else:
        if choice != "":
            return None
        else:
            with_id = False
            car_id = None
            main()


def enter_name(what):
    # allows user to enter car's name (brand or model) and checks if it's valid;
    # uses name_is_valid() to check the entered name;
    # returns string or None  (if user enters an empty line);
    # argument describes which of two names is entered currently ('brand' or 'model');
    global with_id, car_id
    choice = input(f"Car {what} (empty string to exit): ")
    choice_no_white_space = choice.replace(" ", "")
    valid_choice = name_is_valid(choice_no_white_space)
    if valid_choice:
        return choice
    else:
        if choice != "":
            return None
        else:
            with_id = False
            car_id = None
            main()


def enter_convertible():
    # allows user to enter Yes/No answer determining if the car is convertible;
    # returns True, False or None  (if user enters an empty line);
    global with_id, car_id
    choice = input(
        "Is this car convertible? [y/n] (empty string to exit): ").lower()
    choice_no_white_space = choice.replace(" ", "")
    if choice != "" and choice != " ":
        while choice_no_white_space != "y" and choice_no_white_space != "n":
            choice_no_white_space = input(
                "Is this car convertible? [y/n] (empty string to exit): ").lower()
            choice_no_white_space = choice.strip()
        if choice_no_white_space == "y":
            return True
        else:
            return False
    else:
        if choice != "":
            return None
        else:
            with_id = False
            car_id = None
            main()


def input_car_data(with_id):
    # lets user enter car data;
    # argument determines if the car's ID is entered (True) or
    # not (False);
    # returns None if user cancels the operation or a dictionary
    # of the following structure:
    # {'id': int, 'brand': str, 'model': str, 'production_year':
    # int, 'convertible': bool}
    global car_id
    if with_id:
        brand = enter_name("brand")
        model = enter_name("model")
        production_year = enter_production_year()
        convertible = enter_convertible()
        car = Car(car_id, brand, model, production_year, convertible)
        json_car_prop = json.dumps(car, cls=encode_Car)
        return json_car_prop
    else:
        car_id = enter_id()


def delete_car():
    # asks user for car's ID and tries to delete it from
    # database;
    global car_id, with_id
    car_id = enter_id()
    while car_id == None:
        car_id = enter_id()
    id_confirmation = check_server(car_id)
    if id_confirmation:
        try:
            reply = requests.delete(f"http://localhost:3000/cars/{car_id}")
        except requests.exceptions.Timeout:
            print("Server is busy. Try again!")
        except requests.RequestException:
            print("Server Error!")
        else:
            if reply.status_code == requests.codes.ok:
                print(f"The car with ID: {car_id} was succesfully deleted")
    else:
        print(f"The car with {car_id} not found!")
    car_id = None
    with_id = False


def add_car():
    # invokes input_car_data(True) to gather car's info and adds
    # it to the database;
    global car_id, with_id
    car_id = enter_id()
    while car_id == None:
        input_car_data(with_id)
    id_confirmation = check_server(car_id)
    if not id_confirmation:
        json_car_prop = input_car_data(with_id)
        header_sent = {"Content-Type": "application/json"}
        try:
            requests.post("http://localhost:3000/cars",
                          headers=header_sent, data=json_car_prop)
        except requests.exceptions.Timeout:
            print("Server is busy. Try again!")
        except requests.RequestException:
            print("Server Error!")
    else:
        print(f"The car with ID: {car_id} is already in database!")
    car_id = None
    with_id = False


def update_car():
    # invokes enter_id() to get car's ID if the ID is present in
    # the database;
    # invokes input_car_data(False) to gather new car's info and
    # updates the database;
    global car_id, with_id
    car_id = enter_id()
    while car_id == None:
        input_car_data(with_id)
    id_confirmation = check_server(car_id)
    if id_confirmation:
        json_car_prop = input_car_data(with_id)
        header_sent = {"Content-Type": "application/json"}
        try:
            requests.put(f"http://localhost:3000/cars/{car_id}",
                         headers=header_sent, data=json_car_prop)
        except requests.exceptions.Timeout:
            print("Server is busy. Try again!")
        except requests.RequestException:
            print("Server Error!")
    else:
        print(f"The car with {car_id} not found!")
    car_id = None
    with_id = False


def main():
    while True:
        if not check_server():
            print("Server is not responding - quitting!")
            exit(1)
        print_menu()
        choice = read_user_choice()
        if choice == '0':
            print("+" + "-" * 9 + "+")
            print("|" + "Bye!".center(9) + "|")
            print("+" + "-" * 9 + "+")
            exit(0)
        elif choice == '1':
            list_cars()
        elif choice == '2':
            add_car()
        elif choice == '3':
            delete_car()
        elif choice == '4':
            update_car()


main()
