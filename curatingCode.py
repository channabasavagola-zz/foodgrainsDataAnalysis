import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

#reading the data from FAO_Crops_area_harvested_Data.xlsx and dumping the data into pickle file for faster further access
harvested_Data = pd.read_excel('FAO_Crops_area_harvested_Data.xlsx')
harvested_Data.to_pickle('harvested_Data.pickle')

#reading the dumped data from pickle file
#harvested_Data = pd.read_pickle('harvested_Data.pickle')

#task1
#collecting columns that needs to be dropped and submitting the list to drop() method to drop respective columns
toBeDropped = [key for key in harvested_Data.keys() if key[-1] == 'F']
harvested_Data.drop(toBeDropped, axis = 1, inplace = True)
#for key in harvested_Data.keys():
#	if key[-1] == 'F':
#		del harvested_Data[key]

#task2
#filtering data with 'country code' less than 1000 after converting them to integer values
harvested_Data['Country Code'].astype('int64')
harvested_Data_country = harvested_Data.loc[harvested_Data['Country Code'] < 1000, : ]
#harvested_Data_country = harvested_Data[[int(code) < 1000 for code in harvested_Data['Country Code']]]
#print(harvested_Data_country.head(50))

#task3
#reading data from crop_codes_names.xlsx and dumpoing the data into pickle file for faster further access
crop_codes_names = pd.read_excel('crop_codes_names.xlsx')
crop_codes_names.to_pickle('crop_codes_names.pickle')
#crop_codes_names = pd.read_pickle('crop_codes_names.pickle')

#task4
#merging crop_codes_names and the data read from other xlsx file on 'item code', I have used 'inner' join
merged_data = pd.merge(crop_codes_names, harvested_Data_country, on = 'Item Code', how = 'inner')
merged_data.to_excel('merged_data.xlsx')
merged_data.to_pickle('merged_data.pickle')
#merged_data = pd.read_pickle('merged_data.pickle')

#task5
#calculating mean accross columns(axis = 1)
area_mean_series = harvested_Data_country.mean(axis = 1).rename('Mean_area')
country_series = harvested_Data_country['Country'].rename('Country')
#concatinating both series to for a dataframe
harvested_country_meanArea = pd.concat([country_series, area_mean_series], axis = 1)
#grouping them by country and adding the average crop land
harvested_country_meanArea = harvested_country_meanArea['Mean_area'].groupby(harvested_country_meanArea['Country']).sum().to_frame()
#sorting the total average crop land in descending order and selecting top 10
harvested_country_meanArea_sorted = harvested_country_meanArea['Mean_area'].sort_values(ascending = False).to_frame().head(10)
#changing the index to a column, to dumping dataframe and taking it back from csv file
harvested_country_meanArea_sorted.to_csv('deleteIt.csv')
harvested_country_meanArea_sorted = pd.read_csv('deleteIt.csv')

#plotting the graph for the above task
topTen = harvested_country_meanArea_sorted['Country']
x_axis = np.arange(len(topTen))
plt.bar(x_axis, harvested_country_meanArea_sorted['Mean_area'], align = 'center', alpha = 0.4)
plt.xticks(x_axis, harvested_country_meanArea_sorted['Country'], rotation = 45)
plt.xlabel('Country')
plt.ylabel('Area in hecters')
plt.title('Average Agricultural Area')
plt.show()

#task6
#calculating average across columns
area_mean_series = merged_data.mean(axis = 1).rename('Mean_area')
toBeDropped = list(merged_data.keys())
#dropping columns not needed
toBeDropped.pop(toBeDropped.index('functional crop type'))
#toBeDropped.pop(toBeDropped.index('functional crop id'))
toBeDropped.pop(toBeDropped.index('Country'))
merged_data.drop(toBeDropped, axis = 1, inplace = True)
merged_data['Mean_area'] = area_mean_series

