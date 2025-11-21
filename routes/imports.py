from flask import Blueprint, render_template, request, redirect, session, flash, url_for, jsonify
from flask_session import Session
from cs50 import SQL
import xaharfuncs as x
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

DataBase = SQL("sqlite:///database.db")