#!/usr/bin/env python
from __future__ import print_function, division
import glob
import os
import sys
import pcmdi_metrics
import genutil
import numpy
import vcs
import click_plots
import json
import ast
import argparse
import cdms2
import MV2
import EzTemplate

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
parser.add_argument("--modal", help="use a custom modal file", default=None)
parser.add_argument("--merge", help="merge json dimensions together", default=None)
parser.add_argument("--split", type=int,
                    help="number of columns after which we split the portrait plot into two rows",
                    default=20)
parser.add_argument("--png_template", help="template for portrait plot png file", default="clickable_portrait.png")
parser.add_argument("--html_template", help="template for html output filename", default="clickable_portrait.html")


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
png_template = genutil.StringConstructor(args.png_template)
html_template = genutil.StringConstructor(args.html_template)


J = pcmdi_metrics.io.base.JSONs(json_files)

pathout = args.results_dir

dic={}
for k in json_keys:
    att = getattr(args,k[2:], None)
    if att is not None:
        dic[k[2:]] = att
        if not isinstance(att, (list, tuple)):
            setattr(targets_template, k[2:], att)
            setattr(png_template, k[2:], att)
            setattr(html_template, k[2:], att)
if args.merge is not None:
    dic["merge"] = args.merge

def scrap(data, axis=0):
    originalOrder = data.getOrder(ids=True)
    if axis not in ['x','y','z','t'] and not isinstance(axis, int):
        order = "({})...".format(axis)
    else:
        order = "{}...".format(axis)
    new = data(order=order)
    axes = new.getAxisList()  # Save for later
    new = MV2.array(new.asma())  # lose dims
    for i in range(new.shape[0] - 1, -1, -1):
        tmp = data[i]
        if tmp.mask.all():
            a = new[:i]
            b = new[i+1:]
            if b.shape[0] == 0:
                new = a
            else:
                new = MV2.concatenate((a,b))
    newAxis = []
    for v in new.getAxis(0):
        newAxis.append(axes[0][int(v)])
    ax = cdms2.createAxis(newAxis, id=axes[0].id)
    axes[0] = ax
    new.setAxisList(axes)
    return new(order=originalOrder)


data = J(**dic)(squeeze=1)
print("SHAPE INIT:", data.shape)
data = scrap(data, axis=1)
data = scrap(data, axis=0)
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

png = png_template()

pth = os.getcwd()
os.chdir(args.results_dir)
print("WE are now in:",os.getcwd())
nX = len(data.getAxis(-1))
if nX < args.split:
    clicks, targets, tips, extras, canvas = click_plots.portrait(
        data, full_dic, targets_template, merge=args.merge, png_file=png)
else:
    M = EzTemplate.Multi(rows=2, columns=1)
    clicks1, targets1, tips1, extras1, canvas = click_plots.portrait(
        data[..., :nX//2], full_dic, targets_template, merge=args.merge, canvas=None, png_file=png, template=M.get())
    clicks2, targets2, tips2, extras2, canvas = click_plots.portrait(
        data[..., nX//2:], full_dic, targets_template, merge=args.merge, canvas=canvas, png_file=png, template=M.get())
    clicks = numpy.concatenate((clicks1, clicks2))
    targets = numpy.concatenate((targets1, targets2))
    tips = numpy.concatenate((tips1, tips2))
    extras = numpy.concatenate((extras1, extras2))

# create the html map element
geo = canvas.geometry()
map_element = vcs.utils.mapPng(
    png, clicks, targets, tips, extras=extras, width=geo["width"], height=geo["height"])
os.chdir(pth)
html_filename = os.path.join(args.results_dir, html_template())
share_pth = "js"
click_plots.write_modal_html(html_filename, map_element,share_pth, args.results_dir, modal=args.modal)

print("Geenrated html at:", html_filename)
