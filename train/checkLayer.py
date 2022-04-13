import os,glob
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geographiclib.geodesic import Geodesic
plt.ion()

def plotLocalBase(minlon, maxlon, minlat, maxlat,resolution='c',coastline=None,figwidth=None,ax=None,
             dlat=5.0, dlon=5.0, topo=None, projection='merc',plateBoundary=True):
    coastlineData = '/home/ayu/SubdInv/models/ne_10m_coastline/ne_10m_coastline'
    physioData = '/home/ayu/PackagesDev/Triforce/physio/physio' #https://water.usgs.gov/GIS/dsdl/physio_shp.zip

    ''' Plot base map with country, state boundaries '''
    minlon,maxlon = minlon-360*(minlon>180),maxlon-360*(maxlon>180)
    rsphere = (6378137.00,6356752.3142)
    lon_centre, lat_centre = (minlon+maxlon)/2, (minlat+maxlat)/2
    distEW = Geodesic.WGS84.Inverse(minlat, minlon, minlat, maxlon)['s12']
    distNS = Geodesic.WGS84.Inverse(minlat, minlon, maxlat, minlon)['s12']
    
    if ax is None:
        figwidth = 6.0 if figwidth is None else figwidth
    else:
        figwidth = None

    if figwidth is not None:
        fig = plt.figure(figsize=[figwidth,figwidth/distEW*distNS])
    elif ax is not None:
        plt.sca(ax)
        fig = plt.gcf()
    else:
        print('Maybe something goes wrong in plotBase, please check!')
        fig = plt.figure()

    if projection == 'lcc':
        m = Basemap(width=distEW, height=distNS, rsphere=rsphere, resolution=resolution, projection='lcc', 
            lat_1=minlat, lat_2=maxlat, lon_0=lon_centre, lat_0=lat_centre)
    elif projection in ['merc','mill']:
        m = Basemap(projection=projection, llcrnrlat=minlat, urcrnrlat=maxlat, 
                    llcrnrlon=minlon, urcrnrlon=maxlon,
                    lat_ts=(minlat+maxlat)/2,resolution=resolution)
    else:
        raise ValueError('Not supported yet.')

    if plateBoundary:
        m.readshapefile('/home/ayu/Projects/Cascadia/Models/Plates/PB2002_boundaries',
                    'PB2002_boundaries',linewidth=2.0,color='orange')
    
    if topo is None:
        if coastline is not None:
            m.readshapefile(coastline,'coastline',linewidth=0.5)
        else:
            m.drawcoastlines()
        m.drawcountries(linewidth=1)
        m.drawparallels(np.arange(minlat,maxlat,dlat), labels=[1,0,0,0])
        m.drawmeridians(np.arange(minlon,maxlon,dlon), labels=[0,0,0,1])
        m.drawstates(color='k', linewidth=0.5,linestyle='solid')
        m.readshapefile(physioData,'physio',linewidth=0.25)
        return (fig,m)
    elif topo is True:
        m.etopo(scale=1.0)
        m.drawparallels(np.arange(minlat,maxlat,dlat), labels=[1,0,0,0])
        m.drawmeridians(np.arange(minlon,maxlon,dlon), labels=[0,0,0,1])
        return (fig,m)
    else:
        raise ValueError('Plot with topo data has not been done yet!')

X,Y,Z = [],[],[]
for fname in glob.glob('vs_out/*.txt'):
    pid = os.path.basename(fname)[:-4]
    lat,lon = map(float,pid.split('_'))
    zdeps,vs,_,_ = np.loadtxt(fname).T
    X.append(lon);Y.append(lat);Z.append(np.interp(40,zdeps,vs))

minlon,maxlon,minlat,maxlat = 70,135,10,55
fig,m = plotLocalBase(minlon,maxlon,minlat,maxlat,dlat=20,dlon=30,resolution='l',plateBoundary=False)
m.scatter(X,Y,s=30,c=Z,latlon=True,cmap='rainbow')




