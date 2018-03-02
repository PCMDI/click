from __future__ import print_function
import os
import sys
import MV2
import vcs
import numpy
import pcmdi_metrics
import pcmdi_metrics.graphics.portraits
import cdms2
from vcs.utils import meshToCoords, mapPng
import genutil
import shutil

#pathout = '/work/gleckler1/www/pptest/'
pathout = '/work/gleckler1/www/portraits/'


levs = [-1e+20, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1e+20]
cols = [144, 145, 146, 147, 'lightgreen', 'green', 'green', 'darkgreen', 152, 153, 154, 155]
P = pcmdi_metrics.graphics.portraits.Portrait()
P1 = pcmdi_metrics.graphics.portraits.Portrait()

P.PLOT_SETTINGS.levels = levs
P1.PLOT_SETTINGS.levels = levs

bg = True
geometry = (2400,1600)
geometry = (1200,800)
x = vcs.init(geometry=geometry, bg=bg)

f=cdms2.open("portrait.nc")

def prep_read(var):
    axes = []
    for ax in var.getAxisList():
        ax.id = ax.full_id
        axes.append(ax)
    var.setAxisList(axes)
    return var

x.scriptrun(
    os.path.join(
        sys.prefix, "share", "pmp", "graphics", 'vcs', 'portraits.scr'))

P.PLOT_SETTINGS.colormap = 'bl_rd_12'
P.PLOT_SETTINGS.missing_color = 'white'  # 240
P.PLOT_SETTINGS.tictable.font = 6

va = .01
P.PLOT_SETTINGS.x1 = 0.05  # .1
P.PLOT_SETTINGS.x2 = .85  # .85
P.PLOT_SETTINGS.y1 = .6 + va
P.PLOT_SETTINGS.y2 = .9 + va

P.PLOT_SETTINGS.xtic2.y1 = P.PLOT_SETTINGS.y1
P.PLOT_SETTINGS.xtic2.y2 = P.PLOT_SETTINGS.y2
P.PLOT_SETTINGS.ytic2.x1 = P.PLOT_SETTINGS.x1
P.PLOT_SETTINGS.ytic2.x2 = P.PLOT_SETTINGS.x2

P.PLOT_SETTINGS.fillareacolors = cols

out1 = prep_read(f("ou1"))
outo21 = prep_read(f("outo21"))

targets = out1.ravel().tolist()
mesh1, template1, meshfill1 = P.plot(out1, x=x, multiple=1.2, bg=bg)
mesh1b, template1b, meshfill1b = P.plot(outo21, x=x, multiple=2.2, bg=bg)

out2 = prep_read(f("ou2"))
outo22 = prep_read(f("outo22"))

P1.PLOT_SETTINGS.colormap = 'bl_rd_12'
# P1.PLOT_SETTINGS.levels = levs  #P.PLOT_SETTINGS.levels   #[-1.e20, -.5, -.4, -.3, -.2, -.1, 0., .1, .2, .3, .4, .5, 1.e20]
# P1.PLOT_SETTINGS.levels = [-1.e20, -.25, -.2, -.15, -.1,-.05, 0., .05, .1, .15, .2, .25, 1.e20]
# P.PLOT_SETTINGS.levels = [-1.e20, .1, .2, .3, .4, .5, .6, .7, .8, .9,1., 1.e20]

# cols = vcs.getcolors(P.PLOT_SETTINGS.levels, range(144, 156), split=1)
P1.PLOT_SETTINGS.tictable.font = 6

P1.PLOT_SETTINGS.x1 = 0.05  # .1
P1.PLOT_SETTINGS.x2 = .85  # .85
P1.PLOT_SETTINGS.y1 = .15
P1.PLOT_SETTINGS.y2 = .45

P1.PLOT_SETTINGS.xtic2.y1 = P1.PLOT_SETTINGS.y1
P1.PLOT_SETTINGS.xtic2.y2 = P1.PLOT_SETTINGS.y2
P1.PLOT_SETTINGS.ytic2.x1 = P1.PLOT_SETTINGS.x1
P1.PLOT_SETTINGS.ytic2.x2 = P1.PLOT_SETTINGS.x2

P1.PLOT_SETTINGS.fillareacolors = cols
P1.PLOT_SETTINGS.missing_color = 240

mesh2, template2, meshfill2 = P1.plot(out2, x=x, multiple=1.2, bg=bg)
mesh2b, template2b, meshfill2b = P1.plot(outo22, x=x, multiple=2.2, bg=bg)

header = x.createtext()
header.To.height = 24
header.To.halign = "center"
header.To.valign = "top"
header.x = .4
header.y = .95

tit = "Ratio of Mod CBF PC1 std to obs PC1 std with 20CR vs ERA20C"   #_v3.1b_vs_v3.4b late 20th"
header.string = [tit]

x.plot(header, bg=bg)


x.png(pathout + 'clickable_variability.png')

clickname = pathout + "clickable_variability.png"
clickname_np = "clickable_variability.png"

areas1 = meshToCoords(mesh1,template1,[meshfill1.datawc_x1,meshfill1.datawc_x2,meshfill1.datawc_y1,meshfill1.datawc_y2],png=clickname)
areas1b = meshToCoords(mesh1b,template1b,[meshfill1b.datawc_x1,meshfill1b.datawc_x2,meshfill1b.datawc_y1,meshfill1b.datawc_y2],png=clickname)
areas2 = meshToCoords(mesh2,template2,[meshfill2.datawc_x1,meshfill2.datawc_x2,meshfill2.datawc_y1,meshfill2.datawc_y2],png=clickname)
areas2b = meshToCoords(mesh2b,template2b,[meshfill2b.datawc_x1,meshfill2b.datawc_x2,meshfill2b.datawc_y1,meshfill2b.datawc_y2],png=clickname)

