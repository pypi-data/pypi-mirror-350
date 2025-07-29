Артур
Ахи 🐺, [23.05.2025 0: 27]
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit,
                             QPushButton, QMessageBox, QTableWidget, QTableWidgetItem,
                             QDialog, QDialogButtonBox, QLabel, QFormLayout)
from PyQt5.QtCore import Qt
import pymysql


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()


class AddEditClientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Client")

        layout = QVBoxLayout()

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Client Name")
        layout.addWidget(self.client_name_input)

        self.client_address_input = QLineEdit()
        self.client_address_input.setPlaceholderText("Client Address")
        layout.addWidget(self.client_address_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(layout)

    def get_data(self):
        return self.client_name_input.text(), self.client_address_input.text()


class AddEditWorkerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Worker")

        layout = QVBoxLayout()

        self.worker_name_input = QLineEdit()
        self.worker_name_input.setPlaceholderText("Worker Name")
        layout.addWidget(self.worker_name_input)

        self.worker_qualification_input = QLineEdit()
        self.worker_qualification_input.setPlaceholderText("Worker Qualification")
        layout.addWidget(self.worker_qualification_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(layout)

    def get_data(self):
        return self.worker_name_input.text(), self.worker_qualification_input.text()


class AddEditOrderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Order")

        layout = QVBoxLayout()

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Client ID")
        layout.addWidget(self.client_id_input)

        self.worker_id_input = QLineEdit()
        self.worker_id_input.setPlaceholderText("Worker ID")
        layout.addWidget(self.worker_id_input)

        self.work_type_input = QLineEdit()
        self.work_type_input.setPlaceholderText("Work Type")
        layout.addWidget(self.work_type_input)

        self.payment_input = QLineEdit()
        self.payment_input.setPlaceholderText("Payment")
        layout.addWidget(self.payment_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.


Артур
Ахи 🐺, [23.05.2025 0: 27]
connect(self.reject)

self.setLayout(layout)


def get_data(self):
    return self.client_id_input.text(), self.worker_id_input.text(), self.work_type_input.text(), self.payment_input.text()


class MainWindow(QMainWindow):
    def __init__(self, user_role):
        super().__init__()
        self.setWindowTitle("Auto Repair Shop Management")
        self.setGeometry(100, 100, 800, 600)
        self.user_role = user_role  # 'admin' or 'user'

        layout = QVBoxLayout()

        self.client_button = QPushButton("Show Clients")
        self.client_button.clicked.connect(self.show_clients)
        layout.addWidget(self.client_button)

        self.worker_button = QPushButton("Show Workers")
        self.worker_button.clicked.connect(self.show_workers)
        layout.addWidget(self.worker_button)

        self.order_button = QPushButton("Show Orders")
        self.order_button.clicked.connect(self.show_orders)
        layout.addWidget(self.order_button)

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        # Add buttons
        self.add_client_button = QPushButton("Add Client")
        self.add_client_button.clicked.connect(self.add_client)
        layout.addWidget(self.add_client_button)

        self.edit_client_button = QPushButton("Edit Client")
        self.edit_client_button.clicked.connect(self.edit_client)
        layout.addWidget(self.edit_client_button)

        self.delete_client_button = QPushButton("Delete Client")
        self.delete_client_button.clicked.connect(self.delete_client)
        layout.addWidget(self.delete_client_button)

        self.add_worker_button = QPushButton("Add Worker")
        self.add_worker_button.clicked.connect(self.add_worker)
        layout.addWidget(self.add_worker_button)

        self.edit_worker_button = QPushButton("Edit Worker")
        self.edit_worker_button.clicked.connect(self.edit_worker)
        layout.addWidget(self.edit_worker_button)

        self.delete_worker_button = QPushButton("Delete Worker")
        self.delete_worker_button.clicked.connect(self.delete_worker)
        layout.addWidget(self.delete_worker_button)

        self.add_order_button = QPushButton("Add Order")
        self.add_order_button.clicked.connect(self.add_order)
        layout.addWidget(self.add_order_button)

        self.edit_order_button = QPushButton("Edit Order")
        self.edit_order_button.clicked.connect(self.edit_order)
        layout.addWidget(self.edit_order_button)

        self.delete_order_button = QPushButton("Delete Order")
        self.delete_order_button.clicked.connect(self.delete_order)
        layout.addWidget(self.delete_order_button)

        # Special function buttons
        self.show_client_orders_button = QPushButton("Show Client Orders")
        self.show_client_orders_button.clicked.connect(self.show_client_orders)
        layout.addWidget(self.show_client_orders_button)

        self.calculate_worker_bonus_button = QPushButton("Calculate Worker Bonus")
        self.calculate_worker_bonus_button.clicked.connect(self.calculate_worker_bonus)
        layout.addWidget(self.calculate_worker_bonus_button)

        self.top_workers_button = QPushButton("Top 3 Workers")
        self.top_workers_button.clicked.connect(self.top_workers)
        layout.addWidget(self.top_workers_button)

        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Database connection
        self.db_connection = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        self.cursor = self.db_connection.cursor()

        # Set permissions based on user role
        self.set_permissions()

    def set_permissions(self):
        if self.user_role == 'user':
            # Regular users can only view data and use special functions
            self.


Артур
Ахи 🐺, [23.05.2025 0: 27]
add_client_button.setEnabled(False)
self.edit_client_button.setEnabled(False)
self.delete_client_button.setEnabled(False)
self.add_worker_button.setEnabled(False)
self.edit_worker_button.setEnabled(False)
self.delete_worker_button.setEnabled(False)
self.add_order_button.setEnabled(False)
self.edit_order_button.setEnabled(False)
self.delete_order_button.setEnabled(False)
elif self.user_role == 'admin':
# Admins can do everything
pass


def logout(self):
    self.close()
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        username, password = login_dialog.get_credentials()
        if self.authenticate_user(username, password):
            role = self.get_user_role(username)
            main_window = MainWindow(role)
            main_window.show()
        else:
            QMessageBox.warning(None, "Login Failed", "Invalid username or password")
            sys.exit()


def authenticate_user(self, username, password):
    # In a real application, you would hash the password and check against the database
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    self.cursor.execute(query, (username, password))
    return self.cursor.fetchone() is not None


def get_user_role(self, username):
    query = "SELECT role FROM users WHERE username = %s"
    self.cursor.execute(query, (username,))
    result = self.cursor.fetchone()
    return result[0] if result else 'user'


def show_client_orders(self):
    row = self.result_table.currentRow()
    if row != -1:
        client_id = self.result_table.item(row, 0).text()
        query = "SELECT * FROM Orders WHERE ClientID = %s"
        self.cursor.execute(query, (client_id,))
        orders = self.cursor.fetchall()
        if orders:
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(len(orders[0]))
            self.result_table.setHorizontalHeaderLabels(["OrderID", "ClientID", "WorkerID", "Work Type", "Payment"])
            for row_number, order in enumerate(orders):
                self.result_table.insertRow(row_number)
                for column_number, data in enumerate(order):
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    else:
        QMessageBox.warning(self, "Warning", "Please select a client to show orders for.")


def calculate_worker_bonus(self):
    query = "SELECT WorkerID, SUM(Payment) * 0.3 AS Bonus FROM Orders GROUP BY WorkerID"
    self.cursor.execute(query)
    worker_bonuses = self.cursor.fetchall()
    if worker_bonuses:
        bonus_text = "WorkerID\tBonus\n"
        for worker_bonus in worker_bonuses:
            worker_id, bonus = worker_bonus
            bonus_text += f"{worker_id}\t{bonus}\n"
        QMessageBox.information(self, "Worker Bonuses", bonus_text)
    else:
        QMessageBox.warning(self, "Warning", "No worker bonuses calculated.")


def top_workers(self):
    query = "SELECT WorkerID, COUNT(*) AS OrdersCount FROM Orders GROUP BY WorkerID ORDER BY OrdersCount DESC LIMIT 3"
    self.cursor.execute(query)
    top_workers = self.cursor.fetchall()
    if top_workers:
        top_workers_text = "Top 3 Workers\n\nWorkerID\tOrders Count\n"
        for worker in top_workers:
            worker_id, orders_count = worker
            top_workers_text += f"{worker_id}\t{orders_count}\n"
        QMessageBox.information(self, "Top 3 Workers", top_workers_text)
    else:
        QMessageBox.warning(self, "Warning", "No top workers found.")


def show_clients(self):
    self.result_table.setRowCount(0)
    query = "SELECT * FROM Clients"
    self.cursor.execute(query)
    clients = self.cursor.fetchall()


Артур
Ахи 🐺, [23.05.2025 0: 27]
if clients:
    self.result_table.setColumnCount(len(clients[0]))
    self.result_table.setHorizontalHeaderLabels(["ClientID", "FullName", "Address"])
    for row_number, client in enumerate(clients):
        self.result_table.insertRow(row_number)
        for column_number, data in enumerate(client):
            self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


def show_workers(self):
    self.result_table.setRowCount(0)
    query = "SELECT * FROM Workers"
    self.cursor.execute(query)
    workers = self.cursor.fetchall()
    if workers:
        self.result_table.setColumnCount(len(workers[0]))
        self.result_table.setHorizontalHeaderLabels(["WorkerID", "FullName", "Qualification"])
        for row_number, worker in enumerate(workers):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(worker):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


def show_orders(self):
    self.result_table.setRowCount(0)
    query = "SELECT * FROM Orders"
    self.cursor.execute(query)
    orders = self.cursor.fetchall()
    if orders:
        self.result_table.setColumnCount(len(orders[0]))
        self.result_table.setHorizontalHeaderLabels(["OrderID", "ClientID", "WorkerID", "Work Type", "Payment"])
        for row_number, order in enumerate(orders):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(order):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


def add_client(self):
    dialog = AddEditClientDialog()
    if dialog.exec_() == QDialog.Accepted:
        client_name, client_address = dialog.get_data()
        query = "INSERT INTO Clients (FullName, Address) VALUES (%s, %s)"
        self.cursor.execute(query, (client_name, client_address))
        self.db_connection.commit()
        self.show_clients()


def edit_client(self):
    row = self.result_table.currentRow()
    if row != -1:
        dialog = AddEditClientDialog()
        client_id = self.result_table.item(row, 0).text()
        client_name = self.result_table.item(row, 1).text()
        client_address = self.result_table.item(row, 2).text()
        dialog.client_name_input.setText(client_name)
        dialog.client_address_input.setText(client_address)
        if dialog.exec_() == QDialog.Accepted:
            new_client_name, new_client_address = dialog.get_data()
            query = "UPDATE Clients SET FullName = %s, Address = %s WHERE ClientID = %s"
            self.cursor.execute(query, (new_client_name, new_client_address, client_id))
            self.db_connection.commit()
            self.show_clients()
    else:
        QMessageBox.warning(self, "Warning", "Please select a client to edit.")


def delete_client(self):
    row = self.result_table.currentRow()
    if row != -1:
        client_id = self.result_table.item(row, 0).text()
        reply = QMessageBox.question(self, 'Delete Client', 'Are you sure you want to delete this client?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            query = "DELETE FROM Clients WHERE ClientID = %s"
            self.cursor.execute(query, (client_id,))
            self.db_connection.commit()
            self.show_clients()
    else:
        QMessageBox.warning(self, "Warning", "Please select a client to delete.")


def add_worker(self):
    dialog = AddEditWorkerDialog()
    if dialog.exec_() == QDialog.Accepted:
        worker_name, worker_qualification = dialog.get_data()
        query = "INSERT INTO Workers (FullName, Qualification) VALUES (%s, %s)"
        self.cursor.


Артур
Ахи 🐺, [23.05.2025 0: 27]
execute(query, (worker_name, worker_qualification))
self.db_connection.commit()
self.show_workers()


def edit_worker(self):
    row = self.result_table.currentRow()
    if row != -1:
        dialog = AddEditWorkerDialog()
        worker_id = self.result_table.item(row, 0).text()
        worker_name = self.result_table.item(row, 1).text()
        worker_qualification = self.result_table.item(row, 2).text()
        dialog.worker_name_input.setText(worker_name)
        dialog.worker_qualification_input.setText(worker_qualification)
        if dialog.exec_() == QDialog.Accepted:
            new_worker_name, new_worker_qualification = dialog.get_data()
            query = "UPDATE Workers SET FullName = %s, Qualification = %s WHERE WorkerID = %s"
            self.cursor.execute(query, (new_worker_name, new_worker_qualification, worker_id))
            self.db_connection.commit()
            self.show_workers()
    else:
        QMessageBox.warning(self, "Warning", "Please select a worker to edit.")


def delete_worker(self):
    row = self.result_table.currentRow()
    if row != -1:
        worker_id = self.result_table.item(row, 0).text()
        reply = QMessageBox.question(self, 'Delete Worker', 'Are you sure you want to delete this worker?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            query = "DELETE FROM Workers WHERE WorkerID = %s"
            self.cursor.execute(query, (worker_id,))
            self.db_connection.commit()
            self.show_workers()
    else:
        QMessageBox.warning(self, "Warning", "Please select a worker to delete.")


def add_order(self):
    dialog = AddEditOrderDialog()
    if dialog.exec_() == QDialog.Accepted:
        client_id, worker_id, work_type, payment = dialog.get_data()
        query = "INSERT INTO Orders (ClientID, WorkerID, WorkType, Payment) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (client_id, worker_id, work_type, payment))
        self.db_connection.commit()
        self.show_orders()


def edit_order(self):
    row = self.result_table.currentRow()
    if row != -1:
        dialog = AddEditOrderDialog()
        order_id = self.result_table.item(row, 0).text()
        client_id = self.result_table.item(row, 1).text()
        worker_id = self.result_table.item(row, 2).text()
        work_type = self.result_table.item(row, 3).text()
        payment = self.result_table.item(row, 4).text()
        dialog.client_id_input.setText(client_id)
        dialog.worker_id_input.setText(worker_id)
        dialog.work_type_input.setText(work_type)
        dialog.payment_input.setText(payment)
        if dialog.exec_() == QDialog.Accepted:
            new_client_id, new_worker_id, new_work_type, new_payment = dialog.get_data()
            query = "UPDATE Orders SET ClientID = %s, WorkerID = %s, WorkType = %s, Payment = %s WHERE OrderID = %s"
            self.cursor.execute(query, (new_client_id, new_worker_id, new_work_type, new_payment, order_id))
            self.db_connection.commit()
            self.show_orders()
    else:
        QMessageBox.warning(self, "Warning", "Please select an order to edit.")


def delete_order(self):
    row = self.result_table.currentRow()
    if row != -1:
        order_id = self.result_table.item(row, 0).text()
        reply = QMessageBox.question(self, 'Delete Order', 'Are you sure you want to delete this order?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            query = "DELETE FROM Orders WHERE OrderID = %s"
            self.cursor.execute(query, (order_id,))
            self.db_connection.commit()
            self.show_orders()
    else:
        QMessageBox.


Артур
Ахи 🐺, [23.05.2025 0: 27]
warning(self, "Warning", "Please select an order to delete.")


def closeEvent(self, event):
    self.db_connection.close()


if name == "__main__":
    app = QApplication(sys.argv)

    # Create users table if it doesn't exist
    try:
        connection = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
        cursor = connection.cursor()

        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'user'
        )
        """)

        # Add default admin user if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
            cursor.execute("INSERT INTO users (username, password, role) VALUES ('user', 'user123', 'user')")
            connection.commit()

        connection.close()
    except Exception as e:
        print(f"Error setting up database: {e}")

    # Show login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        username, password = login_dialog.get_credentials()

        # Authenticate user
        try:
            connection = pymysql.connect(host='localhost', user='root', password='', database='auto_repair_shop')
            cursor = connection.cursor()

            cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result:
                role = result[0]
                window = MainWindow(role)
                window.show()
                sys.exit(app.exec_())
            else:
                QMessageBox.warning(None, "Login Failed", "Invalid username or password")
                sys.exit(1)

        except Exception as e:
            QMessageBox.critical(None, "Database Error", f"Could not connect to database: {e}")
            sys.exit(1)
    else:
        sys.exit(0)