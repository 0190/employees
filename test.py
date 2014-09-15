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
        self.employee_name = 'Masha'
        self.employee_position = 'Junior QA'

    def tearDown(self):
        self.trans.rollback()
        self.session.close()
        self.connection.close()

    def test_add_employee(self):
        add_employee(self.session, self.employee_name, self.employee_position)
        added = self.session.query(Employee).filter_by(name=self.employee_name, position=self.employee_position).first()
 
        self.assertEqual(added.name, self.employee_name)
        self.assertEqual(added.position, self.employee_position)

    def test_find_employees_by_name(self):
        new_employee = Employee(name=self.employee_name, position=self.employee_position)
        
        self.session.add(new_employee)
        self.session.commit()

        found = find_employees_by_name(self.session, self.employee_name)

        self.assertEqual(found[0], new_employee)

    def test_find_employees_by_position(self):
        new_employee = Employee(name=self.employee_name, position=self.employee_position)

        self.session.add(new_employee)
        self.session.commit()

        found = find_employees_by_position(self.session, self.employee_position)

        self.assertEqual(found[0], new_employee)

    def test_add_skills(self):
        new_employee = Employee(name=self.employee_name, position=self.employee_position)
        skill_list = ['Reading', 'Sleeping', 'Eating']

        self.session.add(new_employee)
        self.session.commit()

        add_skills(self.session, self.employee_name, skill_list)

        self.assertEqual(new_employee.skills, skill_list)

    def test_find_employees_by_skill(self):
        pass

if __name__ == '__main__':
    unittest.main()