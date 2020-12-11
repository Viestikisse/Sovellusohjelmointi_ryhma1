class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://Admin:kiisu@localhost/TUASreservations'

    SQLALCHEMY_TRACK_MODIFICATIONS = False