#calculating for C3annual, C3perennial, C4annual, C4perennial, N_fixing in the order of countries occuring in 'topTen' list
C3annual, C3perennial, C4annual, C4perennial, N_fixing = [], [], [], [], []
for country_name in topTen:
	df = merged_data.loc[merged_data['Country'] == country_name, : ].groupby('functional crop type').sum()
	df.reset_index(level=0, inplace=True)
	dict_of_final_data = df.set_index('functional crop type').T.to_dict('list')
	C3annual.append(dict_of_final_data['C3annual'][0] if 'C3annual' in dict_of_final_data.keys() else 0)
	C3perennial.append(dict_of_final_data['C3perennial'][0] if 'C3perennial' in dict_of_final_data.keys() else 0)
	C4annual.append(dict_of_final_data['C4annual'][0] if 'C4annual' in dict_of_final_data.keys() else 0)
	C4perennial.append(dict_of_final_data['C4perennial'][0] if 'C4perennial' in dict_of_final_data.keys() else 0)
	N_fixing.append(dict_of_final_data['N-fixing'][0] if 'N-fixing' in dict_of_final_data.keys() else 0)

#plotting the stacked bar chart for the same using matplotlib
width = 0.5

p1 = plt.bar(x_axis, C3annual, width, color = 'g', alpha = 0.3)
p2 = plt.bar(x_axis, C3perennial, width, color = 'c', alpha = 0.5)
p3 = plt.bar(x_axis, C4annual, width, color = 'y', alpha = 0.6)
p4 = plt.bar(x_axis, C4perennial, width, color = 'r', alpha = 0.7)
p5 = plt.bar(x_axis, N_fixing, width, color = 'k', alpha = 0.4)

plt.ylabel('Area in hecters')
plt.title('Cropland area by functional type and country')
plt.xticks(x_axis, harvested_country_meanArea_sorted['Country'], rotation = 45)
plt.xlabel('Country')
plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('mean_area, C3annual', 'mean_area, C3perennial', 'mean_area, C4annual', 'mean_area, C4perennial', 'mean_area, N_fixing'))
plt.show()

#task7
#creating a copy not to mess with original data
harvested_Data_Bel_Lux = harvested_Data.copy()
#collecting rows for Belgium and luxembourg respectively
harvested_Data_Bel = harvested_Data_Bel_Lux.loc[harvested_Data_Bel_Lux['Country'] == 'Belgium', : ]
harvested_Data_Lux = harvested_Data_Bel_Lux.loc[harvested_Data_Bel_Lux['Country'] == 'Luxembourg', : ]
#harvested_Data_Bel_Lux = harvested_Data_Bel_Lux.loc[harvested_Data_Bel_Lux['Country'] == 'Belgium-Luxembourg', : ]

#sorting the list of items just for visual comparison, not actually needed, to be removed
Bel_crop_list = harvested_Data_Bel['Item'].sort_values().tolist()
Lux_crop_list = harvested_Data_Lux['Item'].sort_values().tolist()
Bel_Lux_crop_list = harvested_Data_Bel_Lux['Item'].sort_values().tolist()


for item in Bel_crop_list:
	if item in Lux_crop_list:
		#if an item is cultivated both in Belgium and Luxembourg after 1999, then it's data is collected
		df1 = harvested_Data_Bel.loc[(harvested_Data_Bel['Country'] == 'Belgium') & (harvested_Data_Bel['Item'] == item), :]
		df2 = harvested_Data_Lux.loc[(harvested_Data_Lux['Country'] == 'Luxembourg') & (harvested_Data_Lux['Item'] == item), :]
		#both rows are appeded and mean is calculated
		appended = df1.append(df2)
		appended_mean = appended.mean(axis = 0)
		year_list = ['Y'+str(year) for year in range(2000,2014)]
		#data from 2000 to 2013 after partition is filled by the mean caculated above for the item cultivated in both coutries!
		for year in year_list:
			harvested_Data_Bel_Lux.loc[(harvested_Data_Bel_Lux['Country'] == 'Belgium-Luxembourg') & (harvested_Data_Bel_Lux['Item'] == item), year] = appended.mean(axis = 0)[year]

harvested_Data_Bel_Lux.to_excel('withThoseMissingDataFrom2000_2013.xlsx')