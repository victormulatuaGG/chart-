#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import SubmitField
import sys

class controls(FlaskForm):
	pause = SubmitField("Pause")
	play = SubmitField("Play")
	previous = SubmitField("Previous")
	next = SubmitField("Next")
