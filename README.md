# charts-display
small website for displaying google sheets charts

To use, please make a .env file with the following information:
```
TITLE = "website title"
COUNT = (whatever number of charts you will display, must match number in this file)
0 = (link to relevant google sheet chart)
# every other chart should be assigned to a variable incrementing from 0
```
You can customise the refresh timer of the page in /app/templates/base.html.

Designed to be used with a certain size of chart, the size of the chart in the Google Sheet should match.

Flask must be configured properly to run 'start' file.
