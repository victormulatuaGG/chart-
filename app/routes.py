#!/usr/bin/python3
import sys, os
from flask import Flask, render_template, request, redirect, url_for
from app import app
from app.forms import controls
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# There should be a .env file created with the following information:
# COUNT = (number of google sheet's chart's embed links)
# 0 = (first google sheet chart embed link)
# and then incrementing numeric assignments of other chart's embed links

# load local variables
load_dotenv()

# pause the automatic switching of graphs
def pauseJob():
    scheduler.pause_job("graph_switch", jobstore=None)
    return

# resume automatic switching of graphs
def resumeJob():
    scheduler.resume_job("graph_switch", jobstore=None)
    return

# move on to the next graph
def changeGraph():
    if changeGraph.count == len(changeGraph.list):
        changeGraph.count = 0
    changeGraph.iframe = changeGraph.list[changeGraph.count]
    changeGraph.count = changeGraph.count + 1
    return

# moving forward and backward through the list
def moveWithinGraph(direction):
    if direction == "next":
        changeGraph()
    elif direction == "previous":
        if changeGraph.count == 1:
            changeGraph.count = len(changeGraph.list) - 1
        else:
            changeGraph.count = changeGraph.count - 2
        changeGraph()
    return

# all of our variables, attached to the above function so they can exist outside of flask
changeGraph.count = 1
changeGraph.iframe = ""
changeGraph.playing = True
changeGraph.list = []

# this extracts all of our relevant google sheets graphs and creates a list of them
count = os.getenv("COUNT")
for x in range(int(count)):
    changeGraph.list.append(os.getenv(str(x)))
changeGraph.iframe = changeGraph.list[0]

# initialise the scheduler that moves between graphs every few seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=changeGraph, trigger="interval", seconds=15, id="graph_switch")
scheduler.start()

# main body of the website, simple navigation controls, rendering the provided html and css files
@app.route('/', methods=['GET', 'POST'])
def root():
    form = controls()
    if form.validate_on_submit():
        if form.pause.data:
            changeGraph.playing = False
            pauseJob()
        elif form.play.data:
            changeGraph.playing = True
            changeGraph()
            resumeJob()
        elif form.next.data:
            moveWithinGraph("next")
            return redirect(url_for("root"))
        elif form.previous.data:
            moveWithinGraph("previous")
            return redirect(url_for("root"))
    return render_template('base.html', title=os.getenv("TITLE"), form=form, iframe=changeGraph.iframe, playing=changeGraph.playing)
