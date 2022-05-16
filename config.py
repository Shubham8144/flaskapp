from re import S
from app import app

app.config["SECRET_KEY"] = "a744b12533e8ccf6f3171883e13cdc3b"

class Config:
    DEBUG = True
    SECRET_KEY = "a744b12533e8ccf6f3171883e13cdc3b"
