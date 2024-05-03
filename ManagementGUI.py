import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from Classes import Employee, Guest, Venue, Supplier, Event, EventType, save_data, load_data, JobTitle
import random


class ManagementSystemGUI:
    def __init__(self, master):
        #Initialize the main window with the necessary widgets and load data from files.

        self.master = master
        self.master.title("Best Events Company Management System")

        # Load data from persistent storage, handling potential errors if data files are missing.
        self.employees = load_data("employees.pkl")
        self.clients_events = load_data("clients_events.pkl")
        self.events = load_data("events.pkl")
        self.suppliers = load_data("suppliers.pkl")
        self.guests = load_data("guests.pkl")
        self.venues = load_data("venues.pkl")

        # Setup the initial interface that users see upon launching the application.
        self.setup_welcome_frame()

    def setup_welcome_frame(self):
        # Set up the welcome frame that allows users to select their role to log in.

        self.welcome_frame = tk.Frame(self.master)
        self.welcome_frame.pack(padx=10, pady=10)
        tk.Label(self.welcome_frame, text="Welcome to the Best Events Company Management System",
                 font=("Arial", 16)).pack(pady=20)
        tk.Label(self.welcome_frame, text="Please select your role to log in:").pack(pady=10)

        self.role_var = tk.StringVar()
        self.role_dropdown = ttk.Combobox(self.welcome_frame, textvariable=self.role_var, state="readonly",
                                          values=("Employee/Manager", "Client"))
        self.role_dropdown.pack(pady=10)
        self.role_dropdown.bind("<<ComboboxSelected>>", self.role_selected)

        self.management_frame = tk.Frame(self.master)

    def role_selected(self, event):
        # Handle the role dselection event.
        role = self.role_var.get()
        self.welcome_frame.pack_forget()
        self.management_frame.pack(padx=10, pady=10)

        # Clear any widgets from the management frame before displaying new widgets
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        if role == "Employee/Manager":
            self.display_employee_management_options()
        elif role == "Client":
            self.display_client_management_options()

    def display_employee_management_options(self):
        # Display the management options for Managing employees and Clients.

        tk.Button(self.management_frame, text="Manage Employees", command=self.manage_employees).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Clients", command=self.manage_clients).pack(pady=10)

    def display_client_management_options(self):
        # Display the management options for Managing Events and Suppliers and Guests.
        tk.Button(self.management_frame, text="Manage Events", command=self.display_event_management).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Suppliers", command=self.display_supplier_management).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Guests", command=self.display_guest_management).pack(pady=10)
        tk.Button(self.management_frame, text="Manage Venues", command=self.manage_venues).pack(pady=10)


    def manage_employees(self):
        self.display_employee_management()

    def manage_clients(self):
        self.display_client_management()

    def display_main_menu(self):
        # First, we ensure all frames are removed or hidden before showing the main menu again.
        for widget in self.master.winfo_children():
            widget.pack_forget()  # This will hide all widgets in the root window

        # Now, call the setup function for the welcome frame to rebuild the main menu
        self.setup_welcome_frame()
        self.welcome_frame.pack(padx=10, pady=10)  # Ensure the welcome frame is visible

    # The employee management system (After user pick the Employee/Manager role they see Manage employee options)
    def display_employee_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        self.employee_tree = ttk.Treeview(self.management_frame,
                                          columns=("ID", "Name", "Department", "Job Title", "Salary"), show="headings")
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Name", text="Name")
        self.employee_tree.heading("Department", text="Department")
        self.employee_tree.heading("Job Title", text="Job Title")
        self.employee_tree.heading("Salary", text="Salary")
        self.employee_tree.pack(padx=10, pady=10, expand=True, fill='both')

        tk.Button(self.management_frame, text="Add Employee", command=self.add_employee).pack(side=tk.LEFT, padx=10,
                                                                                              pady=10)
        tk.Button(self.management_frame, text="Delete Employee", command=self.delete_employee).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Modify Employee", command=self.modify_employee).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Display Employee Details", command=self.display_employee).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)

        self.update_employee_tree()

    def update_employee_tree(self):
        self.employee_tree.delete(*self.employee_tree.get_children())
        for emp_id, emp in self.employees.items():
            self.employee_tree.insert("", "end",
                                      values=(emp.id, emp.name, emp.department, emp.job_title.value, emp.salary))

    def add_employee(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Employee")

        # Generate the next unique employee ID
        next_id = max(self.employees.keys(), default=0) + 1

        # Name entry
        tk.Label(add_window, text="Name:").grid(row=1, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=1, column=1)

        # Department entry
        tk.Label(add_window, text="Department:").grid(row=2, column=0)
        department_var = tk.StringVar()
        department_dropdown = ttk.Combobox(add_window, textvariable=department_var, state="readonly",
                                           values=["Event Planner", "Sales", "Event Director", "Hospitality",
                                                   "Management", "Operations"])
        department_dropdown.grid(row=2, column=1)

        # Job Title entry
        tk.Label(add_window, text="Job Title:").grid(row=3, column=0)
        job_title_var = tk.StringVar()
        job_title_dropdown = ttk.Combobox(add_window, textvariable=job_title_var, state="readonly",
                                          values=[jt.value for jt in JobTitle])
        job_title_dropdown.grid(row=3, column=1)

        # Salary (automatically assigned)
        salary = random.randint(30000, 100000)
        tk.Label(add_window, text="Assigned Salary: $" + str(salary)).grid(row=4, column=1)

        # Save button
        tk.Button(add_window, text="Save Employee",
                  command=lambda: self.save_new_employee(add_window, next_id, name_entry.get(), department_var.get(),
                                                         job_title_var.get(), salary)).grid(row=5, columnspan=2)

    def save_new_employee(self, add_window, emp_id, name, department, job_title, salary):
        job_title_enum = JobTitle[job_title.replace(' ', '_').upper()]  # Convert string to JobTitle enum
        if name and department and job_title:
            new_emp = Employee(emp_id, name, department, job_title_enum, salary)
            self.employees[emp_id] = new_emp
            save_data(self.employees, "employees.pkl")
            self.update_employee_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Employee added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_employee(self):
        selected_item = self.employee_tree.selection()
        if selected_item:
            emp_id = int(self.employee_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you want to delete this employee?"):
                del self.employees[emp_id]
                save_data(self.employees, "employees.pkl")
                self.update_employee_tree()
                messagebox.showinfo("Success", "Employee deleted successfully")
        else:
            messagebox.showerror("Error", "No employee selected")

    def modify_employee(self):
        selected_item = self.employee_tree.selection()
        if selected_item:
            emp_id = int(self.employee_tree.item(selected_item, 'values')[0])
            employee = self.employees.get(emp_id)
            if employee:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Employee Details")

                # Entry for Name
                tk.Label(modify_window, text="Name:").grid(row=0, column=0)
                name_entry = tk.Entry(modify_window)
                name_entry.insert(0, employee.name)
                name_entry.grid(row=0, column=1)

                # Dropdown for Department
                tk.Label(modify_window, text="Department:").grid(row=1, column=0)
                department_var = tk.StringVar(value=employee.department)
                department_dropdown = ttk.Combobox(modify_window, textvariable=department_var, state="readonly",
                                                   values=["Event Planner", "Sales", "Event Director", "Hospitality",
                                                           "Management", "Operations"])
                department_dropdown.grid(row=1, column=1)

                # Dropdown for Job Title
                tk.Label(modify_window, text="Job Title:").grid(row=2, column=0)
                job_title_var = tk.StringVar(value=employee.job_title.value)
                job_title_dropdown = ttk.Combobox(modify_window, textvariable=job_title_var, state="readonly",
                                                  values=[jt.value for jt in JobTitle])
                job_title_dropdown.grid(row=2, column=1)

                # Entry for Salary
                tk.Label(modify_window, text="Salary:").grid(row=3, column=0)
                salary_entry = tk.Entry(modify_window)
                salary_entry.insert(0, str(employee.salary))
                salary_entry.grid(row=3, column=1)

                # Save button
                tk.Button(modify_window, text="Save Changes",
                          command=lambda: self.apply_employee_changes(modify_window, emp_id, name_entry.get(),
                                                                      department_var.get(), job_title_var.get(),
                                                                      salary_entry.get())).grid(row=4, columnspan=2)
            else:
                messagebox.showerror("Error", "Employee not found")
        else:
            messagebox.showerror("Error", "No employee selected")

    def apply_employee_changes(self, modify_window, emp_id, name, department, job_title, salary):
        employee = self.employees[emp_id]
        if name and department and job_title and salary:
            employee.name = name
            employee.department = department
            employee.job_title = JobTitle[job_title.replace(' ', '_').upper()]
            employee.salary = int(salary)
            save_data(self.employees, "employees.pkl")
            self.update_employee_tree()
            modify_window.destroy()
            messagebox.showinfo("Success", "Employee details updated successfully")
        else:
            messagebox.showerror("Error", "All fields are required")

    def display_employee(self):
        emp_id = simpledialog.askinteger("Display Employee", "Enter Employee ID:")
        if emp_id is not None:
            employee = self.employees.get(emp_id)
            if employee:
                details = f"ID: {employee.id}\nName: {employee.name}\nDepartment: {employee.department}\nJob Title: {employee.job_title.name}\nSalary: ${employee.salary}"
                messagebox.showinfo("Employee Details", details)
            else:
                messagebox.showerror("Error", f"No employee found with ID: {emp_id}")
        else:
            messagebox.showerror("Error", "Invalid Employee ID")

    # The Client management system (After user pick the Employee/Manager role they see Manage Clients option)
    def display_client_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        self.client_tree = ttk.Treeview(self.management_frame,
                                        columns=("Client ID", "Type", "Date", "Time", "Duration", "Venue"),
                                        show="headings")
        self.client_tree.heading("Client ID", text="Client ID")
        self.client_tree.heading("Type", text="Type")
        self.client_tree.heading("Date", text="Date")
        self.client_tree.heading("Time", text="Time")
        self.client_tree.heading("Duration", text="Duration")
        self.client_tree.heading("Venue", text="Venue")
        self.client_tree.pack(padx=10, pady=10, fill='both', expand=True)

        tk.Button(self.management_frame, text="Add Client", command=self.add_client).pack(side=tk.LEFT, padx=10,
                                                                                          pady=10)
        tk.Button(self.management_frame, text="Delete Client", command=self.delete_client).pack(side=tk.LEFT, padx=10,
                                                                                                pady=10)
        tk.Button(self.management_frame, text="Modify Client", command=self.modify_client).pack(side=tk.LEFT, padx=10,
                                                                                                pady=10)
        tk.Button(self.management_frame, text="Display Client Details", command=self.display_client_details).pack(
            side=tk.LEFT, padx=10, pady=10)

        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)

        self.update_client_tree()

    def update_client_tree(self):
        self.client_tree.delete(*self.client_tree.get_children())
        for client_id, details in self.clients_events.items():
            self.client_tree.insert("", "end", values=(
                client_id, details['type'], details['date'], details['time'], details['duration'], details['venue']))

    def add_client(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Client")

        client_id = max(self.clients_events.keys(), default=0) + 1

        tk.Label(add_window, text="Assigned Client ID:").grid(row=0, column=0)
        tk.Label(add_window, text=str(client_id)).grid(row=0, column=1)

        tk.Label(add_window, text="Type:").grid(row=1, column=0)
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(add_window, textvariable=type_var, state="readonly",
                                     values=["Wedding", "Birthday", "Corporate", "Other"])
        type_dropdown.grid(row=1, column=1)

        tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Time (HH:MM):").grid(row=3, column=0)
        time_entry = tk.Entry(add_window)
        time_entry.grid(row=3, column=1)

        tk.Label(add_window, text="Duration (Hours):").grid(row=4, column=0)
        duration_entry = tk.Entry(add_window)
        duration_entry.grid(row=4, column=1)

        tk.Label(add_window, text="Venue:").grid(row=5, column=0)
        venue_var = tk.StringVar()
        venue_dropdown = ttk.Combobox(add_window, textvariable=venue_var, state="readonly",
                                      values=["Venue A", "Venue B", "Venue C"])
        venue_dropdown.grid(row=5, column=1)

        tk.Button(add_window, text="Save Client",
                  command=lambda: self.save_new_client(add_window, client_id, type_var.get(), date_entry.get(),
                                                       time_entry.get(), duration_entry.get(), venue_var.get())).grid(
            row=6, columnspan=2)

    def save_new_client(self, add_window, client_id, type, date, time, duration, venue):
        if type and date and time and duration and venue:
            self.clients_events[client_id] = {'type': type, 'date': date, 'time': time, 'duration': duration,
                                              'venue': venue}
            save_data(self.clients_events, "clients_events.pkl")
            self.update_client_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Client added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_client(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            client_id = int(self.client_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you want to delete this client?"):
                del self.clients_events[client_id]
                save_data(self.clients_events, "clients_events.pkl")
                self.update_client_tree()
                messagebox.showinfo("Success", "Client deleted successfully")
        else:
            messagebox.showerror("Error", "No client selected")

    def modify_client(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            client_id = int(self.client_tree.item(selected_item, 'values')[0])
            client_details = self.clients_events.get(client_id)
            if client_details:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Client Details")

                tk.Label(modify_window, text="Type:").grid(row=0, column=0)
                type_var = tk.StringVar(value=client_details['type'])
                type_dropdown = ttk.Combobox(modify_window, textvariable=type_var, state="readonly",
                                             values=["Wedding", "Birthday", "Corporate", "Other"])
                type_dropdown.grid(row=0, column=1)

                tk.Label(modify_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0)
                date_entry = tk.Entry(modify_window)
                date_entry.insert(0, client_details['date'])
                date_entry.grid(row=1, column=1)

                tk.Label(modify_window, text="Time (HH:MM):").grid(row=2, column=0)
                time_entry = tk.Entry(modify_window)
                time_entry.insert(0, client_details['time'])
                time_entry.grid(row=2, column=1)

                tk.Label(modify_window, text="Duration (Hours):").grid(row=3, column=0)
                duration_entry = tk.Entry(modify_window)
                duration_entry.insert(0, client_details['duration'])
                duration_entry.grid(row=3, column=1)

                tk.Label(modify_window, text="Venue:").grid(row=4, column=0)
                venue_var = tk.StringVar(value=client_details['venue'])
                venue_dropdown = ttk.Combobox(modify_window, textvariable=venue_var, state="readonly",
                                              values=["Venue A", "Venue B", "Venue C"])
                venue_dropdown.grid(row=4, column=1)

                tk.Button(modify_window, text="Save Changes",
                          command=lambda: self.apply_client_changes(modify_window, client_id, type_var.get(),
                                                                    date_entry.get(), time_entry.get(),
                                                                    duration_entry.get(), venue_var.get())).grid(row=5,
                                                                                                                 columnspan=2)
            else:
                messagebox.showerror("Error", "Client not found")
        else:
            messagebox.showerror("Error", "No client selected")

    def apply_client_changes(self, modify_window, client_id, type, date, time, duration, venue):
        if type and date and time and duration and venue:
            self.clients_events[client_id] = {'type': type, 'date': date, 'time': time, 'duration': duration,
                                              'venue': venue}
            save_data(self.clients_events, "clients_events.pkl")
            self.update_client_tree()
            modify_window.destroy()
            messagebox.showinfo("Success", "Client details updated successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_client_details(self):
        client_id = simpledialog.askinteger("Display Client", "Enter Client ID:")
        if client_id is not None:
            client_details = self.clients_events.get(client_id)
            if client_details:
                details = f"Type: {client_details['type']}\nDate: {client_details['date']}\nTime: {client_details['time']}\nDuration: {client_details['duration']} hours\nVenue: {client_details['venue']}"
                messagebox.showinfo("Client Details", f"Client ID: {client_id}\nDetails:\n{details}")
            else:
                messagebox.showerror("Error", f"No details found for client with ID: {client_id}")
        else:
            messagebox.showerror("Error", "Invalid Client ID")

    # The Supplier management system (After user pick the Client role they see Manage Suppliers option
    def display_supplier_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        self.supplier_tree = ttk.Treeview(self.management_frame,
                                          columns=("Supplier ID", "Name", "Service", "Contact Details"),
                                          show="headings")
        self.supplier_tree.heading("Supplier ID", text="Supplier ID")
        self.supplier_tree.heading("Name", text="Name")
        self.supplier_tree.heading("Service", text="Service")
        self.supplier_tree.heading("Contact Details", text="Contact Details")

        self.supplier_tree.pack(padx=10, pady=10, expand=True, fill='both')

        tk.Button(self.management_frame, text="Add Supplier", command=self.add_supplier).pack(side=tk.LEFT, padx=10,
                                                                                              pady=10)
        tk.Button(self.management_frame, text="Delete Supplier", command=self.delete_supplier).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Modify Supplier", command=self.modify_supplier).pack(side=tk.LEFT,
                                                                                                    padx=10, pady=10)
        tk.Button(self.management_frame, text="Display Supplier Details", command=self.display_supplier_details).pack(
            side=tk.LEFT, padx=10, pady=10)

        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)

        self.update_supplier_tree()

    def update_supplier_tree(self):
        self.supplier_tree.delete(*self.supplier_tree.get_children())
        for supplier_id, supplier in self.suppliers.items():
            self.supplier_tree.insert("", "end", values=(
            supplier_id, supplier.name, supplier.service_type, supplier.contact_details))

    def add_supplier(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Supplier")
        next_id = max(self.suppliers.keys(), default=0) + 1

        tk.Label(add_window, text="Supplier ID:").grid(row=0, column=0)
        tk.Label(add_window, text=str(next_id)).grid(row=0, column=1)

        tk.Label(add_window, text="Name:").grid(row=1, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Type of Supplier:").grid(row=2, column=0)
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(add_window, textvariable=type_var, state="readonly",
                                     values=["Catering Company", "Cleaning Company", "Decorations Company",
                                             "Entertainment Company", "Furniture Supply Company"])
        type_dropdown.grid(row=2, column=1)

        tk.Label(add_window, text="Contact Details:").grid(row=3, column=0)
        contact_details_entry = tk.Entry(add_window)
        contact_details_entry.grid(row=3, column=1)

        tk.Button(add_window, text="Save Supplier",
                  command=lambda: self.save_new_supplier(add_window, next_id, name_entry.get(), type_var.get(),
                                                         contact_details_entry.get())).grid(row=4, columnspan=2)

    def save_new_supplier(self, add_window, supplier_id, name, service_type, contact_details):
        if name and service_type and contact_details:
            new_supplier = Supplier(supplier_id, name, service_type, contact_details)  # Now matches the constructor
            self.suppliers[supplier_id] = new_supplier
            save_data(self.suppliers, "suppliers.pkl")
            self.update_supplier_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Supplier added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_supplier(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            supplier_id = int(self.supplier_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you really want to delete this supplier?"):
                del self.suppliers[supplier_id]
                save_data(self.suppliers, "suppliers.pkl")
                self.update_supplier_tree()
                messagebox.showinfo("Success", "Supplier deleted successfully")
        else:
            messagebox.showerror("Error", "No supplier selected")

    def modify_supplier(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            supplier_id = int(self.supplier_tree.item(selected_item, 'values')[0])
            supplier = self.suppliers.get(supplier_id)
            if supplier:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Supplier Details")

                tk.Label(modify_window, text="Name:").grid(row=0, column=0)
                name_entry = tk.Entry(modify_window)
                name_entry.insert(0, supplier.name)
                name_entry.grid(row=0, column=1)

                tk.Label(modify_window, text="Service:").grid(row=1, column=0)
                service_var = tk.StringVar(value=supplier.service_type)
                service_dropdown = ttk.Combobox(modify_window, textvariable=service_var, state="readonly",
                                                values=["Catering Company", "Cleaning Company", "Decorations Company",
                                                        "Entertainment Company", "Furniture Supply Company"])
                service_dropdown.grid(row=1, column=1)

                tk.Label(modify_window, text="Contact Details:").grid(row=2, column=0)
                contact_details_entry = tk.Entry(modify_window)
                contact_details_entry.insert(0, supplier.contact_details)
                contact_details_entry.grid(row=2, column=1)

                tk.Button(modify_window, text="Save Changes",
                          command=lambda: self.apply_supplier_changes(modify_window, supplier_id, name_entry.get(),
                                                                      service_var.get(),
                                                                      contact_details_entry.get())).grid(row=3,
                                                                                                         columnspan=2)
            else:
                messagebox.showerror("Error", "Supplier not found")
        else:
            messagebox.showerror("Error", "No supplier selected")

    def apply_supplier_changes(self, modify_window, supplier_id, name, service, contact_details):
        if name and service and contact_details:
            supplier = self.suppliers.get(supplier_id)
            if supplier:
                supplier.name = name
                supplier.service_type = service
                supplier.contact_details = contact_details
                save_data(self.suppliers, "suppliers.pkl")
                self.update_supplier_tree()
                modify_window.destroy()
                messagebox.showinfo("Success", "Supplier details updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update supplier details")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_supplier_details(self):
        selected_item = self.supplier_tree.selection()
        if selected_item:
            supplier_id = int(self.supplier_tree.item(selected_item, 'values')[0])
            supplier = self.suppliers.get(supplier_id)
            if supplier:
                details = f"Supplier ID: {supplier_id}\nName: {supplier.name}\nService: {supplier.service_type}"
                messagebox.showinfo("Supplier Details", details)
            else:
                messagebox.showerror("Error", "No supplier found")
        else:
            messagebox.showerror("Error", "No supplier selected")

    # The Event management system (After user pick the Client role they see Manage Event option
    def display_event_management(self):
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        self.event_tree = ttk.Treeview(self.management_frame,
                                       columns=("Event ID", "Event Name", "Type", "Date", "Venue", "Theme", "Invoice"),
                                       show="headings")
        self.event_tree.heading("Event ID", text="Event ID")
        self.event_tree.heading("Event Name", text="Event Name")
        self.event_tree.heading("Type", text="Type")
        self.event_tree.heading("Date", text="Date")
        self.event_tree.heading("Venue", text="Venue")
        self.event_tree.heading("Theme", text="Theme")
        self.event_tree.heading("Invoice", text="Invoice")
        self.event_tree.pack(padx=10, pady=10, expand=True, fill='both')

        tk.Button(self.management_frame, text="Add Event", command=self.add_event).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Delete Event", command=self.delete_event).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Modify Event", command=self.modify_event).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Display Event Details", command=self.display_event_details).pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT,
                                                                                                   padx=10, pady=10)
        self.update_event_tree()

    def update_event_tree(self):
        self.event_tree.delete(*self.event_tree.get_children())
        for event_id, event in self.events.items():
            self.event_tree.insert("", "end",
                                   values=(event_id, event['name'], event['type'], event['date'], event['venue'],
                                           event['theme'], event['invoice']))

    def add_event(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Event")

        event_id = max(self.events.keys(), default=0) + 1

        tk.Label(add_window, text="Event Name:").grid(row=0, column=0)
        event_name_entry = tk.Entry(add_window)
        event_name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Type:").grid(row=1, column=0)
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(add_window, textvariable=type_var, state="readonly", values=["Wedding", "Birthday", "Corporate", "Other"])
        type_dropdown.grid(row=1, column=1)

        tk.Label(add_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=2, column=1)

        tk.Label(add_window, text="Venue:").grid(row=3, column=0)
        venue_var = tk.StringVar()
        venue_dropdown = ttk.Combobox(add_window, textvariable=venue_var, state="readonly", values=["Venue A", "Venue B", "Venue C"])
        venue_dropdown.grid(row=3, column=1)

        tk.Label(add_window, text="Theme:").grid(row=4, column=0)
        theme_entry = tk.Entry(add_window)
        theme_entry.grid(row=4, column=1)

        invoice_number = random.randint(5000, 25000)  # Assuming invoice should be random as before
        tk.Label(add_window, text="Invoice Number:").grid(row=5, column=0)
        tk.Label(add_window, text=str(invoice_number)).grid(row=5, column=1)

        tk.Button(add_window, text="Save Event", command=lambda: self.save_new_event(add_window, event_id, event_name_entry.get(), type_var.get(), date_entry.get(), venue_var.get(), theme_entry.get(), invoice_number)).grid(row=6, columnspan=2)

    def save_new_event(self, add_window, event_id, name, type_str, date, venue, theme, invoice):
        if name and type_str and date and venue and theme:
            new_event = {
                'name': name,
                'type': type_str,
                'date': date,
                'venue': venue,
                'theme': theme,
                'invoice': invoice
            }
            self.events[event_id] = new_event
            save_data(self.events, "events.pkl")
            self.update_event_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Event added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def delete_event(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = int(self.event_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you really want to delete this event?"):
                del self.events[event_id]
                save_data(self.events, "events.pkl")
                self.update_event_tree()
                messagebox.showinfo("Success", "Event deleted successfully")
        else:
            messagebox.showerror("Error", "No event selected")

    def modify_event(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = int(self.event_tree.item(selected_item, 'values')[0])
            event = self.events.get(event_id)
            if event:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Event Details")

                tk.Label(modify_window, text="Event Name:").grid(row=0, column=0)
                event_name_entry = tk.Entry(modify_window)
                event_name_entry.insert(0, event['name'])
                event_name_entry.grid(row=0, column=1)

                tk.Label(modify_window, text="Type:").grid(row=1, column=0)
                type_var = tk.StringVar(value=event['type'])
                type_dropdown = ttk.Combobox(modify_window, textvariable=type_var, state="readonly", values=["Wedding", "Birthday", "Corporate", "Other"])
                type_dropdown.grid(row=1, column=1)

                tk.Label(modify_window, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
                date_entry = tk.Entry(modify_window)
                date_entry.insert(0, event['date'])
                date_entry.grid(row=2, column=1)

                tk.Label(modify_window, text="Venue:").grid(row=3, column=0)
                venue_var = tk.StringVar(value=event['venue'])
                venue_dropdown = ttk.Combobox(modify_window, textvariable=venue_var, state="readonly", values=["Venue A", "Venue B", "Venue C"])
                venue_dropdown.grid(row=3, column=1)

                tk.Label(modify_window, text="Theme:").grid(row=4, column=0)
                theme_entry = tk.Entry(modify_window)
                theme_entry.insert(0, event['theme'])
                theme_entry.grid(row=4, column=1)

                tk.Button(modify_window, text="Save Changes", command=lambda: self.apply_event_changes(modify_window, event_id, event_name_entry.get(), type_var.get(), date_entry.get(), venue_var.get(), theme_entry.get(), event['invoice'])).grid(row=5, columnspan=2)
            else:
                messagebox.showerror("Error", "Event not found")
        else:
            messagebox.showerror("Error", "No event selected")

    def apply_event_changes(self, modify_window, event_id, name, type, date, venue, theme, invoice):
        if name and type and date and venue and theme:
            updated_event = {'name': name, 'type': type, 'date': date, 'venue': venue, 'theme': theme, 'invoice': invoice}
            self.events[event_id] = updated_event
            save_data(self.events, "events.pkl")
            self.update_event_tree()
            modify_window.destroy()
            messagebox.showinfo("Success", "Event details updated successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_event_details(self):
        selected_item = self.event_tree.selection()
        if selected_item:
            event_id = int(self.event_tree.item(selected_item, 'values')[0])
            event = self.events.get(event_id)
            if event:
                details = f"Event ID: {event_id}\nEvent Name: {event['name']}\nType: {event['type']}\nDate: {event['date']}\nVenue: {event['venue']}\nTheme: {event['theme']}\nInvoice: {event['invoice']}"
                messagebox.showinfo("Event Details", details)
            else:
                messagebox.showerror("Error", "No event found")
        else:
            messagebox.showerror("Error", "No event selected")

    # The Guest management system (After user pick the Client role they see Manage Guest option
    def display_guest_management(self):
        """Display the guest management interface."""
        for widget in self.management_frame.winfo_children():
            widget.destroy()

        # Adjust column headings to accommodate first and last names
        self.guest_tree = ttk.Treeview(self.management_frame,
                                       columns=("Guest ID", "First Name", "Last Name", "Contact Details"),
                                       show="headings")
        self.guest_tree.heading("Guest ID", text="Guest ID")
        self.guest_tree.heading("First Name", text="First Name")
        self.guest_tree.heading("Last Name", text="Last Name")
        self.guest_tree.heading("Contact Details", text="Contact Details")
        self.guest_tree.pack(padx=10, pady=10, expand=True, fill='both')

        # Adding, deleting, modifying, and displaying details of guests
        tk.Button(self.management_frame, text="Add Guest", command=self.add_guest).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Delete Guest", command=self.delete_guest).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Modify Guest", command=self.modify_guest).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Display Guest Details", command=self.display_guest_details).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.management_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT, padx=10, pady=10)

        self.update_guest_tree()

    def update_guest_tree(self):
        """Refresh the guest display tree."""
        self.guest_tree.delete(*self.guest_tree.get_children())
        for guest_id, guest in self.guests.items():
            self.guest_tree.insert("", "end", values=(guest_id, guest.f_name, guest.l_name, guest.contact_details))

    def add_guest(self):
        """Add a new guest."""
        add_window = tk.Toplevel(self.master)
        add_window.title("Add New Guest")
        guest_id = max(self.guests.keys(), default=0) + 1

        tk.Label(add_window, text="First Name:").grid(row=0, column=0)
        f_name_entry = tk.Entry(add_window)
        f_name_entry.grid(row=0, column=1)

        tk.Label(add_window, text="Last Name:").grid(row=1, column=0)
        l_name_entry = tk.Entry(add_window)
        l_name_entry.grid(row=1, column=1)

        tk.Label(add_window, text="Contact Details:").grid(row=2, column=0)
        contact_details_entry = tk.Entry(add_window)
        contact_details_entry.grid(row=2, column=1)

        tk.Button(add_window, text="Save Guest",
                  command=lambda: self.save_new_guest(add_window, guest_id, f_name_entry.get(),
                                                      l_name_entry.get(), contact_details_entry.get())).grid(row=3, columnspan=2)

    def save_new_guest(self, add_window, guest_id, f_name, l_name, contact_details):
        """Save the newly added guest information."""
        if f_name and l_name and contact_details:
            new_guest = Guest(guest_id, f_name, l_name, contact_details)
            self.guests[guest_id] = new_guest
            save_data(self.guests, "guests.pkl")
            self.update_guest_tree()
            add_window.destroy()
            messagebox.showinfo("Success", "Guest added successfully")
        else:
            messagebox.showerror("Error", "All fields are required!")


    def delete_guest(self):
        selected_item = self.guest_tree.selection()
        if selected_item:
            guest_id = int(self.guest_tree.item(selected_item, 'values')[0])
            if messagebox.askyesno("Confirm", "Do you really want to delete this guest?"):
                del self.guests[guest_id]
                save_data(self.guests, "guests.pkl")
                self.update_guest_tree()
                messagebox.showinfo("Success", "Guest deleted successfully")
        else:
            messagebox.showerror("Error", "No guest selected")

    def modify_guest(self):
        #Modify an existing guest's details.
        selected_item = self.guest_tree.selection()
        if selected_item:
            guest_id = int(self.guest_tree.item(selected_item, 'values')[0])
            guest = self.guests.get(guest_id)
            if guest:
                modify_window = tk.Toplevel(self.master)
                modify_window.title("Modify Guest Details")

                tk.Label(modify_window, text="First Name:").grid(row=0, column=0)
                f_name_entry = tk.Entry(modify_window)
                f_name_entry.insert(0, guest.f_name)
                f_name_entry.grid(row=0, column=1)

                tk.Label(modify_window, text="Last Name:").grid(row=1, column=0)
                l_name_entry = tk.Entry(modify_window)
                l_name_entry.insert(0, guest.l_name)
                l_name_entry.grid(row=1, column=1)

                tk.Label(modify_window, text="Contact Details:").grid(row=2, column=0)
                contact_details_entry = tk.Entry(modify_window)
                contact_details_entry.insert(0, guest.contact_details)
                contact_details_entry.grid(row=2, column=1)

                tk.Button(modify_window, text="Save Changes",
                          command=lambda: self.apply_guest_changes(modify_window, guest_id, f_name_entry.get(),
                                                                   l_name_entry.get(), contact_details_entry.get())).grid(row=3, columnspan=2)
            else:
                messagebox.showerror("Error", "Guest not found")
        else:
            messagebox.showerror("Error", "No guest selected")

    def apply_guest_changes(self, modify_window, guest_id, f_name, l_name, contact_details):
        #Apply changes to an existing guest's details.
        if f_name and l_name and contact_details:
            guest = self.guests.get(guest_id)
            if guest:
                guest.f_name = f_name
                guest.l_name = l_name
                guest.contact_details = contact_details
                save_data(self.guests, "guests.pkl")
                self.update_guest_tree()
                modify_window.destroy()
                messagebox.showinfo("Success", "Guest details updated successfully")
            else:
                messagebox.showerror("Error", "Failed to update guest details")
        else:
            messagebox.showerror("Error", "All fields are required!")

    def display_guest_details(self):
        #Display details of a specific guest
        guest_id = simpledialog.askinteger("Display Guest", "Enter Guest ID:")
        if guest_id is not None:
            guest = self.guests.get(guest_id)
            if guest:
                details = f"ID: {guest.guest_id}\nFirst Name: {guest.f_name}\nLast Name: {guest.l_name}\nContact Details: {guest.contact_details}"
                messagebox.showinfo("Guest Details", details)
            else:
                messagebox.showerror("Error", f"No guest found with ID: {guest_id}")
        else:
            messagebox.showerror("Error", "Invalid Guest ID")

    def manage_venues(self):
        try:
            self.management_frame.pack_forget()
            self.venue_frame = tk.Frame(self.master)
            self.venue_frame.pack(padx=10, pady=10)

            self.venue_tree = ttk.Treeview(self.venue_frame, columns=("Venue ID", "Name", "Address", "Contact Details", "Min Guests", "Max Guests"), show="headings")
            self.venue_tree.heading("Venue ID", text="Venue ID")
            self.venue_tree.heading("Name", text="Name")
            self.venue_tree.heading("Address", text="Address")
            self.venue_tree.heading("Contact Details", text="Contact Details")
            self.venue_tree.heading("Min Guests", text="Min Guests")
            self.venue_tree.heading("Max Guests", text="Max Guests")
            self.venue_tree.pack(padx=10, pady=10, fill='both', expand=True)
            self.update_venue_tree()

            tk.Button(self.venue_frame, text="Add Venue", command=self.add_venue).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(self.venue_frame, text="Delete Venue", command=self.delete_venue).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(self.venue_frame, text="Modify Venue", command=self.modify_venue).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(self.venue_frame, text="Display Venue Details", command=self.display_venue_details).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(self.venue_frame, text="Back to Menu", command=self.display_main_menu).pack(side=tk.LEFT, padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Error", "Failed to manage venues: " + str(e))
            self.display_main_menu()

    def update_venue_tree(self):
        try:
            self.venue_tree.delete(*self.venue_tree.get_children())
            for venue_id, venue in self.venues.items():
                self.venue_tree.insert("", "end", values=(venue.venue_id, venue.name, venue.address, venue.contact_details, venue.min_guests, venue.max_guests))
        except Exception as e:
            messagebox.showerror("Error", "Failed to update venue data: " + str(e))

    def add_venue(self):
        try:
            add_window = tk.Toplevel(self.master)
            add_window.title("Add New Venue")
            next_venue_id = max(int(vid) for vid in self.venues.keys()) + 1

            tk.Label(add_window, text="Venue ID:").grid(row=0, column=0)
            venue_id_entry = tk.Entry(add_window)
            venue_id_entry.insert(0, str(next_venue_id))
            venue_id_entry.config(state='readonly')
            venue_id_entry.grid(row=0, column=1)

            tk.Label(add_window, text="Name:").grid(row=1, column=0)
            name_var = tk.StringVar()
            name_dropdown = ttk.Combobox(add_window, textvariable=name_var, values=["Venue A", "Venue B", "Venue C", "Venue D", "Custom"], state="readonly")
            name_dropdown.grid(row=1, column=1)

            tk.Label(add_window, text="Address:").grid(row=2, column=0)
            address_entry = tk.Entry(add_window)
            address_entry.grid(row=2, column=1)

            tk.Label(add_window, text="Contact Details:").grid(row=3, column=0)
            contact_details_entry = tk.Entry(add_window)
            contact_details_entry.grid(row=3, column=1)

            tk.Label(add_window, text="Min Guests:").grid(row=4, column=0)
            min_guests_entry = tk.Entry(add_window)
            min_guests_entry.grid(row=4, column=1)

            tk.Label(add_window, text="Max Guests:").grid(row=5, column=0)
            max_guests_entry = tk.Entry(add_window)
            max_guests_entry.grid(row=5, column=1)

            tk.Button(add_window, text="Save Venue", command=lambda: self.save_new_venue(next_venue_id, name_var.get(), address_entry.get(),
                                                                                       contact_details_entry.get(), min_guests_entry.get(), max_guests_entry.get(), add_window)).grid(row=6, columnspan=2)
        except Exception as e:
            messagebox.showerror("Error", "Failed to add new venue: " + str(e))
            if 'add_window' in locals():
                add_window.destroy()

    def save_new_venue(self, venue_id, name, address, contact_details, min_guests, max_guests, window):
        try:
            if name and address and contact_details and min_guests and max_guests:
                new_venue = Venue(venue_id, name, address, contact_details, min_guests, max_guests)
                self.venues[venue_id] = new_venue
                save_data(self.venues, "venues.pkl")
                self.update_venue_tree()
                window.destroy()
                messagebox.showinfo("Success", "Venue added successfully")
            else:
                messagebox.showerror("Error", "All fields are required!")
        except Exception as e:
            messagebox.showerror("Error", "Failed to save new venue: " + str(e))
            if 'window' in locals():
                window.destroy()

    def delete_venue(self):
        try:
            selected_item = self.venue_tree.selection()
            if selected_item:
                venue_id = int(self.venue_tree.item(selected_item, 'values')[0])
                if venue_id in self.venues:
                    if messagebox.askyesno("Confirm", "Do you want to delete this venue?"):
                        del self.venues[venue_id]
                        save_data(self.venues, "venues.pkl")
                        self.update_venue_tree()
                        messagebox.showinfo("Success", "Venue deleted successfully")
                else:
                    messagebox.showerror("Error", "Venue not found")
            else:
                messagebox.showerror("Error", "No venue selected")
        except Exception as e:
            messagebox.showerror("Error", "Failed to delete venue: " + str(e))

    def modify_venue(self):
        try:
            selected_item = self.venue_tree.selection()
            if selected_item:
                venue_id_str = self.venue_tree.item(selected_item, 'values')[0]
                venue_id = int(venue_id_str)
                venue = self.venues.get(venue_id)
                if venue:
                    modify_window = tk.Toplevel(self.master)
                    modify_window.title("Modify Venue")

                    tk.Label(modify_window, text="Name:").grid(row=1, column=0)
                    name_entry = tk.Entry(modify_window)
                    name_entry.insert(0, venue.name)
                    name_entry.grid(row=1, column=1)

                    tk.Label(modify_window, text="Address:").grid(row=2, column=0)
                    address_entry = tk.Entry(modify_window)
                    address_entry.insert(0, venue.address)
                    address_entry.grid(row=2, column=1)

                    tk.Label(modify_window, text="Contact Details:").grid(row=3, column=0)
                    contact_details_entry = tk.Entry(modify_window)
                    contact_details_entry.insert(0, venue.contact_details)
                    contact_details_entry.grid(row=3, column=1)

                    tk.Label(modify_window, text="Min Guests:").grid(row=4, column=0)
                    min_guests_entry = tk.Entry(modify_window)
                    min_guests_entry.insert(0, venue.min_guests)
                    min_guests_entry.grid(row=4, column=1)

                    tk.Label(modify_window, text="Max Guests:").grid(row=5, column=0)
                    max_guests_entry = tk.Entry(modify_window)
                    max_guests_entry.insert(0, venue.max_guests)
                    max_guests_entry.grid(row=5, column=1)

                    tk.Button(modify_window, text="Save Changes", command=lambda: self.save_new_venue(
                        venue_id, name_entry.get(), address_entry.get(), contact_details_entry.get(),
                        min_guests_entry.get(), max_guests_entry.get(), modify_window)).grid(row=6, columnspan=2)
                else:
                    messagebox.showerror("Error", "Venue not found")
            else:
                messagebox.showerror("Error", "No venue selected")
        except Exception as e:
            messagebox.showerror("Error", "Failed to modify venue details: " + str(e))
            if 'modify_window' in locals():
                modify_window.destroy()

    def display_venue_details(self):
        try:
            venue_id = simpledialog.askinteger("Display Venue", "Enter Venue ID:")
            if venue_id is not None:
                venue = self.venues.get(venue_id)
                if venue:
                    details = f"Venue ID: {venue.venue_id}\nName: {venue.name}\nAddress: {venue.address}\nContact Details: {venue.contact_details}\nMin Guests: {venue.min_guests}\nMax Guests: {venue.max_guests}"
                    messagebox.showinfo("Venue Details", details)
                else:
                    messagebox.showerror("Error", f"No venue found with ID: {venue_id}")
            else:
                messagebox.showerror("Error", "Invalid Venue ID")
        except Exception as e:
            messagebox.showerror("Error", "Failed to display venue details: " + str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ManagementSystemGUI(root)
    root.mainloop()
