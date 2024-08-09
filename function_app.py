import azure.functions as func
import logging
import mysql.connector
from mysql.connector import Error
from hashlib import sha256

def connect_to_db():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="mysql-15f7ba09-iitgn.g.aivencloud.com",
            user="avnadmin",
            password="AVNS_6wfyzI92dJdCHffXIrK",
            database="issues",
            port=21719,
        )
        return conn
    except Error as e:
        logging.error(f"Error connecting to MySQL: {str(e)}")
        raise

app = func.FunctionApp()

@app.route(route="HomePage", auth_level=func.AuthLevel.ANONYMOUS)
def home_page(req: func.HttpRequest) -> func.HttpResponse:
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home Page</title>
    </head>
    <style>
    /* General Styles */
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f0f2f5;
    color: #333;
}

/* Navigation Bar */
nav {
    background-color: #007bff;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: white;
}

#logo {
    display: flex;
    align-items: center;
}

#logo img {
    height: 50px;
    width: 50px;
    margin-right: 15px;
}

#nav-text {
    font-size: 18px;
    font-weight: bold;
}

/* Main Body */
#main-body {
    display: flex;
    justify-content: space-around;
    margin-top: 50px;
    padding: 20px;
}

.cards {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 250px;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
}

.cards:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-text {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
}

/* Button Styles */
button {
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #0056b3;
}

button a {
    color: white;
    text-decoration: none;
}

button a:hover {
    text-decoration: underline;
}

    </style>
    <body>
        <nav>
            <span id="logo">
                <img src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/IIT_Gandhinagar_Logo.svg/300px-IIT_Gandhinagar_Logo.svg.png" alt="">
                <p id="nav-text">Expert Tech Support at Your Service</p>
            </span>
        </nav>
        <div id="main-body">
            <div class="cards" id="LEFT-CARD">
                <p class="card-text">Admin Login</p>
                <button><a href="/api/login">Click here</a></button>
            </div>
            <div class="cards">
                <p class="card-text">Existing Query Status</p>
                <button><a href="/api/QueryStatus">Click here</a></button>
            </div>
            <div class="cards">
                <p class="card-text">New Query</p>
                <button><a href="/api/NewQuery">Click here</a></button>
            </div>
        </div>
    </body>
    </html>
    """
    return func.HttpResponse(html_content, mimetype="text/html")

@app.route(route="login", auth_level=func.AuthLevel.ANONYMOUS)
def admin_page(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "POST":
        username = req.form.get('username')
        password = req.form.get('password')

        try:
            conn = connect_to_db()
            cursor = conn.cursor(dictionary=True)
            
            # Check if the user exists and the password is correct
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user = cursor.fetchall()[0]
            
            cursor.close()
            conn.close()
            if user["password"]==password and user["username"]==username:
                # If authentication is successful, set a session or token (simulated here)
                # req.route_params['is_authenticated'] = True
                return func.HttpResponse(status_code=302, headers={"Location": "/api/CheckDB"})
            else:
                return func.HttpResponse("Invalid username or password", status_code=401)
        except Error as e:
            logging.error(f"Error querying MySQL: {str(e)}")
            return func.HttpResponse("Failed to authenticate.", status_code=500)
    

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Page</title>
    </head>
    <style>
/* General Styles */
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f0f2f5;
    color: #333;
}

/* Navigation Bar */
nav {
    background-color: #007bff;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    color: white;
}

#logo {
    display: flex;
    align-items: center;
}

#logo img {
    height: 50px;
    width: 50px;
    margin-right: 15px;
}

#nav-text {
    font-size: 18px;
    font-weight: bold;
}

/* Main Body */
#main-body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 80vh;
    padding: 20px;
}

#main-body p {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Form Styles */
#admin-detail {
    margin-bottom: 20px;
    text-align: left;
}

label {
    display: block;
    font-size: 14px;
    margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
    width: calc(100% - 22px);
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
}

/* Button Styles */
button {
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    width: 100%;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #0056b3;
}

button a {
    color: white;
    text-decoration: none;
}

button a:hover {
    text-decoration: underline;
}
    </style>
    <body>
        <nav>
            <span id="logo">
                <a href="/api/homepage"><img src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/IIT_Gandhinagar_Logo.svg/300px-IIT_Gandhinagar_Logo.svg.png" alt=""></a>
                <p id="nav-text">Expert Tech Support at Your Service</p>
            </span>
        </nav>
        <div id="main-body">
            <div>
                <p>Login for admin page</p>
                <form method="post" action="/api/login">
                    <div id="admin-detail">
                        <label for="username">Username</label>
                        <input type="text" name="username" required>
                        <br>
                        <label for="password">Password</label>
                        <input type="password" name="password" required>
                    </div>
                    <button>Login</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return func.HttpResponse(html_content, mimetype="text/html")

@app.route(route="NewQuery", auth_level=func.AuthLevel.ANONYMOUS)
def new_query(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "POST":
        name = req.form.get('name')
        email = req.form.get('email')
        number = req.form.get('number')
        subject = req.form.get('subject')
        issue = req.form.get('issue')
        link = req.form.get('link')

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO issue_details (name, email, number, subject, issue, link, date, time, status)
            VALUES (%s, %s, %s, %s, %s, %s, CURDATE(), CURTIME(), 0)
            """
            cursor.execute(query, (name, email, number, subject, issue, link))
            conn.commit()
            cursor.close()
            conn.close()
            
            return func.HttpResponse("Issue submitted successfully!", status_code=200)
        except Error as e:
            logging.error(f"Error inserting into MySQL: {str(e)}")
            return func.HttpResponse("Failed to submit the issue.", status_code=500)
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Query</title>
    </head>
        <style>
    /* General Styles */
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f7f7f7;
    color: #333;
}

