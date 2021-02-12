import OpenBlender
import pandas as pd
import json
from datetime import datetime as dt


data = pd.read_csv('input/corona.csv')

# column headers
# 'confirmed', 'countryregion', 'deaths', 'latitude', 'longitude',
# 'provincestate', 'recovered', 'timestamp'

data  = data.drop_duplicates()

# make it easier for visualization
dates = [dt.fromtimestamp(i) for i in data['timestamp']]
data.insert(1,"date",dates)

# sort by date/timestamp
data = data.sort_values(by=['date'])


distinctDates = list(set(list(data['timestamp'])))
distinctPS = list(set(list(data['provincestate'])))

country 	  = dict()
provice_state = dict()

for date in distinctDates:
	currData = data[data['timestamp'] == date]
	for prov_state in distinctPS:
		specificData   = currData[currData['provincestate'] == prov_state]
		country_region = specificData['countryregion']
		confirmed	   = specificData['confirmed'] 
		deaths		   = specificData['deaths']
		recovered	   = specificData['recovered']


		# if havent done this country/region yet, we must add its skeleton
		if(country_region not in country.keys()):
			country[country_region] = {'pstate':[prov_state],'dates':[date],'agg_confirmed':[confirmed],
			'agg_deaths':[deaths],'agg_recovered':[recovered]}
		else:
			# if havent added this state yet
			if(prov_state not in country[country_region].keys()):
				country[country_region]['pstate'].append(prov_state)
			
			# add the current date
			country[country_region]['dates'].append(date)

			# either append the confirmed amount for this date (if nothing for this date has been entered yet) 
			# or add it to the current index (if something from this date was already added))
			if(len(country[country_region]['agg_confirmed'])<len(country[country_region]['dates'])):
				country[country_region]['agg_confirmed'].append(confirmed)
			country[country_region]['agg_confirmed'][len(country[country_region]['dates'])-1] = country[country_region]['agg_confirmed'][len(country[country_region]['dates'])-1] + confirmed

			# The two below are the same logic as the one above, only for their var
			if(len(country[country_region]['agg_deaths'])<len(country[country_region]['dates'])):
				country[country_region]['agg_deaths'].append(deaths)
			country[country_region]['agg_deaths'][len(country[country_region]['dates'])-1] = country[country_region]['agg_deaths'][len(country[country_region]['dates'])-1] + deaths

			if(len(country[country_region]['agg_recovered'])<len(country[country_region]['dates'])):
				country[country_region]['agg_recovered'].append(confirmed)
			country[country_region]['agg_recovered'][len(country[country_region]['dates'])-1] = country[country_region]['agg_recovered'][len(country[country_region]['dates'])-1] + recovered