
# coding: utf-8

# import necessary modules

# In[1]:


import vcs # For plots
import vcsaddons # module containing pcoords
import cdms2 # for data
import glob # to list files in directories
import pcmdi_metrics # for special json loader class
import os
import numpy as np
from __future__ import print_function


# ## Work around to visualize plot in Jupyter Notebook
# This class allow use to use vcsaddons plots 

# In[2]:


import tempfile
import base64
class VCSAddonsNotebook(object):
    def __init__(self, x):
        self.x = x
    def _repr_png_(self):
        fnm = tempfile.mktemp()+".png"
        x.png(fnm)
        encoded = base64.b64encode(open(fnm, "rb").read())
        return encoded
    def __call__(self):
        return self


# # Data

# In[3]:


exp = 'historical'
exp = 'amip'
exp = 'picontrol'


# JSON read-in

# In[4]:


# Prepare list of json files

# Location on your computer
json_pth = "/Users/lee1043/Documents/Research/PMP/ParallelCoordinates/JSONs/"
json_files = glob.glob(
            os.path.join(
                json_pth,
                exp,
                "*_2.5x2.5_regrid2_regrid2_metrics_InterModelStat.json"))

#mypath = '/work/gleckler1/processed_data/cmip5clims_metrics_package-'+exp+'/cmec_11022017'
mypath = "/Users/lee1043/Documents/Research/PMP/ParallelCoordinates/JSONs/"+exp
onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))] 
#onlyfiles.remove('rst_2.5x2.5_regrid2_regrid2_metrics.json')
json_files = []
for onlyfile in onlyfiles:
    json_files.append(os.path.join(mypath,onlyfile))
    
#print json_files


# Below loop is for getting units from JSON

# In[5]:


units_list=[]
import json

for json_file in json_files:
    f = open(json_file)
    d = json.loads(f.read())
    f.close()

    try:
        units_list.append(d["RESULTS"]["ACCESS1-0"]["units"])
    except:
        units_list.append('NOT_IN_JSON')
        pass   


# In[6]:


models = sorted(d['RESULTS'].keys(),key=lambda s: s.lower())
print(models)
models.insert(0, models.pop(models.index('median')))
models.insert(1, models.pop(models.index('mean')))
print(models)


# In[7]:


# Read them in via pmp special json class
J = pcmdi_metrics.pcmdi.io.JSONs(json_files)

# Retrieve data we need for plot
# Annual mean RMS (XYT dimensions)
# All models and all variables
rms_xyt = J(statistic=["rms_xy"],season=["ann"],region="global",model=models)(squeeze=1)
rms_xyt_djf = J(statistic=["rms_xy"],season=["djf"],region="global",model=models)(squeeze=1)
rms_xyt_mam = J(statistic=["rms_xy"],season=["mam"],region="global",model=models)(squeeze=1)
rms_xyt_jja = J(statistic=["rms_xy"],season=["jja"],region="global",model=models)(squeeze=1)
rms_xyt_son = J(statistic=["rms_xy"],season=["son"],region="global",model=models)(squeeze=1)


# Let's take a look at the array generated
# Note the axis are strings of varialbes used and models
# The order of the axes is the order on the plot

# In[8]:


# Ok now let's create a VCS pcoord graphic method

# initialize a canvas
x = vcs.init(geometry=(1200,800),bg=True)


# # Preparing the plot
# ## Data
# 'id' is used for variable in plot the JSON class returns var as "pmp", here "RMS" is more appropriate
# 
# 'title' is used to draw the plot title (location/font controlled by template)
# 
# ## Template
# The template section prepares where data will be rendered on plot, and the fonts used
# 
# fonts are controlled via textorientation and texttable VCS primary objects
# 
# Here we need to angle a bit the xlabels (45 degrees)
# 
# We also want to turn off the boxes around the legend and the data area.

# In[9]:


# Prepare the graphics
# Set variable name
rms_xyt.id = "RMS"
# Set units of each variables on axis
# This is a trick to have units listed on plot
rms_xyt.getAxis(-2).units = units_list
# Sets title on the variable
rms_xyt.title = "Annual Mean Absolute Error"

# Preprare the canvas areas
t = vcs.createtemplate()
# Create a text orientation object for xlabels
to = x.createtextorientation()
to.angle = -75
to.halign = "right"
# Tell template to use this orientation for x labels
t.xlabel1.textorientation = to.name

# Define area where plot will be drawn in x direction
t.reset('x',0.05,0.9,t.data.x1,t.data.x2)
ln = vcs.createline()

# Turn off box around legend
ln.color = [[0,0,0,0]]
t.legend.line = ln
# turn off box around data area
t.box1.priority = 0

# Define box where legend will be drawn
t.legend.x1 = .91
t.legend.x2 = .99
# use x/y of data drawn for legend height
t.legend.y1 = 0.1
t.legend.y2 = 0.9


# ## Graphic method
# Set graphic method as parallel coordinate plot

# In[10]:


def set_pcoord_gm(x):

    gm = vcsaddons.createparallelcoordinates(x=x)

    # Control line colors
    gm.colormap = 'rainbow'
    gm.linecolors = vcs.getcolors(list(np.arange(len(models))), range(16,240))
    gm.linewidths=[5.,5.,1.]

    # Control markers
    gm.markersizes = [0,0,1.2]
    gm.markertypes = [
        'cross', 'cross', 
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',
        'star','diamond_fill','triangle_up_fill','triangle_down_fill','square_fill',   
        'dot',
        ]

    return(gm)


# ## Generate parallel plot for annual mean

# In[11]:


# Plot with default values of graphic method
x.clear()
vcs.utils.defaultColorsRange = range(16,240)
x.setcolormap("rainbow")

gm = set_pcoord_gm(x)
gm.plot(rms_xyt, template=t, bg=True)

x.png('Parallel_Plot_'+exp+'_ann.png')


# ## Loop for generating parallel plots for seasons

# In[12]:


for season in ['djf','mam','jja','son']:
    x.clear()
    
    if season == 'djf':
        d = rms_xyt_djf
    elif season == 'mam':
        d = rms_xyt_mam
    elif season == 'jja':
        d = rms_xyt_jja
    elif season == 'son':
        d = rms_xyt_son
        
    # Set variable name
    d.id = "RMS"
    # Set units of each variables on axis
    # This is a trick to have units listed on plot
    d.getAxis(-2).units = units_list
    # Sets title on the variable
    d.title = season.upper()+" Mean Absolute Error, "+exp.upper()

    gm = set_pcoord_gm(x)
    gm.plot(d, template=t, bg=True)
    x.png('Parallel_Plot_'+exp+'_'+season+'.png')

