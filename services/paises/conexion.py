from flask import Flask, jsonify,request
from flask_restful import Api, Resource
import mysql.connector
import hashlib
import requests

mi_db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="biblioteca"
)
mi_cursor = mi_db.cursor()