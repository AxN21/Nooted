
# Nooted

Nooted is a simple web application that allows users to write notes and keep track of them, with an interface designed for simplicity.

## System Requirements
The below requirements need to be installed on the system to run the project.

-   Running Postgrasql instance
-   Python 3 (`3.11.2`)

## Running the project
This project is built using Python, and utilizes the Flask framework. You can use SQLAlchemy while running the project in development mode, but a Postgrasql database is needed for production.

Install all system requirements (see above)

Set up a python virtual environment 
    
    $ python3 -m venv venv
    
Activate the virtual environment

    - macOS/Linux: $ source venv/bin/Activate
    - Windows: $ venv\Scripts\activate.bat
    
Install the python requirements 

    $ python3 -m pip install -r requirements.txt

Dublicate the .env.example file, and name the dublicate file .env
        
    - You need to populate the .env file now
    - SECRET_KEY=' random string '
    - DATABASE_URL=' Your actual database url (for production) '
    
Run the project using 

    $ flask run

When you stop working on the project you need to deactivate the virtual environment

    $ deactivate