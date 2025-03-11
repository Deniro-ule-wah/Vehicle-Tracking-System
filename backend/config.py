class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vehicles.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True
    UPDATE_INTERVAL = 5000  # milliseconds