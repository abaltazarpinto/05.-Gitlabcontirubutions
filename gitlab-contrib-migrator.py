#!/usr/bin/python

import sys
from datetime import datetime
from bs4 import BeautifulSoup
import os
from tqdm import tqdm


#function that creates the commits based on the number of contributions and date
def createNumOfCommitsOnDate(contribCount, date):
    numOfCommits = contribCount
    for i in range(contribCount):
        os.system('echo "Commit number {} on {}" >> commit.md'.format(i+1, date.strftime("%m-%d-%Y")))

    for i in tqdm(range(numOfCommits)):
        os.system('echo "Commit number {} on {}" >> commit.md'.format(i+1, date.strftime("%m-%d-%Y")))
        os.system('set GIT_COMMITTER_DATE="{} 12:00:00"'.format(date.strftime("%m-%d-%Y")))
        os.system('set GIT_AUTHOR_DATE="{} 12:00:00"'.format(date.strftime("%m-%d-%Y")))
        os.system('git add --all > NUL')
        os.system('git commit --date="{} 12:00:00" -m "Commit number {} on {}" > NUL'.format( date.strftime("%Y-%m-%d"), (i+1), date.strftime("%m-%d-%Y")))
"""       
def createNumOfCommitsOnDate(numOfCommits, date):
    if numOfCommits > 30:
        numOfCommits = 30
    for i in tqdm(range(numOfCommits)):
        os.system('echo "Commit number {} on {}" >> commit.md'.format((i+1), date.strftime("%m-%d-%Y")))
        os.system('export GIT_COMMITTER_DATE="{} 12:00:00"'.format(date.strftime("%m-%d-%Y")))
        os.system('export GIT_AUTHOR_DATE="{} 12:00:00"'.format(date.strftime("%m-%d-%Y")))
        os.system('git add --all > /dev/null')
        os.system('git commit --date="{} 12:00:00" -m "Commit number {} on {}" > /dev/null'.format( date.strftime("%Y-%m-%d"), (i+1), date.strftime("%m-%d-%Y")))
""" 
#function that parses the HTML and creates the commits
def parseHTMLAndCreateCommits(htmlContents, startDate):
    soup = BeautifulSoup(htmlContents, 'html.parser')
    dateRects = soup.find_all("rect", {"class": "user-contrib-cell has-tooltip"})
    print("Starting commits!\n")
    for dateRect in tqdm(dateRects):
        contribsAndDate = dateRect["title"].split("<br />")
        try:
            contribCount = int(contribsAndDate[0].split(" ")[0])
        except ValueError:
            continue
        date = datetime.strptime(contribsAndDate[1], '<span class="gl-text-gray-300">%A %b %d, %Y</span>')
        if startDate == -1 or startDate <= date:
            createNumOfCommitsOnDate(contribCount, date)
    print("Created commits for contrib chart! Use 'git push' to push to remote or use 'git log' to check commit log")

#function that parses the arguments
def parseArgs(argv):
    if (len(argv) < 2):
        print( "Help - Try running: \n\ngitlab-contrib-migrator.py <htmlFile> <startDate> \n\nhtmlFile = HTML file with GitLab info \nstartDate = start commit date in MM-DD-YYYY format" )
        exit()
    try:
        file = open(argv[1], 'rb')
        htmlContents = file.read()
    except:
        print( "Error when trying to read the HTML file: {}".format(argv[1]) )
        exit()
    if (len(argv) == 3):
        try:
            startDate = datetime.strptime(argv[2], '%m-%d-%Y')
            return (htmlContents, startDate)
        except:
            print( "Error trying to parse start commit date: {} - proceeding without start date".format(argv[2]) )
    return (htmlContents, -1)

#main function that calls the other functions
def main(argv):
    htmlContents, startDate = parseArgs(argv)
    parseHTMLAndCreateCommits(htmlContents, startDate)

#checks if the code is being run as the main program
if __name__ == "__main__":
   main(sys.argv)