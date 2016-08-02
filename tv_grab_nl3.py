#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
    SYNOPSIS

    tv_grab_py_API is a pythonAPI that trawls several sources for TV
    programming information and outputs it in XMLTV-formatted output (see
    http://wiki.xmltv.org/index.php/XMLTVFormat). Users of MythTV
    (http://www.mythtv.org) will appreciate the output generated by this
    grabber, because it fills the category fields, i.e. colors in the EPG,
    and has logos for most channels automagically available. Check the
    website below for screenshots.  The newest version of this script can be
    found here:

         https://github.com/tvgrabbers/tvgrabpyAPI/

    USAGE

    Check the web site above and/or run script with --help and start from there

    REQUIREMENTS

    * Python 2.7.9 or higher
    * The pytz module:             http://pypi.python.org/pypi/pytz
    * The requests module:         https://pypi.python.org/pypi/requests
    * The DataTreeGrab module:     https://github.com/tvgrabbers/DataTree/
    * Connection with the Internet

    QUESTIONS

    Questions (and patches) are welcome at:
    https://github.com/tvgrabbers/tvgrabpyAPI/issues
    https://groups.google.com/forum/#!forum/tvgrabnlpy

    UPGRADE NOTES

    If you were using tv_grab_nl from the XMLTV bundle then enable the
    compat flag or use the --compat command-line option.  Otherwise, the
    xmltvid's are wrong and you will not see any new data in MythTV.

    HISTORY

    tv_grab_nl_py used to be called tv_grab_nl_pdb, created by Paul de Bruin
    and first released on 2003/07/09. At the same time the code base switched
    from using CVS to SVN at Google Code, and as a result the version numbering
    scheme has changed. The lastest official release of tv_grab_nl_pdb is 0.48.
    The first official release of tv_grab_nl_py is 6. In 2012, The codebase
    moved to Git, and the version number was changed once more. The latest
    subversion release of tv_grab_nl_py is r109. The first Git release of
    tv_grab_nl_py is 2012-03-11 12:03.

    As of december 2014/ januari 2015 Version 2 a whole new era:
      Upgrading argument processing from getopt to argparse.
      Added genre/subgenre translation table and file (tv_grab_nl_py.set).
        Automatically adding new genre/subgenre combinations on every scan.
        This contains also other translation tables which mostly get updated on
        every scan and gets created with defaults if not existing.
      Added session log function (to the configname with .log added)
        the last log is saved to .old (like with .conf, .opt and .set files)
      Added multiple new sources
      Added ttvdb.com lookup for missing season/episode info
      Added sqlyte caching
      Added multithreading

    In 2016 we are working on transforming tv_grab_nl_py to a generic API:
    tv_grab_py_API which will support multiple frontends. This will move
    tv_grab_nl_py to version 3 and tv_grab_py_API to version 1.

    CONTRIBUTORS

    Main author: Paul de Bruin (paul at pwdebruin dot net)
    Previous maintainer: Freek Dijkstra (software at macfreek dot nl)
    As of 'december 2014':
    Hika van den Hoven hikavdh at gmail dot com, but also active on the
    mythtv list: mythtv-users at mythtv dot org
    Kyle Luna, who especially worked hard on aligning the sources

    Michel van der Laan made available his extensive collection of
    high-quality logos that is used by this script.

    Several other people have provided feedback and patches:
    Huub Bouma, Michael Heus, Udo van den Heuvel, Han Holl, Hugo van der Kooij,
    Roy van der Kuil, Ian Mcdonald, Dennis van Onselen, Remco Rotteveel, Paul
    Sijben, Willem Vermin, Michel Veerman, Sietse Visser, Mark Wormgoor.

    LICENSE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Python 3 compatibility
from __future__ import unicode_literals
# from __future__ import print_function

# Modules we need
import sys, locale, tvgrabpyAPI

try:
    unichr(42)
except NameError:
    unichr = chr    # Python 3

# check Python version
if sys.version_info[:3] < (2,7,9):
    sys.stderr.write("tv_grab_py_API requires Pyton 2.7.9 or higher\n")
    sys.exit(2)

if sys.version_info[:2] >= (3,0):
    sys.stderr.write("tv_grab_py_API does not yet support Pyton 3 or higher.\nExpect errors while we proceed\n")

locale.setlocale(locale.LC_ALL, '')

if tvgrabpyAPI.version()[1:4] < (1,0,1):
    sys.stderr.write("tv_grab_nl3_py requires tv_grab_py_API 1.0.0 or higher\n")
    sys.exit(2)

class Configure(tvgrabpyAPI.Configure):
    def __init__(self):
        # We need these in __init__ to determin log names etc. If not set here we use defaults
        tvgrabpyAPI.Configure.__init__(self, name = 'tv_grab_nl3_py', datafile = 'tv_grab_nl')
        # Version info and description from the frontend as returned by the version function
        self.country = 'The Netherlands'
        self.description = 'Dutch/Flemish grabber combining multiple sources.'
        self.major = 3
        self.minor = 0
        self.patch = 1
        self.patchdate = u'20160619'
        self.alfa = False
        self.beta = True
        # The default timezone to use in the xmltv output file. Can be overruled in the users configuration.
        self.opt_dict['output_tz'] = 'Europe/Amsterdam'
        # Where to get the json datafile and updates (if different from the API location)
        self.source_url = 'https://raw.githubusercontent.com/tvgrabbers/sourcematching/master'
        self.update_url = 'https://github.com/tvgrabbers/tvgrabpyAPI/releases/latest'
        self.compat_text = '.tvgids.nl'

# end Configure()

# allow this to be a module
if __name__ == '__main__':
    config = Configure()
    x = tvgrabpyAPI.grabber_main(config)
    config.close()
    sys.exit(x)
