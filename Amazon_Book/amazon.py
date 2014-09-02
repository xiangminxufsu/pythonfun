from __future__ import print_function
import argparse
import requests
import os
import io
from lxml import etree
from bs4 import BeautifulSoup
from storm.locals import *
import sqlite3
from table_handler import *
import logging


class Book(object):

    __storm_table__ = "books"
    id = Int(primary=True)
    title = Unicode()
    authors = Unicode()
    rentPrice = Unicode()
    buyPrice = Unicode()

    ageRange = Unicode()
    gradeLvl = Unicode()
    lexile = Unicode()
    series = Unicode()
    paperback = Unicode()
    publisher = Unicode()
    language = Unicode()
    isbn10 = Unicode()
    isbn13 = Unicode()
    asin = Unicode()
    productDim = Unicode()
    shipWeight = Unicode()
    hardcover = Unicode()
    avgReview = Unicode()
    bestSellerRanks = Unicode()

    review1 = Unicode()
    review2 = Unicode()
    review3 = Unicode()
    review4 = Unicode()

    recommend1 = Unicode()
    recommend2 = Unicode()
    recommend3 = Unicode()
    recommend4 = Unicode()


def parseDetails(data, price, review, recommend):

    fields = ['Age Range', 'Grade Level', 'Lexile Measure',
              'Series', 'Paperback', 'Publisher', 'Language',
              'ISBN-10', 'ISBN-13', 'ASIN', 'Product Dimensions',
              'Shipping Weight', 'Average Customer Review',
              'Amazon Best Sellers Rank', 'Hardcover']
    details = {k: " " for k in fields}

    for x in data:
        temp = x.split(':')
        if temp[0] in fields:
            details[temp[0]] = temp[1]

    priceFields = ['Buy New', 'Rent']
    prices = {k: " " for k in priceFields}

    for x in price:
        temp = x.split(':')
        if temp[0] in priceFields:
            prices[temp[0]] = temp[1]

    reviewFields = [1, 2, 3, 4]
    reviews = {k: " " for k in reviewFields}

    count = 1
    for x in review:
        if count < 5:
            reviews[count] = x
            count += 1

    recommendFields = [1, 2, 3, 4]
    recommends = {k: " " for k in recommendFields}

    count = 1
    for x in recommend:
        if count < 5:
            recommends[count] = x
            count += 1

    return details, prices, reviews, recommends


def createAndStoreBook(store, bookJSON):

    newBook = Book()
    newBook.title = unicode(bookJSON['Book']['Title'])
    newBook.authors = unicode(bookJSON['Book']['Authors'])
    newBook.buyPrice = unicode(bookJSON['Book']['Prices']['Buy New'])
    newBook.rentPrice = unicode(bookJSON['Book']['Prices']['Rent'])
    newBook.ageRange = unicode(
        bookJSON['Book']['Product Details']['Age Range'])
    newBook.gradeLvl = unicode(
        bookJSON['Book']['Product Details']['Grade Level'])
    newBook.lexile = unicode(
        bookJSON['Book']['Product Details']['Lexile Measure'])
    newBook.series = unicode(bookJSON['Book']['Product Details']['Series'])
    newBook.paperback = unicode(
        bookJSON['Book']['Product Details']['Paperback'])
    newBook.publisher = unicode(
        bookJSON['Book']['Product Details']['Publisher'])
    newBook.language = unicode(bookJSON['Book']['Product Details']['Language'])
    newBook.isbn10 = unicode(bookJSON['Book']['Product Details']['ISBN-10'])
    newBook.isbn13 = unicode(bookJSON['Book']['Product Details']['ISBN-13'])
    newBook.asin = unicode(bookJSON['Book']['Product Details']['ASIN'])
    newBook.productDim = unicode(
        bookJSON['Book']['Product Details']['Product Dimensions'])
    newBook.shipWeight = unicode(
        bookJSON['Book']['Product Details']['Shipping Weight'])
    newBook.hardcover = unicode(
        bookJSON['Book']['Product Details']['Hardcover'])
    newBook.avgReview = unicode(
        bookJSON['Book']['Product Details']['Average Customer Review'])
    newBook.bestSellerRanks = unicode(
        bookJSON['Book']['Product Details']['Amazon Best Sellers Rank'])

    newBook.review1 = unicode(bookJSON['Book']['Reviews'][1])
    newBook.review2 = unicode(bookJSON['Book']['Reviews'][2])
    newBook.review3 = unicode(bookJSON['Book']['Reviews'][3])
    newBook.review4 = unicode(bookJSON['Book']['Reviews'][4])

    newBook.recommend1 = unicode(bookJSON['Book']['Recommends'][1])
    newBook.recommend2 = unicode(bookJSON['Book']['Recommends'][2])
    newBook.recommend3 = unicode(bookJSON['Book']['Recommends'][3])
    newBook.recommend4 = unicode(bookJSON['Book']['Recommends'][4])

    # print(unicode(bookJSON['Book']['Recommends'][1]))
    store.add(newBook)
    store.flush()
    return newBook
    # print "%r, %r" % (newBook.id, newBook.hardcover)


