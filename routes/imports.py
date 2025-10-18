from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_session import Session
from cs50 import SQL
from xaharfuncs import match_passwords, valid_date