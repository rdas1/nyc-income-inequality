from flask import Flask, render_template, make_response, request, Response
import folium
import json
import requests
import os
import pandas as pd
from branca.colormap import linear

app = Flask(__name__)

@app.route('/')
def index():

	ny_coords = (40.7128, -74.0060)
	census_tracts = r'census_t.geojson'
	census_income = pd.read_csv('census_income.csv')

	colormap = linear.RdBu_06.scale(
    census_income['2013-2017'].min(),
    census_income['2013-2017'].max())
	print(colormap(31966.2255623417))

	census_income_dict = census_income.set_index('Census Tract')['2013-2017'].to_dict()
	print(census_income_dict[36061016001])
	print(census_income['2013-2017'].max())

	print(census_income[:5])
	#sqf_data = r'sqf_cleaned.csv'
	#sqf_data = pd.read_csv('sqf_cleaned.csv')
	#school_districts = r'untitled.json'

	#stop_and_frisk_file = os.path.join('/Users/rajdas/Downloads/', 'sqf-2018.csv')
	#stop_and_frisk_full_data = pd.read_csv('sqf-2018.csv')

	#school_demographic_data_full = pd.read_csv('nyc_school_demographics.csv')
	#school_demographic_data = school_demographic_data_full[school_demographic_data_full['Year'] == '2018-19']

	#school_demographic_data[['# Black']] = school_demographic_data[['# Black']].apply(pd.to_numeric, errors='coerce')

	#print("pls " + (school_demographic_data[school_demographic_data['Administrative District'] == '01']).to_string())
	#print("pls??")

	#print (sqf_data[:5])

	m = folium.Map(location=ny_coords, tiles="Stamen Toner", zoom_start=13)

	#colormap = linear.YlGn_09.scale(
    #sqf_data.SQF.min(),
    #sqf_data.SQF.max())

	#print(colormap(5.0))

	#sqf_dict = sqf_data.set_index('Precinct')['SQF']

	#print(sqf_dict[0])

	#color_dict = {key: colormap(sqf_dict[key]) for key in sqf_dict.keys()}

	folium.GeoJson(
	    census_tracts,
	    style_function=lambda feature: {
	        'fillColor': colormap(census_income_dict[int(feature['properties']['geoid'])]),
	        #'threshold_scale': [20000, 50000, 100000, 150000],
	        'fill_opacity':0.7,
	        
	        'weight': 1,
	        #'dashArray': '5, 5'
	    }
	).add_to(m)

	folium.LayerControl().add_to(m)

	'''
	folium.GeoJson(
	    census_tracts,
	    style_function=lambda feature: {
	        'fillColor': 'red' if feature['properties']['geoid'] == '36085990100' else '#ffffff',
	        'color': 'gray',
	        'weight': 2,
	        'dashArray': '5, 5'
	    }
	).add_to(m)
	

	folium.LayerControl().add_to(m)
	'''

	'''folium.Choropleth(
	    geo_data=census_tracts,
	    data=census_income,
	    columns=['Census Tract', '2013-2017'],
	    key_on='feature.properties.geoid',
	    fill_color='Reds',
	).add_to(m)'''
	

	'''folium.Choropleth(
	    geo_data=precincts,
	    fill_color='YlOrRd', 
	    fill_opacity=0.7, 
	    line_opacity=0.2,
	    #threshold_scale = [0,0.25,0.5,0.75, 1],
	    data = sqf_data,
	    key_on='feature.properties.precinct',
	    columns = ['Precinct', 'SQF']
	).add_to(m)'''


	'''folium.Choropleth(
	    geo_data=school_districts,
	    fill_color='YlOrRd', 
	    fill_opacity=0.7, 
	    line_opacity=0.2,
	    threshold_scale = [0,0.25,0.5,0.75, 1],
	    data = school_demographic_data,
	    key_on='feature.properties.school_dist',
	    columns = ['Administrative District', '# Black']
	    #legend_name='Immigration to Canada'
	).add_to(m)'''
	
	m.save('templates/map.html')

	response = make_response(render_template("map.html"))
	return response

'''
	folium.Choropleth(
	    geo_data=precincts,
	    data=stop_and_frisk,
	    columns=['STOP_FRISK_ID', 'STOP_LOCATION_PRECINCT'],
	    #key_on='feature.properties.name',
	    fill_color='YlOrRd', 
	    fill_opacity=0.7, 
	    line_opacity=0.2
	    #legend_name='Immigration to Canada'
	).add_to(m)
'''

'''
	folium.Choropleth(
	    geo_data=precincts,
	    data=stop_and_frisk,
	    columns=['STOP_FRISK_ID', 'STOP_LOCATION_PRECINCT'],
	    #key_on='feature.properties.name',
	    fill_color='YlOrRd', 
	    fill_opacity=0.7, 
	    line_opacity=0.2
	    #legend_name='Immigration to Canada'
	).add_to(m)'''


if __name__ == '__main__':
    app.run(debug=True)
