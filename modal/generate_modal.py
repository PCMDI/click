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
import cdms2
import MV2


click_egg_path = click_plots.click_egg_path

parser = pcmdi_metrics.pcmdi.pmp_parser.PMPParser()
parser.use("--results_dir")

parser.add_argument("--data_path", help="input data path")
parser.add_argument("--files_glob_pattern",
                    help="glob pattern to select correct files in input directory")
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
parser.add_argument(
    "--names-update", help="a dictionary to update axes labels", default={})
parser.add_argument("--modal", help="use a custom modal file", default=None)
parser.add_argument(
    "--merge", help="merge json dimensions together", default=None)
parser.add_argument("--split", type=int,
                    help="number of columns after which we split the portrait plot into two rows",
                    default=20)
parser.add_argument("--png_template", help="template for portrait plot png file",
                    default="clickable_portrait.png")
parser.add_argument("--html_template", help="template for html output filename",
                    default="clickable_portrait.html")
parser.add_argument(
    "--no_target", help="png file to use when target png is missing")
parser.add_argument(
    "--no_data", help="png file to use when no data is available")
parser.add_argument(
    "--sector", help="name of extra variable to use as 'sector' (triangles) in portrait plot")


# first make sure we do not use --help yet
yanked_help = False
if "--help" in sys.argv:
    sys.argv.remove("--help")
    yanked_help = True
if "-h" in sys.argv:
    sys.argv.remove("-h")
    yanked_help = True
args, unknown = parser.parse_known_args()


#######################################################

# make sure we have default
data_path = "data/mode"
files_glob_pattern = "*.json"

if args.parameters is not None:  # User sent param file need to look for datapth and pattern
    with open(args.parameters) as f:
        code = compile(f.read(), args.parameters, 'exec')
        global_vars = {}
        local_vars = {}
        exec(code, global_vars, local_vars)
        if "data_path" in local_vars:
            data_path = local_vars["data_path"]
        if "files_glob_pattern" in local_vars:
            files_glob_pattern = local_vars["files_glob_pattern"]
# If passed from command line, overwrite this
if args.data_path is not None:
    data_path = args.data_path
if args.files_glob_pattern is not None:
    files_glob_pattern = args.files_glob_pattern
json_files = glob.glob(
    os.path.join(
        data_path,
        files_glob_pattern))

print("LOOKING AT PATTERN:", files_glob_pattern, "in", data_path)
print("We are looking at {:d} Json Files:".format(len(json_files)))

# Load json and figure out keys to add
J = pcmdi_metrics.io.base.JSONs(json_files)
json_keys = set()
for k in J.getAxisIds():
    json_keys.add("--{}".format(k))


# Ok now add all these keys to parameter
for k in json_keys:
    parser.add_argument(k, default=None, type=ast.literal_eval)

# do we need to add back help
if yanked_help:
    sys.argv.insert(1, "--help")
args = parser.get_parameter(argparse_vals_only=False)
targets_template = genutil.StringConstructor(args.targets_template)
png_template = genutil.StringConstructor(args.png_template)
html_template = genutil.StringConstructor(args.html_template)


pathout = args.results_dir

dic = {}
for k in json_keys:
    att = getattr(args, k[2:], None)
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
    if axis not in ['x', 'y', 'z', 't'] and not isinstance(axis, int):
        order = "({})...".format(axis)
    else:
        order = "{}...".format(axis)
    new = data(order=order)
    axes = new.getAxisList()  # Save for later
    new = MV2.array(new.asma())  # lose dims
    for i in range(new.shape[0] - 1, -1, -1):
        tmp = new[i]
        if tmp.mask.all():
            a = new[:i]
            b = new[i+1:]
            if b.shape[0] == 0:
                new = a
            else:
                new = MV2.concatenate((a, b))
    newAxis = []
    for v in new.getAxis(0):
        newAxis.append(axes[0][int(v)])
    ax = cdms2.createAxis(newAxis, id=axes[0].id)
    axes[0] = ax
    new.setAxisList(axes)
    return new(order=originalOrder)


