#! /usr/local/bin/python2.5

import feedparser
from datetime import datetime

#  USER OPTIONS AND CUSTOMIZATION
#
checkedoutfeeds =	["http://catalog.spl.org/rss/itemsout.jsp?id=something",
	 "http://catalog.spl.org/rss/itemsout.jsp?id=something else"]
holdfeeds =	["http://catalog.spl.org/rss/holds.jsp?id=something",
	 "http://catalog.spl.org/rss/holds.jsp?id=something-else"]
#
# toggle whether to show the name of the person next to each book.
showname = True # Set to True if you have more than one feed.

#if a string is bigger than n characters, shorten it and add an ellpsis
#I'm also remvoing a trailing slash which the library adds sometimes
def truncate(str,n):
	if str[-1]=='/':
		str=str[:-1]
	if len(str)>n:
		return str[0:n-3]+"..."
	else:
		return str

#Extracts the date from the summary part of the RSS feed and parses it.
#I'm using the specific knowledge of how this particular RSS feed displays
#the date (as mm/dd/yyyy)
def extractdate(str):
	loc = str.find("Date Due:")
	daystr = str[loc+10:loc+20]
	return datetime.strptime(daystr,"%m/%d/%Y")

#determines the status of a hold
def extractstatus(str):
	loc = str.find("Status:")
	if loc==-1:
		return "ready for pickup"
	else:
		return str[loc+8:]

#extracts the title from the feed
def extracttitle(str):
	loc = str.find(":")
	return str[loc+2:]

#defines the order in which to sort the holds
def sortkey(blahlist):
	blah=blahlist[1]
	if blah=="ready for pickup":
		return 0
	if blah=="in transit":
		return 1
	if blah=="active":
		return 2
	if blah=="suspended":
		return 3
	return 10

# takes the items out list and returns a list of books and due dates
def itemsoutlist(booklist,tag):
	return [(extractdate(book.summary),truncate(book.title,40),tag) for book in booklist]

def holdslist(booklist,tag):
	return [(truncate(extracttitle(book.title),40),extractstatus(book.summary),tag)
				for book in booklist]


# BEGIN EXECUTION
#because its a cgi script
print """Content-Type: text/html; charset=UTF-8

<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<meta name="viewport" content="width=350px">
		<title>Library Books</title>
	</head>
	<body>
		<link href="style.css" rel="stylesheet" type="text/css" media="all">
		<p>
			<a href='http://seattle.bibliocommons.com/'>Go to
			library web page.</a>
		<br><br>"""

# Checked out feeds
parsedfeeds = [feedparser.parse(feed) for feed in checkedoutfeeds]
list=[]
for feed in parsedfeeds:
	list.extend(itemsoutlist(feed.entries[1:],feed.feed.title.split()[0]))
list.sort()

#begin outputting html
print "<table><tr><th class=title>Books Checked Out</th>"
if showname:
	print "<th class=due>Due Date</th><th class=who>Who</th>"
print "</tr>"
for book in list:
	print "<tr><td class=title>"+book[1]+"</td>"
	print "<td class=due>"+book[0].strftime("%a %b %d")+"</td>"
	if showname:
		print "<td class=who>"+book[2]+"</td>"
	print "</tr>"
print "</table><br>"


# hold feeds
parsedfeeds=[feedparser.parse(feed) for feed in holdfeeds]
list=[]
for feed in parsedfeeds:
	list.extend(holdslist(feed.entries[1:],feed.feed.title.split()[0]))
list.sort(key=sortkey)

#ouput hold html
print "<table><tr><th class=title>Books On Hold</th>"
if showname:
	print "<th class=due>Status</th><th class=who>Who</th>"
print "</tr>"
for book in list:
	print "<tr><td class=title>"+book[0]+"</td>"
	print "<td class=status>"+book[1].capitalize()+"</td>"
	if showname:
		print "<td class=who>"+book[2]+ "</td>"
	print "</tr>"
print "</table>"

print "<a href='http://seattle.bibliocommons.com/'>Go to library web page.</a>"
print "</body></html>"
