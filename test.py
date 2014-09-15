import random
import unittest
from employees import *

Session = sessionmaker()
engine = create_engine('sqlite:///employees.db', echo=True)

class EmployeesTest(unittest.TestCase):

    def setUp(self):
        self.connection = engine.connect()
        self.trans = self.connection.begin()
        self.session = Session(bind=self.connection)

    def tearDown(self):
        self.trans.rollback()
        self.session.close()

    def test_add_employee(self):
        employee_name = 'Masha'
        employee_position = 'Junior QA'

        add_employee(self.session, employee_name, employee_position)
        added = self.session.query(Employee).filter_by(name=employee_name, position=employee_position).first()
 
        self.assertEqual(added.name, employee_name)
        self.assertEqual(added.position, employee_position)

    def test_find_employees_by_name(self):
        employee_name = 'Masha'
        employee_position = 'Junior QA'
        new_employee = Employee(name=employee_name, position=employee_position)
        
        self.session.add(new_employee)
        self.session.commit()

        found = find_employees_by_name(self.session, employee_name)

        self.assertEqual(found[0], new_employee)

    def test_find_employees_by_position(self):
        pass

    def test_find_employees_by_skill(self):
        pass

if __name__ == '__main__':
    unittest.main()