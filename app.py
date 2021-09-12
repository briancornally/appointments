#!/usr/bin/env python3
from flask import render_template
from app import app, db
from app.models import *

dir(app)

if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)

