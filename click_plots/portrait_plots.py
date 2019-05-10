from pcmdi_metrics.graphics.portraits import Portrait
import vcs
import click_plots
import numpy
import pkg_resources
import os

egg_path = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse("pcmdi_metrics"), "share/pmp")


def reverse(inverted, value):
    if value in inverted:  # ok it was an updated name
        return inverted[value]
    else:
        return value


def add_extra_vertices(array):
    tmp = array.tolist()
    for i in range(array.shape[0]):
        tmp2 = tmp[i]
        tmp2[0].append(tmp2[0][-1])
        tmp2[1].append(tmp2[1][-1])
        tmp[i] = tmp2
    return numpy.array(tmp)


class ClickablePortrait(Portrait):
    def __init__(self, *args, **kargs):
        super(ClickablePortrait, self).__init__(*args, **kargs)
        SET = self.PLOT_SETTINGS
        # Viewport on the Canvas
        SET.x1 = .20  # .05
        SET.x2 = .90
        SET.y1 = .2
        SET.y2 = .8

        #va = .01
        # SET.x1 = 0.05 #  .1
        # SET.x2 = .85  #.85
        #SET.y1 = .6 + va
        #SET.y2 = .9 + va

        # SET.xtic2.y1=P.PLOT_SETTINGS.y1
        # SET.xtic2.y2=P.PLOT_SETTINGS.y2
        # SET.ytic2.x1=P.PLOT_SETTINGS.x1
        # SET.ytic2.x2=P.PLOT_SETTINGS.x2

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
        SET.logo = os.path.join(egg_path, "graphics",
                                "png", "PCMDILogo_300x98px_72dpi.png")
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
        self.nodata_png = kargs.get("nodata_png", os.path.join(
            click_plots.click_egg_path, "nodata.png"))
        self.missing_png = kargs.get("missing_png", os.path.join(
            click_plots.click_egg_path, "missing.png"))

    def plot(self, data, full_dic, merge=None,
             template=None, multiple=1.1,
             sector=None):

        yax = [full_dic.get(s, s)+"  " for s in data.getAxis(-2)]
        xax = [full_dic.get(s, s)+"   " for s in data.getAxis(-1)]

        # Preprocessing step to "decorate" the axes on our target variable
        # It DOES modify the data axes
        self.decorate(data, yax, xax)

        mesh, template, meshfill = super(ClickablePortrait, self).plot(
            data, template=template, multiple=multiple)

        png_file = self.png_template()
        self.x.png(png_file)

        # targets, tips, extras = click_plots.createModalTargets(data, self.targets_template, x_key, y_key, full_dic, merge=merge, sector=sector)
        targets, tips, extras, tips_lbls_x, extras_lbls_x, tips_lbls_y, extras_lbls_y = self.createModalTargets(
            data, full_dic, merge=merge, sector=sector)
        # Creates clickable polygons numpy arrays
        click_areas = vcs.utils.meshToPngCoords(mesh, template, [
            meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
        click_labels_x = vcs.utils.axisToPngCoords([], meshfill, template, 'x1', [
            meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
        click_labels_y = vcs.utils.axisToPngCoords([], meshfill, template, 'y1', [
            meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)

        targets_lbls_x = [
            meshfill.xticlabels1[k] for k in sorted(meshfill.xticlabels1)]
        targets_lbls_y = [
            meshfill.yticlabels1[k] for k in sorted(meshfill.yticlabels1)]
        # when using multiple we have different shapes so we need to "extend"
        if click_areas.shape[-1] > click_labels_x.shape[-1]:
            # ok more vertices in click area
            click_labels_x = add_extra_vertices(click_labels_x)
            click_labels_y = add_extra_vertices(click_labels_y)
        elif click_areas.shape[-1] < click_labels_x.shape[-1]:
            # ok less vertices in click area
            click_areas = add_extra_vertices(click_areas)

        clicks = numpy.concatenate(
            (click_areas, click_labels_x, click_labels_y))
        targets = numpy.concatenate((targets, targets_lbls_x, targets_lbls_y))
        tips = numpy.concatenate((tips, tips_lbls_x, tips_lbls_y))
        extras = numpy.concatenate((extras, extras_lbls_x, extras_lbls_y))

        return clicks, targets, tips, extras

    def createModalTargets(self, data, update_names, merge=None, sector=None):

        # Data went throught decorate function so ids names are all messed
        # But original_id was  preserved here
        # Season is optional. If used, we expect a single string value that indicates the sector
        # Axes have been "decorated" via self.decorate()
        x_key = data.getAxis(-1).original_id
        y_key = data.getAxis(-2).original_id

        outs = []  # list of target html files
        tips = []  # list of tooltips
        extras = []  # list of extra attributes for "area" tags
        xouts = []
        xextras = []
        youts = []
        yextras = []
        flt = data.ravel()
        inverted = {v: k for k, v in update_names.items()}
        indx = 0

        yaxis_list = data.getAxis(0).id.split("___")
        xaxis_list = data.getAxis(-1).id.split("___")
        x_keys = x_key.split("_")
        y_keys = y_key.split("_")
        if sector is not None:
            s_key = sector.id
            s_value = getattr(self.targets_template, s_key)
            s_index = sector[:].tolist().index(s_value)
            if s_index == len(sector)-1:
                sec_right = sector[0]
            else:
                sec_right = sector[s_index+1]
            sec_left = sector[s_index-1]
        else:
            s_key = ""
            s_value = ""
            sec_right = ""
            sec_left = ""

        # Y axis
        for y_index, y_value in enumerate(yaxis_list):
            if merge is not None:
                for merger in merge:
                    if merger[0] in y_keys:  # ok it applies
                        values = y_value.split("_")
                        for value, key in zip(values, merger):
                            for template_to_set in [self.targets_template,
                                                    self.xlabels_targets_template,
                                                    self.ylabels_targets_template]:
                                if template_to_set is not None:
                                    setattr(template_to_set, key,
                                            reverse(inverted, value.strip()))
            else:
                for template_to_set in [self.targets_template,
                                        self.xlabels_targets_template,
                                        self.ylabels_targets_template]:
                    if template_to_set is not None:
                        setattr(template_to_set, y_key,
                                reverse(inverted, y_value.strip()))
            # Taking care of ylabels
            if self.ylabels_targets_template is not None:
                youts.append("{}<br><div id='thumbnail'><img src='{}' width=205></div>".format(y_value, self.ylabels_targets_template()))
                yhtml_id = "{}-na-na".format(y_value)
                y_down = yaxis_list[y_index-1]+"-na-na"
                if y_index == len(yaxis_list) - 1:
                    y_up = yaxis_list[0]+"-na-na"
                else:
                    y_up = yaxis_list[y_index+1]+"-na-na"
                yextras.append("id='{}' data-image='{}' "
                                "data-yaxisName='{}'"
                                "data-yaxis='{}' data-yaxisDown='{}' data-yaxisUp='{}' "
                                .format(yhtml_id, self.ylabels_targets_template(),
                                        y_key,
                                        y_value, y_down, y_up))
            else:
                youts.append("{}".format(y_value))
                yextras.append("")
            # X axis
            for x_index, x_value in enumerate(xaxis_list):
                if merge is not None:
                    for merger in merge:
                        if merger[0] in x_keys:  # ok it applies
                            values = x_value.split("_")
                            for value, key in zip(values, merger):
                                for template_to_set in [self.targets_template,
                                                        self.xlabels_targets_template,
                                                        self.ylabels_targets_template]:
                                    if template_to_set is not None:
                                        setattr(template_to_set, key,
                                                reverse(inverted, value.strip()))
                else:
                    for template_to_set in [self.targets_template,
                                            self.xlabels_targets_template,
                                            self.ylabels_targets_template]:
                        if template_to_set is not None:
                            setattr(template_to_set, x_key,
                                    reverse(inverted, x_value.strip()))
                fnm = self.targets_template()
                if y_index == 0:
                    x_left = xaxis_list[x_index-1]+'-na-na'
                    if x_index == len(xaxis_list) - 1:
                        x_right = xaxis_list[0]+'-na-na'
                    else:
                        x_right = xaxis_list[x_index+1]+'-na-na'
                    if self.xlabels_targets_template is not None:
                        xouts.append("{}<br><div id='thumbnail'><img src='{}' width=200></div>".format(x_value, self.xlabels_targets_template()))
                        xhtml_id = "{}-na-na".format(x_value)
                        xextras.append("id='{}' data-image='{}' "
                                        "data-xaxisName='{}'"
                                        "data-xaxis='{}' data-xaxisLeft='{}' data-xaxisRight='{}' "
                                        .format(xhtml_id, self.xlabels_targets_template(),
                                                x_key,
                                                x_value, x_left, x_right))
                    else:
                        xouts.append("{}".format(x_value))
                        xextras.append("")
                # Here we test if
                outs.append(fnm)
                image = outs[-1].replace("html", "png")
                if not os.path.exists(fnm):
                    image = self.missing_png
                value = flt[indx]
                # Each area must know which areas are next to it so the modal can traverse them
                # We assign an id of the form "x_value-y_value" to each area
                # We then save neightbor ids in "data-" tags that the javascript will use to traverse by model/variable/etc...
                x_left = xaxis_list[x_index-1]+"-" + \
                    y_value if x_index != 0 else ""
                x_left += "-{}".format(s_value)
                x_right = xaxis_list[x_index+1]+"-"+y_value \
                    if x_index+1 < len(xaxis_list) else ""
                x_right += "-{}".format(s_value)
                y_down = x_value+"-" + \
                    yaxis_list[y_index-1] \
                    if y_index != 0 else ""
                y_down += "-{}".format(s_value)
                y_up = x_value+"-" + \
                    yaxis_list[y_index+1] \
                    if y_index+1 < len(yaxis_list) else ""
                y_up += "-{}".format(s_value)

                s_right = "{}-{}-{}".format(x_value, y_value, sec_right)
                s_left = "{}-{}-{}".format(x_value, y_value, sec_left)

                if numpy.ma.is_masked(value):
                    image = self.nodata_png
                tips.append("%s: %s<br>%s: %sValue: %.3g<div id='thumbnail'><img src='%s' width=200></div>" %
                            (x_key, x_value, y_key, y_value, value, image))
                html_id = "{}-{}-{}".format(x_value, y_value, s_value)
                extras.append("id='{}' data-value='{}' data-image='{}' "
                              "data-xaxisName='{}' data-yaxisName='{}' data-sectorName='{}' "
                              "data-xaxis='{}' data-xaxisLeft='{}' data-xaxisRight='{}' "
                              "data-yaxis='{}' data-yaxisDown='{}' data-yaxisUp='{}' "
                              "data-sector='{}' data-sectorLeft='{}' data-sectorRight='{}'"
                              .format(html_id, value, image,
                                      x_key, y_key, s_key,
                                      x_value, x_left, x_right,
                                      y_value, y_down, y_up,
                                      s_value, s_left, s_right))
                indx += 1
        return outs, tips, extras, xouts, xextras, youts, yextras
