from pcmdi_metrics.graphics.portraits import Portrait
import vcs
import click_plots
import numpy
import pkg_resources
import os

egg_path = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse("pcmdi_metrics"), "share/pmp")


def setup_portrait(P):
    SET = P.PLOT_SETTINGS
    # Viewport on the Canvas
    SET.x1 = .20  # .05
    SET.x2 = .90
    SET.y1 = .2
    SET.y2 = .8

    #va = .01
    # P.PLOT_SETTINGS.x1 = 0.05 #  .1
    # P.PLOT_SETTINGS.x2 = .85  #.85
    #P.PLOT_SETTINGS.y1 = .6 + va
    #P.PLOT_SETTINGS.y2 = .9 + va

    # P.PLOT_SETTINGS.xtic2.y1=P.PLOT_SETTINGS.y1
    # P.PLOT_SETTINGS.xtic2.y2=P.PLOT_SETTINGS.y2
    # P.PLOT_SETTINGS.ytic2.x1=P.PLOT_SETTINGS.x1
    # P.PLOT_SETTINGS.ytic2.x2=P.PLOT_SETTINGS.x2

    # Both X (horizontal) and y (VERTICAL) ticks
    # Text table
    SET.tictable = vcs.createtexttable()
    SET.tictable.color = "black"  # "grey"

    # X (bottom) ticks
    # Text Orientation
    SET.xticorientation = vcs.createtextorientation()
    SET.xticorientation.angle = -90  # -70
    SET.xticorientation.halign = "right"
    SET.xticorientation.height = 12
    # Y (vertical) ticks
    SET.yticorientation = vcs.createtextorientation()
    SET.yticorientation.angle = 0
    SET.yticorientation.halign = "right"
    SET.yticorientation.height = 12

    # Parameters
    SET.parameterorientation = vcs.createtextorientation()
    SET.parameterorientation.height = 60
    SET.parametertable = vcs.createtexttable()
    SET.parametertable.color = "blue"

    # We can turn off the "grid"
    SET.draw_mesh = "y"

    # Control color for missing
    SET.missing_color = "light grey"

    # Tics length
    #SET.xtic1.y1 = SET.y1
    #SET.xtic1.y2 = SET.y2
    #SET.ytic1.x1 = SET.x1
    #SET.ytic1.x2 = SET.x2

    # Logo can be a string or an image
    SET.logo = P.PLOT_SETTINGS.logo = os.path.join(egg_path,
                                                   "graphics", "png", "PCMDILogo_300x98px_72dpi.png")
    SET.logo.x = .93
    SET.logo.y = .95
    SET.logo.width = 85

    # Timestamp
    SET.time_stamp = vcs.createtext()
    SET.time_stamp.color = "blue"
    SET.time_stamp.y = [.9]
    SET.time_stamp.x = [.98]
    SET.time_stamp.halign = "right"
    # or we can turn it off
    SET.time_stamp = None

    SET.legend.x1 = .95
    SET.legend.x2 = .97

    # level to use
    SET.levels = [-.7, -.6, -.5, -.4, -.3, -.2, -.1,
                  0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1., 1.1, 1.2, 1.3, 1.4, 1.5]
    SET.levels = [-.5, -.4, -.3, -.2, -.1,
                  0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1., 1.1, 1.2, 1.3, 1.4, 1.5]
    SET.levels = [-1.e20, -.5, -.4, -.3, -.2, -.1,
                  0, .1, .2, .3, .4, .5, 1.e20]

    # Colormap
    #SET.colormap = "inferno"
    vcs.scriptrun(os.path.join(egg_path,
                               "graphics", "vcs", "portraits.scr"))
    SET.colormap = 'bl_rd_12'
    cols = vcs.getcolors(SET.levels, list(range(144, 156)), split=1)
    SET.fillareacolors = cols
    SET.parametertable.expansion = 100

    # colors to use
    # SET.fillareacolors = vcs.getcolors(SET.levels)


def add_extra_vertices(array):
    tmp = array.tolist()
    for i in range(array.shape[0]):
        tmp2 = tmp[i]
        tmp2[0].append(tmp2[0][-1])
        tmp2[1].append(tmp2[1][-1])
        tmp[i] = tmp2
    return numpy.array(tmp)


def portrait(data, full_dic, targets_template, merge=None, png_file="portrait.png",
             canvas=None, template=None, nodata_png=None, missing_png=None, multiple=1.1):
    x_key = data.getAxis(-1).id
    y_key = data.getAxis(-2).id
    yax = [full_dic.get(s, s)+"  " for s in data.getAxis(-2)]
    xax = [full_dic.get(s, s)+"   " for s in data.getAxis(-1)]
    # Preprocessing step to "decorate" the axes on our target variable
    if canvas is None:
        x = vcs.init(bg=True, geometry=(1200, 800))
    else:
        x = canvas
    P = Portrait()
    setup_portrait(P)
    P.decorate(data, yax, xax)

    mesh, template, meshfill = P.plot(
        data, x=x, template=template, multiple=multiple)

    x.png(png_file)

    targets, tips, extras = click_plots.createModalTargets(data, targets_template, x_key, y_key, full_dic, merge=merge,
                                                           nodata_png=nodata_png, missing_png=missing_png)

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

    print("OK CONCATENATING:", click_areas.shape,
          click_labels_x.shape, click_labels_y.shape)
    # when using multiple we have different shapes so we need to "extend"
    if click_areas.shape[-1] > click_labels_x.shape[-1]:
        # ok more vertices in click area
        print("trust thing")
        click_labels_x = add_extra_vertices(click_labels_x)
        click_labels_y = add_extra_vertices(click_labels_y)
    elif click_areas.shape[-1] < click_labels_x.shape[-1]:
        # ok less vertices in click area
        print("second thing")
        click_areas = add_extra_vertices(click_areas)

    print("OK CONCATENATING:", click_areas.shape,
          click_labels_x.shape, click_labels_y.shape)
    clicks = numpy.concatenate((click_areas, click_labels_x, click_labels_y))
    targets = numpy.concatenate((targets, targets_lbls_x, targets_lbls_y))
    tips = numpy.concatenate((tips, tips_lbls_x, tips_lbls_y))
    extras = numpy.concatenate((extras, extras_lbls_x, extras_lbls_y))

    return clicks, targets, tips, extras, x
