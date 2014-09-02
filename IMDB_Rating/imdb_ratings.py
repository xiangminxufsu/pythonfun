"""
Reads from standard input movie entries from an exported
imdb database. It then finds the movies made between
1950 and 1967 (inclusive) with a rating below 3.0 (exclusive)
and at least 30 votes. It prints the titles of such movies to
standard output.
"""
from __future__ import print_function
from format import CsvHandler, XmlHandler,HtmlHandler,MVprinter
import re
import sys
import csv


class GroupMovieByElements(object):

    """
    Class for parsing an exported imdb database line.
    Finds the Title of the film,  the year it was made,
    the number of votes it recieved, and its rating.
    """

    def __init__(self, string):
        """
        Finds and sets the number of votes, rating, title, and year
        from the given string
        """
        self._votes=-1
        self._title=""
        self._rating=-1.0
        self._year=-1
        mvyear=-1   #initilize mvyear

        if len(string.split())>=4 and string.split()[1].isdigit() is True\
        and re.match("^\d+?\.\d+?$", string.split()[2]) is not None:
            #parse votes,second in list
            self._votes=int(string.split()[1])
            slist=string.split() 
            #parse rating float
            self._rating=float(slist[2]) 
            del slist[0],slist[0],slist[0] 
            #parse year
            for x in slist:
                if x[0]=='(' and x[-1]==')':
                    stryear=x
                    slist.remove(stryear) #remove (year) in the list
                    if len(x)>=6 and x[1:5].isdigit() is True:
                        mvyear=int(x[1:5]) #extract year
                    break
            

            self._year=mvyear
            #parse title
            self._title=' '.join(slist).replace('"',"")
            #print (slist)
        

    @property
    def votes(self):
        """
        Getter function for votes
        """
        return self._votes

    @property
    def rating(self):
        """
        Getter function for rating
        """
        return self._rating

    @property
    def title(self):
        """
        Getter function for title
        """
        return self._title

    @property
    def year(self):
        """
        Getter function for year
        """
        return self._year
######################################################################

def condition(imdb_record):
    """
    Determines if a movie is between 2010 (inclusive),
    has a rating greater than 8.0 (exclusive), and at least 1000 votes
    """
    if(imdb_record.rating>8.0 and imdb_record.votes>=1000 \
        and imdb_record.year==2010):
        return True
    return False
#######################################################################

if __name__ =='__main__':
    f=open('ratings.list')
    content=f.readlines()
    format=sys.argv[1]
    mlist=[]
    for x in content:
        movie=GroupMovieByElements(x)
        if condition(movie):
            mlist.append(movie)
   #remove dup in mlist
    for x in mlist:
        count=0
        for y in mlist:
            if (x.title==y.title):
                count+=1
        if count>=2:
            mlist.remove(x)  

    if format=='csv':
        handler=CsvHandler()
    if format=='xml':
        handler=XmlHandler()
    if format=='html':
        handler=HtmlHandler()
    printer=MVprinter(handler)
    printer.print_movie_table(mlist)