/* Navbar */
#navbar {
    background-color: #007bff;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: white;
}

#navbar #logo {
    height: 50px;
    width: 50px;
}

#navbar p {
    margin: 0;
    font-size: 18px;
    font-weight: bold;
}

/* Main Header */
main header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: #004085;
    color: white;
}

main header h1 {
    font-size: 28px;
    margin: 0;
}

.adminlog {
    background-color: #ffc107;
    padding: 10px 20px;
    border-radius: 5px;
    color: #333;
    text-decoration: none;
    font-weight: bold;
}

.adminlog:hover {
    background-color: #e0a800;
}

/* Form Container */
.form-container {
    display: flex;
    justify-content: center;
    margin: 40px 20px;
}

.left-container {
    flex: 1;
    padding: 20px;
    text-align: center;
    background-color: #e9ecef;
    border-radius: 10px;
    margin-right: 20px;
}

#side-text {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}

.help img {
    max-width: 100%;
    border-radius: 10px;
}

.form-wrapper {
    flex: 2;
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-header {
    margin-bottom: 20px;
}

#Form-head {
    font-size: 22px;
    margin: 0;
    text-align: center;
}

.form-input {
    display: flex;
    flex-direction: column;
}

.form-input input[type="text"],
.form-input input[type="email"],
.form-input input[type="tel"],
.form-input select,
.form-input textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
}

#file-container h3 {
    margin-bottom: 10px;
    font-size: 18px;
}

