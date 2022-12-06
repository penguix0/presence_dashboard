from flask_login import login_required, current_user
from dashboard import app
from flask import jsonify, render_template, request, send_from_directory
from dashboard import Organisation, Employee, Settings, db
from flask_wtf.csrf import generate_csrf


## The url of the dashboard
@app.route("/", methods=["GET"])
@app.route("/dashboard/", methods=["POST", "GET"])
@login_required
def dashboard():
    # When theres a post request
    if request.method == "POST":
        # get data
        employee = request.form.to_dict()
        # check if the employee has a name and a a new presence value
        if "employee_name" in employee and "present" in employee:
            employee_first_name = employee["employee_name"].split("_")[0]
            employee_last_name = employee["employee_name"].split("_")[1]
            employee_to_update = Employee.query.filter_by(organisation_id=current_user.id,
                                                        first_name=employee_first_name,
                                                        last_name=employee_last_name).first()
            if employee_to_update:
                if employee["present"] == True or employee["present"] == "True" or employee["present"] == "true":
                    employee_to_update.present = True
                    db.session.commit()
                if employee["present"] == False or employee["present"] == "False" or employee["present"] == "false":
                    employee_to_update.present = False
                    db.session.commit()


    employees = Employee.query.filter_by(organisation_id=current_user.id).order_by(Employee.first_name).all()
    current_settings = Settings.query.filter_by(organisation_id=current_user.id).first()
    loginMessage = current_settings.loginMessage
    logoutMessage = current_settings.logoutMessage
    messageTime = current_settings.messageTime
    name = Organisation.query.filter_by(id=current_user.id).first().username
    return render_template(app.config["INDEX_PATH"], employees=employees, 
                                                     loginMessage=loginMessage,
                                                     logoutMessage=logoutMessage,
                                                     messageTime=messageTime,
                                                     name=name)

@app.route("/userbanner", methods=["GET"])
@login_required
def userBanner():
    return send_from_directory(app.config["UPLOAD_FOLDER"], current_user.image_file)

@app.route('/_refresh_csrf', methods=['GET'])
##@roles_accepted('admin', 'copy', 'client')
def csrf_refresh():
    token = generate_csrf()
    return jsonify(token)


@app.route("/dashboard/employees/", methods=["GET"])
@login_required
def get_employees():
    if request.method == "GET":
        ## Get the employees of the current logged in organisation
        employees_list = Employee.query.filter_by(organisation_id=current_user.id).order_by(Employee.last_name).all()
        ## Convert those employees list to a dict and send the dictionary off to the user
        employees_dict = {}
        for employee in employees_list:
            employees_dict[(employee.first_name + "_" + employee.last_name)] = employee.present
        employees_dict = jsonify(employees_dict)
        return employees_dict
