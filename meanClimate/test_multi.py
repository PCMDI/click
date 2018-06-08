import glob
import json
import os
import sys
import pcmdi_metrics
import genutil
import numpy

parser = pcmdi_metrics.pcmdi.pmp_parser.PMPParser()

parser.use("--exp")
parser.use("--results_dir")

parser.add_argument("--data_path", help="input data path", default="data/v1.1")
parser.add_argument("--statistic", help="statistic to use",
                    default="rms_devam_xy")
parser.add_argument("--title", help="title for plot")
parser.add_argument("--files_glob_pattern", help="glob pattern to select correct files in input directory",
                    default="*.json")
parser.add_argument("--bad", help="list of bad models", default=[])
parser.add_argument("--seasons",help="seasons to process", default=['djf', 'mam', 'jja', 'son'])
args = parser.get_parameter()

exp = args.exp
injpath = args.data_path
pathout = args.results_dir
tit = args.title
stat = args.stat
bad_models = args.bad
seasons = args.seasons

head1 = 'CMIP5 ' + exp.upper() + ' simulations (1981-2005 climatology)'

head2 = 'Relative errors (statistics normalized by median error)'

#######################################################

print "looking in:", injpath
json_files = glob.glob(
    os.path.join(
        injpath,
        args.files_glob_pattern))

print "We are looking at {:d} Json Files:".format(len(json_files))
print " ".join(json_files)

possible_jsons = {}
for f in json_files:
    J = pcmdi_metrics.pcmdi.io.JSONs([f, ])
    for v in J.getAxis("variable")[:]:
        v = str(v)
        if not v in possible_jsons:
            possible_jsons[v] = {}
        possible_jsons[v][f] = J.getAxis("model")

J = pcmdi_metrics.pcmdi.io.JSONs(json_files)

models = sorted(J.getAxis("model")[:])


print "original models:", models
print "We will be manually excluding:", bad_models
for m in bad_models:
    print" bad at:", models.index(m)
    models.pop(models.index(m))

variables = sorted(J.getAxis("variable")[:])
print "We read in {:d} models: {}:".format(len(models), models)
print "We read in {:d} variables: {}:".format(len(variables), variables)


#w = sys.stdin.readline()


rms_xy = J(model=models, statistic=[stat], region="global")(squeeze=1)

if stat == 'rms_xyt':
    rms_xy = J(statistic=["rms_xyt"], region="global")(squeeze=1)

median = genutil.statistics.median(rms_xy, axis=1)[0]

# match  shapes
rms_xy, median = genutil.grower(rms_xy, median)

# Loose info on median
median = median.filled()
# normalize
rms_xy = (rms_xy-median) / median

######## PLOTTING ###########################################################################
# VCS Canvas
import vcs
x = vcs.init(bg=True, geometry=(1200, 800))  # (800,800)
# Load our "pretty" colormap
x.scriptrun(
    os.path.join(
        sys.prefix,
        "share",
        "pmp",
        "graphics",
        'vcs',
        'portraits.scr'))
x.setcolormap("bl_rd_12")

import pcmdi_metrics.graphics.portraits
P = pcmdi_metrics.graphics.portraits.Portrait()

execfile('vcs_details.py')

# P.PLOT_SETTINGS.colorm
# CHANGE FROM UNICODE TO BYTE STRINGS
yax = [s.encode('utf-8')+"  " for s in models]

# CHANGE VARIABLE NAMES

var_full_dic = {'pr': 'Precipitation'}

var_fullname = [var_full_dic.get(v, v)+"   " for v in variables]

# Preprocessing step to "decorate" the axes on our target variable

P.decorate(rms_xy, var_fullname, yax)


header = x.createtext()
header.To.height = 24
header.To.halign = "center"
header.To.valign = "top"
header.x = .55
header.y = .85

#tit =  'TESTING 123 ...'
#header.string = [tit]
#x.plot(header, bg=1)

# SAVE PLOT
# x.png(pathout + 'crap')  # + '_' + scale)

if stat != 'rms_xyt':
    mesh, template, meshfill = P.plot(rms_xy[..., 0], x=x)
if stat == 'rms_xyt':
    mesh, template, meshfill = P.plot(rms_xy, x=x)


#mesh, template, meshfill = P.plot(rms_xy[...,0:4],x=x,multiple=multi)

click_name = 'roadmap_' + exp + '_' + stat

x.png(os.path.join(pathout, click_name + ".png"))

