# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

# Database connection
conn = sqlite3.connect('pharmacy.db', check_same_thread=False)
c = conn.cursor()

# Create table for drugs
c.execute('''CREATE TABLE IF NOT EXISTS drugs
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER, expiry_date TEXT)''')
conn.commit()

# Inventory transaction log for dispensed or received drugs
c.execute('''CREATE TABLE IF NOT EXISTS inventory_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_id INTEGER,
    quantity INTEGER,
    transaction_date TEXT,
    transaction_type TEXT,
    FOREIGN KEY(drug_id) REFERENCES drugs(id)
)''')
conn.commit()


# SQL query to retrieve all drugs
select_all_drugs = """
    SELECT d.id, d.name, d.expiry_date
    FROM drugs d
    LEFT JOIN inventory_log l ON d.id = l.drug_id
    GROUP BY d.id
    ORDER BY d.name, d.expiry_date ASC
"""
# global variables
current_date = date.today().isoformat()

# Routes
@app.route('/')
def index():
    try:
        # Sort drugs by name and expiry_date
        c.execute(select_all_drugs)
        drugs = c.fetchall()
        return render_template('index.html', drugs=drugs)
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"An error occurred: {e}")
        return "An error occurred", 500

@app.route('/add', methods=['GET', 'POST'])
def add_drug():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        expiry_date = request.form['expiry_date']
        c.execute("INSERT INTO drugs (name, quantity, expiry_date) VALUES (?, ?, ?)", (name, 0, expiry_date))
        conn.commit()
        drug_id = c.lastrowid
        c.execute("INSERT INTO inventory_log (drug_id, quantity, transaction_date, transaction_type) VALUES (?, ?, DATE('now'), 'received')", (drug_id, quantity))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add_drug.html')


# Prescription management
c.execute('''CREATE TABLE IF NOT EXISTS prescriptions
             (id INTEGER PRIMARY KEY AUTOINCREMENT, prescription_serial_number TEXT)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS prescription_drugs
             (id INTEGER PRIMARY KEY AUTOINCREMENT, prescription_id INTEGER, drug_id INTEGER, quantity INTEGER, prescription_date TEXT, FOREIGN KEY(prescription_id) REFERENCES prescriptions(id), FOREIGN KEY(drug_id) REFERENCES drugs(id))''')
conn.commit()


@app.route('/add_prescription', methods=['GET', 'POST'])
def add_prescription():
    if request.method == 'POST':
        prescription_serial_number_1 = request.form['prescription_serial_number_1']
        prescription_serial_number_2 = request.form['prescription_serial_number_2']
        prescription_serial_number = prescription_serial_number_1 + prescription_serial_number_2
        c.execute("INSERT INTO prescriptions (prescription_serial_number) VALUES (?)", (prescription_serial_number,))
        conn.commit()
        prescription_id = c.lastrowid
        # Add prescribed drugs and update inventory log
        drug_id = request.form.get('drugs')
        quantity = request.form.get('quantity', 1)
        prescription_date = request.form.get('prescription_date')
        c.execute("INSERT INTO prescription_drugs (prescription_id, drug_id, quantity, prescription_date) VALUES (?, ?, ?, ?)", (prescription_id, drug_id, quantity, prescription_date))
        conn.commit()
        # Update inventory log for dispensed drug
        c.execute("INSERT INTO inventory_log (drug_id, quantity, transaction_date, transaction_type) VALUES (?, ?, ?, 'dispensed')", (drug_id, -int(quantity), prescription_date))
        conn.commit()
        return redirect(url_for('index'))
    # Sort drugs by name and expiry_date
    c.execute(select_all_drugs)
    drugs = c.fetchall()
    return render_template('add_prescription.html', drugs=drugs, current_date=current_date)


@app.route('/inventory_count', methods=['GET', 'POST'])
def inventory_count():
    c.execute(select_all_drugs)
    drugs = c.fetchall()
    if request.method == 'POST':
        drug_id = request.form.get('drug_id')
        date_str = request.form.get('date')
        c.execute("SELECT name, expiry_date FROM drugs WHERE id = ?", (drug_id,))
        drug_details = c.fetchone()

        if drug_details:
            c.execute("SELECT SUM(quantity) AS total_quantity FROM inventory_log WHERE drug_id = ? AND transaction_date <= ? GROUP BY drug_id", (drug_id, date_str))
            result = c.fetchone()
            total_quantity = result[0] if result else 0  # Handle case when no results are found
            return render_template('inventory_count.html',current_date=current_date, drugs=drugs, drug_details=drug_details, total_quantity=total_quantity, date=date_str)
        else:
            return "Drug not found", 404
    return render_template('inventory_count.html', current_date=current_date, drugs=drugs)

if __name__ == '__main__':
    app.run(debug=True)