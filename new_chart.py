import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

x_name=None	#x-axis name
y_name=None #y-axis name
x_list=[]	#store x value	
y_list=[]	#store y value
file_name = sys.argv[1]
dest_file = 'output.png'
maxbudget=0

with open(file_name,"rb") as csvfile:

	reader=csv.reader(csvfile)
	firstline=True

	for row in reader:

		if firstline:
			y_name=row[0]
			x_name=row[1]
			firstline=False
			continue

		elif row[0]=='':
			break

		else:
			budget=int(row[0][1:].replace(',',''))  #get the year removing '$' and ','
			maxbudget=max(maxbudget,budget)
			y_list.append(budget)
			temdate=dt.datetime.strptime(row[1], '%d-%b-%y').date() #translate string to date
			x_list.append(temdate)

print x_list, y_list
assert len(x_list)==len(y_list)

date1=x_list[0]-dt.timedelta(days=1)  #begining date showing in the fig
date2=x_list[len(x_list)-1]+dt.timedelta(days=1) #end date showing in the fig
fig,ax=plt.subplots()
ax.plot_date(x_list,y_list,'ro')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d-%y'))
ax.set_ylim(0,maxbudget+1000)
ax.set_xlim(date1,date2)
ax.set_xlabel(x_name,fontsize=14,style='italic',fontweight='bold')
ax.set_ylabel(y_name,fontsize=14,style='italic',fontweight='bold')
fig.autofmt_xdate()
plt.savefig(dest_file)
plt.close()

