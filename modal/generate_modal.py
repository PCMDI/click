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
import json
import ast
import argparse
import MV2
pre_parser = argparse.ArgumentParser()
pre_parser.add_argument("--data_path", help="input data path", default="data/modes")
pre_parser.add_argument("--files_glob_pattern", help="glob pattern to select correct files in input directory",
                    default="*.json")

parser = pcmdi_metrics.pcmdi.pmp_parser.PMPParser()
parser.use("--results_dir")

parser.add_argument("--data_path", help="input data path", default="data/modes")
parser.add_argument("--files_glob_pattern", help="glob pattern to select correct files in input directory",
                    default="*.json")
parser.add_argument("--json-preprocessor", help="if sending json files use this script to preprocess",
                    default=None)
parser.add_argument("--title", help="title for plot")
parser.add_argument("--bad", help="list of bad models", default=[])
parser.add_argument("--normalize", 
                    help="normalize results by statistic", default=False)
parser.add_argument("--targets_template",
                    default="data/plots/Panel6_%(mode)_%(season)_%(model)_%(rip).png",
                    help="template to find targets destination")
parser.add_argument("--flip", action="store_true", default=False)
parser.add_argument("--names-update", help="a dictionary to update axes labels", default={})

# first make sure we do not use --help yet
yanked_help = False
if "--help" in sys.argv:
    sys.argv.remove("--help")
    yanked_help = True
if "-h" in sys.argv:
    sys.argv.remove("-h")
    yanked_help = True
args, unknown = parser.parse_known_args()

injpath = args.data_path

#######################################################

print("looking in:", injpath, args.files_glob_pattern)
json_files = glob.glob(
    os.path.join(
        injpath,
        args.files_glob_pattern))

print("We are looking at {:d} Json Files:".format(len(json_files)))

json_keys = set()
for j in json_files:
    with open(j) as f:
        inp = json.load(f)
        if "json_structure" in inp:
            for k in inp["json_structure"]:
                json_keys.add("--{}".format(k))

# Ok now add all these keys to parameter
for k in json_keys:
    parser.add_argument(k, default=None, type=ast.literal_eval)

# do we need to add back help
if yanked_help:
    sys.argv.insert(1,"--help")
args = parser.get_parameter(argparse_vals_only=False)
targets_template = genutil.StringConstructor(args.targets_template)

J = pcmdi_metrics.io.base.JSONs(json_files)

pathout = args.results_dir

dic={}
for k in json_keys:
    att = getattr(args,k[2:], None)
    if att is not None:
        dic[k[2:]] = att
        if not isinstance(att, (list, tuple)):
            setattr(targets_template, k[2:], att)

print("DICT FOR JSNO:",dic)
data = J(**dic)(squeeze=1)

if args.normalize is not False:
    if args.normalize == "median":
        median = genutil.statistics.median(data, axis=1)[0]
        data, median = genutil.grower(data, median)
        # Loose info on median
        median = median.filled()
        # normalize
        data = (data-median) / median
    else:
        dic["statistic"] = args.normalize
        norm = J(**dic)
        data /= norm

if args.flip:
    data = MV2.transpose(data)

# prepare axis name for portrait plot
# Add extra sapaces at the end
full_dic = {'pr': 'Precipitation'}
full_dic.update(args.names_update)
x_key = data.getAxis(-1).id
y_key = data.getAxis(-2).id
print("KEY: ______________________", x_key, y_key)
yax = [full_dic.get(s,s)+"  " for s in data.getAxis(-2)]
xax = [full_dic.get(s, s)+"   " for s in data.getAxis(-1)]

# Preprocessing step to "decorate" the axes on our target variable
x = vcs.init(bg=True, geometry=(1200, 800))
P = pcmdi_metrics.graphics.portraits.Portrait()
click_plots.setup_portrait(P)
P.decorate(data, yax, xax)

mesh, template, meshfill = P.plot(data, x=x)

png_file = "modal.png"
x.png(os.path.join(args.results_dir, png_file))
targets, tips, extras = click_plots.createModalTargets(data, targets_template, x_key, y_key)

pth = os.getcwd()
os.chdir(args.results_dir)
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
print("WE are now in:",os.getcwd())
map_element = vcs.utils.mapPng(
    png_file, clicks, targets, tips, extras=extras, width=geo["width"], height=geo["height"])
os.chdir(pth)
fnm = os.path.join(pathout, "clickable_6.html")

share_pth = "js"
click_plots.write_modal_html(fnm, map_element,share_pth, args.results_dir)

print("Geenrated html at:", fnm)
