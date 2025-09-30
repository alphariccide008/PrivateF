from os import getenv

user = getenv('CRYPTOWEB_USER')
password = getenv('CRYPTOWEB_PWD')
database = getenv('CRYPTOWEB_DB')
host = getenv('CRYPTOWEB_HOST')


SECRET_KEY="R5T6Y7UHJIKOLO987EROELFKGWASDDJNRFTGHVN"
ADMIN_EMAIL="godspowerlawrence008@gmail.com"
USER_PROFILE_PATH="pkg/static/profiles/"
# SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:@localhost:3306/moniepoint"

# SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://cryptofianance:ikechi100@cryptofianance.mysql.pythonanywhere-services.com/cryptofianance$maindb"

