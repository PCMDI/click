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
help="number of columns after which we split the portrait plot into two rows", default=20)
parser.add_argument("--png_template", help="template for portrait plot png file", default="clickable_portrait.png")
parser.add_argument("--html_template", hrlp="template for html output filename", default="clickable_portrait.html")


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

png = os.path.join(args.results_dir, png_template(())   

def portrait(data, full_dic, png_file="portrait.png", canvas=None, template=None):
    x_key = data.getAxis(-1).id
    y_key = data.getAxis(-2).id
    yax = [full_dic.get(s,s)+"  " for s in data.getAxis(-2)]
    xax = [full_dic.get(s, s)+"   " for s in data.getAxis(-1)]
    # Preprocessing step to "decorate" the axes on our target variable
    if canvas is None:
        x = vcs.init(bg=True, geometry=(1200, 800))
    else:
        x = canvas
    P = pcmdi_metrics.graphics.portraits.Portrait()
    click_plots.setup_portrait(P)
    P.decorate(data, yax, xax)

    mesh, template, meshfill = P.plot(data, x=x, template=template)

    x.png(png_file)
    targets, tips, extras = click_plots.createModalTargets(data, targets_template, x_key, y_key, merge=args.merge)

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
    return map_element, x

nX = len(xax)
pth = os.getcwd()
os.chdir(args.results_dir)
if nX < args.split:
    map_elements, canvas = portrait(data, full_dic, png=png())
else:
    M = EzTemplate.Multi(rows=2, columns=1)
    map_elements1, canvas = portrait(data[...,:nX//2], full_dic, canvas=None, png=None, template=M.get())
    map_elements2, canvas = portrait(data[...,nX//2:], full_dic, canvas=canvas, png=png(), template=M.get())

os.chdir(pth)
html_filename = os.path.join(args.results_dir, html_template(())   
share_pth = "js"
click_plots.write_modal_html(html_filename, map_element,share_pth, args.results_dir, modal=args.modal)

print("Geenrated html at:", fnm)
