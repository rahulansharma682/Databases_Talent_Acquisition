# Databases_Talent_Acquisition

A Streamlit-based web application for managing and querying data related to recruiters, jobs, and candidates. The dashboard allows users to perform CRUD operations and execute complex queries on a MySQL database.

Features

1. Add Data, View Data.
2. Execute Complex Queries.

Set Up and Installation

1. Install MySQL Connector: ```pip install mysql-connector-python```
2. Install Streamlit: ```pip install streamlit```

Usage

1. Update Database Connection Details in create_connection()
```
   connection = mysql.connector.connect(
    host="localhost",  
    user="your_username",       
    password="your_password",  
    database="final_project"  
)
```
2. To execute the application, run the following command: ```streamlit run Interface.py```

