import os
import numpy.ma
import shutil
import vcs
import pkg_resources
import warnings

click_egg = pkg_resources.resource_filename(pkg_resources.Requirement.parse("click_plots"), "share/click_plots")


def reverse(inverted, value):
    if value in inverted:  # ok it was an updated name
        return inverted[value]
    else:
        return value

def createModalTargets(data, targets_template, x_key, y_key, update_names,
                       modal=None, merge=None, nodata_png=None, missing_png=None, sector=None):
    # Season is optional. If used, we expect a single string value that indicates the sector
    # Axes have been "decorated" via P.decorate()
    outs = []  # list of target html files
    tips = []  # list of tooltips
    extras = []  # list of extra attributes for "area" tags
    flt = data.ravel()
    inverted = {v: k for k, v in update_names.items()}
    indx = 0
    if nodata_png is None:
        nodata_png = os.path.join(click_egg, "nodata.png")
    if missing_png is None:
        missing_png = os.path.join(click_egg, "missing.png")

    yaxis_list = data.getAxis(0).id.split("___")
    xaxis_list = data.getAxis(-1).id.split("___")
    x_keys = x_key.split("_")
    y_keys = y_key.split("_")
    if sector is not None:
        s_key = sector.id
        s_value = getattr(targets_template, s_key)
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
                        setattr(targets_template, key, reverse(inverted, value.strip()))
        else:
            setattr(targets_template, y_key, reverse(inverted, y_value.strip()))
        # X axis
        for x_index, x_value in enumerate(xaxis_list):
            if merge is not None:
                for merger in merge:
                    if merger[0] in x_keys:  # ok it applies
                        # print("FOUND {} in {}".format(merger[0], y_key))
                        values = x_value.split("_")
                        for value, key in zip(values, merger):
                            # print("SEtting {} to -{}-".format(key, value.strip()))
                            setattr(targets_template, key, reverse(inverted, value.strip()))
            else:
                setattr(targets_template, x_key, reverse(inverted, x_value.strip()))
            fnm = targets_template()
            # Here we test if
            outs.append(fnm)
            image = outs[-1].replace("html", "png")
            if not os.path.exists(fnm):
                image = missing_png
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
            y_left = x_value+"-" + \
                yaxis_list[y_index-1] \
                if y_index != 0 else ""
            y_left += "-{}".format(s_value)
            y_right = x_value+"-" + \
                yaxis_list[y_index+1] \
                if y_index+1 < len(yaxis_list) else ""
            y_right += "-{}".format(s_value)
            
            s_right = "{}-{}-{}".format(x_value, y_value, sec_right)
            s_left = "{}-{}-{}".format(x_value, y_value, sec_left)

            if numpy.ma.is_masked(value):
                image = nodata_png
            tips.append("%s: %s<br>%s: %sValue: %.3g<div id='thumbnail'><img src='%s' width=200></div>" %
                        (x_key, x_value, y_key, y_value, value, image))
            html_id = "{}-{}-{}".format(x_value, y_value, s_value)
            extras.append("id='{}' data-value='{}' data-image='{}' "
                          "data-xaxisName='{}' data-yaxisName='{}' data-sectorName='{}' "
                          "data-xaxis='{}' data-xaxisLeft='{}' data-xaxisRight='{}' "
                          "data-yaxis='{}' data-yaxisLeft='{}' data-yaxisRight='{}' "
                          "data-sector='{}' data-sectorLeft='{}' data-sectorRight='{}'"
                          .format(html_id, value, image,
                                  x_key, y_key, s_key,
                                  x_value, x_left, x_right,
                                  y_value, y_left, y_right,
                                  s_value, s_left, s_right))
            indx += 1
    return outs, tips, extras


def write_modal_html(html_file, map_element, share_pth ,pathout, modal=None):
    full_share_path = os.path.join(pathout, share_pth)
    if not os.path.exists(full_share_path):
        os.makedirs(full_share_path)
    for file in ["mapper.js", "cvi_tip_lib.js", "tooltip.css"]:
        shutil.copy2(os.path.join(vcs.vcs_egg_path, file), full_share_path)
    if modal is not None:
        if not os.path.exists(modal):
            warnings.warn("Could not locate your modal file {}, falling back on default".format(modal))
            modal = os.path.join(click_egg,"js", "modal.js")
    else:
        modal = os.path.join(click_egg,"js", "modal.js")
    shutil.copy2(modal, full_share_path)

    with open(html_file, "w") as f:
        f.write("<html><head>")
        f.write('<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>')
        f.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>')
        f.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">')
        f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>')
        f.write(
            '<script type="text/javascript" src="%s/modal.js"></script>' % share_pth)
        f.write(
            "<script type='text/javascript' src='%s/mapper.js'></script>" % share_pth)
        f.write(
            "<script type='text/javascript' src='%s/cvi_tip_lib.js'></script>" % share_pth)
        f.write(
            '<link rel="stylesheet" type="text/css" href="%s/tooltip.css" />' % share_pth)
        f.write("</head><body>")
        f.write("<h1>Clickable Portraits Plots</h1>")
        f.write(map_element)
        # f.write("$('area').hover(function(){$(this).css('border','5px');},function(){$(this).css('border','0px');});")
        f.write("</body></head></html>")
