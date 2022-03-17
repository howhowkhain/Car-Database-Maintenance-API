App for database maintenance as bellow example (eg. maintenace of a database for cars).

The App is working as an RESTfull API using Comand Prompt terminal (Windows) or
any other OS terminal.

The App is using http protocol for server comunication (CRUD).

Bellow example is simulating communication with an HTTP server where a database for cars is stored
as a json file (a json object containing the details for all database existing cars).

Use the json-server to simulate the functionality of the App.

Run:

- to start json-server:

json-server --watch "NODE JS SERVER-CARS DATABASE/database.json" absolut file path

- to start python file "Cars Database Maintenace.py"

python "Cars Database Maintenace.py" absolute file path
