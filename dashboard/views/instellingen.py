from flask_login import login_required, current_user, fresh_login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, FloatField, PasswordField
from wtforms.validators import InputRequired, Length, DataRequired
from dashboard import app, db, Employee, Settings, Organisation, bcrypt
from os import path, remove
from flask import redirect, request, url_for, render_template
from secrets import token_hex
from PIL import Image

@app.route("/instellingen", methods=["GET"])
@app.route("/instellingen/", methods=["GET"])
@app.route("/instellingen/dashboard", methods=["GET", "POST"])
@login_required
def instellingen_dashboard():
    if request.method == "GET":
        ## End block 1
        ## Block 2 -- Welcome user
        username = Organisation.query.filter_by(id=current_user.id).first().username
        ## End block 2
        ## Block 3 -- login and logout messages
        current_settings = Settings.query.filter_by(organisation_id=current_user.id).first()
        login_message = current_settings.loginMessage
        logout_message = current_settings.logoutMessage
        return render_template(app.config['SETTINGS_DASHBOARD_PATH'],
                               username=username,
                               login_message=login_message,
                               logout_message=logout_message)

class ChangeBannerForm(FlaskForm):
    picture = FileField("Update de banner", validators=[FileAllowed(app.config["ALLOWED_EXTENSIONS"])], id="real-file-button")
    changeBannerSubmit = SubmitField("Opslaan", id="submit")

def savePicture(form_picture):
    prev_picture = path.join(app.config["UPLOAD_FOLDER"], current_user.image_file)
    if path.exists(prev_picture) and not path.basename(prev_picture) == 'default.jpg':
        remove(prev_picture)

    random_hex = token_hex(8)
    _, file_extension = path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = path.join(app.config["UPLOAD_FOLDER"], picture_filename)
    
    ## resize image to prevent saving big images
    output_size = (800, 450)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    
    image.save(picture_path)

    return picture_filename

@app.route("/instellingen/bestanden", methods=["GET", "POST"])
@login_required
def instellingen_bestanden():
    changeBannerForm = ChangeBannerForm()
    
    if changeBannerForm.validate_on_submit():
        if changeBannerForm.picture.data:
            picture_file = savePicture(changeBannerForm.picture.data)
            current_user.image_file = picture_file
            db.session.commit()

        return redirect(url_for("instellingen_bestanden"))

    return render_template(app.config['SETTINGS_BESTANDEN_PATH'], form=changeBannerForm)

## These are the two forms which are going to be used for adding and deleting employees
class NewUserForm(FlaskForm):
    new_user_first_name = StringField(validators=[InputRequired(), Length(
                        min=2, max=40)], render_kw={"placeholder": "Voornaam"}, id="first_name")
    new_user_last_name = StringField(validators=[InputRequired(), Length(
                             min=2, max=40)], render_kw={"placeholder": "Achternaam"}, id="last_name")
    new_user_submit = SubmitField("Opslaan", id="submit")

class DeleteUserForm(FlaskForm):
    delete_user_first_name = StringField(validators=[InputRequired(), Length(
                        min=2, max=40)], render_kw={"placeholder": "Voornaam"}, id="first_name")
    delete_user_last_name = StringField(validators=[InputRequired(), Length(
                             min=2, max=40)], render_kw={"placeholder": "Achternaam"}, id="last_name")
    delete_user_submit = SubmitField("Opslaan", id="submit")

@app.route("/instellingen/medewerkers", methods=["GET", "POST"])
@login_required
def instellingen_medewerkers():
    newUserForm = NewUserForm()
    deleteUserForm = DeleteUserForm()

    ## Instead of using .validate_on_submit() which would be good for just one form, we use .validate() and check if the submit button is pressed.
    ## Using .validate_on_submit() would lead to issues when you're using multiple forms.
    ## https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms
    
    ## Add an employee
    if newUserForm.new_user_submit.data and newUserForm.validate():
        first_name = newUserForm.new_user_first_name.data
        ## Remove all extra spaces
        first_name = " ".join(first_name.split())
        last_name = newUserForm.new_user_last_name.data
        ## Remove all extra spaces
        last_name = " ".join(last_name.split())
        new_employee = Employee(first_name=first_name, last_name=last_name, organisation_id=current_user.id)
        db.session.add(new_employee)
        db.session.commit()
    
    ## Delete an employee
    if deleteUserForm.delete_user_submit.data and deleteUserForm.validate():
        first_name = deleteUserForm.delete_user_first_name.data
        ## Remove all extra spaces at the end of the string
        first_name = "".join(first_name.rstrip())
        last_name = deleteUserForm.delete_user_last_name.data
        ## Remove all extra spaces at the end of the string
        last_name = "".join(last_name.rstrip())
        employee_to_delete = Employee.query.filter_by(first_name=first_name, 
                                                      last_name=last_name, 
                                                      organisation_id=current_user.id).first()
        
        ## If the employee actually exists and thus is able to be deleted
        if employee_to_delete:
            db.session.delete(employee_to_delete)
            db.session.commit()

    employees = Employee.query.filter_by(organisation_id=current_user.id).all()
    return render_template(app.config['SETTINGS_MEDEWERKERS_PATH'],
                           newUserForm=newUserForm, deleteUserForm=deleteUserForm, employees=employees)