.form-input input[type="submit"] {
    background-color: #007bff;
    border: none;
    color: white;
    padding: 10px 15px;
    font-size: 16px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.form-input input[type="submit"]:hover {
    background-color: #0056b3;
}

    </style>
    <body>
        <div id="navbar">
            <a href="/api/homepage"><img id="logo" src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/IIT_Gandhinagar_Logo.svg/300px-IIT_Gandhinagar_Logo.svg.png" alt=""></a>
            <p>Expert Tech Support at Your Service</p>
        </div>
        <main>
            <header>
                <h1>Issue-Tracker</h1>
                <span>
                    <a href="/api/login" class='adminlog' >Admin</a>
                </span>
            </header>
            <div class="form-container">
                <div class="left-container">
                    <h1 id="side-text">
                        READY TO SERVE YOU.. <br>24/7
                        <br><br>
                    </h1>
                    <div class="help">
                        <img width="252" src="https://5.imimg.com/data5/SELLER/Default/2023/7/327287103/OL/UU/FB/10317855/repair-and-maintenance-service-500x500.png" alt="Help Image">
                    </div>
                </div>
                <div class="form-wrapper">
                    <div class="form-header">
                        <h1 id="Form-head">Please submit your Issues to the admin</h1>
                    </div>
                    <div class="form-input">
                        <form action="/api/NewQuery" method="post">
                            <input type="text" name="name" placeholder="Your Full Name" required>
                            <input type="email" name="email" id="email" placeholder="Your Email address" required>
                            <input type="tel" name="number" id="number" placeholder="Contact Number" required>
                            <select name="subject" id="s3" required>
                                <option value="">Choose Issue Subject</option>
                                <option value="Light Fixture not working">Light Fixture not working</option>
                                <option value="Exhaust fan not working">Exhaust fan not working</option>
                                <option value="Ceiling Fan not working">Ceiling Fan not working</option>
                                <!-- Add other options as needed -->
                            </select>
                            <textarea name="issue" id="issue" rows="5" cols="50" placeholder="Explain Your Issue Briefly" required></textarea>
                            <div id="file-container">
                                <h3>Upload an image</h3>
                                <input type="link" name="link" placeholder="Media link">
                            </div>
                            <input type="submit" id="button">
                        </form>
                    </div>
                </div>
            </div>
        </main>
    </body>
    </html>
    """
    
    return func.HttpResponse(html_content, mimetype="text/html")

@app.route(route="QueryStatus", auth_level=func.AuthLevel.ANONYMOUS)
def query_status(req: func.HttpRequest) -> func.HttpResponse:
    name = req.form.get('name')
    mobile = req.form.get('mobile')

    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT issue_id, subject, issue, status FROM issue_details WHERE name=%s AND number=%s"
        cursor.execute(query, (name, mobile))
        user_issues = cursor.fetchall()
        
        cursor.close()
        conn.close()

        issue_list_html = ""
        if user_issues:
            issue_list_html = "<ul>"
            for issue in user_issues:
                status = "Open" if issue['status'] == 0 else "Closed"
                issue_list_html += f"<li><strong>Issue ID:</strong> {issue['issue_id']}<br><strong>Subject:</strong> {issue['subject']}<br><strong>Issue:</strong> {issue['issue']}<br><strong>Status:</strong> {status}</li>"
            issue_list_html += "</ul>"
        else:
            issue_list_html = "<p>No issues found for the provided details.</p>"

    except Error as e:
        logging.error(f"Error querying MySQL: {str(e)}")
        return func.HttpResponse("Failed to retrieve the status.", status_code=500)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Query Status</title>
        <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            color: #333;
            
        }}
        #navbar {{
            background-color: #007bff;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: white;
        }}
        #navbar #logo {{
            height: 50px;
            width: 50px;
        }}
        #navbar p {{
            margin: 0;
            font-size: 18px;
            font-weight: bold;
        }}
        main header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background-color: #004085;
            color: white;
        }}
        main header h1 {{
            font-size: 28px;
            margin: 0;
        }}
        .adminlog {{
            background-color: #ffc107;
            padding: 10px 20px;
            border-radius: 5px;
            color: #333;
            text-decoration: none;
            font-weight: bold;
        }}
        .adminlog:hover {{
            background-color: #e0a800;
        }}
        /* Form Container */
        .form-container {{
            display: flex;
            justify-content: center;
            margin: 40px 20px;
        }}
        .form-header {{
            margin-bottom: 20px;
            text-align: center;
        }}
        #Form-head {{
            font-size: 22px;
            margin: 0;
        }}
        .form-input {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 300px;
        }}
        .form-input input[type="text"],
        .form-input input[type="tel"] {{
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 14px;
        }}
        .form-input input[type="submit"] {{
            background-color: #007bff;
            border: none;
            color: white;
            padding: 10px 15px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 100%;
        }}
        .form-input input[type="submit"]:hover {{
            background-color: #0056b3;
        }}
        #results {{
            margin: 40px 20px;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}
        #results h2 {{
            font-size: 22px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .issue-item {{
            padding: 15px;
            border-bottom: 1px solid #ddd;
        }}
        .issue-item:last-child {{
            border-bottom: none;
        }}
        .issue-item h3 {{
            margin: 0;
            font-size: 18px;
        }}
        .issue-item p {{
            margin: 5px 0;
            font-size: 14px;
            color: #666;
        }}
        </style>
    </head>
    <body>
        <div id="navbar">
            <a href="/api/homepage"><img id="logo" src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/IIT_Gandhinagar_Logo.svg/300px-IIT_Gandhinagar_Logo.svg.png" alt=""></a>
            <p>Expert Tech Support at Your Service</p>
        </div>
        <main>
            <header>
                <h1>Issue-Tracker</h1>
                <span>
                    <a href="/api/login" class='adminlog'>Admin</a>
                </span>
            </header>
            <div class="form-container">
                <div class="form-header">
                    <h1 id="Form-head">Issue Status</h1>
                </div>
                <div class="form-input">
                    <form action="/api/QueryStatus" method="post">
                        <input type="text" name="name" placeholder="Your Full Name" required>
                        <input type="tel" name="mobile" placeholder="Contact Number" required>
                        <input type="submit" id="button">
                    </form>
                </div>
            </div>
            <div id="results">
                {issue_list_html}
            </div>
        </main>
    </body>
    </html>
    """
    return func.HttpResponse(html_content, mimetype="text/html")

@app.route(route="CheckDB", auth_level=func.AuthLevel.ANONYMOUS)
def check_db_status(req: func.HttpRequest) -> func.HttpResponse:
    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        
        # Execute a query to fetch all records from the 'issues' table
        cursor.execute("SELECT * FROM issue_details")
        records = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Generate HTML content to display the records
        if records:
            table_rows = ""
            for record in records:
                table_rows += f"""
                <tr>
                    <td>{record['issue_id']}</td>
                    <td>{record['name']}</td>
                    <td>{record['email']}</td>
                    <td>{record['number']}</td>
                    <td>{record['subject']}</td>
                    <td>{record['issue']}</td>
                    <td>{record['status']}</td>
                </tr>
                """
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Admin Panel</title>
                <link rel="stylesheet" href="/static/db_status.css">
            </head>
            <style>
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    color: #333;
    margin: 0;
    padding: 0;
    text-align: center;
}

