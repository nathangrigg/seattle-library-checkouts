# Note

The Seattle Public Library no longer offers RSS feeds of checkouts or holds, so this **no longer works**. It may, however, be useful to some people as a prototype. To get holds and checkouts from the Seattle Public Library, you might try [my fork of checkcards][1].

# Description

This python cgi script downloads RSS feeds from the Seattle Public Library and parses them. It then prints out a table of books you have checked out and books you have on hold.

# Requirements

Requires the [feedparser][2] python module.

# Usage

In the first few lines of the code, there is a place for the private RSS feed addresses that you can get from the Seattle Public Library. You will need to edit these before using.


[1]: https://github.com/nathan11g/checkcards
[2]: http://feedparser.org
