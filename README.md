# Pharmacy Inventory Management System

This is a web application built with Python and Flask that allows pharmacies to manage their drug inventory, track prescriptions, and monitor stock levels. The application provides features such as adding new drugs, creating prescriptions, dispensing drugs, and viewing inventory counts on any given date.

## Features

- Add new drugs to the inventory
- Create prescriptions with serial numbers
- Dispense prescribed drugs and update stock levels
- View current inventory count
- Track inventory history with transaction logs
- Calculate inventory count on a specific date

## Installation

1. Clone the repository:
   git clone https://github.com/OmarAbdelqader/pharma_app.git
2. Navigate to the project directory:
   cd pharma_app
3. Create and activate a virtual environment (optional but recommended):
   python -m venv env
   source env/bin/activate  # On Windows, use env\Scripts\activate
4. Install the required dependencies:
   pip install flask
5. Run the application:
   python app.py
6. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Add new drugs to the inventory by providing the drug name, quantity, and expiry date.
2. Create prescriptions by entering the prescription serial number and selecting the prescribed drug(s) and quantity.
3. View the current inventory count on the homepage.
4. Access the "Inventory Count" page to view the inventory count of a specific drug on a selected date.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please open an issue or submit a pull request.

