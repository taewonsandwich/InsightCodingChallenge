# Insight Data Science Coding Challenge
This is a submission to the coding challenge by Insight Data Science, as part of the application to Data Engineering Fellowship Program. 

###Written and submitted by Tae Won Chung

# Description
The script-`moneytracker.py`- written in python3 for this challenge is located under /src folder. 

The scipt first parses the input file `itcont.txt` into a DataFrame object from `pandas` library. Although the file could have been read as a whole using `pandas.read_table` function, I decided to stick with 'read by line' approach as suggested by the guidelines.

This data frame also contains running median value, total value, and the count of donations by (recipient, zipcode) and by (recipient, date) categories. The two outputs `medianvals_by_zip.txt` and `medianvals_by_date.txt` are stored in /output folder. 

The script uses following libraries

1. pandas
2. numpy








