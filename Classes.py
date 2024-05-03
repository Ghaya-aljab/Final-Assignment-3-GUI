import pickle
from enum import Enum

class JobTitle(Enum):
    """Enumeration for job titles within the company."""
    SALES_MANAGER = "Sales Manager"
    SALES_PERSON = "Salesperson"
    MARKETING_MANAGER = "Marketing Manager"
    MARKETER = "Marketer"
    ACCOUNTANT = "Accountant"
    DESIGNER = "Designer"
    HANDYMAN = "Handyman"

class EventType(Enum):
    """Enumeration for types of events the company manages."""
    WEDDING = "Wedding"
    BIRTHDAY = "Birthday"
    THEMED_PARTY = "Themed Party"
    GRADUATION = "Graduation"

class Employee:
    """Base class for employees, containing general employee details and functionalities."""
    def __init__(self, id, name, department, job_title: JobTitle, salary):
        self.id = id
        self.name = name
        self.department = department
        self.job_title = job_title
        self.salary = salary

    def update_details(self, **kwargs):
        # Update employee details dynamically using keyword arguments
        for key, value in kwargs.items():
            setattr(self, key, value)

    def display(self):
        print("Employee ID:", self.id)
        print("Name:", self.name)
        print("Department:", self.department)
        print("Job Title:", self.job_title)
        print("Salary:", self.salary)


    # These methods are implemented in the GUI
    def add_employee():
        pass  # Implemented in GUI

    def delete_employee():
        pass  # Implemented in GUI

    def modify_employee():
        pass  # Implemented in GUI

class Manager(Employee):
    """Specialized class for managers, extending Employee with management-specific attributes."""
    def __init__(self, id, name, department, job_title: JobTitle, salary, age, dob, passport_details, subordinates=None):
        super().__init__(id, name, department, job_title, salary, age, dob, passport_details)
        self.subordinates = subordinates if subordinates else []

    def add_subordinate(self, employee):
        # Add an employee to the manager's list of subordinates
        self.subordinates.append(employee)

    def remove_subordinate(self, employee):
        # Remove an employee from the manager's list of subordinates
        self.subordinates = [sub for sub in self.subordinates if sub.id != employee.id]

    # These methods are implemented in the GUI
    def add_manager():
        pass  # Implemented in GUI

    def delete_manager():
        pass  # Implemented in GUI

    def modify_manager():
        pass  # Implemented in GUI

class Event:
    """Class representing events managed by the company."""
    def __init__(self, event_id, type: EventType, theme, date, time, duration, venue, client_id, suppliers, guest_list, invoice):
        self.event_id = event_id
        self.type = type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue = venue  # Aggregation relationship with Venue
        self.client_id = client_id
        self.suppliers = suppliers
        self.guest_list = guest_list
        self.invoice = invoice

    def display(self):
        print("Event ID:", self.event_id)
        print("Type:", self.type)
        print("Theme:", self.theme)
        print("Date:", self.date)
        print("Time:", self.time)
        print("Duration:", self.duration)
        print("Venue:", self.venue)
        print("Client ID:", self.client_id)
        print("Suppliers:", self.suppliers)
        print("Guest List:", self.guest_list)
        print("Invoice:", self.invoice)

    # These methods are implemented in the GUI
    def add_event():
        pass  # Implemented in GUI

    def delete_event():
        pass  # Implemented in GUI

    def modify_event():
        pass  # Implemented in GUI

class Client:
    """Class representing clients who host or sponsor events."""
    def __init__(self, client_id, name, address, contact_details, budget):
        self.client_id = client_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.budget = budget

    def display(self):
        print("Client ID:", self.client_id)
        print("Name:", self.name)
        print("Address:", self.address)
        print("Contact Details:", self.contact_details)
        print("Budget:", self.budget)

    # These methods are implemented in the GUI
    def add_client():
        pass  # Implemented in GUI

    def delete_client():
        pass  # Implemented in GUI

    def modify_client():
        pass  # Implemented in GUI

class Guest:
    """Class representing guests attending the events."""
    def __init__(self, guest_id, f_name, l_name, contact_details):
        self.guest_id = guest_id
        self.f_name = f_name
        self.l_name = l_name
        self.contact_details = contact_details

    def display(self):
        print("Guest ID:", self.guest_id)
        print("First Name:", self.f_name)
        print("Last Name:", self.l_name)
        print("Contact Details:", self.contact_details)

    # These methods are implemented in the GUI
    def add_guest():
        pass  # Implemented in GUI

    def delete_guest():
        pass  # Implemented in GUI

    def modify_guest():
        pass  # Implemented in GUI

class Supplier:
    """Class representing suppliers providing services for events."""
    def __init__(self, supplier_id, name, contact_details, service_type):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_details = contact_details
        self.service_type = service_type

    def display(self):
        print("Supplier ID:", self.supplier_id)
        print("Name:", self.name)
        print("Contact Details:", self.contact_details)
        print("Service Type:", self.service_type)

    # These methods are implemented in the GUI
    def add_supplier():
        pass  # Implemented in GUI

    def delete_supplier():
        pass  # Implemented in GUI

    def modify_supplier():
        pass  # Implemented in GUI

class Venue:
    """Class representing venues where events are held."""
    def __init__(self, venue_id, name, address, contact_details, min_guests, max_guests):
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.min_guests = min_guests
        self.max_guests = max_guests

    def display(self):
        print("Venue ID:", self.venue_id)
        print("Name:", self.name)
        print("Address:", self.address)
        print("Contact Details:", self.contact_details)
        print("Minimum Guests:", self.min_guests)
        print("Maximum Guests:", self.max_guests)

    # These methods are implemented in the GUI
    def add_venue():
        pass  # Implemented in GUI

    def delete_venue():
        pass  # Implemented in GUI

    def modify_venue():
        pass  # Implemented in GUI

# Functions to save and load data using pickle
def load_data(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("File not found. Initializing new data.")
        return {}

def save_data(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

