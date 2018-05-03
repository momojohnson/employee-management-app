import unittest
from flask_testing import TestCase
from app import create_app, db 
from flask import url_for
from app.models import Department, Employee, Role

class TestBase(TestCase):
    
    def create_app(self):
        config_name = "testing"
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='postgresql:///test_db'
            )
        return app
    
    def setUp(self):
        """
        Create various tables in the db
        """
        db.create_all()
        admin = Employee(username="admin", password="admin2016", is_admin=True)
        
        employee = Employee(username="test_user", password="test2016")
        
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()
    
    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


# class TestModels(TestBase):
    
#     def test_employee_model(self):
#         self.assertEqual(Employee.query.count(), 2)
    
#     def test_department_model(self):
#         """
#         Test number of records in Department table
#         """

#         # create test department
#         department = Department(name="IT", description="The IT Department")

#         # save department to database
#         db.session.add(department)
#         db.session.commit()

    #     self.assertEqual(Department.query.count(), 1)
    # def test_role_model(self):
    #     """
    #     Test number of records in Role table
    #     """

    #     # create test role
    #     role = Role(name="CEO", description="Run the whole company")

    #     # save role to database
    #     db.session.add(role)
    #     db.session.commit()

    #     self.assertEqual(Role.query.count(), 1)

class TestViews(TestBase):
    def test_home_page(self):
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)
        
if __name__ == "__main__":
    unittest.main()