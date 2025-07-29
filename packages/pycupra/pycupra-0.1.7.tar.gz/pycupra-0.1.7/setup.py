import setuptools

# read the contents of your README file
from os import path
from pycupra.__version__ import __version__ as lib_version
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def local_scheme(version):
    return ""

setuptools.setup(
    name='pycupra',
    version=lib_version,
    description='A library to read and send vehicle data via Cupra/Seat portal using the same API calls as the MyCupra/MySeat mobile app.',
    author='WulfgarW',
    #author_email='xxx@googlemail.com',
    url='https://github.com/WulfgarW/pycupra',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    provides=["pycupra"],
    install_requires=list(open("requirements.txt").read().strip().split("\n")),
    #use_scm_version=True,
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=[
        'setuptools_scm',
    ]
)
