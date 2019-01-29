import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup as soup
import numpy as np
import datetime
import time
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests

#write files 
filename = "taghazout_surf_data.csv"
f = open(filename, "w")

#create headers and write headers
headers = "date,swell_height_ft,swell_period_secs,wind_speed_mph,swell_dir,wind_dir"
f.write(headers + "\n")

#create days and months range 
days = np.asarray(range(1,32))
type(days)
months = np.asarray(range(1,13))
#months

for month in months:
	for day in days:
		#sleep to avoid overloading server
		time.sleep(5)
		url = "https://magicseaweed.com/spot-daily-history.php?spotId=131&month=" + str(month) + "&day=" + str(day)
		#make request
		print url
		try:
			r = requests.get(url, verify=False)
		except:
			print "day out of range"
		page_html = r.text
		page_soup = soup(page_html,"html.parser")

		#get table container
		container = page_soup.findAll("table")[1]

		#get row
		rows = container.findAll("tr")

		for row in rows[4:]:
			#get forecast date
			try:
				year = row.find("span",{"class":"forecastDayName"}).text
				forecast_date = row.find("td", {"class":"forecastDate"}).text.strip()
				forecast_date = forecast_date.replace(year,str(year)+"/")
				print forecast_date
			except:
				print "year out of range"

			#get swell height
			try:
				swell_height = row.findAll("span", {"class":"forecastBigLetters"})[0].text
			except:
				print "NaN"

			try:
				swell_period = row.findAll("span", {"class":"forecastBigLetters"})[1].text
			except:
				print "NaN"

			try:
				wind_speed = row.findAll("span", {"class":"forecastBigLetters"})[2].text
			except:
				print "NaN"

			try:
				#swell direction
				swell_dir = row.findAll("td")[4].img.attrs["src"]
				swell_dir = swell_dir.replace("http://images.magicseaweed.com/swellArrows/","")
				swell_dir = swell_dir.replace(".png","")
			except:
				print "NaN"

			try:
				#wind direction
				wind_dir = row.findAll("td")[7].img.attrs["src"]
				wind_dir = wind_dir.replace("http://images.magicseaweed.com/newWindArrows/","")
				wind_dir = wind_dir.replace(".png","")
				print wind_dir
			except:
				print "NaN"

			#write to file
			f.write(forecast_date.encode('utf8') + "," + swell_height.encode('utf8') + "," + swell_period.encode('utf8') + "," + wind_speed.encode('utf8') + "," + swell_dir.encode('utf8') + "," + wind_dir.encode('utf8') + "\n")
f.close()