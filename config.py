class Config:
    DEBUG = True

    #PITÄÄ MUOKATA, nameen ja passwordiin oma, samoin db-nimeen
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://Admin:kiisu@localhost/TUASreservations'

    SQLALCHEMY_TRACK_MODIFICATIONS = False