import unittest
from table_handler import *
from amazon import *
from cStringIO import StringIO
import sys


class TestSequenceFunctions(unittest.TestCase):

    blist = [
        {
            'Book': {
                'Prices': {
                    'Buy New': u'$78.03',
                    'Rent': u'$29.70'},
                'Product Details': {
                    'Publisher': u'Springer; 2nd edition (July 26, 2008)',
                    'Paperback': ' ',
                    'Age Range': ' ',
                    'Shipping Weight':
                        u'3.2 pounds (View shipping rates and policies)',
                    'Language': u'English',
                    'ASIN': ' ',
                    'Series': ' ',
                    'Product Dimensions': u'9.4 x 7.2 x 1.4 inches',
                    'Average Customer Review': '(4.4,65)',
                    'Hardcover': u'730 pages',
                    'Grade Level': ' ',
                    'ISBN-10': u'1848000693',
                    'ISBN-13': u'978-1848000698',
                    'Amazon Best Sellers Rank': u'#21,422 in Books',
                    'Lexile Measure': ' '},
                'Authors': u'Steven S Skiena',
                'Reviews': {
                    1: u' ',
                    2: u' ',
                    3: u' ',
                    4: u' '},
                'Title': u'The Algorithm Design Manual',
                'Recommends': {
                    1: u'The Art of Computer Programming, Volumes',
                    2: u"Hacker's Delight (2nd Edition)",
                    3: u'The Algorithm Design Manual',
                    4: u'Introduction to Algorithms'}}}]

    def test_book_printer_xml(self):

        old_stdout = sys.stdout
        sys.stdout = bookOutput = StringIO()
        printer = BookPrinter(xmlHandler())
        printer.print_book_table(TestSequenceFunctions.blist)

        sys.stdout = old_stdout

        # print (open("xmlValid.txt").read())
        # print (bookOutput.getvalue())
        assert str(open("test_files/xmlValid.txt").read()
                   ) == str(bookOutput.getvalue()), "Error in XML handler."

    def test_book_printer_html(self):

        old_stdout = sys.stdout
        sys.stdout = bookOutput = StringIO()
        printer = BookPrinter(htmlHandler())
        printer.print_book_table(TestSequenceFunctions.blist)

        sys.stdout = old_stdout

        # print (open("htmlValid.txt").read())
        # print (bookOutput.getvalue())
        assert str(open("test_files/htmlValid.txt").read()
                   ) == str(bookOutput.getvalue()), "Error in HTML handler."

    def test_book_printer_csv(self):

        old_stdout = sys.stdout
        sys.stdout = bookOutput = StringIO()
        printer = BookPrinter(csvHandler())
        printer.print_book_table(TestSequenceFunctions.blist)

        sys.stdout = old_stdout

        # print (open("htmlValid.txt").read())
        # print (bookOutput.getvalue())
        assert str(
            open("test_files/csvValid.txt").read()) == str(
            bookOutput.getvalue()), "Error in book printer handler output."

    def test_book_parsing(self):

        book = parsehtml(open('test_files/algBook').read())
        validBook = open('test_files/bookValid').read()
        old_stdout = sys.stdout
        sys.stdout = parsedInfo = StringIO()
        print(
            book.bktitle,
            book.authors,
            book.price,
            book.detail,
            book.json,
            book.review)
        sys.stdout = old_stdout
        # print(parsedInfo.getvalue())
        # print(validBook)
        assert parsedInfo.getvalue() == str(
            validBook), "Error in book parsing."

    def test_book_storing(self):

        db = create_database('sqlite:')
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
            " shipWeight VARCHAR, avgReview VARCHAR, review1  VARCHAR,"
            " review2  VARCHAR, review3  VARCHAR, review4  VARCHAR)")
        myBook = createAndStoreBook(store, TestSequenceFunctions.blist[0])
        assert myBook is not None, "Error in book storing."

    def test_arg(self):

        retlist, format = arg()
        assert retlist == [
        ] and format is None, "Error in arg() returns with no data."

    def test_main(self):

        mainReturn = main()
        print(mainReturn)
        assert mainReturn == 0, "Error in main() not returning 0."


if __name__ == '__main__':
    unittest.main()
