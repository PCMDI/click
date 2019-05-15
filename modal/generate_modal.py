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
import ast
import MV2


click_egg_path = click_plots.click_egg_path

parser = pcmdi_metrics.pcmdi.pmp_parser.PMPParser()
parser.use("--results_dir")


graph = parser.add_argument_group("graphics", "Graphics Related Controls")
inpt = parser.add_argument_group("input", "Input Data Related Controls")
outpt = parser.add_argument_group("output", "Output Related Controls")
web = parser.add_argument_group("web", "Web pages related arguments (modal)")


inpt.add_argument("--data_path", help="input data path")
inpt.add_argument("--files_glob_pattern",
                    help="glob pattern to select correct files in input directory")
inpt.add_argument("--json-preprocessor", help="if sending json files use this script to preprocess",
                    default=None)
web.add_argument("--title", help="title for plot")
inpt.add_argument("--bad", help="list of bad models", default=[])
inpt.add_argument("--normalize",
                    help="normalize results by statistic", default=False)
web.add_argument("--modal", help="use a custom modal javascript file", default=None)
web.add_argument("--cell_tooltips_html_template", help="html code for tooltip, png image template defined bellow",
                 default="{x_key}: {x_value}<br>{y_key}: {y_value}<br>Value: {value:3g}<div id='thumbnail'><img src='{image}' width=200></div>")
web.add_argument("--cell_tooltips_images_template",
                    default="data/plots/Panel6_%(mode)_%(season)_%(model)_%(rip).png",
                    help="template to find tooltips targets destination")
web.add_argument("--cell_modal_images_template",
                    default=True,
                    help="template to find modal targets destination. If set to `True` then copies tooltip")
web.add_argument("--xlabels_tooltips_html_template",
                    default="{value}<br><div id='thumbnail'><img src='{image}' width=200></div>",
                    help="html code for x labels tooltips")
web.add_argument("--xlabels_tooltips_images_template",
                    default=None,
                    help="template to find targets destination for x labels")
web.add_argument("--xlabels_modal_images_template",
                    default=True,
                    help="template to find modal target destination for x labels. If set to `True` then copies tooltip")
web.add_argument("--ylabels_tooltips_html_template",
                    default="{value}<br><div id='thumbnail'><img src='{image}' width=200></div>",
                    help="html code for y labels tooltips")
web.add_argument("--ylabels_tooltips_images_template",
                    default=None,
                    help="template to find targets destination for y labels")
web.add_argument("--ylabels_modal_images_template",
                    default=True,
                    help="template to find modal targets destination for y labels. If set to `True` then copies tooltip")
graph.add_argument("--flip", action="store_true", default=False)
graph.add_argument(
    "--names-update", help="a dictionary to update axes labels", default={})
inpt.add_argument(
    "--merge", help="merge json dimensions together", default=None)
graph.add_argument("--split", type=int,
                    help="number of columns after which we split the portrait plot into two rows",
                    default=20)
graph.add_argument("--watermark", help="use this image (or text if path is missing) as watermark")
graph.add_argument("--watermark_font", help="For text watermark use this VCS font",default=1)
graph.add_argument("--watermark_size", help="For text watermark use this font size",default=100)
graph.add_argument("--watermark_math", help="For text watermark that need math rendering",action="store_true", default=False)
graph.add_argument("--watermark_color",
                   help="For text watermark use this font color [r,g,b,opacity]",
                   type=ast.literal_eval,
                   default=[60,50,50,25])
outpt.add_argument("--png_template", help="template for portrait plot png file",
                    default="clickable_portrait.png")
outpt.add_argument("--png_size",help="png output size", default="800x600")
web.add_argument("--html_template_file", help="template for html output filename",
                    default="clickable_portrait.html")
web.add_argument(
    "--no_target", help="png file to use when target png is missing")
web.add_argument(
    "--no_data", help="png file to use when no data is available")
web.add_argument(
    "--thumbnails", help="generate thumbnails images png", action="store_true", default=False)
