from __future__ import print_function


class CsvHandler():

	def header(self,hdata):

		msg="{v}, {r}, {y}, {t}"

		assert len(hdata)==4

		print (msg.format(v=hdata[0],r=hdata[1],y=hdata[2],t=hdata[3]))

	def row(self,rdata):

		msg="{v}, {r}, {y}, {t}"

		for x in rdata:
		
			print(msg.format(v=x.votes,r=x.rating,\

				y=x.year,t=x.title))

class XmlHandler():
	def header(self,hdata):
		pass

	def row(self,rdata):
		print ("<movies>")
		for x in rdata:
			print("  <movie>")
			print("    <title>{t}</title>".format(t=x.title))
			print("    <votes>{v}</votes>".format(v=x.votes))
			print("    <rating>{r}</rating>".format(r=x.rating))
			print("    <year>{y}</year>".format(y=x.year))
			print("  </movie>\n")
			#print ('\n')
		print("</movies>")

class HtmlHandler():
	def header(self,hdata):
		pass

	def row(self,rdata):
		print("<html>")
		print("<head><title>Movies</title><head>\n")
		print("<body>\n")
		print("<h2>Movie</h2>\n<hr>\n")
		for x in rdata:
			print("<i><font face='verdana'>",end=' ')
			print("{t},</font>&nbsp</i>".format(t=x.title),end=" ")
			print("{v},&nbsp".format(v=x.votes),end=" ")
			print("{r},&nbsp".format(r=x.rating),end=" ")
			print("{y}".format(y=x.year),end=" ")
			print("<br></br>")


class MVprinter(object):

	def __init__(self, handler):

		self.handler = handler

	def print_movie_table(self,mlist):

		#for m in mlist:

		self.handler.header(["Votes", "Rating", "Year", "Title"])

		self.handler.row(mlist)

		



