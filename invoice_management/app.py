from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response, send_file
import mysql.connector
import jsonify
import pdfkit
import os
from flask import jsonify




app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
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
        # Establish a database connection
        connection = check_db_connection()
        
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Execute the queries
            cursor.execute("SELECT SUM(total) AS total_amount_due FROM invoices WHERE status = 'open';")
            total_amount_due = cursor.fetchone()['total_amount_due']

            cursor.execute("SELECT SUM(total) AS total_amount_received FROM invoices WHERE status = 'paid';")
            total_amount_received = cursor.fetchone()['total_amount_received']

            cursor.execute("SELECT COUNT(*) AS total_invoices FROM invoices;")
            total_invoices = cursor.fetchone()['total_invoices']

            cursor.execute("SELECT COUNT(*) AS total_invoices_due FROM invoices WHERE status = 'open';")
            total_invoices_due = cursor.fetchone()['total_invoices_due']

            cursor.execute("SELECT COUNT(DISTINCT c.id) AS customers_with_pending_invoices FROM customers c INNER JOIN invoices i ON c.email = i.custom_email WHERE i.status = 'open';")
            customers_with_pending_invoices = cursor.fetchone()['customers_with_pending_invoices']
            
            connection.close()

            return render_template('dashboard.html', 
                                   total_amount_due=total_amount_due,
                                   total_amount_received=total_amount_received,
                                   total_invoices=total_invoices,
                                   total_invoices_due=total_invoices_due,
                                   customers_with_pending_invoices=customers_with_pending_invoices)



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
    db = check_db_connection()  # Get the database connection

    if db is None:
        return "Error: Database connection failed!"

    cursor = db.cursor()
    
    if request.method == 'POST':
        # Fetch data from the form
        invoiceName = request.form['invoiceName']
        customer_name = request.form['customer_name']
        email = request.form['email']
        house_no = request.form['house_no']
        city = request.form['city']
        country = request.form['country']
        postcode = request.form['postcode']
        phone = request.form['phone']
        
        try:
            cursor.execute("SELECT * FROM invoices WHERE invoice = %s", (invoiceName,))
            existing_invoice = cursor.fetchone()

            if existing_invoice:
                flash("Invoice number already exists. Please use a different invoice number.", 'error')
                return render_template('create_invoice_new_customer.html')
                # return redirect(url_for('create_invoice_new_customer'))
            else:
                add_customer = ("INSERT INTO customers "
                                "(invoice, name, email, house_no, city, country, postcode, phone) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

                customer_data = (invoiceName, customer_name, email, house_no, city, country, postcode, phone)

                cursor.execute(add_customer, customer_data)
                db.commit()
                session['invoiceName'] = invoiceName
                session['email'] = email

                return redirect(url_for('create_invoice_main'))       
        except Exception as e:
            db.rollback()
            return f"Error: {e}"
        finally:
            cursor.close()
            db.close()

    return render_template('create_invoice_new_customer.html')

@app.route('/create_invoice_main', methods=['GET', 'POST'])
def create_invoice_main():
    if 'username' not in session:
        return redirect(url_for('login'))

    invoiceName = request.args.get('invoiceName')  
    email = request.args.get('email')
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()
        connection.close()

        return render_template('create_invoice_main.html', invoiceName=invoiceName, products=products)

    return "Error: Database connection failed."

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'})

    # Retrieve data sent from the front-end
    data = request.json
    invoiceName = data.get('invoiceName')
    email = data.get('email')
    createDate = data.get('createDate')
    dueDate = data.get('dueDate')
    totalAmount = data.get('totalAmount')

    # Retrieve selected product, quantity, and product id
    selected_products = data.get('selectedProducts')
    print(selected_products)
    # Perform operations to insert the invoice and associated products into the database
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()

        try:
            # Insert into the invoices table
            insert_query = "INSERT INTO invoices (invoice, custom_email, invoice_date, invoice_due_date, total, status) VALUES (%s, %s, %s, %s, %s, 'open')"
            cursor.execute(insert_query, (invoiceName, email, createDate, dueDate, totalAmount))
            connection.commit()
            # print(selected_products)
            # Insert selected products into invoice_items table
            for product in selected_products:
                
                arr = product['text'].split("-")
                product_name = arr[0].strip()
                product_price = arr[2].strip()
                product_id = int(product['id'].strip())
                quantity = int(arr[1].replace('Quantity:', '').strip())
                print(product_name, product_id, product_price, quantity)
                # product_name, quantity_price = product.split('- Quantity: ')
                # product_id = int(data.get('products')[[item[1] for item in data.get('products')].index(product_name)][0])
                # quantity = int(quantity_price.split(' - ')[0])

                # Insert product into invoice_items table
                insert_invoice_item_query = "INSERT INTO invoice_items (invoice, product_id, product_name, qty, purchaseDate) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_invoice_item_query, (invoiceName, product_id, product_name, quantity, createDate))
                connection.commit()

            flash(f'Invoice {invoiceName} generated successfully!', 'success')
            cursor.close()
            connection.close()
            return redirect(url_for('manage_invoices'))          

        except Exception as e:
            connection.rollback()
            cursor.close()
            connection.close()
            return jsonify({'error': f'Error generating invoice: {str(e)}'})
    
    return jsonify({'error': 'Database connection failed'})



@app.route('/create_invoice/existing_customer', methods=['GET', 'POST'])
def create_invoice_existing_customer():
    db = check_db_connection()  # Get the database connection

    if db is None:
        return "Error: Database connection failed!"

    cursor = db.cursor()

    print("existing")
    customers = get_existing_customers()
    if request.method == 'POST':
        # Fetch data from the form
        invoiceName = request.form['invoiceName']
        selected_customer_id = request.form['existing_customer']
        try:
            cursor.execute("SELECT * FROM invoices WHERE invoice = %s", (invoiceName,))
            existing_invoice = cursor.fetchone()

            if existing_invoice:
                flash("Invoice number already exists. Please use a different invoice number.", 'error')
                return render_template('create_invoice_existing_customer.html', customers=customers)

            # Fetch customer details based on the selected ID
            cursor.execute("SELECT * FROM customers WHERE id = %s", (selected_customer_id,))
            customer_data = cursor.fetchone()

            session['invoiceName'] = invoiceName
            session['email'] = customer_data[3]  # Assuming email is at index 3 in customer_data

            return redirect(url_for('create_invoice_main'))
        except Exception as e:
            db.rollback()
            return f"Error: {e}"
        finally:
            cursor.close()
            db.close()

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
            query = "SELECT * FROM customers"
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

    


# @app.route('/manage_invoices')
# def manage_invoices():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     # Add logic to fetch and display invoices from the database
#     connection = check_db_connection()
#     if connection:
#         cursor = connection.cursor()
#         query = "SELECT * FROM invoices"
#         cursor.execute(query)
#         invoices = cursor.fetchall()
#         connection.close()

#         # Check if invoices are being fetched properly
#         print(invoices)  # Check the console/terminal for output

    

#         return render_template('manage_invoice.html', invoices=invoices)


# Assuming you have your database connection and app setup correctly
# Replace `check_db_connection()` with your actual database connection setup

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

        # Check if invoices are being fetched properly
        print(invoices)  # Check the console/terminal for output

        return render_template('manage_invoice.html', invoices=invoices)
    
@app.route('/update_status/<int:invoice_id>', methods=['POST'])
def update_status(invoice_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()
        # Fetch the current status of the invoice
        query_status = "SELECT status FROM invoices WHERE id = %s"
        cursor.execute(query_status, (invoice_id,))
        current_status = cursor.fetchone()[0]

        # Toggle the status
        new_status = 'paid' if current_status == 'open' else 'open'

        # Update the status in the database
        update_query = "UPDATE invoices SET status = %s WHERE id = %s"
        cursor.execute(update_query, (new_status, invoice_id))
        connection.commit()
        connection.close()

        # Optionally, you can add a flash message or any other feedback here
        flash(f"Invoice ID {invoice_id} status changed to {new_status}")

        return redirect(url_for('manage_invoices'))
    return "Database connection error"



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


# Add the following route for deleting products
@app.route('/delete_products', methods=['POST', 'GET'])
def delete_products():
    if 'username' not in session:
        return redirect(url_for('login'))

    connection = check_db_connection()
    if connection:
        cursor = connection.cursor()

        try:
            # Get the list of product IDs to be deleted
            products_to_delete = request.form.getlist('delete_products[]')

            if products_to_delete:
                # Create a comma-separated string of product IDs for the SQL query
                product_ids_str = ', '.join(map(str, products_to_delete))

                # Delete selected products from the database
                delete_query = f"DELETE FROM products WHERE product_id IN ({product_ids_str})"
                cursor.execute(delete_query)
                connection.commit()

                flash(f"{len(products_to_delete)} product(s) deleted successfully!", 'success')
            else:
                flash("No products selected for deletion.", 'info')

        except Exception as e:
            connection.rollback()
            flash(f"Error deleting products: {str(e)}", 'error')
        finally:
            connection.close()

    return redirect(url_for('manage_products'))

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
    
def fetch_invoice_details(invoice_id):
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM invoices WHERE invoice = %s", (invoice_id,))
        invoice_details = cursor.fetchone()

        connection.close()
        return invoice_details
    return None

# Fetch Invoice Items from Database
def fetch_invoice_items(invoice_id):
    connection = check_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM invoice_items WHERE invoice = %s", (invoice_id,))
        invoice_items = cursor.fetchall()
        print(invoice_items)
        connection.close()
        return invoice_items
    return None

# Generate Invoice PDF
def generate_invoice_pdf(invoice_id):
    invoice_details = fetch_invoice_details(invoice_id)
    items = fetch_invoice_items(invoice_id)

    if not invoice_details or not items:
        return None  # Handle the case where fetching fails

    rendered = render_template('invoice_template.html', invoice=invoice_details, items=items)

    try:
        pdf = pdfkit.from_string(rendered, False)
        pdf_filename = f"invoice_{invoice_id}.pdf"
        with open(pdf_filename, 'wb') as f:
            f.write(pdf)
        return pdf_filename
    except Exception as e:
        print(f"Failed to generate PDF: {e} in main generate_invoice_pdf")
        return None



@app.route('/generate_invoice_pdf_endpoint/<int:invoice_id>', methods=['GET'])
def generate_invoice_pdf_endpoint(invoice_id):
    # Logic to generate the PDF file for the given invoice_id
    # Assume `generate_pdf(invoice_id)` is a function that generates the PDF file path

    pdf_path = generate_invoice_pdf(invoice_id)  # Replace with your PDF generation logic

    if pdf_path:
        try:
            response = make_response(send_file(pdf_path, as_attachment=True))
            response.headers['Content-Disposition'] = f'attachment; filename=invoice_{invoice_id}.pdf'
            # Optionally, remove the generated PDF after sending
            # os.remove(pdf_path)
            return response
        except Exception as e:
            print(f"Failed to send PDF: {e}")
            return jsonify({'error': 'Failed to send PDF'})
    else:
        return jsonify({'error': 'Failed to generate PDF in endpoint'})



# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
