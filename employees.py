import sqlalchemy
import unittest
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref


engine = create_engine('sqlite:///employees.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

employee_skills = Table('employee_skills', Base.metadata,
                        Column('employee_id', Integer, ForeignKey('employees.id')),
                        Column('skill_id', Integer, ForeignKey('skills.id')))

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)
    skills = relationship('Skill', secondary=employee_skills, backref='employees')

    def __repr__(self):
        return '<Employee(id = %s, name = %s, position = %s)>' % (self.id, self.name, self.position)

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    skill_name = Column(String)

    def __repr__(self):
        return '<Skill(id = %s, skill_name = %s)>' % (self.id, self.skill_name)
  
Base.metadata.create_all(engine)

def add_employee(session, employee_name, employee_position):
    session.add(Employee(name=employee_name, position=employee_position))
    session.commit()

def add_skills(session, employee_name, skill_list):
    employee = session.query(Employee).filter_by(name=employee_name).first()
    for skill_name in skill_list:
        skill = session.query(Skill).filter_by(skill_name=skill_name).first()
    if skill:
        employee.skills.append(skill)
    else:
        employee.skills.append(Skill(skill_name=skill))
    session.commit()

def find_employees_by_name(session, employee_name):
    return session.query(Employee).filter_by(name=employee_name).all()

def find_employees_by_position(session, employee_position):
    return session.query(Employee).filter_by(position=employee_position).all()

def find_employees_by_skill(session, skill):
    return session.query(Employee).filter(Employee.skills.any(skill_name=skill)).all()


