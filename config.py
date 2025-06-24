
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, render_template_string, session, flash
from pony.orm import Database, Required, Optional, Set, PrimaryKey, db_session, commit, select

db = Database()
app = Flask(__name__)
app.secret_key = "gremio"