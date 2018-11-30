from pcmdi_metrics.graphics.portraits import Portrait
import vcs
import click_plots
import numpy

def portrait(data, full_dic, targets_template, merge=None, png_file="portrait.png", canvas=None, template=None):
    x_key = data.getAxis(-1).id
    y_key = data.getAxis(-2).id
    yax = [full_dic.get(s,s)+"  " for s in data.getAxis(-2)]
    xax = [full_dic.get(s, s)+"   " for s in data.getAxis(-1)]
    # Preprocessing step to "decorate" the axes on our target variable
    if canvas is None:
        x = vcs.init(bg=True, geometry=(1200, 800))
    else:
        x = canvas
    P = Portrait()
    click_plots.setup_portrait(P)
    P.decorate(data, yax, xax)

    mesh, template, meshfill = P.plot(data, x=x, template=template)

    x.png(png_file)

    targets, tips, extras = click_plots.createModalTargets(data, targets_template, x_key, y_key, merge=merge)

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

    return clicks, targets, tips, extras, x
