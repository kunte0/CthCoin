import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
# THREADS_PER_PAGE = 2

# DISABLE protection agains *Cross-site Request Forgery (CSRF)*
WTF_CSRF_ENABLED = False


SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Supress warnings
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "dsadcsrf_wowso_secure10219832918321"

SESSION_COOKIE_NAME = "cthcoin_session"
# Secret key for signing cookies
SECRET_KEY = "ao_this_is_acookie!§key392183289189321"
