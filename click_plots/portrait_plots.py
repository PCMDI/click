from pcmdi_metrics.graphics.portraits import Portrait
import datetime
import vcs
import click_plots
import numpy
import pkg_resources
import os
import warnings

egg_path = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse("pcmdi_metrics"), "share/pmp")


def generate_thumbnail(image, size):
    thumb = list(os.path.splitext(image))
    thumb[0] = thumb[0]+"_thumb"
    thumb = "".join(thumb)
    if not os.path.exists(thumb):
        try:
            from PIL import Image
        except ImportError:
            warnings.warn("Could not find pillow module, will use original")
            return image
        img = Image.open(image)
        img.thumbnail([int(x) for x in size.split("x")])
        img.save(thumb, "png")
    return thumb


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

        # Logo can be a string or an image
        SET.logo = kargs["logo"]
        SET.logo.x = kargs["logo_x"]
        SET.logo.y = kargs["logo_y"]
        SET.logo.width = kargs["logo_width"]

        # Timestamp
        if kargs["time_stamp"]:
            SET.time_stamp = vcs.createtext()
            SET.time_stamp.color = "darkblue"
            SET.time_stamp.y = [.95]
            SET.time_stamp.x = [.98]
            SET.time_stamp.halign = "right"
        else:
            # or we can turn it off
            SET.time_stamp = None

        SET.legend.x1 = .95
        SET.legend.x2 = .97

        # level to use
        SET.levels = [-1.e20, -.5, -.4, -.3, -.2, -.1,
                      0, .1, .2, .3, .4, .5, 1.e20]

        # Colormap
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

    def cleanup_image(self, image, thumbnail=False):
        if (image.find("://") != -1 or os.path.exists(image)) and thumbnail:
            image = generate_thumbnail(image, self.thumbnails_size)
        if image.find("://") == -1 and not os.path.exists(image):
            image = self.missing_png
        return self.cleanup(image)

    def cleanup(self, target):
        if target is None:
            return
        if self.web_root is not None and self.local_root is not None:
            target = target.replace(self.local_root, self.web_root)
        return target

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
        targets, tips, extras, tips_lbls_x, extras_lbls_x, tips_lbls_y, extras_lbls_y = self.createModalTargets(
            data, full_dic, merge=merge, sector=sector)
        # Creates clickable polygons numpy arrays
        click_areas = vcs.utils.meshToPngCoords(mesh, template, [
            meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
        click_labels_x1 = vcs.utils.axisToPngCoords([], meshfill, template, 'x1', [
            meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
        click_labels_x2 = vcs.utils.axisToPngCoords([], meshfill, template, 'x2', [
            meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
        click_labels_x = numpy.concatenate((click_labels_x1, click_labels_x2))
        targets_lbls_x = [
            meshfill.xticlabels1[k] for k in sorted(meshfill.xticlabels1)] 
        targets_lbls_x += [
            meshfill.xticlabels2[k] for k in sorted(meshfill.xticlabels2)] 
        if self.ylabels_tooltips_images_template is not None:
            click_labels_y1 = vcs.utils.axisToPngCoords([], meshfill, template, 'y1', [
                meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
            click_labels_y2 = vcs.utils.axisToPngCoords([], meshfill, template, 'y2', [
                meshfill.datawc_x1, meshfill.datawc_x2, meshfill.datawc_y1, meshfill.datawc_y2], png=png_file)
            targets_lbls_y = [
                meshfill.yticlabels1[k] for k in sorted(meshfill.yticlabels1)]
            targets_lbls_y += [
                meshfill.yticlabels2[k] for k in sorted(meshfill.yticlabels2)]
            click_labels_y = numpy.concatenate((click_labels_y1, click_labels_y2))

        # when using multiple we have different shapes so we need to "extend"
        if click_areas.shape[-1] > click_labels_x.shape[-1]:
            # ok more vertices in click area
            click_labels_x = add_extra_vertices(click_labels_x)
        elif click_areas.shape[-1] < click_labels_x.shape[-1]:
            # ok less vertices in click area
            click_areas = add_extra_vertices(click_areas)
        if self.ylabels_tooltips_images_template is not None:
            if click_areas.shape[-1] > click_labels_y.shape[-1]:
                click_labels_y = add_extra_vertices(click_labels_y)
            elif click_areas.shape[-1] < click_labels_y.shape[-1]:
                # ok less vertices in click area
                click_areas = add_extra_vertices(click_areas)

        clicks = click_areas
        if self.xlabels_tooltips_images_template is not None:
            clicks = numpy.concatenate((clicks, click_labels_x))
            targets = numpy.concatenate((targets, targets_lbls_x))
            tips = numpy.concatenate((tips, tips_lbls_x, tips_lbls_x))
            extras = numpy.concatenate((extras, extras_lbls_x, extras_lbls_x))
        if self.ylabels_tooltips_images_template is not None:
            clicks = numpy.concatenate((clicks, click_labels_y))
            targets = numpy.concatenate((targets, targets_lbls_x))
            tips = numpy.concatenate((tips, tips_lbls_y, tips_lbls_y))
            extras = numpy.concatenate((extras, extras_lbls_y, extras_lbls_y))

        print("OUT:", clicks.shape, targets.shape, tips.shape, extras.shape)
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
        
        yaxis_list = [y.strip() for y in yaxis_list]
        xaxis_list = [x.strip() for x in xaxis_list]

        x_keys = x_key.split("_")
        y_keys = y_key.split("_")
        if sector is not None:
            s_key = sector.id
            s_value = getattr(self.cell_tooltips_images_template, s_key)
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
                            for template_to_set in [self.cell_tooltips_images_template,
                                                    self.cell_modal_images_template,
                                                    self.cell_modal_json_template,
                                                    self.xlabels_tooltips_images_template,
                                                    self.xlabels_modal_images_template,
                                                    self.ylabels_tooltips_images_template,
                                                    self.ylabels_modal_images_template,
                                                    ]:
                                if template_to_set is not None:
                                    setattr(template_to_set, key,
                                            reverse(inverted, value.strip()))
            else:
                for template_to_set in [self.cell_tooltips_images_template,
                                        self.cell_modal_images_template,
                                        self.cell_modal_json_template,
                                        self.xlabels_tooltips_images_template,
                                        self.xlabels_modal_images_template,
                                        self.ylabels_tooltips_images_template,
                                        self.ylabels_modal_images_template,
                                        ]:
                    if template_to_set is not None:
                        setattr(template_to_set, y_key,
                                reverse(inverted, y_value.strip()))
            # Taking care of ylabels
            if self.ylabels_tooltips_images_template is not None:
                image = self.cleanup_image(
                    self.ylabels_tooltips_images_template(), self.thumbnails)
                youts.append(self.cleanup(self.ylabels_tooltips_html_template().format(
                    value=y_value, image=image)))
                yhtml_id = "{}-na-na".format(y_value)
                y_down = yaxis_list[y_index-1]+"-na-na"
                if y_index == len(yaxis_list) - 1:
                    y_up = yaxis_list[0]+"-na-na"
                else:
                    y_up = yaxis_list[y_index+1]+"-na-na"
                yextras.append("id='{}' data-image='{}' "
                               "data-yaxisName='{}'"
                               "data-yaxis='{}' data-yaxisDown='{}' data-yaxisUp='{}' "
                               .format(yhtml_id, self.cleanup_image(self.ylabels_modal_images_template()),
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
                            # temporaray solution start -- variable_region of mean climate
                            if len(merger) == 2 and len(values) == 3:
                                value0 = x_value.split("_")[0]
                                value1 = x_value.split(value0 + '_')[1]
                                values = [value0, value1]
                            # temporary solution end -- jwlee
                            for value, key in zip(values, merger):
                                for template_to_set in [self.cell_tooltips_images_template,
                                                        self.cell_modal_images_template,
                                                        self.cell_modal_json_template,
                                                        self.xlabels_tooltips_images_template,
                                                        self.xlabels_modal_images_template,
                                                        self.ylabels_tooltips_images_template,
                                                        self.ylabels_modal_images_template,
                                                        ]:
                                    if template_to_set is not None:
                                        setattr(template_to_set, key,
                                                reverse(inverted, value.strip()))
                else:
                    for template_to_set in [self.cell_tooltips_images_template,
                                            self.cell_modal_images_template,
                                            self.cell_modal_json_template,
                                            self.xlabels_tooltips_images_template,
                                            self.xlabels_modal_images_template,
                                            self.ylabels_tooltips_images_template,
                                            self.ylabels_modal_images_template,
                                            ]:
                        if template_to_set is not None:
                            setattr(template_to_set, x_key,
                                    reverse(inverted, x_value.strip()))
                if y_index == 0:
                    x_left = xaxis_list[x_index-1]+'-na-na'
                    if x_index == len(xaxis_list) - 1:
                        x_right = xaxis_list[0]+'-na-na'
                    else:
                        x_right = xaxis_list[x_index+1]+'-na-na'
                    if self.xlabels_tooltips_images_template is not None:
                        image = self.cleanup_image(
                            self.xlabels_tooltips_images_template(), self.thumbnails)
                        xouts.append(self.cleanup(self.xlabels_tooltips_html_template().format(
                            value=x_value, image=image)))
                        xhtml_id = "{}-na-na".format(x_value)
                        xextras.append("id='{}' data-image='{}' "
                                       "data-xaxisName='{}'"
                                       "data-xaxis='{}' data-xaxisLeft='{}' data-xaxisRight='{}' "
                                       .format(xhtml_id, self.cleanup_image(self.xlabels_modal_images_template()),
                                               x_key,
                                               x_value, x_left, x_right))
                    else:
                        xouts.append("{}".format(x_value))
                        xextras.append("")
                # Here we test if
                fnm_tip = self.cleanup(self.cell_tooltips_images_template())
                outs.append(fnm_tip)
                modal_image = self.cell_modal_images_template()
                modal_image = self.cleanup_image(
                    modal_image.replace("html", "png"), self.thumbnails)
                image = self.cell_tooltips_images_template().replace("html", "png")
                image = self.cleanup_image(image, self.thumbnails)
                value = flt[indx]
                # Each area must know which areas are next to it so the modal can traverse them
                # We assign an id of the form "x_value-y_value" to each area
                # We then save neightbor ids in "data-" tags that the javascript will use
                # to traverse by model/variable/etc...
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
                    modal_image = self.nodata_png
                tips.append(self.cleanup(self.cell_tooltips_html_template().format(
                    x_key=x_key, x_value=x_value, y_key=y_key, y_value=y_value, value=value, image=image)))
                html_id = "{}-{}-{}".format(x_value, y_value, s_value)
                json_pth = self.cleanup(self.cell_modal_json_template())
                extras.append("id='{}' data-value='{}' data-image='{}' "
                              "data-xaxisName='{}' data-yaxisName='{}' data-sectorName='{}' "
                              "data-xaxis='{}' data-xaxisLeft='{}' data-xaxisRight='{}' "
                              "data-yaxis='{}' data-yaxisDown='{}' data-yaxisUp='{}' "
                              "data-sector='{}' data-sectorLeft='{}' data-sectorRight='{}' "
                              "data-json='{}'"
                              .format(html_id, value, modal_image,
                                      x_key, y_key, s_key,
                                      x_value, x_left, x_right,
                                      y_value, y_down, y_up,
                                      s_value, s_left, s_right,
                                      json_pth))
                indx += 1
        return outs, tips, extras, xouts, xextras, youts, yextras