def createJSON(title, authors, price, details, review, recommend):

    details, price, review, recommend = parseDetails(
        details, price, review, recommend)
    myJSON = {
        "Book": {
            "Title": title,
            "Authors": authors,
            "Prices": price,
            "Product Details": details,
            "Reviews": review,
            "Recommends": recommend}}
    # print(myJSON)
    return myJSON


def RecommendFunc(div):

    if div is None:
        return []

    RecList = []
    li = div.find_all('li')

    for EachBook in li:
        Booklink = EachBook.find('a')
        for BookInfo in Booklink.stripped_strings:
            if BookInfo is not None:
                RecList.append(BookInfo)
            break

    # print(RecList)
    logging.info('recommend list is {x}'.format(x=RecList))
    return RecList


def TitleFunc(div):

    if div is None:
        return ' '

    # print(div.span.string)
    return div.span.string


def AuthorFunc(authorspans):

    if authorspans is None:
        logging.warning('title will be None!')
        return ' '

    authorlist = []
    for authorspan in authorspans:
        if authorspan is not None:
            peopletype = authorspan.find(attrs={"class": "contribution"})
            if peopletype is not None and peopletype.find('span') is not None:
                typename = str(peopletype.span.string)
                if typename != "(Author), " and typename != "(Author)":
                    continue

        for subspan in authorspan:
            if subspan.name == 'a':
                authorlist.append(subspan.string)
                # print(subspan.string)
                break

            if subspan.name == 'span':
                if(subspan.find('a')is not None):
                    authorlist.append(subspan.a.string)
                    break

    ret = ','.join(authorlist)
    # print (ret)
    logging.info('author {x} is found'.format(x=ret))
    return ret


def PriceFunc(soup):

    pricelist = []
    s = soup.find(id='buyNewSection')
    rentprice = soup.find(id="rentPrice")

    if rentprice is None:
        logging.warning('price not found!')
        return pricelist

    for y in s.find_all('span'):
        if y.string is not None and y.string[0] == '$':
            newprice = "Buy New:" + y.string
            pricelist.append(newprice)
            break

    if rentprice is not None:
        pricelist.append("Rent:" + rentprice.string)

    # print(pricelist)
    logging.info('price is found, good')
    return pricelist


def DetailFunc(detail_bullets):

    if detail_bullets is None:
        logging.warning('details not found for this book!')
        return []

    detaillist = []
    detaili = detail_bullets.find_all('li')  # get all the <li> into detaili

    for x in detaili:
        if x.strings is None:
            del x
        for y in x:
            if y.name == 'a':
                del y

    for x in detaili:
        oneinfo = ''
        count = 0
        for y in x.strings:
            if y == "Average Customer Review:":
                count = 1
                break
            y = y.strip()
            oneinfo += y
        if count == 1:  # stop searching when meeting review
            break
        detaillist.append(oneinfo)

    # find reviews
    spanreview = detail_bullets.find(attrs={"class": "crAvgStars"})
    if spanreview is not None:
        for spanstring in spanreview.strings:
            if(len(spanstring) > 14 and spanstring[-14:] == "out of 5 stars"):
                reviewscore = float(spanstring[0:3])
            if(len(spanstring) > 17 and
               spanstring[-16:] == "customer reviews"):
                total = int(spanstring[0:-17].replace(",", ""))

    ReviewsScore = "Average Customer Review:" + \
        "({x},{y})".format(x=reviewscore, y=total)
    detaillist.append(ReviewsScore)
    rankli = detail_bullets.find(id="SalesRank")

    for x in rankli.strings:
        xsplit = x.split()  # get first rank
        bestrank = ''
        if len(xsplit) == 4 and xsplit[3] == '(' and xsplit[2] == 'Books':
            del xsplit[3]
            bestrank = "Amazon Best Sellers Rank:" + ' '.join(xsplit)
            detaillist.append(bestrank)
            break

    logging.info('details is found, good')
    return detaillist


