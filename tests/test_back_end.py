import unittest

from flask_testing import TestCase 
from flask import abort, url_for

from app import create_app, db
from app.models import Department, Employee, Role

class TestBase(TestCase):

    def create_app(self):
        # setting of testing configuration
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'mysql://admin:admin@localhost/dream_team_test'
            )

        return app

    def setUp(self):
        """
        Setup method will be call before every test.
        Initialize create all tables in the database before testing starts
        """
        db.create_all()

        #create a test admin

        admin = Employee(username="admin", password="admintest", is_admin=True)

        #create test non-admin user

        employee = Employee(username="test_employee", password="test")

        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        This method will be called after every successfully test
        Drop tables from the datables
        """
        db.session.remove()
        db.drop_all()

class TestModels(TestBase):


    def test_employee_model(self):
        """
        Test number of records in employee table
        """

        self.assertEqual(Employee.query.count(), 2)


    def test_department_model(self):
        """
        Test number of records in deparment table
        """
        department = Department(name="IT", description="Technology Dept")
        db.session.add(department)
        db.session.commit()
        self.assertEqual(Department.query.count(), 1)


    def test_role_model(self):
        """
        Test number of records in role department
        """
        role = Role(name="CEO", description="CEO of our company")
        db.session.add(role)
        db.session.commit()
        self.assertEqual(Role.query.count(), 1)

class TestView(TestBase):
    
    def test_home_page_view(self):
        """
        Test if the home page is accessible without login
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)


    def test_login_page_view(self):

        """
        Test if login page is accessible
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
    
    def test_log_out_view(self):
        """
        Test that logot link is inaccessible without the user loggin  and
        redirects to login page then to logout page
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that admin dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


    def test_deparments_views(self):
        """
        Test that department page is inaccessible without login
        and redirects to login then to department page
        """ 
        target_url = url_for('admin.list_all_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)

    def test_roles_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    def test_employees_view(self):
        """
        Test that employees page is inaccessible without login
        and redirects to login page then to employees page
        """
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    # create a route to raise 403 error via abort
    def test_403_forbidden(self):
        @self.app.route("/403")
        def forbidden_error():
            abort(403)
        response = self.client.get("/403")
        self.assertEqual(response.status_code, 403)
        self.assertTrue('403 Error' in str(response.data))

    def test_404_not_found(self):
        """
        Test for 404 page not found
        """

        response = self.client.get("/gonowhere")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in str(response.data))

    def test_500_internal_server_error(self):
        """
        Test for 500 internal server error
        """
        @self.app.route("/500")
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in str(response.data))


    


    

if __name__ == '__main__':
    unittest.main()