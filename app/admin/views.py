from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from . import admin
from . forms import DepartmentForm, EmployeeAssignmentForm, RoleForm
from   app  import db
from .. models import Department, Employee, Role

def check_admin():
    """
    Avoid non admin from accessing admin route
    """
    if not current_user.is_admin:
      abort(403)
      
@admin.route("/departments")
@login_required
def list_all_departments():
  """
  List all department
  
  """
  check_admin()
  departments = Department.query.all()
  return render_template("admin/departments/departments.html", departments=departments, title="Departments")


@admin.route("/departments/add", methods=["GET", "POST"])
@login_required
def add_department():
  """
  Add a new department to the database
  
  """
  check_admin()
  add_department = True
  department_form = DepartmentForm()
  if department_form.validate_on_submit():
    department = Department(name=department_form.name.data,
                 description= department_form.description.data)
    try:
      db.session.add(department)
      db.session.commit()
      flash("Department successfully added to database")
    except:
      flash("This department has alread been added.")
    
    return redirect(url_for("admin.list_all_departments"))
    
  return render_template('admin/departments/department.html', action="Add", department_form=department_form, add_department=add_department,
                        title="Departments")
                        
  
@admin.route("/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
  """
    Edit a department
  """
  add_department = False
  department = Department.query.get_or_404(id)
  department_form = DepartmentForm(obj=department)
  if department_form.validate_on_submit():
    department.name = department_form.name.data
    department.description = department_form.description.data
    db.session.commit()
    flash("You have success edited {} department".format(department.name))
    return redirect(url_for("admin.list_all_departments"))
  
  department_form.name.data = department.name
  department_form.description = department.description
  return render_template("admin/departments/department.html", action="Edit", department_form=department_form, add_department=add_department)
  


@admin.route("/departments/delete/<int:id>", methods=["GET", "POST"])
def delete_department(id):
  """
  Delete a particular department from the database
  """
  check_admin()
  department = Department.query.get_or_404(id)
  db.session.delete(department)
  db.session.commit()
  flash("Deparment successfully deleted")
  
  return redirect(url_for("admin.list_all_departments"))


@admin.route('/roles')
@login_required
def list_roles():
  """
  List all roles
  """
  check_admin()
  roles = Role.query.all()
  return render_template('admin/roles/roles.html', roles=roles, title="Roles")
  
@admin.route('/roles/add',  methods=["GET", "POST"])
@login_required
def add_roles():
  """
  Add a role of an employee
  """
  add_role = True
  role_form = RoleForm()
  if role_form.validate_on_submit():
    role = Role(name=role_form.name.data, description=role_form.description.data)
    try:
      db.session.add(role)
      db.session.commit()
      flash("Role for {} successfully added".format(role.name))
      return redirect(url_for('admin.list_roles'))
    except:
      flash("{} has already been added".format(role_form.data.name))
  return render_template('admin/roles/role.html', add_roles=add_role, role_form=role_form, title="Add Role")
      
@admin.route('/roles/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_role(id):
  """
  Edit a particular role
  """
  check_admin()
  add_role = False
  role = Role.query.get_or_404(id)
  role_form = RoleForm(obj=role)
  if role_form.validate_on_submit():
    role.name = role_form.name.data
    role.description = role_form.description.data 
    db.session.commit()
    flash("You have successfully changed role to {}".format(role_form.name.data))
    return redirect(url_for('admin.list_roles'))
  
  return render_template("admin/roles/role.html", add_role=add_role, role_form=role_form, title="Edit Role")
    
@admin.route("/roles/delete/<int:id>", methods=["GET, POST"])
@login_required
def delete_role(id):
  """
  Delete a role from the database
  """
  check_admin()
  role = Role.query.get_or_404(id)
  db.session.delete(role)
  return redirect(url_for("admin.list_roles"))
  
@admin.route("/employees")
@login_required
def list_employees():
  """
    List all employees
  """
  check_admin()
  employees = Employee.query.all()
  return render_template("admin/employees/employees.html", employees=employees, title="Employees")


@admin.route("/employees/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign_employee(id):
  """
  Assign a department and role to an employee
  """
  check_admin()
  employee = Employee.query.get_or_404(id)
  if employee.is_admin:
    #Prevent admin from being assigned.
    abort(403)
  employee_assign_form = EmployeeAssignmentForm(obj=employee)
  if employee_assign_form.validate_on_submit():
    employee.department = employee_assign_form.department.data
    employee.role = employee_assign_form.role.data
    db.session.add(employee)
    db.session.commit()
    flash("You have successfully assigned a department and role")
    return redirect(url_for('admin.list_employees'))
      
  return render_template('admin/employees/employee.html',
                           employee=employee, employee_assign_form=employee_assign_form,
                           title='Assign Employee')
      
      
    
  
  
  