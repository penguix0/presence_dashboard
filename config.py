from os import path
## library to generate secret key
from secrets import token_urlsafe

## Secret key which gets automatically generated
SECRET_KEY = token_urlsafe(32)

## Port to host the web page on
PORT = 9999

## Disable DEBUG
DEBUG = True

## Path to the index page
INDEX_PATH = "index.html"
## Path to the instellingen pages
SETTINGS_DASHBOARD_PATH = "settings/dashboard.html"
SETTINGS_BESTANDEN_PATH = "settings/bestanden.html"
SETTINGS_MEDEWERKERS_PATH = "settings/medewerkers.html"
SETTINGS_NOTIFICATIES_PATH = "settings/notificaties.html"
SETTINGS_TIJD_PATH = "settings/tijd.html"
SETTINGS_ACCOUNT_PATH = "settings/account.html"
PAGE_NOT_FOUND_PATH = "errorhandling/page_not_found.html"
LOGIN_PATH = "authorization/login.html"
REGISTER_PATH = "authorization/register.html"
## Folder to upload the uploaded databases to:
UPLOAD_FOLDER = 'database/banners/'
ALLOWED_EXTENSIONS = ["png", "jpg"]

## Allowed email characters
REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

## Path to the image foler
IMAGE_FOLDER = path.join("static", "images")



