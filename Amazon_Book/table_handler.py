import sys


class csvHandler(object):

    def header(self, hdata):

        print(",".join(hdata))

    def row(self, rdata):

        print(",".join(rdata[1]))


class xmlHandler(object):

    def header(self, hdata):

        print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        print("<document>")

    def row(self, rdata):

        count = 0
        for r in rdata[1]:
            if count > 0:
                print "\t",
            print(
                "\t<" +
                rdata[0][count].replace(
                    " ",
                    "") +
                ">" +
                r +
                "</" +
                rdata[0][count].replace(
                    " ",
                    "") +
                ">")
            count += 1


class htmlHandler(object):

    def header(self, hdata):

        print("<!DOCTYPE html>")
        print("<html>")
        print("<title>Movies</title>")
        print("<body>")
        print("\t<table border=\"1\" style=\"width:1024px\">")
        print("\t\t<tr>")

        for h in hdata:
            print("\t\t\t<th>" + h + "</th>")

        print("\t\t</tr>")

    def row(self, rdata):

        print("\t\t<tr>")

        for r in rdata[1]:
            print("\t\t\t<td>" + r + "</td>")

        print("\t\t</tr>")


class BookPrinter(object):

    def __init__(self, handler):

        self.handler = handler

    def print_book_table(self, blist):

        # print header

        self.handler.header(["Title",
                             "Authors",
                             "Buy New",
                             "Rent",
                             "Age Range",
                             "Grade Level",
                             "Lexile Measure",
                             "Series",
                             "Paperback",
                             "Publisher",
                             "Language",
                             "ISBN-10",
                             "ISBN-13",
                             "ASIN",
                             "Product Dimensions",
                             "Shipping Weight",
                             "Hardcover",
                             "Average Customer review",
                             "Amazon Best Sellers Rank"])

        # print book data
        pd = 'Product Details'
        for b in blist:
            self.handler.row([["Title",
                               "Authors",
                               "Buy New",
                               "Rent",
                               "Age Range",
                               "Grade Level",
                               "Lexile Measure",
                               "Series",
                               "Paperback",
                               "Publisher",
                               "Language",
                               "ISBN-10",
                               "ISBN-13",
                               "ASIN",
                               "Product Dimensions",
                               "Shipping Weight",
                               "Hardcover",
                               "Average Customer review",
                               "Amazon Best Sellers Rank"],
                              [b['Book']['Title'],
                               b['Book']['Authors'],
                               b['Book']['Prices']['Buy New'],
                               b['Book']['Prices']['Rent'],
                               b['Book'][pd]['Age Range'],
                               b['Book'][pd]['Grade Level'],
                               b['Book'][pd]['Lexile Measure'],
                               b['Book'][pd]['Series'],
                               b['Book'][pd]['Paperback'],
                               b['Book'][pd]['Publisher'],
                               b['Book'][pd]['Language'],
                               b['Book'][pd]['ISBN-10'],
                               b['Book'][pd]['ISBN-13'],
                               b['Book'][pd]['ASIN'],
                               b['Book'][pd]['Product Dimensions'],
                               b['Book'][pd]['Shipping Weight'],
                               b['Book'][pd]['Hardcover'],
                               b['Book'][pd]['Average Customer Review'],
                               b['Book'][pd]['Amazon Best Sellers Rank']]])

        handlerType = self.handler.__class__.__name__

        if handlerType == "htmlHandler":
            print("\t</table>\n</body>\n</html>")
        elif handlerType == "xmlHandler":
            print("</document>")
