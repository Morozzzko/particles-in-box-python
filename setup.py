# -*- coding: utf-8 -*-

from setuptools import setup

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ''

setup(
    name="Particles in Box",
    version="0.1",
    packages=['particles'],
    scripts=['particles.py'],
    requires=['numpy', 'pyside'],
    license="MIT",
    description="A simple tool to visualize granular gas behavior in a box",
    long_description=long_description,
    author="Gennady Gaidukov",
    author_email="",
    url="https://gitlab.com/Morozzzko/particles-in-box",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ]

)
