import random
import unittest
from employees import *

Session = sessionmaker()
engine = create_engine('sqlite:///:memory:', echo=False)
Base.metadata.create_all(engine)


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
        added = self.session.query(Employee).first()
 
        self.assertEqual(added.name, self.employee_name)
        self.assertEqual(added.position, self.employee_position)

    def test_add_skill(self):
        new_employee = add_employee(self.session, self.employee_name, self.employee_position)
        skill_name = 'Reading'

        add_skill(self.session, new_employee, skill_name)

        self.assertEqual(new_employee.skills[0].skill_name, skill_name)

    def test_add_existing_skill(self):
        new_employee = add_employee(self.session, self.employee_name, self.employee_position)
        skill_name = 'Reading'
        self.session.add(Skill(skill_name='Reading'))
        self.session.commit()

        add_skill(self.session, new_employee, skill_name)

        self.assertEqual(new_employee.skills[0].skill_name, skill_name)

    def test_add_skills(self):
        new_employee = add_employee(self.session, self.employee_name, self.employee_position)
        skill_list = ['Reading', 'Sleeping', 'Eating']

        add_skills(self.session, new_employee, skill_list)

        self.assertEqual([skill.skill_name for skill in new_employee.skills], skill_list)

    def test_find_employees_by_name(self):
        new_employee = add_employee(self.session, self.employee_name, self.employee_position)

        found = find_employees_by_name(self.session, self.employee_name)
        self.assertEqual(found, [new_employee])

    def test_find_employees_by_position(self):
        new_employee = add_employee(self.session, self.employee_name, self.employee_position)

        found = find_employees_by_position(self.session, self.employee_position)
        self.assertEqual(found, [new_employee])

    def test_find_employees_by_skill(self):
        new_employee = add_employee(self.session, self.employee_name, self.employee_position)

        skill = 'Reading'
        new_employee.skills.append(Skill(skill_name=skill))

        found = find_employees_by_skill(self.session, skill)
        self.assertEqual(found, [new_employee])

if __name__ == '__main__':
    unittest.main()