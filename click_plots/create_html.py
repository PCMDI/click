import os
import shutil
import vcs
import pkg_resources
import warnings
import genutil

click_egg = pkg_resources.resource_filename(
    pkg_resources.Requirement.parse("click_plots"), "share/click_plots")


def write_modal_html(html_file, map_element, share_pth, pathout, modal=None, title="Clickable Portrait Plots", toggle_image=None, png_template=genutil.StringConstructor("clickable_portraits%(colormap).png"), description=None):
    full_share_path = os.path.join(pathout, share_pth)
    if not os.path.exists(full_share_path):
        os.makedirs(full_share_path)
    for file in ["mapper.js", "cvi_tip_lib.js", "tooltip.css"]:
        shutil.copy2(os.path.join(vcs.vcs_egg_path, file), full_share_path)
    shutil.copy(os.path.join(click_egg,"js","toggle_image.js"), full_share_path)
    if modal is not None:
        if not os.path.exists(modal):
            warnings.warn(
                "Could not locate your modal file {}, falling back on default".format(modal))
            modal = os.path.join(click_egg, "js", "modal.js")
    else:
        modal = os.path.join(click_egg, "js", "modal.js")
    shutil.copy2(modal, full_share_path)

    with open(html_file, "w") as f:
        f.write("<html><head>")
        f.write('<script src="https://code.jquery.com/jquery-3.4.1.min.js" crossorigin="anonymous"></script>')
        f.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>')
        f.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">')
        f.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>')
        f.write(
            '<script type="text/javascript" src="%s/modal.js"></script>' % share_pth)
        if toggle_image is not None:
            f.write(
                "<script type='text/javascript' src='%s/toggle_image.js'></script>" % share_pth)
        f.write(
                "<script type='text/javascript' src='%s/mapper.js'></script>" % share_pth)
        f.write(
            "<script type='text/javascript' src='%s/cvi_tip_lib.js'></script>" % share_pth)
        f.write(
            '<link rel="stylesheet" type="text/css" href="%s/tooltip.css" />' % share_pth)
        f.write('<script type="text/javascript">')
        f.write('<!--')
        f.write('window.onload=function() {')
        f.write('    toggle_image.add(document.getElementById("wrapper"),options);')
        f.write('};')
        f.write('-->')
        f.write('</script>')
        f.write("</head><body>")
        f.write("<h1>{}</h1>".format(title))

        # description
        if description is not None:
            f.write("<style>p.description {margin-left: 25px;}</style>")
            f.write("<p class=description>"+description+"</p>")

        # toggle image button
        f.write("<style>p.button {margin-left: 25px;}</style>")
        f.write("<p class=button>Colormaps: ")
        if toggle_image is not None:
            for name in toggle_image:
                if name == "default":
                    png_template.colormap = ""
                else:
                    png_template.colormap = "_" + name
                f.write('<button onclick="changeColormap(\'{0}\')" id="{1}">{1}</button>'.format(png_template(),name))
            f.write("<br></p>")

        f.write(map_element)
        # f.write("$('area').hover(function(){$(this).css('border','5px');},function(){$(this).css('border','0px');});")
        f.write("</body></html>")
