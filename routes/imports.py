from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_session import Session
from cs50 import SQL
import xaharfuncs as x
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

DataBase = SQL("sqlite:///database.db")