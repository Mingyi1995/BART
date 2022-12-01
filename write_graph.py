#!/usr/bin/env python
# coding: utf-8

# In[27]:


import numpy as np
import pandas as pd
import geopandas as gpd
import fiona
from geopy.distance import distance,geodesic
import networkx as nx
pd.set_option('display.max_columns', None)
warnings.filterwarnings('ignore')


# In[6]:


yellow = ['ANTC','PCTR','PITT','NCON','CONC','PHIL','WCRK','LAFY',
        'ORIN','ROCK','MCAR','19TH','12TH','WOAK','EMBR',
        'MONT','POWL','CIVC','16TH','24TH','GLEN','BALB',
        'DALY','COLM','SSAN','SBRN','MLBR','SFIA']
orange = ['RICH','DELN','PLZA','NBRK','DBRK','ASHB','MCAR',
          '19TH','12TH','LAKE','FTVL','COLS','SANL','BAYF',
          'HAYW','SHAY','UCTY','FRMT','WARM','MLPT','BERY']
red = ['RICH','DELN','PLZA','NBRK','DBRK','ASHB','MCAR',
          '19TH','12TH','WOAK','EMBR',
        'MONT','POWL','CIVC','16TH','24TH','GLEN','BALB',
        'DALY','COLM','SSAN','SBRN','MLBR','SFIA']
blue = ['DUBL','WDUB','CAST','BAYF','SANL','COLS','FTVL',
        'LAKE','WOAK','EMBR','MONT','POWL','CIVC','16TH',
        '24TH','GLEN','BALB','DALY']
green = ['BERY','MLPT','WARM','FRMT','UCTY','SHAY','HAYW',
         'BAYF','SANL','COLS','FTVL',
        'LAKE','WOAK','EMBR','MONT','POWL','CIVC','16TH',
        '24TH','GLEN','BALB','DALY']
grey = ['COLS','OAKL']


# In[7]:




gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
gdf = gpd.read_file('doc.kml', driver='KML')

station_name = pd.read_excel('Station_Names.xls')

station_latlon = dict(zip(gdf['Name'],zip(gdf.geometry.y,gdf.geometry.x)))

code_name = {'12TH':'12th St/Oakland City Center',
 '16TH':'16th St/Mission',
 '19TH':'19th St/Oakland',
 '24TH':'24th St/Mission',
 'ANTC':'Antioch',
 'ASHB':'Ashby',
 'BALB':'Balboa Park',
 'BAYF':'Bay Fair',
 'BERY':'Berryessa/North San Jose',
 'CAST':'Castro Valley',
 'CIVC':'Civic Center/UN Plaza',
 'COLM':'Colma',
 'COLS':'Coliseum/Airport Connector',
 'CONC':'Concord',
 'DALY':'Daly City',
 'DBRK':'Downtown Berkeley',
 'DELN':'El Cerrito del Norte',
 'DUBL':'Dublin/Pleasanton',
 'EMBR':'Embarcadero',
 'FRMT':'Fremont',
 'FTVL':'Fruitvale',
 'GLEN':'Glen Park',
 'HAYW':'Hayward',
 'LAFY':'Lafayette',
 'LAKE':'Lake Merritt',
 'MCAR':'MacArthur',
 'MLBR':'Millbrae',
 'MLPT':'Milpitas',
 'MONT':'Montgomery St',
 'NBRK':'North Berkeley',
 'NCON':'North Concord/Martinez',
 'OAKL':'Oakland International Airport',
 'ORIN':'Orinda',
 'PCTR':'Pittsburg Center',
 'PHIL':'Pleasant Hill/Contra Costa Centre',
 'PITT':'Pittsburg/Bay Point',
 'PLZA':'El Cerrito Plaza',
 'POWL':'Powell St',
 'RICH':'Richmond',
 'ROCK':'Rockridge',
 'SANL':'San Leandro',
 'SBRN':'San Bruno',
 'SFIA':'San Francisco International Airport',
 'SHAY':'South Hayward',
 'SSAN':'South San Francisco',
 'UCTY':'Union City',
 'WARM':'Warm Springs/South Fremont',
 'WCRK':'Walnut Creek',
 'WDUB':'West Dublin/Pleasanton',
 'WOAK':'West Oakland'}


# In[8]:


G = nx.Graph()
G.add_nodes_from(set(yellow+orange+red+blue+green+grey))
for line in [yellow+orange+red+blue+green+grey]:   
    for i,stat in enumerate(line):
        if i < len(line)-1:
            G.add_weighted_edges_from([(line[i],line[i+1],
                                        geodesic(station_latlon[code_name[line[i]]],
                                                 station_latlon[code_name[line[i+1]]]).miles)])
            
nx.write_gpickle(G, 'graph.pickle')


# In[25]:


o_list = []
d_list = []
dist = []
for o in list(G.nodes):
    for d in list(G.nodes):
        o_list += [o]
        d_list += [d]
        dist += [geodesic(station_latlon[code_name[o]],
                          station_latlon[code_name[d]]).miles]
dist_df = pd.DataFrame()
dist_df['o'] = o_list
dist_df['d'] = d_list
dist_df['dist'] = dist
dist_df.to_csv('nodes_dist.csv',index=False)


# In[ ]:




