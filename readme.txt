*Steps to Run the App Server:*

1. *Extract the Zip File:*
   Unzip the contents of the provided file to access the project.

2. *Open the Terminal:*
   Navigate to the folder where the project is located.

3. *Create a Virtual Environment:*
   python -m venv myenv
   

4. *Activate the Virtual Environment:*
   On macOS/Linux:
   source myenv/bin/activate
   
   On Windows:
   myenv\Scripts\activate
   

5. *Install Dependencies:*
   Use pip to install the required packages from the requirements file:
   pip install -r requirements.txt
   

6. *Navigate to the Project Directory:*
   Change the current directory to the trueDialer folder:
   cd trueDialer/
   

7. *Database Migrations:*
   Prepare the database for the application:
   python manage.py makemigrations
   

8. *Apply Migrations:*
   Apply the migrations to the database:
   python manage.py migrate
   

9. *Populate the Database:*
   Run the script to populate the database with initial data:
   python populate_db.py
   

10. *Start the Server:*
    Launch the application server:
    python manage.py runserver



Below is an API documentation for the provided endpoints:

---

## TrueDialer API Documentation

### Register User
Registers a new user in the TrueDialer system.

- **URL:** `api/register/`
- **Method:** POST
- **Parameters:**
  - None
  
#### Request Body:
- **name** (string, required): The name of the user.
- **phone_number** (string, required): The phone number of the user.
- **email** (string, optional): The email address of the user.
- **password** (string, required): The password for the user account.

#### Example Request:
```json
{
  "name": "John Doe",
  "phone_number": "1234567890",
  "email": "john@example.com",
  "password": "securepassword"
}
```

Endpoint Security: All endpoints require authentication for access. Basic Authentication with the provided phone_number as username and a password must be included in the request headers for each endpoint.

After running `python populate_db.py`, a superuser is generated with the following credentials:

Name: 'admin'
Password: '1234'
Phone Number: '1234'
You can use these credentials to authenticate as a superuser if you don't want to register a new user for accessing the following endpoints.

---

### Mark Spam
Marks a phone number as spam.

- **URL:** `api/mark-spam/`
- **Method:** POST
- **Parameters:**
  - None

#### Request Body:
- **phone_number** (string, required): The phone number to mark as spam.

#### Example Request:
```json
{
  "phone_number": "1234567890"
}
```

---

### Search Contacts
Searches for contacts by name or phone number.

- **URL:** `/search/{search_query}/`
- **Method:** GET
- **Parameters:**
  - **search_query** (string, required): The name or phone number to search for.

#### Example Request:
- URL: `/search/John`
- URL: `/search/1234567890`

#### Example Response:
- HTTP Status Code: 200
- Response Body:
```json
[
  {
    "name": "John Doe",
    "phone_number": "1234567890",
    "spam_reports": 3
  },
  {
    "id": 5,
    "name": "Jane Smith",
    "phone_number": "9876543210",
    "spam_reports": 1
  }
]
```

---

### Contact Detail
Retrieves details of a specific contact by its ID. Person’s email is only displayed if the person is a registered user and the user who is searching is in the person’s contact list.

- **URL:** `/detail/{id}/`
- **Method:** GET
- **Parameters:**
  - **id** (integer, required): The ID of the contact.

#### Example Request:
- URL: `/detail/1/`

#### Example Response:
- HTTP Status Code: 200
- Response Body:
```json
{
  "id": 1,
  "name": "John Doe",
  "phone_number": "1234567890",
  "email": "john@example.com"
}
```

---

This concludes the TrueDialer API documentation. Use the provided endpoints to interact with the TrueDialer system according to your requirements.


    