data = J(**dic)(squeeze=1)
for i in range(len(data.shape)):
    data = scrap(data, axis=i)
if args.normalize is not False:
    if args.normalize == "median":
        median = genutil.statistics.median(data, axis=1)[0]
        data, median = genutil.grower(data, median)
        # Loose info on median
        median = median.filled()
        # normalize
        data = (data-median) / median
    else:
        for k in args.normalize:
            dic[k] = args.normalize[k]
        norm = J(**dic)(squeeze=1)
        data /= norm

if args.flip:
    data = MV2.transpose(data)
# prepare axis name for portrait plot
# Add extra sapaces at the end
full_dic = {'pr': 'Precipitation'}
full_dic.update(args.names_update)


pth = os.getcwd()
if not os.path.exists(args.results_dir):
    print("Creating non-existing output directory: {}".format(args.results_dir))
    os.makedirs(args.results_dir)
os.chdir(args.results_dir)


def onePortraitPlotPass(data, full_dic, targets_template, args, png_file, canvas, multiple=1.1, sector=None):
    nX = len(data.getAxis(-1))
    if nX < args.split:
        clicks, targets, tips, extras, canvas = click_plots.portrait(
            data, full_dic, targets_template, merge=args.merge,canvas=canvas, png_file=png_file,
            nodata_png=args.no_data,
            missing_png=args.no_target, multiple=multiple, sector=sector)
    else:
        vcs.scriptrun(os.path.join(click_egg_path, "template_bottom.json"))
        vcs.scriptrun(os.path.join(click_egg_path, "template_top.json"))
        clicks1, targets1, tips1, extras1, canvas = click_plots.portrait(
            data[..., :nX//2], full_dic, targets_template, merge=args.merge, canvas=canvas,
            png_file=png, template='click_portraits_top', nodata_png=args.no_data,
            missing_png=args.no_target, multiple=multiple, sector=sector)
        clicks2, targets2, tips2, extras2, canvas = click_plots.portrait(
            data[..., nX//2:], full_dic, targets_template, merge=args.merge, canvas=canvas,
            png_file=png, template='click_portraits_bottom', nodata_png=args.no_data,
            missing_png=args.no_target, multiple=multiple, sector=sector)
        clicks = numpy.concatenate((clicks1, clicks2))
        targets = numpy.concatenate((targets1, targets2))
        tips = numpy.concatenate((tips1, tips2))
        extras = numpy.concatenate((extras1, extras2))
    return clicks, targets, tips, extras, canvas


canvas = None
if args.sector is not None:
    data = data(order="({})...".format(args.sector))
    sectors = data.getAxis(0)
    nSectors = len(sectors) / 10.
    clicks = None
    for i, sec in enumerate(sectors):
        setattr(targets_template, args.sector, sec)
        setattr(png_template, args.sector, sec)
        png = png_template()
        sec_clicks, sec_targets, sec_tips, sec_extras, canvas = onePortraitPlotPass(
            data[i], full_dic, targets_template, args, png, canvas, multiple=i + 1 + nSectors, sector=data.getAxis(0))
        if clicks is None:
            clicks, targets, tips, extras = sec_clicks, sec_targets, sec_tips, sec_extras
        else:
            clicks = numpy.concatenate((clicks, sec_clicks))
            targets = numpy.concatenate((targets, sec_targets))
            tips = numpy.concatenate((tips, sec_tips))
            extras = numpy.concatenate((extras, sec_extras))
else:
    png = png_template()
    clicks, targets, tips, extras, canvas = onePortraitPlotPass(
        data, full_dic, targets_template, args, png, canvas)


# create the html map element
geo = canvas.geometry()
map_element = vcs.utils.mapPng(
    png, clicks, targets, tips, extras=extras, width=geo["width"], height=geo["height"])
os.chdir(pth)
html_filename = os.path.join(args.results_dir, html_template())
share_pth = "js"
click_plots.write_modal_html(
    html_filename, map_element, share_pth, args.results_dir, modal=args.modal)

print("Generated html at:", html_filename)
