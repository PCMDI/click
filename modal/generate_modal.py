#!/usr/bin/env python
from __future__ import print_function
import glob
import os
import sys
import pcmdi_metrics
import pcmdi_metrics.graphics.portraits
import genutil
import numpy
import vcs
import click_plots

parser = pcmdi_metrics.pcmdi.pmp_parser.PMPParser()

parser.use("--results_dir")

parser.add_argument("--data_path", help="input data path", default="data/v1.0")
parser.add_argument("--statistic", help="statistic to use",
                    default="rms_devam_xy")
parser.add_argument("--title", help="title for plot")
parser.add_argument("--files_glob_pattern", help="glob pattern to select correct files in input directory",
                    default="*.json")
parser.add_argument("--bad", help="list of bad models", default=[])
parser.add_argument("--seasons", help="seasons to process",
                    default=['djf', 'mam', 'jja', 'son'])
parser.add_argument("--region", help="region to use", default="global")
parser.add_argument("--normalize", action="store_true",
                    help="normalize results by median", default=False)
parser.add_argument("--mode", help="mode to use", default="NAO")
parser.add_argument("--rip", help="", default="r1i1p1")
parser.add_argument("--targets_template",
                    default="data/pngs/%(mode)/Panel7_%(mode)_%(season)_%(model)_%(rip).png"
                    help="template to find targets destination")
parser.add_argument("--statistic", "--stat", dest="stat",
                    help="statistic to use", default="bias_xy")
args = parser.get_parameter()

targets_template = genutil.StringConstructor(args.targets_template)

injpath = args.data_path
pathout = args.results_dir
tit = args.title
stat = args.stat
bad_models = args.bad
seasons = args.seasons
targets_template.stat = stat
head1 = 'CMIP5 simulations (1981-2005 climatology)'

head2 = 'Relative errors (statistics normalized by median error)'

#######################################################

print("looking in:", injpath)
json_files = glob.glob(
    os.path.join(
        injpath,
        args.files_glob_pattern))

print("We are looking at {:d} Json Files:".format(len(json_files)))
print(" ".join(json_files))

J = pcmdi_metrics.pcmdi.io.JSONs(json_files)

models = sorted(J.getAxis("model")[:])

print("original models:", models)
print("We will be manually excluding:", bad_models)
for m in bad_models:
    print(" bad at:", models.index(m))
    models.pop(models.index(m))

variables = sorted(J.getAxis("variable")[:])
print("We read in {:d} models: {}:".format(len(models), models))
print("We read in {:d} variables: {}:".format(len(variables), variables))

data = J(model=models, statistic=[stat], region=args.region)(squeeze=1)

if args.normalize:
    median = genutil.statistics.median(data, axis=1)[0]
    data, median = genutil.grower(data, median)
    # Loose info on median
    median = median.filled()
    # normalize
    data = (data-median) / median


yax = [s+"  " for s in models]

# CHANGE VARIABLE NAMES

var_full_dic = {'pr': 'Precipitation'}

var_fullname = [var_full_dic.get(v, v)+"   " for v in variables]

# Preprocessing step to "decorate" the axes on our target variable
x = vcs.init(bg=True, geometry=(1200, 800))
P = pcmdi_metrics.graphics.portraits.Portrait()
click_plots.setup_portrait(P)
P.decorate(data, var_fullname, yax)

mesh, template, meshfill = P.plot(data[..., 0], x=x)

png_file = os.path.join(pathout, "clickable6.png")
x.png(png_file)
print("SENDING:", targets_template.template)
targets, tips, extras = click_plots.createModalTargets(data[..., 0], targets_template)

# Creates clickable polygons numpy arrays
click_areas = vcs.utils.meshToPngCoords(mesh, template, [
    meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
click_labels_x = vcs.utils.axisToPngCoords([], meshfill, template, 'x1', [
    meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
click_labels_y = vcs.utils.axisToPngCoords([], meshfill, template, 'y1', [
    meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)

targets_lbls_x = extras_lbls_x = tips_lbls_x = [
    meshfill.xticlabels1[k] for k in sorted(meshfill.xticlabels1.keys())]
targets_lbls_y = extras_lbls_y = tips_lbls_y = [
    meshfill.xticlabels1[k] for k in sorted(meshfill.xticlabels1.keys())]

clicks = numpy.concatenate((click_areas, click_labels_x, click_labels_y))
targets = numpy.concatenate((targets, targets_lbls_x, targets_lbls_y))
tips = numpy.concatenate((tips, tips_lbls_x, tips_lbls_y))
extras = numpy.concatenate((extras, extras_lbls_x, extras_lbls_y))

geo = x.geometry()
# create the html map element
map_element = vcs.utils.mapPng(
    png_file, clicks, targets, tips, extras=extras, width=geo["width"], height=geo["height"])

fnm = os.path.join(pathout, "clickable_6.html")

share_pth = os.path.join(pathout,"js")
click_plots.write_modal_html(fnm, map_element,share_pth)

print("Geenrated html at:", fnm)