h1, h2 {
    color: #4a90e2;
}

h1 {
    margin-top: 20px;
}

h2 {
    margin-bottom: 20px;
}

/* Table Styles */
table {
    width: 80%;
    margin: 0 auto;
    border-collapse: collapse;
    background-color: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    background-color: #4a90e2;
    color: white;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}

tr:hover {
    background-color: #ddd;
}

/* Responsive Styles */
@media (max-width: 768px) {
    table {
        width: 100%;
    }

    th, td {
        display: block;
        width: 100%;
        box-sizing: border-box;
    }

    th, td {
        padding: 10px;
        text-align: right;
    }

    th {
        background-color: #4a90e2;
        color: white;
    }
}
"""+ f"""

            </style>
            <body>
                <div id="navbar">
                <a href="/api/homepage"><img id="logo" src="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/IIT_Gandhinagar_Logo.svg/300px-IIT_Gandhinagar_Logo.svg.png" alt="" height=60px ></a>
                <p>Expert Tech Support at Your Service</p>
                </div>
                <h1>Admin Panel</h1>
                <h2>Below are the records in the Database</h2>
                <table border="1">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Number</th>
                        <th>Subject</th>
                        <th>Issue</th>
                        <th>Status (Open/Closed)</th>
                    </tr>
                    {table_rows}
                </table>
            </body>
            </html>
            """
        else:
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Admin Panel</title>
            </head>
            <body>
                <h1>Database Connection Successful!</h1>
                <h2>No records found in the 'issues' table.</h2>
            </body>
            </html>
            """

        return func.HttpResponse(html_content, mimetype="text/html")
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Panel</title>
        </head>
        <body>
            <h1>All submitted Issues Below</h1>
            <p>{error_message}</p>
        </body>
        </html>
        """
        return func.HttpResponse(html_content, mimetype="text/html", status_code=500)