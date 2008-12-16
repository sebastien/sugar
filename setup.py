#!/usr/bin/python
# Encoding: ISO-8859-1
# -----------------------------------------------------------------------------
# Project           :   Sugar
# -----------------------------------------------------------------------------
# Author            :   Sebastien Pierre                 <sebastien@type-z.org>
# License           :   Revised BSD License
# -----------------------------------------------------------------------------
# Creation date     :   18-Mar-2008
# Last mod.         :   18-Mar-2008
# -----------------------------------------------------------------------------

from distutils.core import setup

NAME        = "Sugar"
VERSION     = "0.8.6"
WEBSITE     = "http://www.ivy.fr/" + NAME.lower()
SUMMARY     = "The Sugar programming language"
DESCRIPTION = """\
Sugar is a new programming language designed to replace JavaScript
for client-side (and server-side) web development. Sugar is inspired by
languages such as Python, Smalltalk, Pascal, Eiffel and Lisp. Sugar can compile
to JavaScript, ActionScript and Python.

Sugar is object-oriented, uses class-based inheritance, and supports many cool
features such as Python-style slicing, pattern matching, closures,
map/filter/reduce syntaxes and optional type checking.
"""

# ------------------------------------------------------------------------------
#
# SETUP DECLARATION
#
# ------------------------------------------------------------------------------

setup(
    name        = NAME,
    version     = VERSION,
    author      = "Sebastien Pierre", author_email = "sebastien@ivy.fr",
    description = SUMMARY, long_description = DESCRIPTION,
    license     = "Revised BSD License",
    keywords    = "programmin language, oop, web, javascript",
    url         =  WEBSITE,
    download_url=  WEBSITE + "/%s-%s.tar.gz" % (NAME.lower(), VERSION) ,
    package_dir = { "": "Sources" },
    package_data= {
    },
    packages    = [
        "sugar"
    ],
    classifiers = [
      "Development Status :: 4 - Beta",
      "Environment :: Console",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: BSD License",
      # TODO: Add more here
      "Natural Language :: English",
      "Operating System :: POSIX",
      "Operating System :: Microsoft :: Windows",
      "Programming Language :: Python",
    ],
    scripts      = ["Scripts/sugar"]
)

# EOF - vim: tw=80 ts=4 sw=4 noet 
