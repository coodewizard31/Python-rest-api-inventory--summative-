> # Inventory Management System

A small admin portal for a retail shop. Staff can **add, view, update and delete** products, and they can even **look up real products** on the [OpenFoodFacts](https://world.openfoodfacts.org) website to fill in the details.

It has three parts that work together:
### 1.The brain , the FLASK REST API that stores & changes the inventory
### 2.Cli.py the input menu that talks commands to the API.
### 3. `test_app.py`, `test_cli.py` that checks everything works as required
The FLASK REST API reaches out to OpenFoodFacts website.
#### PROJECT TREE/STRUCTURE

├── app.py
├── cli.py
├── readme.md
├── requirements.txt
└── test_cli.py
### Installation & setup guide
You need **Python 3.9 or newer** and **Git**.
git clone **https://github.com/coodewizard31/Python-rest-api-inventory--summative-.git**
cd inventory-system
### Install Packages.
pip install -r requirements.txt
### How to run  
1.Start the API run **python app.py** you will see Running on http://127.0.0.1:5000 now debug will be on 
2. Terminal 2 you will start the menu by running **python cli.py**
### API endpoints
You will see http://127.0.0.1:5000 the API is there .
The CRUD routes; GET, PATCH, POST & DELETE.
Method -> Route ->What it does? 
GET | `/inventory` -> Get all items 
GET | `/inventory/<id>` -> Get one item
POST | `/inventory` ->|Add an item 
PATCH | `/inventory/<id>` ->Update price or stock 
DELETE | `/inventory/<id>` ->Remove an item 
GET | `/lookup?barcode=...` -> Search OpenFoodFacts 
POST | `/inventory/from-api` -> Search OpenFoodFacts and add the result 
Try them all out in postman & see for youself how they behave 