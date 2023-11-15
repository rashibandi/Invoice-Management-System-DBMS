from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '03feb2003'
app.config['MYSQL_DATABASE_DB'] = 'invoiceManagement'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Function to check MySQL connection
def check_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            database=app.config['MYSQL_DATABASE_DB'],
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            print("Connected")
            return connection
        else:
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Function to validate login (replace with your actual user authentication logic)
def validate_login(username, password):
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username =%s AND password =%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        connection.close()

        print(f"Validation: username={username}, password={password}, user={user}")
        return user is not None
    return False

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Hi")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Received: username={username}, password={password}")

        if validate_login(username, password):
            session['username'] = username

            print(f"Login successful for user: {username}")
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Dashboard route
@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        print("dashboard")
        return render_template('dashboard.html')

# Invoices route
@app.route('/invoices')
def invoices():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Add logic to fetch and display invoices from the database
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM invoices"
        cursor.execute(query)
        invoices = cursor.fetchall()
        connection.close()

        return render_template('invoices.html', invoices=invoices)

# New route for creating invoices
@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get the selected customer type from the form
        customer_type = request.form.get('customer_type')

        if customer_type == 'new':
            # Logic for creating invoice for a new customer
            return redirect(url_for('create_invoice_new_customer'))

        elif customer_type == 'existing':
            # Logic for creating invoice for an existing customer
            return redirect(url_for('create_invoice_existing_customer'))

    return render_template('create_invoice.html')

# Route for creating invoice for a new customer
@app.route('/create_invoice/new_customer', methods=['GET', 'POST'])
def create_invoice_new_customer():
    # Add logic for creating invoice for a new customer
    return render_template('create_invoice_new_customer.html')

# Route for creating invoice for an existing customer
@app.route('/create_invoice/existing_customer', methods=['GET', 'POST'])
def create_invoice_existing_customer():
    print("existing")
    customers = get_existing_customers() 
    print(customers)
    return render_template('create_invoice_existing_customer.html', customers=customers)

def get_existing_customers():
    try:
        # Establish a connection to the database
        connection = check_db_connection()

        if connection:
            print("Connected to the database")
            cursor = connection.cursor()

            # Fetch existing customers from the 'customers' table
            query = "SELECT id, name FROM customers"
            cursor.execute(query)
            customers = cursor.fetchall()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            print("Customers:", customers)
            return customers

    except Exception as e:
        print(f"Error fetching existing customers: {str(e)}")
        return []
# Route for processing the selection of an existing customer
@app.route('/create_invoice/existing_customer_details', methods=['POST'])
def existing_customer_details():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get the selected customer ID from the form
    customer_id = request.form.get('existing_customer')

    # Fetch customer details based on the customer_id
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM customers WHERE id = %s"
        cursor.execute(query, (customer_id,))
        customer_details = cursor.fetchone()
        connection.close()

        return render_template('existing_customer_details.html', customer=customer_details)

# Manage Invoices route
@app.route('/manage_invoices')
def manage_invoices():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Add logic to fetch and display invoices from the database
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM invoices"
        cursor.execute(query)
        invoices = cursor.fetchall()
        connection.close()

        return render_template('manage_invoices.html', invoices=invoices)


# Products route
@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Add logic to fetch and display products from the database
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()
        connection.close()

        return render_template('products.html', products=products)

# Create Product route
@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']

        connection = check_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO products (product_name, product_price) VALUES (%s, %s)"
            cursor.execute(query, (product_name, product_price))
            connection.commit()
            connection.close()

            flash(f"Product '{product_name}' created successfully!", 'success')
            return redirect(url_for('products'))

    return render_template('create_product.html')

#Manage Products route
@app.route('/manage_products')
def manage_products():
    if 'username' not in session:
        return redirect(url_for('login'))

    connection = check_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM products"
            cursor.execute(query)
            products = cursor.fetchall()
            connection.close()

            return render_template('manage_products.html', products=products)

        except Exception as e:
            flash(f"Error fetching products: {str(e)}", 'error')
            return redirect(url_for('dashboard'))

    flash("Error connecting to the database.", 'error')
    return redirect(url_for('dashboard'))

# Customers route
@app.route('/customers')
def customers():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Add logic to fetch and display customers from the database
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM customers"
        cursor.execute(query)
        customers = cursor.fetchall()
        connection.close()

        return render_template('customers.html', customers=customers)

# Create Customer route
@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle form submission to create a new customer
        # Extract form data and insert into the customers table
        pass  # Add your logic here

    return render_template('create_customer.html')

# Manage Customers route
@app.route('/manage_customers')
def manage_customers():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Add logic to fetch and display customers from the database
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM customers"
        cursor.execute(query)
        customers = cursor.fetchall()
        connection.close()

        return render_template('manage_customers.html', customers=customers)



# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
