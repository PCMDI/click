import glob
import json
import os, sys
import pcmdi_metrics
import pcmdi_metrics.graphics.portraits
import genutil
import numpy, MV2
import vcs

inpath = '/work/lee1043/cdat/pmp/pmp_results/tree_v0.3/pmp_v1.1.2/metrics_results/monsoon/monsoon_wang/cmip5/historical/test1/monsoon-wang_CMIP5_historical-regrid2_regrid2_2018-07-19-10-58-22.json'

J = pcmdi_metrics.io.base.JSONs([inpath])

print(J.getAxisIds())

models_list = sorted(J.getAxis("model")[:], key=lambda s:s.lower())
#models_list.remove("observations")
print models_list, len(models_list)

stats_list = sorted(J.getAxis("statistic")[:], key=lambda s:s.lower())
#models_list.remove("observations")
print stats_list, len(stats_list)

dom_list = sorted(J.getAxis("domain")[:], key=lambda s:s.lower())
#models_list.remove("observations")
dom_list.remove('AllMW')
print dom_list, len(dom_list)

drms =J(statistic=["rmsn"],domain=dom_list,model=models_list)(squeeze=1)
dthreat =J(statistic=["threat_score"],domain=dom_list,model=models_list)(squeeze=1)
dthreat = MV2.subtract(1.,dthreat) 

print drms.shape, dthreat.shape

threat_med = genutil.statistics.median(dthreat,axis=0)[0]
t_med = threat_med.filled()
threat_norm = MV2.divide(MV2.subtract(dthreat.filled(),t_med),t_med)
threat_norm = MV2.subtract(1.,dthreat)

rms_med = genutil.statistics.median(drms,axis=0)[0]
rms_med = rms_med.filled()
rms_norm = MV2.divide(MV2.subtract(drms.filled(),rms_med),rms_med)

rms_norm = numpy.transpose(rms_norm)
threat_norm = numpy.transpose(threat_norm)

#x=vcs.init(bg=True,geometry=(1200,600))

x=vcs.init(bg=False,geometry=(1200,1800))

x.scriptrun(
    os.path.join(
        sys.prefix,
        "share",
        "pmp",
        "graphics",
        'vcs',
        'portraits.scr'))

#x.setcolormap("bl_rd_12")
x.setcolormap("blue2orange")

yax = [s.encode('utf-8')+' ' for s in models_list]  # CHANGE FROM UNICODE TO BYTE STRINGS
xax = [s.encode('utf-8')+' ' for s in dom_list]

P = pcmdi_metrics.graphics.portraits.Portrait()
P.PLOT_SETTINGS.xticorientation.height = 12
P.PLOT_SETTINGS.yticorientation.height = 12
SET = P.PLOT_SETTINGS
SET.x1 = .15
SET.x2 = .85
SET.y1 = .65
SET.y2 = .95
SET.levels = [-.3, -.2, -.1,0.,.1,.2,.3]
SET.levels.insert(0,-1.e20)
SET.levels.append(1.e20)

P2 = pcmdi_metrics.graphics.portraits.Portrait()
P2.PLOT_SETTINGS.xticorientation.height = 12
P2.PLOT_SETTINGS.yticorientation.height = 12
SET2 = P2.PLOT_SETTINGS
SET2.x1 = .15
SET2.x2 = .85
SET2.y1 = .15
SET2.y2 = .45
SET2.levels = [-.3, -.2, -.1,0.,.1,.2,.3]
SET2.levels.insert(0,-1.e20)
SET2.levels.append(1.e20)

# Preprocessing step to "decorate" the axis
P.decorate(rms_norm, xax, yax)
P.plot(rms_norm,x=x,bg=0)
P2.decorate(threat_norm, xax, yax)
P2.plot(threat_norm,x=x,bg=0)

header = x.createtext()
header.To.height = 12
header.To.halign = "center"
header.To.valign = "top"
header.x = .5
header.y = .97

header.string = 'RMSE (normalized by median error)'
x.plot(header, bg=0)

header2 = x.createtext()
header2.To.height = 12
header2.To.halign = "center"
header2.To.valign = "top"
header2.x = .5
header2.y = .57

header2.string = '1 - Threat Score (normalized by median error)' 
x.plot(header2, bg=0)



#P.plot(threat_norm,x=x,bg=0)
x.png('crap.png')
