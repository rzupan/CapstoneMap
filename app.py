from flask import Flask, render_template, request
import pandas as pd
import folium
import dill
import branca
import requests

app = Flask(__name__)
#app.config['EXPLAIN_TEMPLATE_LOADING'] = True

outL = dill.load(open('outlierCrash.pkd','rb'))

lat = []
lon = []
val = []

for item in outL:
    lat.append(item[0])
    lon.append(item[1])
    val.append(outL[item])
    
outLDF = pd.DataFrame({'latitude': lat, 'longitude': lon, 'count':val})

def geocode(address):
    params = { 'format'        :'json', 
               'addressdetails': 1, 
               'q'             : address}
    headers = { 'user-agent'   : 'TDI' }   #  Need to supply a user agent other than the default provided 
                                           #  by requests for the API to accept the query.
    return requests.get('http://nominatim.openstreetmap.org/search', params=params, headers=headers)

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/Graph', methods=['GET', 'POST'])
def show_Graph():
    
    response = geocode(request.form['adr'])
    if response.json():
            
        us_map = folium.Map(location=[response.json()[0]['lat'], response.json()[0]['lon']], zoom_start=13)
        
        folium.Marker([response.json()[0]['lat'], response.json()[0]['lon']], tooltip="<i>"+request.form['adr']+"</i>").add_to(us_map)
        
        cmap = branca.colormap.LinearColormap(colors=['blue','red'], vmin=42,vmax=853)
        cmap = cmap.to_step(index=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900])
        cmap.caption = 'Number of Car Crashes'
        cmap.add_to(us_map)
        
        for lat,lon,count in zip(outLDF['latitude'],outLDF['longitude'],outLDF['count']):
            folium.CircleMarker(
                [lat,lon],
                radius = .06*count,
                popup = ('Location: ' + str(lat) + ', ' + str(lon) + '<br>'
                         'Crashes: ' + str(count)
                        ),
                color='b',
                fill_color=cmap(count),
                fill=True,
                fill_opacity=1
                ).add_to(us_map)
        return us_map._repr_html_()
    
    else:
        
        return render_template('mistake.html')


if __name__ == "__main__":
    app.run(port=33507)
