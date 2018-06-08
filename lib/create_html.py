import os
import sys
import shutil


def createModalTargets(data, targets_template, season=""):
    # Season is optional. If used, we expect a single string value that indicates the season
    # Axes have been "decorated" via P.decorate()
    outs = []  # list of target html files
    tips = []  # list of tooltips
    extras = []  # list of extra attributes for "area" tags
    flt = data.ravel()
    indx = 0
    # Y axis

    variable_list = data.getAxis(0).id.split("___")
    model_list = data.getAxis(-1).id.split("___")
    for variable_index, variable in enumerate(variable_list):
        targets_template.variable = variable
        # X axis
        for model_index, model in enumerate(model_list):
            targets_template.model = model
            fnm = targets_template()
            # Here we test if
            outs.append(fnm)
            image = outs[-1].replace("html", "png")
            value = flt[0]
            # Each area must know which areas are next to it so the modal can traverse them
            # We assign an id of the form "model-variable-season" to each area
            # We then save neightbor ids in "data-" tags that the javascript will use to traverse by model/variable/etc...
            model_left = model_list[model_index-1]+"-" + \
                variable+"-"+season if model_index != 0 else ""
            model_right = model_list[model_index+1]+"-"+variable + \
                "-"+season if model_index+1 < len(model_list) else ""
            variable_left = model+"-" + \
                variable_list[variable_index-1]+"-" + \
                season if variable_index != 0 else ""
            variable_right = model+"-" + \
                variable_list[variable_index+1]+"-" + \
                season if variable_index+1 < len(variable_list) else ""
            tips.append("Model: %s<br>Variable: %sValue: %.3g<div id='thumbnail'><img src='%s' width=200></div>" %
                        (model, variable, value, image))
            html_id = "{}-{}-{}".format(model, variable, season)
            extras.append("id='{}' data-value='{}' data-image='{}'"
                          "data-model='{}' data-modelLeft='{}' data-modelRight='{}'"
                          "data-variable='{}' data-variableLeft='{}' data-variableRight='{}'"
                          "data-season='{}'"  # data-seasonLeft='{}' data-seasonRight='{}'"
                          .format(html_id, value, image, model, model_left, model_right, variable, variable_left, variable_right, season))
            indx += 1
    return outs, tips, extras


def write_modal_html(html_file, map_element, share_pth):
    print "TIPS AND MAPPER:", share_pth+"/mapper.js"
    if not os.path.exists(share_pth):
        os.makedirs(share_pth)
    for file in ["mapper.js", "modal.js", "cvi_tip_lib.js", "tooltip.css"]:
        shutil.copy2(os.path.join(sys.prefix, "share", "vcs", file), share_pth)
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
