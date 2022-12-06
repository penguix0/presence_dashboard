from flask import redirect, render_template, url_for, request
from flask_login import login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError
from dashboard import db, app, Organisation, Settings, bcrypt, login_manager
from re import fullmatch

class RegisterForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "E-mail"})
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Gebruikersnaam"}) 
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Wachtwoord"})
    submit = SubmitField("Registreer")

    def validate_email(self, email):
        existing_email = Organisation.query.filter_by(email=email.data).first()
        if existing_email == True:
            raise ValidationError("Het e-mail adres is al een keer geregistreerd, login of gebruik een ander email adres.")

class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "E-mail"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Wachtwoord"})
    show_password = BooleanField('Maak wachtwoord zichtbaar', id='check')
    rememberme = BooleanField(id="rememberme")
    submit = SubmitField("Login")

@login_manager.user_loader
def load_user(organisation_id):
    return Organisation.query.get(int(organisation_id))

@app.errorhandler(401)
def custom_401(error):
    return redirect(url_for("login"))

@app.errorhandler(404)
def custom_404(error):
    return render_template(app.config["PAGE_NOT_FOUND_PATH"])

## Check if the user came from somewhere but was logged out.
## In that case redirect the user back, else just go to the fallback page
def redirect_dest(fallback):
    dest_url = request.args.get('next')
    if not dest_url:
        dest_url = url_for(fallback)
    return redirect(dest_url)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    error = None
    message = None

    ## If the user submitted his login
    if form.validate_on_submit():
        ## Loop up the account and check if credentials are correct
        organisation = Organisation.query.filter_by(email=form.email.data.lower()).first()
        if organisation != None:
            if bcrypt.check_password_hash(organisation.password, form.password.data):
                login_user(organisation, remember=form.rememberme.data)
                return redirect_dest(fallback="dashboard")
            else:
                message = "Password incorrect"
        else:
            error = "Organisatie niet gevonden! Check of je de correcte inlog gegevens hebt gebruikt of maak een account aan!"

    return render_template(app.config["LOGIN_PATH"], form=form, error=error, message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    error = None
    if form.validate_on_submit():
        if Organisation.query.filter_by(username=form.username.data).first() and Organisation.query.filter_by(email=form.email.data.lower()).first():
            error = "E-mail en gebruikersnaam al gebruikt"
        ## If the email is already in the database
        elif Organisation.query.filter_by(email=form.email.data.lower()).first():
            error = "E-mail al gebruikt!"
        ## If the username is already in the database
        elif Organisation.query.filter_by(username=form.username.data).first():
            error = "Gebruikersnaam al gekozen!"
        ## Check if the email uses valid characters
        elif not fullmatch(app.config["REGEX"], form.email.data):
            error = "E-mail gebruikt ongeldige tekens."
        # elif not fullmatch(app.config["REGEX"], form.username.data):
        #     error = "Gebruikersnaam gebruikt ongeldige tekens."
        # elif not fullmatch(app.config["REGEX"], form.password.data):
        #     error = "Wachtwoord gebruikt ongeldige tekens."
        elif (not Organisation.query.filter_by(username=form.username.data).first() 
            and not Organisation.query.filter_by(email=form.email.data.lower()).first()):
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_organisation = Organisation(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
            db.session.add(new_organisation)
            db.session.commit()
            new_settings = Settings(loginMessage="Welkom", logoutMessage="Dag", messageTime=3, organisation_id=new_organisation.id)
            db.session.add(new_settings)
            db.session.commit()
            return redirect(url_for("login"))
    
    return render_template(app.config["REGISTER_PATH"], form=form, error=error)

@app.route("/logout", methods=["POST", "GET"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("login"))