## These are the two forms which we will be using to set the different notifications
class LoginMessageForm(FlaskForm):
    loginMessage = StringField(validators=[InputRequired(), Length(
                        min=2, max=120)], id="loginMessage")
    loginSubmit = SubmitField("Opslaan", id="submit")

class LogoutMessageForm(FlaskForm):
    logoutMessage = StringField(validators=[InputRequired(), Length(
                             min=2, max=120)], id="logoutMessage")
    logoutSubmit = SubmitField("Opslaan", id="submit")

@app.route("/instellingen/notificaties", methods=["GET", "POST"])
@login_required
def instellingen_notificaties():
    loginForm = LoginMessageForm()
    logoutForm = LogoutMessageForm()
    
    ## Instead of using .validate_on_submit() which would be good for just one form, we use .validate() and check if the submit button is pressed.
    ## Using .validate_on_submit() would lead to issues when you're using multiple forms.
    ## https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms
  
    ## Save the new login message when the submit button is pressed.
    if loginForm.loginSubmit.data and loginForm.validate():
        loginMessage = loginForm.loginMessage.data
        ## Update the loginMessage in the SQLAlchemy database
        current_settings = Settings.query.filter_by(organisation_id=current_user.id).first()
        current_settings.loginMessage = loginMessage
        db.session.commit()

    ## Save the new logout message when the submit button is pressed.
    if logoutForm.logoutSubmit.data and logoutForm.validate():
        logoutMessage = logoutForm.logoutMessage.data
        ## Update the logoutMessage in the SQLAlchemy database.
        current_settings = Settings.query.filter_by(organisation_id=current_user.id).first()
        current_settings.logoutMessage = logoutMessage
        db.session.commit()

    currentLoginMessage = Settings.query.filter_by(organisation_id=current_user.id).first().loginMessage
    currentLogoutMessage = Settings.query.filter_by(organisation_id=current_user.id).first().logoutMessage

    return render_template(app.config['SETTINGS_NOTIFICATIES_PATH'], loginForm=loginForm, 
                                                                         logoutForm=logoutForm,
                                                                         loginMessage=currentLoginMessage,
                                                                         logoutMessage=currentLogoutMessage)

class TimeForm(FlaskForm):
    messageTime = FloatField(id="messageTime", validators=[DataRequired()])
    submit = SubmitField("Opslaan", id="submit")

@app.route("/instellingen/tijd", methods=["GET", "POST"])
@login_required
def instellingen_tijd():
    form = TimeForm()

    if form.validate_on_submit():
        messageTime = form.messageTime.data
        ## Check if the user has filled in a falid float.
        try:
            messageTime = float(messageTime)
        except ValueError:
            pass

        ## If the user has indeed filled in a falid value
        if type(messageTime) == float:
            ## Update the messageTime in the SQLAlchemy database
            current_settings = Settings.query.filter_by(organisation_id=current_user.id).first()
            current_settings.messageTime = messageTime
            db.session.commit()

    currentMessageTime = Settings.query.filter_by(organisation_id=current_user.id).first().messageTime
    return render_template(app.config['SETTINGS_TIJD_PATH'], form=form, messageTime=currentMessageTime)

class DeleteAccountForm(FlaskForm):
    delete_account_submit = SubmitField("Verwijder account", id="submit")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Oude wachtwoord"})
    new_password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Nieuw wachtwoord"})
    password_submit = SubmitField("Wijzigen", id="submit")


@app.route("/instellingen/account", methods=["GET", "POST"])
@fresh_login_required
def instellingen_account():
    username = current_user.username
    email = current_user.email
    deleteAccountForm = DeleteAccountForm()
    changePasswordForm = ChangePasswordForm()

    if deleteAccountForm.delete_account_submit.data and deleteAccountForm.validate():
        Organisation.query.filter_by(id=current_user.id).delete()
        db.session.commit()

    if changePasswordForm.password_submit.data and changePasswordForm.validate():
        if bcrypt.check_password_hash(current_user.password, changePasswordForm.old_password.data):
            hashed_password = bcrypt.generate_password_hash(changePasswordForm.new_password.data)
            current_user.password = hashed_password
            db.session.commit()

    return render_template(app.config["SETTINGS_ACCOUNT_PATH"], username=username, email=email, deleteAccountForm=deleteAccountForm, password=changePasswordForm)