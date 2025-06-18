from flask import Flask, render_template, request, redirect
from pony.orm import Database, Required, Optional, Set, PrimaryKey

db = Database()
app = Flask(__name__)

