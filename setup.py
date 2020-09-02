
from setuptools import setup, find_packages
from os import path

# extract version
path = path.realpath('laser_pointer/_version.py')
version_ns = {}
with open(path, encoding="utf8") as f:
    exec(f.read(), {}, version_ns)
version = version_ns['__version__']

setup(
    name="laser_poitner",
    version=version,
    packages=find_packages(),
    install_requires = [
        'matplotlib',
        'mpl-interactions>=0.5.2'
    ],
    author          = 'Ian Hunt-Isaak',
    author_email    = 'ianhuntisaak@gmail.com',
    license         = 'BSD',
    platforms       = "Linux, Mac OS X, Windows",
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Matplotlib'
    ],
    url = 'https://github.com/hekstra-lab/laser-pointer',
)