def ReviewFunc(divreview):

    if divreview is None:
        logging.warning('review not found for this book')
        return []

    reviewlist = []
    section = divreview.find_all(attrs={"class": "a-section"})

    for x in section:
        if x.find('div') is None:
            reviewstr = ""
            for string in x.strings:
                reviewstr += string
            reviewlist.append(reviewstr)

    logging.info('reviews is found, good!')
    return reviewlist


class parsehtml(object):

    def __init__(self, string):
        soup = BeautifulSoup(string)
        # title
        self._bktitle = TitleFunc(soup.find(id="title"))
        # recommand
        self._recommend = RecommendFunc(soup.find(id="purchaseShvl"))
        # author
        self._authors = AuthorFunc(
            soup.find_all(
                attrs={
                    "class": "author notFaded"}))
        # print(self._authors)
        # price
        self._price = PriceFunc(soup)
        # product details
        self._detail = DetailFunc(soup.find(id="detail-bullets"))
        # parse most useful reviews
        self._review = ReviewFunc(soup.find(id="revMHRL"))

    @property
    def bktitle(self):
        return self._bktitle

    @property
    def authors(self):
        return self._authors

    @property
    def price(self):
        return self._price

    @property
    def detail(self):
        return self._detail

    @property
    def review(self):
        return self._review

    @property
    def json(self):
        return createJSON(
            self._bktitle,
            self._authors,
            self._price,
            self._detail,
            self._review,
            self._recommend)

    @property
    def recommend(self):
        return self._recommend


def arg():
    retlist = []
    parser = argparse.ArgumentParser(description='Input a directory or website link is \
    required,output format is optional ')
    parser.add_argument('-u', '--link')
    parser.add_argument('-d', '--directory')
    parser.add_argument('-o', '--output')
    args = vars(parser.parse_args())

    x = None
    format = None

    if args['link'] is not None:
        logging.info("link is found, now get data from link")
        link = args['link']
        r = requests.get(link)
        x = parsehtml(r.text)
        retlist.append(x.json)

    if args['directory'] is not None:
        logging.info("directory is found, now get data from files")
        curdir = os.getcwd()
        tardir = args['directory']

        for tarfile in os.listdir(tardir):
            if tarfile.endswith(".html"):
                tarfile = tardir + '/' + tarfile
                text = open(tarfile, "r").read()
                x = parsehtml(text)
                retlist.append(x.json)

    if args['output'] is not None:
        logging.info("output format {x} is found".format(x=args['output']))
        if args['output'] in ['xml', 'html', 'csv']:
            format = args['output']

    return retlist, format


def main():

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(filename)s\
        [line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='Amazon.log',
        filemode='w')

    logging.info("OK,program is starting")
    retlist, format = arg()

    if(os.path.isfile("amazon.db")):
        os.remove("amazon.db")

    db = create_database('sqlite:amazon.db')
    store = Store(db)
    store.execute(
        "CREATE TABLE books "
        "(id INTEGER PRIMARY KEY, title VARCHAR,"
        " authors VARCHAR, buyPrice VARCHAR, rentPrice VARCHAR,"
        " hardcover VARCHAR, bestSellerRanks VARCHAR,"
        " ageRange VARCHAR, gradeLvl  VARCHAR,"
        " lexile VARCHAR, series VARCHAR, paperback VARCHAR,"
        " publisher VARCHAR, language VARCHAR, isbn10 VARCHAR,"
        " isbn13 VARCHAR, asin VARCHAR, productDim VARCHAR,"
        " shipWeight VARCHAR, avgReview VARCHAR, review1 VARCHAR,"
        " review2 VARCHAR, review3 VARCHAR,"
        " review4 VARCHAR, recommend1 VARCHAR,"
        " recommend2 VARCHAR, recommend3 VARCHAR, recommend4 VARCHAR)")

    for x in retlist:
        createAndStoreBook(store, x)

    if format is not None:
        # print("Formatting will be: " + format)
        if format == 'csv':
            handler = csvHandler()
        elif format == 'html':
            handler = htmlHandler()
        elif format == 'xml':
            handler = xmlHandler()

        printer = BookPrinter(handler)
        printer.print_book_table(retlist)

    store.commit()

    return 0

if __name__ == '__main__':
    main()
