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
import pkg_resources

click_egg_path = click_plots.click_egg_path
pmp_egg_path = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse("pcmdi_metrics"), "share/pmp")

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
inpt.add_argument("--normalize_axis",
                  help="axis over which to normalize results by statistic", default=-1)
web.add_argument(
    "--modal", help="use a custom modal javascript file", default=None)
web.add_argument("--cell_tooltips_html_template", help="html code for tooltip, png image template defined bellow",
                 default="{x_key}: {x_value}<br>{y_key}: {y_value}<br>Value: {value:3g}<div id='thumbnail'><img src='{image}' width=200></div>")
web.add_argument("--cell_tooltips_images_template",
                 default="data/plots/Panel6_%(mode)_%(season)_%(model)_%(rip).png",
                 help="template to find tooltips targets destination")
web.add_argument("--cell_modal_images_template",
                 default=True,
                 help="template to find modal targets destination. If set to `True` then copies tooltip")
web.add_argument("--cell_modal_json_template",
                 default="",
                 help="template to find destination. If set to `True` then copies tooltip")
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
web.add_argument("--web_root", default=None,
                 help="subsitute `local_root` with this after checking files exists, this allows to post web link to " +
                 "pictures while still checking pictures are available on disk")
web.add_argument("--local_root", default=None,
                 help="subsitute this string with `web_root` argument" +
                 " in template strings after checking target existence." +
                 " this allows to use web link while" +
                 " still checking that target are available locally")
web.add_argument("--toggle_image", default=None,
                 help="List of alternate colormap to use", nargs="*")
web.add_argument("--description_html", default=None,
                 help="Few lines of text for detailed description at top of the html page, if needed")
graph.add_argument("--hide_cdat_logo", default=False,
                   help="Hide CDAT logo", action="store_true")
graph.add_argument("--custom_logo", default=os.path.join(pmp_egg_path,
                                                         "graphics", "png", "PCMDILogo_300x98px_72dpi.png"),
                   help="File to use for custom logo")
graph.add_argument("--custom_logo_x",
                   default=0.9,
                   help="x location of logo on plot as ratio, default=0.9")
graph.add_argument("--custom_logo_y",
                   default=0.9,
                   help="y location of logo on plot as ratio, default=0.9")
graph.add_argument("--custom_logo_width",
                   default=300,
                   help="width in pixel for logo")
graph.add_argument("--triangle_indicator", default=None, 
                   help="path for triangle_indicator image")
graph.add_argument("--triangle_indicator_x",
                   default=0.1,
                   help="x location of triangle_indicator on plot as ratio")
graph.add_argument("--triangle_indicator_y",
                   default=0.9,
                   help="y location of triangle_indicator on plot as ratio")
graph.add_argument("--triangle_indicator_width",
                   default=150,
                   help="width in pixel for triangle_indicator")
graph.add_argument("--portrait_templates_json_file",
                   default=None,
                   help="json file containing vcs templates definitions, template names must be: click_portraits_one/click_portraits_top/click_portraits_bottom")
graph.add_argument("--flip", action="store_true", default=False)
graph.add_argument(
    "--names-update", help="a dictionary to update axes labels", default={})
inpt.add_argument(
    "--merge", help="merge json dimensions together", default=None)
graph.add_argument("--split", type=int,
                   help="number of columns after which we split the portrait plot into two rows",
                   default=20)
graph.add_argument(
    "--watermark", help="use this image (or text if path is missing) as watermark")
graph.add_argument("--watermark_font",
                   help="For text watermark use this VCS font", default=1)
graph.add_argument("--watermark_size",
                   help="For text watermark use this font size", default=100)
graph.add_argument("--watermark_math", help="For text watermark that need math rendering",
                   action="store_true", default=False)
graph.add_argument("--watermark_color",
                   help="For text watermark use this font color [r,g,b,opacity]",
                   type=ast.literal_eval,
                   default=[60, 50, 50, 25])
graph.add_argument("--time_stamp",
                   default=False, help="turn on time stamp on plot")
graph.add_argument("--reverse_sorted_yaxis", help="sort y axis values in reversed order",
                   default=False, action="store_true")
graph.add_argument("--reverse_sorted_xaxis", help="sort x axis values in reversed order",
                   default=False, action="store_true")
outpt.add_argument("--png_template", help="template for portrait plot png file",
                   default="clickable_portrait%(colormap).png")
outpt.add_argument("--png_size", help="png output size", default="800x600")
web.add_argument("--html_template_file", help="template for html output filename",
                 default="clickable_portrait.html")
web.add_argument(
    "--no_target", help="png file to use when target png is missing",
    default=os.path.join(click_egg_path, "share", "missing.png"))
web.add_argument(
    "--no_data", help="png file to use when no data is available",
    default=os.path.join(click_egg_path, "share", "no_data.png"))
web.add_argument(
    "--thumbnails", help="generate thumbnails images png", action="store_true", default=False)
web.add_argument(
    "--thumbnails_size", help="size to generate thumbnails images png", default="150x150")
inpt.add_argument(
    "--sector", help="name of extra variable to use as 'sector' (triangles) in portrait plot")