web.add_argument(
    "--thumbnails_size", help="size to generate thumbnails images png", default="150x150")
inpt.add_argument(
    "--sector", help="name of extra variable to use as 'sector' (triangles) in portrait plot")
graph.add_argument("--levels", help="levels to use for portrait plots")
graph.add_argument("--colors", help="colors to use for portrait plots")
graph.add_argument("--colormap", help="colormap to use for portrait plots", default=None)

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
    inpt.add_argument(k, default=None, type=ast.literal_eval)

# do we need to add back help
if yanked_help:
    sys.argv.insert(1, "--help")
args = parser.get_parameter(argparse_vals_only=False)

names = ["png_template", "html_template_file"]
for elt in ["cell", "xlabels", "ylabels"]:
    names.append("{}_tooltips_html_template".format(elt))
    for elt_type in ["tooltips", "modal"]:
        names.append("{}_{}_images_template".format(elt, elt_type))
for name in names:
    if getattr(args, name) not in [None, True]:
        exec("{name} = genutil.StringConstructor(args.{name})".format(name=name), globals(), locals())
    else:
        exec("{name} = args.{name}".format(name=name), globals(), locals())
if xlabels_modal_images_template is True:
    xlabels_modal_images_template = xlabels_tooltips_images_template
if ylabels_modal_images_template is True:
    ylabels_modal_images_template = ylabels_tooltips_images_template
if ylabels_modal_images_template is True:
    ylabels_modal_images_template = ylabels_tooltips_images_template
if cell_modal_images_template is True:
    cell_modal_images_template = cell_tooltips_images_template
pathout = args.results_dir

dic = {}
for k in json_keys:
    att = getattr(args, k[2:], None)
    if att is not None:
        dic[k[2:]] = att
        if not isinstance(att, (list, tuple)):
            for name in names:
                cmd = "if isinstance({name}, genutil.StringConstructor): setattr({name}, k[:2], att)".format(name=name)
                exec(cmd, globals(), locals())
if args.merge is not None:
    dic["merge"] = args.merge


data = J(**dic)(squeeze=1)

if args.flip:
    data = MV2.transpose(data)
if args.normalize is not False:
    if args.normalize == "median":
        median = genutil.statistics.median(data, axis=data.ndim-1)[0]
        data, median = genutil.grower(data, median)
        # Loose info on median
        median = median.filled()
        # normalize
        data = (data-median) / median
    elif callable(args.normalize):  # Test if callable
        data = args.normalize(data, J, args)
    else:
        for k in args.normalize:
            dic[k] = args.normalize[k]
        norm = J(**dic)(squeeze=1)
        data /= norm

# prepare axis name for portrait plot
# Add extra spaces at the end
full_dic = args.names_update


pth = os.getcwd()
if not os.path.exists(args.results_dir):
    print("Creating non-existing output directory: {}".format(args.results_dir))
    os.makedirs(args.results_dir)
os.chdir(args.results_dir)

geo = args.png_size.split("x")
x = vcs.init(bg=True, geometry={"width":int(geo[0]), "height":int(geo[1])})
CP = click_plots.ClickablePortrait(
    x=x, nodata_png=args.no_data, missing_png=args.no_target)

# tips and modal templatates
CP.thumbnails = args.thumbnails
CP.thumbnails_size = args.thumbnails_size
for name in names:
    print("SETTING: {} on CP".format(name))
    exec("setattr(CP,'{name}',{name})".format(name=name), globals(), locals())
CP.PLOT_SETTINGS.fillareacolors = args.colors
CP.PLOT_SETTINGS.levels = args.levels
CP.PLOT_SETTINGS.colormap = args.colormap


