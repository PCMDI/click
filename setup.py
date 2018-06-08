from distutils.core import setup
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
f = open("lib/version.py", "w")
print >>f, "__version__ = '%s'" % Version
print >>f, "__git_tag_describe__ = '%s'" % descr
print >>f, "__git_sha1__ = '%s'" % commit
f.close()


packages = {'click_plots': 'lib',
            }
scripts = ['modal/generate_modal.py']

data_files = [
              #('share/click_plots', 'some_file'),
              ]

setup(name='click_plots',
      version=descr,
      author='PCMDI',
      description='tools to click on plots',
      url='http://github.com/PCMDI/click',
      packages=packages.keys(),
      package_dir=packages,
      scripts=scripts,
      data_files=data_files
      )
