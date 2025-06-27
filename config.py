import os
from flask_env import MetaFlaskEnv

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecret'
    DEBUG=True
    FLASK_RUN_PORT=6000