def onePortraitPlotPass(data, full_dic, CP, merge, multiple=1.1, sector=None):
    nX = len(data.getAxis(-1))
    if nX < args.split:
        clicks, targets, tips, extras = CP.plot(
            data, full_dic, merge=merge,
            multiple=multiple, sector=sector)
    else:
        vcs.scriptrun(os.path.join(click_egg_path, "template_bottom.json"))
        vcs.scriptrun(os.path.join(click_egg_path, "template_top.json"))
        if CP.PLOT_SETTINGS.colormap is None:
            CP.PLOT_SETTINGS.colormap= "bl_rd_12"
        if CP.PLOT_SETTINGS.levels is None:
            min, max = vcs.minmax(data)
            if max != 0:
                max = max + .000001
            levs = vcs.mkscale(min, max)
            CP.PLOT_SETTINGS.levels = levs
            if CP.PLOT_SETTINGS.fillareacolors is None:
                if CP.PLOT_SETTINGS.colormap == "bl_rd_12":
                    CP.PLOT_SETTINGS.fillareacolors = vcs.getcolors(levs, list(range(144, 156)), split=1)
                else:
                    CP.PLOT_SETTINGS.fillareacolors = vcs.getcolors(levs)

        clicks1, targets1, tips1, extras1 = CP.plot(
            data[..., :nX//2], full_dic, merge=merge,
            template='click_portraits_top',
            multiple=multiple, sector=sector)
        clicks2, targets2, tips2, extras2 = CP.plot(
            data[..., nX//2:], full_dic, merge=merge,
            template='click_portraits_bottom',
            multiple=multiple, sector=sector)
        clicks = numpy.concatenate((clicks1, clicks2))
        targets = numpy.concatenate((targets1, targets2))
        tips = numpy.concatenate((tips1, tips2))
        extras = numpy.concatenate((extras1, extras2))
    return clicks, targets, tips, extras


if args.sector is not None:
    data = data(order="({})...".format(args.sector))
    sectors = data.getAxis(0)
    nSectors = len(sectors) / 10.
    clicks = None
    for i, sec in enumerate(sectors):
        for name in names:
            sub = getattr(CP, name)
            if isinstance(sub, genutil.StringConstructor):
                setattr(sub, args.sector, sec)
        sec_clicks, sec_targets, sec_tips, sec_extras = onePortraitPlotPass(
            data[i], full_dic, CP, merge=args.merge, multiple=i + 1 + nSectors, sector=data.getAxis(0))
        if clicks is None:
            clicks, targets, tips, extras = sec_clicks, sec_targets, sec_tips, sec_extras
        else:
            clicks = numpy.concatenate((clicks, sec_clicks))
            targets = numpy.concatenate((targets, sec_targets))
            tips = numpy.concatenate((tips, sec_tips))
            extras = numpy.concatenate((extras, sec_extras))
else:
    clicks, targets, tips, extras, = onePortraitPlotPass(
        data, full_dic, CP, merge=args.merge)


# create the html map element
png = png_template()
geo = CP.x.geometry()
map_element = vcs.utils.mapPng(
    png, clicks, targets, tips, extras=extras, width=geo["width"], height=geo["height"])
if args.watermark is not None:
    if not os.path.isabs(args.watermark):  # relpath
        watermark_path = os.path.join(pth, args.watermark)
    else:
        watermark_path = args.watermark
    if not os.path.exists(watermark_path):  # not here must be text
        watermark = vcs.createtext()
        watermark.x = [.5]
        watermark.y = [.5]
        watermark.halign = "center"
        watermark.valign = "half"
        watermark.height = args.watermark_size
        watermark.angle = -45
        watermark.color = args.watermark_color
        watermark.font = args.watermark_font
        if args.watermark_math:
            watermark.string = r"${}$".format(args.watermark)
        else:
            watermark.string = args.watermark
        CP.x.plot(watermark)
    else:  # Ok it's a png file
        width = args.watermark_size
        watermark = vcs.utils.Logo(watermark_path, width=width)
        watermark.x = .5
        watermark.y = .5
        watermark.plot(CP.x)
    CP.x.png(png)
os.chdir(pth)
html_filename = os.path.join(args.results_dir, html_template_file())
share_pth = "js"
click_plots.write_modal_html(
    html_filename, map_element, share_pth, args.results_dir, modal=args.modal, title=args.title)

print("Generated html at:", html_filename)