# Creates clickable polygons numpy arrays
click_areas = vcs.utils.meshToPngCoords(mesh, template, [
                                     meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=pathout + click_name + ".png")

import genutil

# This is a template for where the target files should be
#targets_template = genutil.StringConstructor("plots/historical/clim/%(variable)/%(variable).%(model)_%(season).png")
#targets_template = genutil.StringConstructor("plots/cmip5/' + exp + '/%(variable)/%(variable).%(model)_%(season).png")

if exp == 'amip':
    targets_template = genutil.StringConstructor(
        "plots/cmip5/amip/%(stat)/%(variable)/%(variable).%(model)_%(season).png")
if exp == 'historical':
    targets_template = genutil.StringConstructor(
        "plots/cmip5/historical/%(stat)/%(variable)/%(variable).%(model)_%(season).png")

# function to create list of target files for each clickable cell
# adapt this to your needs, html files here will not exist


def createHtml(target, json_file, exp, stat, sanitize_json=True):
    with open(json_file) as f:
        jsn = json.load(f)
    fname = "{}_{}_{}.html".format(
        target.variable, target.model, target.season)
    if not os.path.exists(os.path.join(pathout, "htmls", "cmip5")):
        os.makedirs(os.path.join(pathout, "htmls", "cmip5"))
    if not os.path.exists(os.path.join(pathout, "htmls", "cmip5", exp)):
        os.makedirs(os.path.join(pathout, "htmls", "cmip5", exp))
    if not os.path.exists(os.path.join(pathout, "htmls", "cmip5", exp, stat)):
        os.makedirs(os.path.join(pathout, "htmls", "cmip5", exp, stat))

    if sanitize_json:
        r = jsn["RESULTS"]
        for k in r.keys():
            if not k.lower().strip() == target.model.lower().strip():
                del(r[k])
#       print "After sanitize:",r.keys()
        mod = r.keys()[0]
        jsn["RESULTS"] = r

        json_file = os.path.join(
            pathout, "htmls", "cmip5", exp, stat, mod + '_' + os.path.basename(json_file))
        with open(json_file, "w") as f:
            #       json.dump(jsn, open(f, json_file,"wb"), sort_keys=True, indent=4, separators=( ',', ': '))
            json.dump(jsn, f, sort_keys=True, indent=4, separators=(',', ': '))
#   print "NEW JSON FILE:",json_file

    targ = '../../../../' + target()
    fname2 = os.path.join(pathout, "htmls", "cmip5", exp,
                          stat, fname)  # PJG add exp and stat
    with open(fname2, "w") as f:
        print>>f, "<html><head></head><body>"
#       print>>f,"<h1>TITLE HERE</h1>"
#       print>>f,"<h2>Model:{}<br>Variable: {}<br>Season {}".format(target.model,target.variable,target.seasonj
        print>>f, "<a href='{}'>Return to roadmap".format(
            os.path.join("..", "..", "..", "../", click_name + '.html'))
        print>>f, "<div><img  width = '100' height = '100' src='{}'></div>".format(
            os.path.join("..", "..", "..", "..", click_name + ".png"))
        print>>f, "<div><center><img src='{}'></center></div></a>".format(
            os.path.join("..", "..", "..", "../", target()))
#       print>>f,"<h3>Additional statistics</h3>"
        print>>f, "<a href='{}'><h3><center>Detailed statistics and provenance</center></h3></a>".format(
            './' + os.path.basename(json_file))

#       print>>f,"<h3>Simulation</h3>"
#       print>>f,jsn["RESULTS"][target.model]["SimulationDescription"]
#       print>>f,"<h3>Provenance</h3>"
#       print>>f,jsn["provenance"]
# print>>f,"<h3>Discalaimer</h3>"
#       print>>f,"<br>"
#       print>>f,jsn["DISCLAIMER"]
        print>>f, "</body>"
        print>>f, "</html>"
    return os.path.join("htmls", "cmip5", exp, stat, fname)


def createTargets(data, targets_template, season, exp, stat):
    # Axes have been "decorated" via P.decorate()
    outs = []  # list of target html files
    tips = []  # list of tooltips
    indx = 0
    flt = data.ravel()
    print "MAX:", flt.max()
    print "MIN:", flt.min()
    # Y axis
    targets_template.season = season
    if stat == 'rms_xy':
        clm = 'clim'
    if stat == 'rms_devzm_xy':
        clm = 'climmzm'
    if stat == 'rms_devam_xy':
        clm = 'climmtm'

    targets_template.stat = clm
    for a in data.getAxis(0).id.split("___"):
        a = a.strip()
        if a in var_full_dic.values():
            for k in var_full_dic.keys():
                if var_full_dic[k] == a:
                    targets_template.variable = k
                    break
        else:
            targets_template.variable = a
        # X axis
        for b in data.getAxis(-1).id.split("___"):
            b = b.strip()
            targets_template.model = b
            fnm = targets_template()
            # Here we test if
            tipsString = "Model: %s<br>Season: %s<br>Variable: %s<br>Value: %.3g<div id='thumbnail'><img src='%%s' width=200></div>" % (
                b, season, a, flt[indx])
            if numpy.ma.is_masked(flt[indx]):
                outs.append("#")
                img = "no_data.png"
            elif os.path.exists(os.path.join(pathout, fnm)):  # png exists
                for k, v in possible_jsons[targets_template.variable].iteritems():
                    if b in v:
                        break
                outs.append(createHtml(targets_template, k, exp, stat, True))
                img = fnm
            else:
                outs.append("#")     # NEEDS TO BE UNCOMMENTED
                img = "missing.png"  # NEEDS TO BE UNCOMMENTED

            tips.append(tipsString % img)
            indx += 1
#       print 'stop in createTargets'
#       w = sys.stdin.readline()
    return outs, tips

if stat == 'rms_xy':
    zrange = range(4)
if stat in ['rms_devam_xy', 'rms_devzm_xy']:
    zrange = [0, 2]  # ... with + 1 below yields 1(DJF) and 3(JJA)


for i, ss in enumerate(zrange):
    if stat in ['rms_devam_xy', 'rms_devzm_xy']:
        multi = i + 1.2
    if stat == 'rms_xy':
        multi = i + 1.4
    mesh, template, meshfill = P.plot(rms_xy[..., i+1], x=x, multiple=multi)
    x.png(os.path.join(pathout, click_name + ".png"))
    click_areas1 = vcs.utils.meshToPngCoords(mesh, template, [
                                          meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=pathout + click_name + ".png")

    it = i
    if stat in ['rms_devam_xy', 'rms_devzm_xy'] and i == 1:
        it = 2
    targets1, tooltips1 = createTargets(
        rms_xy[..., it+1], targets_template, seasons[it+1], exp, stat)
    if i == 0:
        click_areas = click_areas1
        targets = targets1
        tooltips = tooltips1
    else:
        targets = numpy.concatenate((targets, targets1))
        tooltips = numpy.concatenate((tooltips, tooltips1))
        click_areas = numpy.concatenate((click_areas, click_areas1))

geo = x.geometry()
# create the html map element
map_element = vcs.utils.mapPng(click_name + ".png", click_areas,
                               targets, tooltips, width=geo["width"], height=geo["height"])
#map_element = vcs.utils.mapPng("clickable.png",click_areas,targets,tooltips,width=800,height=1200)


# In[14]:

# write the html
share_pth = os.path.join(sys.prefix, "share", "vcs")
share_pth = "."  # pathout
with open(os.path.join(pathout, click_name + ".html"), "w") as f:
    f.write("<html><head>")
    f.write("<script type='text/javascript' src='%s/mapper.js'></script>" % share_pth)
    f.write(
        "<script type='text/javascript' src='%s/cvi_tip_lib.js'></script>" % share_pth)
    f.write('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>')
    f.write(
        '<link rel="stylesheet" type="text/css" href="%s/tooltip.css" />' % share_pth)
    f.write("</head><body>")
    f.write("<center><h2>" + head1 + "</h2>")
    f.write("<center><h2>" + tit + "</h2>")
    f.write("<h2>" + head2 + "</h2>")  # </center>")
    f.write(map_element)
    f.write("<h3>" + "Absolute Errors" + "</h3>")  # </center>")
    f.write("<div><img  width = '700' height = '700' src='ParallelCoordinates/Parallel_Plot_" +
            exp + "_djf.png'></div>")
    f.write("<div><img  width = '700' height = '700' src='ParallelCoordinates/Parallel_Plot_" +
            exp + "_mam.png'></div>")
    f.write("<div><img  width = '700' height = '700' src='ParallelCoordinates/Parallel_Plot_" +
            exp + "_jja.png'></div>")
    f.write("<div><img  width = '700' height = '700' src='ParallelCoordinates/Parallel_Plot_" +
            exp + "_son.png'></div>")

    f.write("</center>")
    # f.write("$('area').hover(function(){$(this).css('border','5px');},function(){$(this).css('border','0px');});")
    f.write("</body></head></html>")

os.popen('chmod 777 %s/*' % pathout).readlines()

#w = sys.stdin.readline()