graph.add_argument("--levels", help="levels to use for portrait plots")
graph.add_argument("--colors", help="colors to use for portrait plots")
graph.add_argument(
    "--colormap", help="colormap to use for portrait plots", default=None)

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
names.append("cell_modal_json_template")
for name in names:
    if getattr(args, name) not in [None, True]:
        exec("{name} = genutil.StringConstructor(args.{name})".format(
            name=name), globals(), locals())
    else:
        exec("{name} = args.{name}".format(name=name), globals(), locals())
print("CELL JSON:", cell_modal_json_template)
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
                cmd = "if isinstance({name}, genutil.StringConstructor): setattr({name}, k[:2], att)".format(
                    name=name)
                exec(cmd, globals(), locals())
if args.merge is not None:
    dic["merge"] = args.merge


data = J(**dic)(squeeze=1)
if data.ndim not in [2, 3]:
    raise RuntimeError(
        "selection leads to untreatable data shape: {} data after reading must 2D or 3D".format(data.shape))

if args.sector is not None:
    data = data(order="({})...".format(args.sector))
if args.flip:
    if data.ndim == 2:
        data = MV2.transpose(data)
    else:  # sectors
        data = MV2.transpose(data, (0, 2, 1))
if args.normalize is not False:
    if args.normalize == "median":
        if isinstance(args.normalize_axis, int):
            norm_axis = data.getAxisIds()[args.normalize_axis]
        else:
            norm_axis = args.normalize_axis
        norm_axis = "({})".format(norm_axis)
        median = genutil.statistics.median(data, axis=norm_axis)[0]
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

# Reverse sort X axis?
if args.reverse_sorted_xaxis:
    data = data[..., ::-1]

# Reverse sort Y axis?
if args.reverse_sorted_yaxis:
    data = data[..., ::-1, :]

# Source default templates
if args.portrait_templates_json_file is None:
    vcs.scriptrun(os.path.join(click_egg_path, "template_bottom.json"))
    vcs.scriptrun(os.path.join(click_egg_path, "template_top.json"))
    vcs.scriptrun(os.path.join(click_egg_path, "template_one.json"))
else:
    vcs.scriptrun(args.portrait_templates_json_file)


pth = os.getcwd()
if not os.path.exists(args.results_dir):
    print("Creating non-existing output directory: {}".format(args.results_dir))
    os.makedirs(args.results_dir)
os.chdir(args.results_dir)

geo = args.png_size.split("x")
x = vcs.init(bg=True, geometry={"width": int(geo[0]), "height": int(geo[1])})

# create the html map element
if args.colormap is not None:
    png_template.colormap = "_" + args.colormap

if args.hide_cdat_logo:
    x.drawlogooff()  # CDAT log on/off

CP = click_plots.ClickablePortrait(
    x=x, nodata_png=args.no_data, missing_png=args.no_target,
    logo=args.custom_logo,
    logo_x=args.custom_logo_x,
    logo_y=args.custom_logo_y,
    logo_width=args.custom_logo_width,
    time_stamp=args.time_stamp)

# tips and modal templates
CP.thumbnails = args.thumbnails
CP.thumbnails_size = args.thumbnails_size
# web target paths...
CP.local_root = args.local_root
CP.web_root = args.web_root
for name in names:
    print("SETTING: {} on CP".format(name))
    exec("setattr(CP,'{name}',{name})".format(name=name), globals(), locals())
CP.PLOT_SETTINGS.fillareacolors = args.colors
CP.PLOT_SETTINGS.levels = args.levels
CP.PLOT_SETTINGS.colormap = args.colormap

# prepare axis name for portrait plot
full_dic = args.names_update


def onePortraitPlotPass(data, full_dic, CP, merge, multiple=1.1, sector=None):
    nX = len(data.getAxis(-1))
    if nX < args.split:
        clicks, targets, tips, extras = CP.plot(
            data, full_dic, merge=merge,
            template="click_portraits_one",
            multiple=multiple, sector=sector)
    else:
        if CP.PLOT_SETTINGS.colormap is None:
            CP.PLOT_SETTINGS.colormap = "bl_rd_12"
        if CP.PLOT_SETTINGS.levels is None:
            min, max = vcs.minmax(data)
            if max != 0:
                max = max + .000001
            levs = vcs.mkscale(min, max)
            CP.PLOT_SETTINGS.levels = levs
            if CP.PLOT_SETTINGS.fillareacolors is None:
                if CP.PLOT_SETTINGS.colormap == "bl_rd_12":
                    CP.PLOT_SETTINGS.fillareacolors = vcs.getcolors(
                        levs, list(range(144, 156)), split=1)
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



png = png_template()

geo = CP.x.geometry()
map_element = vcs.utils.mapPng(
    png, clicks, targets, tips, extras=extras, width=geo["width"], height=geo["height"], id_image='clickable_portrait')

if args.triangle_indicator is not None:
    triangle_indicator_path = args.triangle_indicator
    width = args.triangle_indicator_width 
    triangle_indicator = vcs.utils.Logo(triangle_indicator_path, width=width)
    triangle_indicator.x = args.triangle_indicator_x
    triangle_indicator.y = args.triangle_indicator_y
    triangle_indicator.plot(CP.x)
    CP.x.png(png)


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
    html_filename, map_element, share_pth, args.results_dir, modal=args.modal, title=args.title,
    toggle_image=args.toggle_image, png_template=png_template, description=args.description_html)

print("Generated html at:", html_filename)
