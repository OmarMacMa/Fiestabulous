from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse, abort
from flask_mysqldb import MySQL
from flask_cors import CORS
from .keys import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import os


def create_app():
    app = Flask(__name__)
    api = Api(app)
    mysql = MySQL(app)
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
    app.config['MYSQL_DB'] = MYSQL_DB
    app.config["ssl_ca"] = "./DigiCertGlobalRootCA.crt.pem"
    CORS(app)
    return app, api, mysql