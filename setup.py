from __future__ import print_function
from setuptools import setup, find_packages
import glob
import subprocess
import os

Version = "0.1.0"
p = subprocess.Popen(
    ("git",
     "describe",
     "--tags"),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
try:
    descr = p.stdout.readlines()[0].strip()
    Version = "-".join(descr.split("-")[:-2])
    if Version == "":
        Version = descr
except:
    descr = Version

p = subprocess.Popen(
    ("git",
     "log",
     "-n1",
     "--pretty=short"),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
try:
    commit = p.stdout.readlines()[0].split()[1]
except:
    commit = ""
f = open("click_plots/version.py", "w")
print("__version__ = '%s'" % Version, file=f)
print("__git_tag_describe__ = '%s'" % descr, file=f)
print("__git_sha1__ = '{}'".format(commit.decode("utf-8")), file=f)
f.close()


packages = find_packages()

scripts = ['modal/generate_modal.py']

data_files = [
              ('share/click_plots/js', ['share/js/modal.js']),
              ('share/click_plots', ['share/template_top.json',
              'share/template_bottom.json', 'share/nodata.png', 'share/missing.png'] ),
              ]

setup(name='click_plots',
      version=descr,
      author='PCMDI',
      description='tools to click on plots',
      url='http://github.com/PCMDI/click',
      packages=packages,
      scripts=scripts,
      data_files=data_files
      )