#maps_template = genutil.StringConstructor("/work/lee1043/cdat/pmp/variability_mode/scripts_consistency_test_b/SAM_redo_with_late_20C_OBS/result_v3.1b_3/analysis/5panel_eofs_pcs/%(MODE)/Panel7_%(MODE)_%(SEASON)_%(MODEL)_%(REALIZATION).png")
maps_template = genutil.StringConstructor("variability/plots/%(MODE)/Panel7_%(MODE)_%(SEASON)_%(MODEL)_%(REALIZATION).png")



def createTargets(data,maps_template):
    print(data.getAxis(-1).id)
    print(data.getAxis(-2).id)
    outs = []
    missing = []
    tips = []
    flt = data.ravel()
    indx = 0
    for a in data.getAxis(-2).id.split("___"):
        sp = a.split("_")
        maps_template.MODE = sp[0]
        maps_template.SEASON = sp[1].upper()
        for b in data.getAxis(-1).id.split("___"):
            mod = b.split()[1]
            sp = mod.split("_")
            maps_template.MODEL = sp[0]
            r = sp[1]
            if len(r)<=2:
                r = "%si1p1" % r
            maps_template.REALIZATION=r
            fnm = maps_template()
#           pth = '/work/gleckler1/www/pptest/'
            pth = '/work/gleckler1/www/portraits/'

#           print('hi -----', maps_template.MODEL)
            if not os.path.exists(pth + fnm):
                maps_template.MODEL = sp[0].lower()
                fnm = maps_template()
            if not os.path.exists(pth + fnm):
                maps_template.MODEL = sp[0].upper()
                fnm = maps_template()
#           print('here is  fnm ', fnm)
            if not os.path.exists(pth + fnm):
                fnm = "/crp/missing.png"
            outs.append(fnm)
#           outs.append(os.path.join("png",os.path.basename(fnm)))
            if os.path.exists(pth + fnm + 'crap'):
                onm = os.path.join(pth + fnm)   #,outs[-1])
#               onm = os.path.join("HTML",outs[-1])
#               print type(onm)
                if not os.path.exists(pth + onm):
                    shutil.copy(pth+fnm,onm)
            else:
                onm = "png/missing.png"
                missing.append(maps_template(MODEL=sp[0]))
            tips.append("Model: %s<br>Realization: %s<br>Mode: %s<br>Season: %s<br>Value: %.3g<div id='thumbnail'><img src='%s' width=200></div>" % (maps_template.MODEL,r,maps_template.MODE,maps_template.SEASON,flt[indx],outs[-1]))
            indx += 1
    return outs, tips, missing

targets1, tooltips1, missing1 = createTargets(out1,maps_template)
targets1b, tooltips1b, missing1b = createTargets(outo21,maps_template)
targets2, tooltips2, missing2 = createTargets(out2,maps_template)
targets2b, tooltips2b, missing2b = createTargets(outo22,maps_template)

areas = numpy.concatenate((areas1,areas1b,areas2,areas2b))
targets = numpy.concatenate((targets1,targets1b,targets2,targets2b))
tooltips = numpy.concatenate((tooltips1,tooltips1b,tooltips2,tooltips2b))

#pathout = '/work/gleckler1/www/pptest/'
pathout = '/work/gleckler1/www/portraits/'
#pathout = ''
img = mapPng(clickname_np,areas,targets,tooltips,width=geometry[0],height=geometry[1])
#map_element = vcs.utils.mapPng(click_name + ".png",click_areas,targets,tooltips,width=geo["width"],height=geo["height"])

with open(pathout +  "clickable_variability.html","w") as f:
    f.write("<html><head>")
    f.write("<script type='text/javascript' src='mapper.js'></script>")
    f.write("<script type='text/javascript' src='cvi_tip_lib.js'></script>")
    f.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>')
    f.write('<link rel="stylesheet" type="text/css" href="tooltip.css" />')
    f.write("</head><body>")
    f.write("<h2><center>CMIP5 historical simulations compared to reference data (1900-2005)</center></h2>")
    f.write("<h2><center>Extra tropical modes of variability</center></h2>")
    f.write(img)
    #f.write("$('area').hover(function(){$(this).css('border','5px');},function(){$(this).css('border','0px');});")
    f.write("<h4> The plot above summarizes the ratio of simulated to observed variability for a selection of extratropical modes and seasons.  Results are shown for individual realizations from the CMIP5 database of historical simulations.  The upper left triangle of each square show results with data from the 20CR reanalysis as the reference dataset, whereas the lower triangle is based on data from ERA20C reanalysis.  In each case, the model anomaly time series is projected onto the leading EOF of the reference dataset which provides a Common Basis Function (CBF) for comparing models with the reference data.   Diagnostics for each case can be reached by clicking on the triangles in the plot, and show: a) andb) the leading EOF of each reference dataset, c) the model pattern estimated from projecting the anomaly time series on the reference CBF pattern, d-f) EOFs 1-3 from the model and g) PC time series showing results from the model.  Results are from Lee et al. (in review). </h4>")
    f.write("</body></head></html>")
print("Done open: clickable_map.html")
 
os.popen('chmod -R 775 %s/*' % pathout).readlines()
