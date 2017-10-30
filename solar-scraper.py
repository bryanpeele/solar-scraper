# import libraries
import urllib.request
from bs4 import BeautifulSoup
import csv
import pandas as pd
from pandas import DataFrame


Latitude_min = -90
Latitude_max =  91
Longitude_min = -180
Longitude_max =  181

#for test
#Latitude_min = -2
#Latitude_max =  2
#Longitude_min = -2
#Longitude_max =  2


filename ="insolation_data_1983-2005.csv"

for Latitude in range(Latitude_min,Latitude_max):
	frames=[]
	for Longitude in range(Longitude_min,Longitude_max):
		# specify the url
		# specify the url
		quote_page = 'https://eosweb.larc.nasa.gov/cgi-bin/sse/interann.cgi?email=skip%40larc.nasa.gov&step=1&lat='	\
					 +str(Latitude)+'&lon='+str(Longitude)+'&ys=1983&ye=2005&p=swv_dwn&submit=Submit'

		# query the website and return the html to the variable ‘page’
		page = urllib.request.urlopen(quote_page)

		# parse the html using beautiful soap and store in variable `soup`
		soup = BeautifulSoup(page, 'html.parser')

		caption = soup.find("caption")

		data=[]

		table = caption.find_parent()


		rows = table.find_all('tr')
		for row in rows:
		    cols = row.find_all('td')
		    cols = [ele.text.strip() for ele in cols]
		    data.append([ele for ele in cols if ele]) # Get rid of empty values

		df = DataFrame(data=data[1:24])
		names=data[0]
		df.columns=names

		df = pd.melt(df,id_vars=['Year'],value_vars=names[1:14],var_name="Month",value_name="Insolation")
		df['Latitude']  = Latitude
		df['Longitude'] = Longitude
		frames.append(df)

	results = pd.concat(frames)
	#print(results)
	if(Latitude==Latitude_min):
		results.to_csv(filename,index=False,header=True)
	else:
		with open(filename, 'a') as f:
			results.to_csv(f,index=False, header=False)

	print('Latitude: '+str(Latitude)+"/"+str(Latitude_max))


