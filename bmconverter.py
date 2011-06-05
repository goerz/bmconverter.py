#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   Copyright (C) 2011  Michael Goerz
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
This script converts between the bookmark description formats used by different
pdf and djvu bookmarking tools such as pdftk, the iText toolbox, pdfLaTeX,
pdfWriteBookmarks, jpdftweak, djvused, and the DJVU Bookmark Tool.

It operates on text files in the various supported formats that describe the
bookmark structure in pdf or djvu files. You can then use the aforementioned
tools to add the described bookmarks to the pdf or djvu file.

In addition to converting between the different formats, the script can also
shift the page numbers associated with the bookmarks. This is useful if you need
to work on a file obtained from a table of contents, where the page numbers in
the pdf might not match the page numbers in the original document, for example.

When used as a module from python, this script provides a toolbox for making
 arbitrary modifications to the bookmark data

Script Usage
============

Usage: bmconverter.py options inputfile [outputfile]


Command Line Options
====================

 --mode in2out        Sets the script's operation mode. This option is required.
 -m  in2out           Short for --mode

 --offset integer     Shifts all pagenumber by integer
 -o integer           Short for --offset

 --long               When used with the 'text' output format, enables the use
                      of full destinations, instead of just page numbers
 -l                   Short for --long

 --help               Displays this message
 -h                   Short for -help

In the mode option, 'in' and 'out' can be any of the supported formats:
'xml', 'text', 'pdftk', 'csv', 'djvused', 'latex', or 'html'

Additionally, 'in' can be 'pdf', in which case the bookmarks are read directly
from the given pdf file. The pdfminer library must be installed for this to
work.

An example usage is 'bmconverter.py --offset 2 --mode xml2text bm.xml bm.txt'

All data is read and written in UTF-8 encoding, with the exception of xml files,
which are read in the encoding declared in their header, but always written in
UTF-8


The XML Format
==============

The XML format supports more of the pdf bookmark than any of the other tools.
It is used by the iText toolbox.

Two examples of such XML files would be

<?xml version="1.0" encoding="ISO8859-1"?>
<Bookmark>
   <Title Action="GoTo" Page="1 XYZ 300 800 0" >root
     <Title Action="GoTo" Open="false" Page="1 FitH 500" >sub 1
       <Title Action="GoTo" Page="1 FitBV 100" >sub 2.1</Title>
       <Title Action="GoTo" Page="1 Fit" >sub 2.2</Title>
     </Title>
     <Title Action="GoTo" Page="1 FitR 200 300 400 500" >sub 2</Title>
   </Title>
</Bookmark>


<?xml version="1.0" encoding="ISO8859-1"?>
<Bookmark>
   <Title Action="GoTo" Named="Title" >Go to the top of the page</Title>
   <Title Color="0 0.50196 0.50196" Style="bold" >
     Toggle the state of the answers</Title>
   <Title Open="false" >Useful links
     <Title Action="URI" URI="http://www.lowagie.com/iText" >
       Bruno&apos;s iText site</Title>
     <Title Action="URI" URI="http://itextpdf.sourceforge.net/" >
       Paulo&apos;s iText site</Title>
     <Title Action="URI" URI="http://sourceforge.net/projects/itext/" >
       iText @ SourceForge</Title>
   </Title>
   <Title >&#48712;&#51665;</Title>
   <Title Action="GoTo" Style="italic" Page="2 FitB" >
     What&apos;s on page 2?</Title>
</Bookmark>

For more details, see the iText documentation.


The Text Format
===============

The text format's purpose is to provide a format that is easier to write by hand
than the XML format that iText can put in a PDF file. The text format cannot
handle all the features the XML format can. It is intended to be used for only
basic bookmarks: a hirarchy of bookmarks, each pointing a page, without further
formatting, external destinations, etc.

The format is used by the pdfWriteBookmarks tool.

The format of the text file is simple: each bookmark is represented by a single
line. The bookmark's level is taken from the indentation. There must be exactly
4 spaces indentation per level. Next is the title of the Bookmark, then a double
colon, and lastly the pagenumber, optionally followed by a destination.

An example bookmark text file is:


Page 1 :: 1
Page 2 :: 2 XYZ null null null
Page 3 :: 3
Sublevels on page 4 :: 4
    Sub1 :: 5 XYZ 0 10 null
    Sub2 :: 5 XYZ 0 20 null
    Sub3 :: 6 XYZ 0 30 null
        SubSub1 :: 6
        SubSub2:: 6
    Sub4 :: 7
        SubSub1 :: 8
        SubSub2 :: 9
    Sub5 :: 10
Page 11 :: 11

Specifically, each line is matched by the following regular expression:

      (?P<indent>\s*)
      (?P<text>\S.*)   ::  [ ]*  (?P<page>[0-9]*)
      [ ]* (?P<dest> (XYZ.*) | (Fit.*))?  [ ]*

The full destinations (e.g. 'XYZ 0 10 null') are only printed if if the --long
option is used.

Note that this format is very limited: it does not express actions other than
GoTo, preserve leading or trailing whitespace in a title, or express titles
that consist only of whitespaces.


The pdftk Format
===============

In the pdftk format, each bookmark is described by three lines, like this:

BookmarkTitle: Page1
BookmarkLevel: 1
BookmarkPageNumber: 1

Lines not belonging to this structure are discarded.
The format is the direct output of the pdftk utility, when run as
#> pdftk file.pdf dumpdata


The html Format
===============

This format is a HTML file with a special structure. Such files are produced by
Adobe Acrobat when you export a PDF file to HTML. They are also used as the
input for the DJVU Bookmark Tool.

An example of the format is the following:

  <html>
  <body>
  <ul>
    <li><a href="#1">Link to page 1</a></li>
    <li><a href="#2">Link to page 2</a></li>
    <li><a href="#3">Chapter 1</a>
      <ul>
        <li><a href="#4">Link to page 4</a></li>
        <li><a href="#5">Link to page 5</a></li>
      </ul>
    </li>
    <li><a href="">Chapter 2, no link here</a>
      <ul>
        <li><a href="#6">Subsection</a>
          <ul>
            <li><a href="#7">Link to page 7</a></li>
            <li><a href="#8">Link to page 8</a></li>
          </ul>
        </li>
        <li><a href="#9">Link to page 9</a></li>
      </ul>
    </li>
    <li><a href="book.djvu#10">Link to page 10 in book.djvu</a></li>
    <li><a href="http://windjview.sourceforge.net">Web link</a></li>
  </ul>
  </body>
  </html>


The csv Format
==============

The csv format is read and writen by the jpdftweak program. Each bookmark is a
line of fields seperated by semicolon. Specifically, the structure of each line
is described by the following extended regular expression:

    (?P<depth>         -?[0-9]+);
    (?P<flags>         O?B?I?);    # open, bold, italic
    (?P<title>         [^;]*);
    (?P<page>          -?[0-9]+)
    (?P<destination>   [ ][^;]+)?  # e.g. FitBV 100
    (?P<moreopts>      ;[^;]*)?    # key1=value1 key2=value2 ...

moreopts keys can be:
  Action        if action is not GoTo
  File          for GoToR actions
  Page          for GoToR actions (the page group is 0 in this case,
                Page consists of page number and destination)
  URI           for URI actions
  Color

Also, the contents of all fields in the csv is escaped: all nonprintable
characters (ascii < 32) and the characters [\:"'] are replaced by '\HH', where
HH is the two digit ascii hex code (in upper case) for that character.


The djvused Format
==================

This format is read and written by the djvused program.

The outline syntax is a single list of the form

(bookmarks ...)

The first element of the list is symbol bookmarks. The subsequent elements are
lists representing the toplevel outline entries. Each outline entry is
represented by a list with the following form:

(title url ... )

The string title is the title of the outline entry. The string url is composed
of the hash character ("#") followed by either the component file identifier or
the page number corresponding to the outline entry. The remaining expressions
describe subentries of this outline entry.

An example of the format is the following:

(bookmarks
 ("level1"
  "#1"
  ("level2"
   "#11"
   ("level3"
    "#20" ) ) )
 ("Bookmark \\"In Quotes\\""
  "../external.djvu#2"
  ("Unicode \\303\\215\\303\\261\\305\\244\\304\\230\\320"
   "www.google.com" ) ) )

Note how the target url can be the pagenumber, an external reference, or a url.
Quotes inside the title have to be escaped. Non-ascii characters are written as
escaped octal UTF-8


The latex Format
================

The latex format results in  a standalone tex file that adds the bookmarks to
the target pdf when compiled with pdflatex (after a few edits). This is
possible by using the pdfpages, hyperref, and bookmark packages. See especially
the documentation of the bookmark package to see how bookmarks are expressed.

An example of the format is the following:

\\bookmark[view={XYZ null null null}, page=1,level=0]{level 1 bookmark}

For parsing the latex format, each \\bookmark entry must be written entirely
one a single line


Interactive Usage
=================
This script was designed to provide a toolbox for working on bookmark
structures when used as module from Python.

The Bookmark class is the central data structure, representing a bookmark tree.
Each nodes holds all the attributes of the bookmark, and a list of all its
children. A number of methods is provided to modify the tree structure.

Note that each bookmark tree has a dummy root, which does not hold any data
(and is ignored in output)

The Tree is iterable in a preorder traversion.

For more information, read the Bookmark class documentation.

Apart from the Bookmark data structure, the module provides importers and
exporters for all the supported formats.

An example of an interactive usage is shown below. It reads the bookmark
structure from a text file, sets the appearance of all bookmarks at a level
deeper than 2 to 'closed' in Acrobat Reader, and write the resulting structure
to an iText xml file.

>>> from bmconverter import *
>>> bm = read_text("bookmarks.txt")
>>> for node in bm:
...     if node.level() > 2:
...         node.open = False
...     else:
...         node.open = True
...
>>> write_xml(bm, "bookmarks.xml")


For the full documentation, run
>>> import bmconverter
>>> help(bmconverter)
inside the python interpretor
"""


import sys
import re
import codecs
from xml.sax import saxutils


def warn(msg):
    """ print a warning message to stderr """
    sys.stderr.write(str(msg))
    sys.stderr.write("\n")

def die(msg):
    """ print a warning message to stderr and exit"""
    sys.stderr.write(str(msg))
    sys.stderr.write("\n")
    exit(2)


def escape_latex(unistring):
    '''Escape a unicode string for LaTeX. '''
    _latex_special_chars = {
        u'$':  u'\\$',
        u'%':  u'\\%',
        u'&':  u'\\&',
        u'#':  u'\\#',
        u'_':  u'\\_',
        u'{':  u'\\{',
        u'}':  u'\\}',
        u'[':  u'{[}',
        u']':  u'{]}',
        u'"':  u"{''}",
        u'\\': u'\\textbackslash{}',
        u'~':  u'\\textasciitilde{}',
        u'<':  u'\\textless{}',
        u'>':  u'\\textgreater{}',
        u'^':  u'\\textasciicircum{}',
        u'`':  u'{}`',   # avoid ?` and !`
    }
    return u''.join(_latex_special_chars.get(c, c) for c in unistring)


class Bookmark:
    """ Tree ADT for the bookmarks

    Every node has the following attributes:
    action       Kind of bookmark (unicode string):
                   "GoTo"    Link to destination in same file (regular)
                   "GoToR"   Link to destination in external file
                   "URI"     Link to an internet address
                   "Launch"  Link to a local file
    title        Title of the Bookmark (unicode string)
    page         Page number the bookmark is pointing to (integer)
    destination  Page Destination (unicode string)
                   The Destination can take the following forms:
                     XYZ left top zoom             Link to position
                     Fit                           Fit page
                     FitH top                      Horiz. Fit
                     FitV left                     Vert. Fit
                     FitR left bottom right top    Fit Rectangle
                     FitB                          Fit Bounding box
                     FitBH top                     Fit bounding box, horiz.
                     FitBV left                    Fit bounding box, vert.
                   left, top zoom, bottom right, left are floats, or 'null'
    named        Named Destination (unicode string)
    namedn       Named Destination, as a name (unicode string)
    file         The file a GoToR or Launch action are referring to
                   (unicode string)
    newwindow    Should file be opened in a new window? (boolean)
    uri          URI that an URI action is referring to (unicode string))
    italic       Should the title be displayed in italics? (boolean)
    bold         Should the title be displayed in bold? (boolean)
    color        Color of the bookmark (unicode string)
    open         Should the bookmark appear open or closed? (boolean)

    There are certain dependencies between the action and the other attributes:

    "Action" = "GoTo" - "Page" | "Named"
        * "Page" = "3 XYZ 70 400 null" - page number followed by a destination
                                                       (/XYZ is also accepted)
        * "Named" = "named_destination"
    "Action" = "GoToR" - "Page" | "Named" | "NamedN", "File", ["NewWindow"]
        * "Page" = "3 XYZ 70 400 null" - page number followed by a destination
                                                   (/XYZ is also accepted)
        * "Named" = "named_destination_as_a_string"
        * "NamedN" = "named_destination_as_a_name"
        * "File" - "the_file_to_open"
        * "NewWindow" - "true" or "false"
    "Action" = "URI" - "URI"
        * "URI" = "http://sf.net" - URI to jump to
    "Action" = "Launch" - "File"
        * "File" - "the_file_to_open_or_execute"

    For the dependencies listed above, cf.
    http://itext.ugent.be/library/api/com/lowagie/text/pdf/SimpleBookmark.html

    For details on the destinations, see p. 552 of the PDF Reference
    http://www.adobe.com/devnet/pdf/pdfs/PDFReference16.pdf

    Bookmark has two compiled regular expressions as class attributes (see
    below) that define the structure of the color attribute and the
    destination attribute, respectively. You can use them to parse the string
    data in these fields.
    The expression for the color is:
            (?P<red>   [0-9]?.?[0-9]+) [ ]+
            (?P<green> [0-9]?.?[0-9]+) [ ]+
            (?P<blue>  [0-9]?.?[0-9]+)
    The expression for the destination is:
            (/?XYZ [ ]*
              (?P<XYZ_left> null | [+-]?[0-9]?.?[0-9]+) [ ]*
              (?P<XYZ_top>  null | [+-]?[0-9]?.?[0-9]+) [ ]*
              (?P<XYZ_zoom> null | [+-]?[0-9]?.?[0-9]+)
            ) |
            (/?Fit) |
            (/?FitH [ ]* (?P<FitH_top>  null | [+-]?[0-9]?.?[0-9]+)) |
            (/?FitV [ ]* (?P<FitV_left> null | [+-]?[0-9]?.?[0-9]+)) |
            (/?FitR [ ]*
              (?P<FitR_left>   null | [+-]?[0-9]?.?[0-9]+) [ ]*
              (?P<FitR_bottom> null | [+-]?[0-9]?.?[0-9]+) [ ]*
              (?P<FitR_right>  null | [+-]?[0-9]?.?[0-9]+) [ ]*
              (?P<RitR_top>    null | [+-]?[0-9]?.?[0-9]+)
            ) |
            (/?FitB) |
            (/?FitBH [ ]* (?P<FitBH_top>  null | [+-]?[0-9]?.?[0-9]+))|
            (/?FitBV [ ]* (?P<FitBV_left> null | [+-]?[0-9]?.?[0-9]+))
    """
    _colorpattern_str = r'''
      (?P<red>   [0-9]?.?[0-9]+) [ ]+
      (?P<green> [0-9]?.?[0-9]+) [ ]+
      (?P<blue>  [0-9]?.?[0-9]+)
    '''
    _destpattern_str = r'''
        (/?XYZ [ ]*
          (?P<XYZ_left> null | [+-]?[0-9]?.?[0-9]+) [ ]*
          (?P<XYZ_top>  null | [+-]?[0-9]?.?[0-9]+) [ ]*
          (?P<XYZ_zoom> null | [+-]?[0-9]?.?[0-9]+)
        ) |
        (/?Fit) |
        (/?FitH [ ]* (?P<FitH_top>  null | [+-]?[0-9]?.?[0-9]+)) |
        (/?FitV [ ]* (?P<FitV_left> null | [+-]?[0-9]?.?[0-9]+)) |
        (/?FitR [ ]*
          (?P<FitR_left>   null | [+-]?[0-9]?.?[0-9]+) [ ]*
          (?P<FitR_bottom> null | [+-]?[0-9]?.?[0-9]+) [ ]*
          (?P<FitR_right>  null | [+-]?[0-9]?.?[0-9]+) [ ]*
          (?P<RitR_top>    null | [+-]?[0-9]?.?[0-9]+)
        ) |
        (/?FitB) |
        (/?FitBH [ ]* (?P<FitBH_top>  null | [+-]?[0-9]?.?[0-9]+))|
        (/?FitBV [ ]* (?P<FitBV_left> null | [+-]?[0-9]?.?[0-9]+))
    '''
    colorpattern = re.compile(_colorpattern_str, re.X)
    destpattern = re.compile(_destpattern_str, re.X)
    def __init__(self):
        self.action = None
        self._level = 0
        self.title  = u""
        self.page   = 0
        self.destination = None
        self.named = None
        self.namedn = None
        self.file = None
        self.newwindow = None
        self.uri = None
        self.italic = False
        self.bold = False
        self.color = None
        self.open = True
        self._children = []
        self._parent = None
        self._childnumber = 0 # the index this node has in its parent's
                              # children array
        self._seen = {} # keeps track of what iterations this node has been seen
                        # in. key is the id of the starting node, value is an
                        # int numbering the iteration.
        self._iteritem = None # the node that the currently running iteration
                              # that started from self is at.
        self._delete = False

    def __setattr__(self, name, value):
        """Enforce integrity of attribute data"""
        if name == 'page':
            if not isinstance(value, int) or (value < 0):
                warn("page must be an integer greater than zero. "
                     +"Set to zero.")
                value = 0
        if name in ['italic', 'bold', 'open', 'newwindow']:
            if not isinstance(value, bool):
                if not ( (name == 'newwindow') and (value is None) ):
                    warn("The attributes 'italic', 'bold', 'open', "
                         + "'newwindow' must be boolean values. "
                         + "%s not set." % name)
                    return None
        if name in ['title', 'file', 'uri', 'destination', 'color', 'action']:
            if value is not None:
                if not isinstance(value, unicode):
                    if name in ['title', 'file', 'uri']:
                        warn("The attribute '%s' " % name \
                             + "must be a unicode string. Trying to convert.")
                    try:
                        value = unicode(value)
                    except UnicodeDecodeError:
                        warn("Could not convert to unicode. " \
                              + "%s not set." % name)
                        return None
        if name == 'action':
            if value not in [None, 'GoTo', 'GoToR', 'URI', 'Launch']:
                warn("%s is not a recognized action. " % value \
                     + "action must be 'GoTo', 'GoToR', 'URI', or 'Launch'. " \
                     + "action not set.")
                return None
        if name == 'destination' and value is not None:
            value = value.strip()
            if not self.destpattern.match(value):
                warn("'%s' is not a valid destination. " % value
                     + "Destinations must have the following pattern:")
                warn(self._destpattern_str)
                warn("Not set.")
                return None
        if name == 'color' and value is not None:
            value = value.strip()
            if not self.colorpattern.match(value):
                warn("'%s' is not a valid color declaration. " % value
                     + "Colors must have the following pattern:")
                warn(self._colorpattern_str)
                warn("Not set.")
                return None
        self.__dict__[name] = value

    def level(self):
        """Return the level this bookmark is in"""
        return self._level

    def children(self):
        """Return a list of all the children"""
        return self._children

    def child(self, i):
        """Return the child with index i or throw an IndexError
        The indexes run from zero to (self.number_of_children()-1). You can also
        use negetive indexes, e.g. i=-1 to address the last child"""
        return self._children[i]

    def parent(self):
        """Return the parent node"""
        return self._parent

    def is_root(self):
        """Check if the node is the root of the bookmark tree"""
        return (self._parent is None)

    def has_children(self):
        """Check if the node has any children"""
        return (len(self._children) > 0)

    def number_of_children(self):
        """Return the number of children"""
        return len(self._children)

    def newchild(self):
        """Create and return a new child.
        """
        child = Bookmark()
        self._children.append(child)
        child._level = self.level() + 1
        child._parent = self
        child._childnumber = len(self._children)-1
        return self.child(-1)

    def set_child(self, i, node):
        """Set the i'th child child to node.
           Raise an IndexError if there is no child with index i
        """
        self._children[i] = node
        oldlevel = node.level()
        node._level = self.level() + 1
        for child in node:
            child._level = self.level() + (child.level() - oldlevel) + 1
        node._parent = self
        node._childnumber = i

    def _obliterate_child(self, childnumber):
        """Remove a child from its parent
        Preferably, use 'delete' and 'flush'
        """
        try:
            # readjust the siblings' childnumbers
            for child in self._children[childnumber:]:
                child._childnumber -= 1
            # cut link to parent
            self.child(childnumber)._parent = None
            # remove from parent's children array
            del self._children[childnumber]
        except IndexError:
            warn("Node does not have a child with index %s" % childnumber)
            warn("Can't delete")

    def __str__(self):
        """The string representation is a multiline listing of all attributes"""
        return ( self.unicode() ).encode('ascii','replace')

    def unicode(self):
        """Return a unicode string representation.
        The unicode string representation is a multiline listing of all
        attributes"""
        s = []
        s.append(u"action      = %s" % self.action)
        s.append(u"level       = %s" % self.level())
        s.append(u"title       = %s" % self.title)
        s.append(u"page        = %s" % self.page)
        s.append(u"destination = %s" % self.destination)
        s.append(u"named       = %s" % self.named)
        s.append(u"namedn      = %s" % self.namedn)
        s.append(u"file        = %s" % self.file)
        s.append(u"newwindow   = %s" % self.newwindow)
        s.append(u"uri         = %s" % self.uri)
        s.append(u"italic      = %s" % self.italic)
        s.append(u"bold        = %s" % self.bold)
        s.append(u"color       = %s" % self.color)
        s.append(u"open        = %s" % self.open)
        s.append(u"childnumber = %s" % self._childnumber)
        s.append(u"length      = %s" % len(self))
        for i in xrange(len(s)):
            s[i] = u"    " * self.level() + s[i] + "\n"
        return ''.join(s)

    def debug(self):
        """Print out a representation of the tree, similar to the text output
        format"""
        if not self.is_root():
            print "    " * ( self.level() - 1 ) \
           + (unicode(self.title)).encode('ascii','replace') + " :: " \
           + str(self.page)
        for child in self.children():
            child.debug()

    def long_debug(self):
        """Print each node in the tree, recursively"""
        self.reset()
        for node in self:
            print str(node)
        self.reset()

    def _obliterate(self):
        """Remove the node from the tree

        Note that you cannot obliterate inside an iterator loop.
        """
        if not self.is_root():
            self._parent._obliterate_child(self._childnumber)

    def delete(self):
        """Flag the node for deletion. You have to call 'flush' to have it
        actually deleted"""
        self._delete = True

    def flush(self):
        """Obliterate all nodes flagged for deletion"""
        self.reset()
        dellist = []
        for node in self:
            if node._delete:
                dellist.append(node)
        self.reset()
        for node in dellist:
            node._obliterate()

    def __iter__(self):
        """The iterator for this class is defined via the next() method"""
        return self

    def next(self):
        """Return the next node in a preorder traversion"""

        def seen_in_run(node, startnode):
            """Checks if the node was seen in the iteration currently running
            from startnode """
            node_iter_nr = node._seen.setdefault(id(startnode), 0)
            return (node_iter_nr >= startnode._seen[id(startnode)])
        def make_seen(node, startnode):
            """Mark node as seen in the iteration currently running from
            startnode """
            node._seen[id(startnode)] = startnode._seen[id(startnode)]

        if self._iteritem is None:
            # start a new iteration run
            self._seen[id(self)] = self._seen.setdefault(id(self), 0) + 1
            self._iteritem = self
        # are there unseen children? If not, find unseen siblings
        if self._iteritem.has_children():
            # finding unseen children is the same as finding the first child's
            # unseen siblings, so we go down one level
            self._iteritem = self._iteritem.child(0)
        # find unseen siblings (i.e. unseen parent's children)
        while not self._iteritem.is_root():
            self._iteritem = self._iteritem.parent()
            if not seen_in_run(self._iteritem.child(-1), self):
                for child in self._iteritem.children():
                    if not seen_in_run(child, self):
                        self._iteritem = child
                        make_seen(self._iteritem, self)
                        return self._iteritem
        # end of iteration
        self.reset()
        raise StopIteration

    def reset(self):
        """Reset the traversion status of the node if it is halfway through an
        iteration run, so that a new iteration can restart"""
        self._iteritem = None

    def shift_pagenumber(self, offset):
        """Shift the pagenumbers in the bookmark tree below this node by the
        specified offset. The starting node is left untouched, except that its
        traversion status is reset.
        """
        self.reset()
        for node in self:
            if isinstance(node.page, int):
                node.page += offset
        self.reset()

    def __iadd__(self, other):
        """Handle the expression 'self += other'
        All the children of other are appended as children of self
        """
        for child in other.children():
            self.newchild()
            self.set_child(-1, child)
        return self

    def __add__(self, other):
        """Handle the expression 'self + other'
        Return a copy of self, with all all the children of other appended as
        children of self
        """
        result = self.copy()
        result += other
        return result

    def __len__(self):
        """Return the number of bookmarks in this tree.
        The root does not count as a bookmark
        """
        l =  len(self._children)
        for child in self._children:
            l += len(child)
        return l

    def has_same_attrs_as(self, other):
        """Test if self has the same attributes as other. This comparison is not
        recursive: self and other can have different children
        """
        result = True
        result &=  (self.action      == other.action)
        result &=  (self.title       == other.title)
        result &=  (self.page        == other.page)
        result &=  (self.destination == other.destination)
        result &=  (self.named       == other.named)
        result &=  (self.namedn      == other.namedn)
        result &=  (self.file        == other.file)
        result &=  (self.newwindow   == other.newwindow)
        result &=  (self.uri         == other.uri)
        result &=  (self.italic      == other.italic)
        result &=  (self.bold        == other.bold)
        result &=  (self.color       == other.color)
        result &=  (self.open        == other.open)
        return result


    def __eq__(self, other):
        """Handle the expression 'self == other'
        Two nodes are equal if all their attributes are equal and all there
        respective children are equal.
        """
        result = ( len(self) == len(other) )
        if result:
            result &= (self.has_same_attrs_as(other))
            if result:
                for (selfchild, otherchild) \
                in zip(self._children, other._children):
                    result &= selfchild.has_same_attrs_as(otherchild)
        return result

    def __ne__(self, other):
        """Handle the expression 'self != other'
        This simply negeates 'self == other'
        """
        return not (self == other)

    def __lt__(self, other):
        """ Handle the expression 'self < other'
        'self < other' is equivalent to 'len(self) < len(other)'"""
        return ( len(self) < len(other) )

    def __le__(self, other):
        """ Handle the expression 'self <= other'
        'self <= other' is equivalent to
        '(len(self) < len(other)) or (self == other)'
        """
        return ( (len(self) < len(other)) or (self == other) )

    def __gt__(self, other):
        """ Handle the expression 'self > other'
        'self > other' is equivalent to 'len(self) < len(other)'"""
        return ( len(self) > len(other) )

    def __ge__(self, other):
        """ Handle the expression 'self >= other'
        'self >= other' is equivalent to
        '(len(self) > len(other)) or (self == other)'
        """
        return ( (len(self) > len(other)) or (self == other) )

    def copy(self):
        """ Return copy """
        newnode = Bookmark()
        newnode.action      = self.action
        newnode.title       = self.title
        newnode.page        = self.page
        newnode.destination = self.destination
        newnode.named       = self.named
        newnode.namedn      = self.namedn
        newnode.file        = self.file
        newnode.newwindow   = self.newwindow
        newnode.uri         = self.uri
        newnode.italic      = self.italic
        newnode.bold        = self.bold
        newnode.color       = self.color
        newnode.open        = self.open
        for child in self.children():
            newnode.newchild()
            newnode.set_child(-1, child.copy())
        return newnode

def usage():
    """Display Program Usage"""
    print """
bmconverter.py
(c) 2007 Michael Goerz - This program is provided under the terms of the GPL.

Usage: bmconverter.py options inputfile [outputfile]


Command Line Options
====================

 --mode in2out        Sets the script's operation mode. This option is required.
 -m  in2out           Short for --mode

 --offset integer     Shifts all pagenumber by integer
 -o integer           Short for --offset

 --long               When used with the 'text' output format, enables the use
                      of full destinations, instead of just page numbers
 -l                   Short for --long

 --help               Displays full help
 -h                   Short for -help

In the mode option, 'in' and 'out' can be any of the supported formats:
'xml', 'text', 'pdftk', 'html', 'djvused', or 'csv'

An example usage is 'bmconverter.py --offset 2 --mode xml2text bm.xml bm.txt'

All data is read and written in UTF-8 encoding, with the exception of xml files,
which are read in the encoding declared in their header, but always written in
UTF-8
"""

def show_help():
    """Display full help"""
    print __doc__

def main():
    """Command line program for converting between bookmark formats"""

    # command line parsing / initialization
    import getopt
    import os.path
    global warn

    if len(sys.argv) < 2:
        usage()
        exit(2)

    try:
        opts, files = getopt.getopt(sys.argv[1:], "hm:o:l",
                                                 ["help", "mode=", "offset=",
                                                  "long"])
    except getopt.GetoptError, details:
        die(details)

    mode = ""
    offset = 0
    text_long = False
    for o, a in opts:
        if o in ("-h", "--help"):
            show_help()
            sys.exit()
        if o in ("-m", "--mode"):
            mode = a
        if o in ("-o", "--offset"):
            try:
                offset = int(a)
            except ValueError:
                die("Offset must be an integer.")
        if o in ("-l", "--long"):
            text_long = True

    # deal with the input- and output file
    if len(files) < 1:
        die("You must provide an input file")
    infilename = files[0]
    if not os.path.isfile(infilename):
        die ("The input file '%s' does not exist" % infilename)
    outfilename = infilename
    if len(files) < 2:
        warn ("You did not provide an output file. "
              +"The input file will be overwritten")
        answer = raw_input("Do you want to overwrite? Yes [No]: ").lower()
        if answer != "yes":
            exit(0)
    else:
        outfilename = files[1]
        if os.path.exists(outfilename):
            warn("The output filename '%s' already exists." % outfilename)
            answer = raw_input("Do you want to overwrite? Yes [No]: ").lower()
            if answer != "yes":
                exit(0)

    # parse the mode, to find out what we have to do
    handlers = {
        'csv'     : (read_csv,     write_csv),
        'html'    : (read_html,    write_html),
        'pdftk'   : (read_pdftk,   write_pdftk),
        'text'    : (read_text,    write_text),
        'xml'     : (read_xml,     write_xml),
        'djvused' : (read_djvused, write_djvused),
        'latex'   : (read_latex,   write_latex),
        'pdf'     : (read_pdf,     None),
    }
    from_format = None
    to_format = None
    mode_pattern = re.compile(r'([a-z]+)2([a-z]+)')
    mode_match = mode_pattern.match(mode)
    if mode_match:
        from_format = mode_match.group(1)
        to_format   = mode_match.group(2)
    else:
        die("Could not get modes. " \
            + "Did you provide the --mode option correctly?\n" \
            + "The correct format is '--mode in2out', where 'in' and 'out' " \
            + "can be 'xml', 'text', 'pdftk', 'html', 'djvused' or 'csv'.")
    from_handler = handlers.setdefault(from_format, (None, None))[0]
    to_handler   = handlers.setdefault(to_format,   (None, None))[1]
    if from_handler is None:
        warn("No Handler for '%s'" % str(from_format))
        die("Did you provide the --mode option correctly?\n" \
            + "The correct format is '--mode in2out', where 'in' and 'out' " \
            + "can be 'xml', 'text', 'pdftk', 'html', 'djvused', or 'csv'.")
    if to_handler is None:
        warn("No Handler for '%s'" % str(to_format))
        die("Did you provide the --mode option correctly?\n" \
            + "The correct format is '--mode in2out', where 'in' and 'out' " \
            + "can be 'xml', 'text', 'pdftk', 'html', 'djvused' or 'csv'.")

    # Execute
    warn("Reading bookmarks in '%s' in %s format" % (infilename, from_format))
    bm = from_handler(infilename)
    if (offset != 0):
        warn("Shifting page-numbers by %i" % offset)
        bm.shift_pagenumber(offset)
    warn("Writing out bookmarks to '%s' in %s format" \
          % (outfilename, to_format))
    if to_format == 'text':
        to_handler(bm, outfilename, text_long)
    else:
        to_handler(bm, outfilename)



def read_xml(infilename):
    """Read in an iText XML file describing the bookmarks, return a root
    bookmark node. The root node itself is empty, and contains all the
    bookmarks as children."""
    root = Bookmark()

    # Define specialized handler class
    from xml.sax import ContentHandler
    class docHandler(ContentHandler):
        def __init__(self, root):
            """Initialize parser state variables """
            self.current_node = root
            self.open_element = ""
        def startElement(self, name, attrs):
            """Hook for opening XML tags """
            if name == "Title":
                self.open_element = name
                self.current_node = self.current_node.newchild()
                node = self.current_node
                node.action = attrs.get("Action", None)
                page = attrs.get("Page", None)
                if (page is not None) and (page.index(" ") >= 0):
                    node.destination = page.split(" ", 1)[1]
                    try:
                        node.page = int(page.split(" ", 1)[0])
                    except ValueError:
                        die("The Page reference '%s' could not be parsed"
                        % page)
                node.named = attrs.get("Named", None)
                node.namedn = attrs.get("NamedN", None)
                node.file = attrs.get("File", None)
                node.newwindow = attrs.get("NewWindow", None)
                node.uri = attrs.get("URI", None)
                style = attrs.get("Style", "").lower()
                if 'italic' in style:
                    node.italic = True
                if 'bold' in style:
                    node.bold = True
                node.color = attrs.get("Color", None)
                if attrs.get("Open", "true").lower() == "false":
                    node.open = False
        def characters(self, content):
            """Hook for XML text data """
            if self.open_element == "Title":
                self.current_node.title += content
        def endElement(self, name):
            """Hook for closing XML tags """
            if name == "Title":
                self.open_element = ""
                linebreak = self.current_node.title.find("\n")
                if linebreak >= 0:
                    self.current_node.title \
                                           = self.current_node.title[:linebreak]
                self.current_node = self.current_node.parent()

    # Create an XML parser
    from xml.sax import make_parser
    parser = make_parser()
    parser.setContentHandler(docHandler(root))

    # Parse the infile;
    try:
        parser.parse(infilename)
    except Exception, data:
        warn("There was a fatal error in parsing the xml file:")
        die(data)

    return root


def write_xml(root, outfilename):
    """Write bookmarks into an iText XML file, encoded in UTF-8"""
    outfile = codecs.open(outfilename, "w", "utf-8")
    def str_bm(node):
        if node.is_root():
            s  = r'<?xml version="1.0" encoding="UTF-8"?>'+"\n"
            s += "<Bookmark>\n"
            for child in node.children():
                s +=  str_bm(child)
            s += "</Bookmark>\n"
        else:
            s  = "  " * node.level()
            s += '<Title'
            if not node.open:
                s += ' Open="%s"'  % (str(node.open).lower())
            if node.action is not None: s += ' Action="%s"' % (node.action)
            if node.action in ['GoTo', 'GoToR']:
                s  += ' Page="%s'  % node.page
                if (node.destination is not None) \
                and (not node.destination == ''):
                    s += ' %s"' % (node.destination)
                else:
                    s += '"'
            if node.color  is not None: s += ' Color="%s"' % (node.color)
            style = ""
            if node.italic:
                style = "italic"
            if node.bold:
                if len(style) > 0: style += " "
                style += "bold"
            if style != "": s += ' Style="%s"' % style
            if node.uri    is not None: s += ' URI="%s"'   \
                      % saxutils.escape(node.uri, {'"':'&quot;', "'": '&apos;'})
            if node.file  is not None: s  += ' File="%s"'  \
                     % saxutils.escape(node.file, {'"':'&quot;', "'": '&apos;'})
            if node.newwindow  is not None:
                s  += ' NewWindow="%s"' % (node.newwindow)
            if node.named is not None: s  += ' Named="%s"' \
                    % saxutils.escape(node.named, {'"':'&quot;', "'": '&apos;'})
            if node.namedn is not None: s  += ' NamedN="%s"' \
                   % saxutils.escape(node.namedn, {'"':'&quot;', "'": '&apos;'})
            s += ' >%s' \
                    % saxutils.escape(node.title, {'"':'&quot;', "'": '&apos;'})
            if node.has_children():
                s += "\n"
                for child in node.children():
                    s +=  str_bm(child)
                s += "  " * node.level()
            s += "</Title>\n"
        return s
    outfile.write(str_bm(root))
    outfile.close()


def read_pdftk(infilename):
    """Read in a pdftk text file describing the bookmarks, return a root
    bookmark node. The root node itself is empty, and contains all the
    bookmarks as children."""
    titlepattern = re.compile(r'BookmarkTitle:\s*(.+)')
    levelpattern = re.compile(r'BookmarkLevel:\s*([0-9]+)\s*')
    pagepattern  = re.compile(r'BookmarkPageNumber:\s*([0-9]+)\s*')
    escape_re = re.compile(r'&#([0-9]+);')
    root = Bookmark()
    current_node = root
    current_level = 0
    infile = codecs.open(infilename, "r", "utf-8")
    line_nr = 0
    title = ""
    level = 0
    page = 0
    for line in infile:
        line_nr += 1
        titlematch = titlepattern.match(line)
        levelmatch = levelpattern.match(line)
        pagematch  = pagepattern.match(line)
        if titlematch:
            title = titlematch.group(1)
            # un-escape non-ascii characters
            def unescape(match):
                """Return the un-escaped replacement for the string matched"""
                number = int(match.group(1))
                return unichr(number)
            while escape_re.search(title):
                title = escape_re.sub(unescape, title)
            title = saxutils.unescape(title, {'&quot;':'"', "&apos;": "'"})
        elif levelmatch:
            level = int(levelmatch.group(1))
        elif pagematch:
            page = int(pagematch.group(1))
            # a pagematch concludes the bookmark, so we can add it to the tree
            if level - current_level > 1:
                die("There's something wrong with the level number"
                    +"at line %s" % line_nr)
            while current_level > level:
                current_node = current_node.parent()
                current_level -= 1
            if level == current_level:
                current_node = current_node.parent()
                current_level -= 1
            current_node = current_node.newchild()
            current_level += 1
            current_node.title       = title.strip()
            current_node.page        = page
            current_node.action      = "GoTo"
        else:
            warn("Ignored line %s. Not parsable" % line_nr)
    infile.close()
    return root


def write_pdftk(root, outfilename):
    """Write bookmarks to a pdftk text file"""
    def escape(source):
        """Receive and return unicode string, convert all non-ascii characters
        (or non-printables) to XML decimal entities"""
        if source is None: return ""
        encoded = []
        for character in source:
            if (ord(character) < 32) or (ord(character) >= 127):
                encoded.append("&#%s;" % ord(character))
            else:
                encoded.append(saxutils.escape(character, {'"':'&quot;'}))
        return (''.join(encoded)).decode('utf-8')
    outfile = codecs.open(outfilename, "w", "utf-8")
    warnings = set()
    for node in root:
        if node.action != 'GoTo':
            warnings.add("WARNING: The pdftk format cannot express bookmarks " \
                + "with actions different from GoTo. The resulting pdftk " \
                + "file will not be an accurate representation of the " \
                + "bookmark structure")
        if (node.color is not None) or (node.bold) or (node.italic):
            warnings.add("WARNING: The pdftk format cannot express formatting")
        if node.destination is not None:
            warnings.add( \
                        "WARNING: The pdftk format cannot express destinations")
        if not node.open:
            warnings.add(\
                        "WARNING: The pdftk format cannot express closed nodes")
        outfile.write(  "BookmarkTitle: %s\n" \
                                % escape( node.title.strip() )  )
        outfile.write("BookmarkLevel: %s\n" % node.level())
        page = node.page
        if page is None: page = 0
        outfile.write("BookmarkPageNumber: %s\n" % page)
    outfile.close()
    for warning in warnings:
        warn("")
        warn(warning)


def read_text(infilename):
    """Read in a text file describing the bookmarks, return a root
    bookmark node. The root node itself is empty, and contains all the
    bookmarks as children."""
    linepattern = re.compile(r'''
      (?P<indent>\s*)
      (?P<text>\S.*)   ::  [ ]*  (?P<page>[0-9]*)
      [ ]* (?P<dest> (XYZ.*) | (Fit.*))?  [ ]*
    ''', re.X)
    root = Bookmark()
    current_node = root
    current_level = 0
    infile = codecs.open(infilename, "r", "utf-8")
    line_nr = 0
    for line in infile:
        line_nr += 1
        match = linepattern.match(line)
        if match:
            indent = match.group('indent')
            level = len(indent.split("    "))
            if level - current_level > 1:
                die("There's something wrong with the indentation "
                    +"at line %s" % line_nr)
            while current_level > level:
                current_node = current_node.parent()
                current_level -= 1
            if level == current_level:
                current_node = current_node.parent()
                current_level -= 1
            current_node = current_node.newchild()
            current_level += 1
            current_node.title       = (match.group('text')).strip()
            try:
                current_node.page        = int((match.group('page')).strip())
            except ValueError:
                warn("page number '%s' in line %s " \
                                    % ((match.group('page')).strip(), line_nr) \
                     +"is not an integer. Setting to 0")

                current_node.page        = 0
            destination = (match.group('dest'))
            if destination is not None:
                current_node.destination = destination.strip()
            current_node.action      = "GoTo"
        else:
            warn("Ignored line %s. Not parsable" % line_nr)
    infile.close()
    return root


def write_text(root, outfilename, long=False):
    """Write bookmarks to a text file"""
    outfile = codecs.open(outfilename, "w", "utf-8")
    warnings = set()
    for node in root:
        title = node.title.strip()
        if title != node.title:
            warnings.add("WARNING: Titles in the text output format will be " \
                + "trimmed")
        if title == '':
            warnings.add("WARNING: The text format cannot express " \
                + "titles consisting only of whitespace. Such titles will be " \
                + "replaced by '_'")
            title = '_'
        if node.action != 'GoTo':
            warnings.add("WARNING: The text format cannot express bookmarks " \
                + "with actions different from GoTo. The resulting text " \
                + "file will not be an accurate representation of the " \
                + "bookmark structure")
        if (node.color is not None) or (node.bold) or (node.italic):
            warnings.add("WARNING: The text format cannot express formatting")
        if not long:
            if (node.destination is not None) or (node.destination != ''):
                warnings.add("WARNING: The text format cannot express " \
                    + "destinations unless you use the --long option")
        if not node.open:
            warnings.add("WARNING: The text format cannot express closed nodes")
        outfile.write("    " * ( node.level() - 1 ))
        outfile.write(title + " :: " + str(node.page))
        if long:
            if (node.destination is not None) and (node.destination != ""):
                outfile.write(" " + node.destination)
        outfile.write("\n")
    outfile.close()
    for warning in warnings:
        warn("")
        warn(warning)


def read_latex(infilename):
    """Read in a latex file describing the bookmarks, return a root
    bookmark node. The root node itself is empty, and contains all the
    bookmarks as children."""
    linepattern = re.compile(r'''
      ^\s*\\bookmark(?P<options>\[.*\])\{(?P<text>.*)\}\s*$
    ''', re.X)
    levelpattern = re.compile(r'[,\[]\s*level\s*=\s*(?P<level>[0-9]+)\s*[,\]]')
    gotorpattern = re.compile(r'[,\[]\s*gotor\s*=\s*(?P<gotor>[^,\]]+)\s*[,\]]')
    namedpattern = re.compile(r'[,\[]\s*named\s*=\s*(?P<named>[^,\]]+)\s*[,\]]')
    uripattern   = re.compile(r'[,\[]\s*uri\s*=\s*(?P<uri>[^,\]]+)\s*[,\]]')
    pagepattern  = re.compile(r'[,\[]\s*page\s*=\s*(?P<page>[0-9]+)\s*[,\]]')
    viewpattern  = re.compile(r'[,\[]\s*view\s*=\s*(?P<view>[^,\]]+)\s*[,\]]')
    destpattern  = re.compile(r'[,\[]\s*dest\s*=\s*(?P<dest>[^,\]]+)\s*[,\]]')
    boldpattern  = re.compile(r'[,\[]\s*bold\s*[,\]]')
    italpattern  = re.compile(r'[,\[]\s*italic\s*[,\]]')
    colorpattern = re.compile(r'''
    [,\[]\s*
    color  \s*=\s*  \[rgb\] \s*
    \{(?P<rgb>[0-9.]+\s*,\s*[0-9.]+\s*,\s*[0-9.]+)\}
    \s*[,\]]
    ''', re.X)
    root = Bookmark()
    current_node = root
    current_level = 0
    infile = codecs.open(infilename, "r", "utf-8")
    line_nr = 0
    for line in infile:
        line_nr += 1
        match = linepattern.match(line)
        if match:
            options = match.group('options')
            # determine level, create appropriate node
            level = 1
            levelmatch = levelpattern.search(options)
            if levelmatch:
                level = int(levelmatch.group('level')) + 1
            if level - current_level > 1:
                die("There's something wrong with the level "
                    +"at line %s" % line_nr)
            while current_level > level:
                current_node = current_node.parent()
                current_level -= 1
            if level == current_level:
                current_node = current_node.parent()
                current_level -= 1
            current_node = current_node.newchild()
            current_level += 1
            # set title
            current_node.title = (match.group('text')).strip()
            # set action and "main" attributes
            gotormatch = gotorpattern.search(options)
            namedmatch = namedpattern.search(options)
            urimatch = uripattern.search(options)
            if gotormatch:
                destmatch = destpattern.search(options)
                if destmatch:
                    current_node.file = destmatch.group('dest')
                else:
                    pagematch = pagepattern.search(options)
                    if pagematch:
                        current_node.page = int(pagematch.group("page"))
                    viewmatch = viewpattern.search(options)
                    if viewmatch:
                        view = viewmatch.group("view")
                        if view.startswith("{"):
                            view = view[1:-1].strip()
                        current_node.destination = view
            elif namedmatch:
                current_node.action = "GoToR"
                current_node.named = namedmatch.group("named")
            elif urimatch:
                current_node.action = "URI"
                current_node.uri = urimatch.group("uri")
            else:
                current_node.action = "GoTo"
                pagematch = pagepattern.search(options)
                if pagematch:
                    current_node.page = int(pagematch.group("page"))
                viewmatch = viewpattern.search(options)
                if viewmatch:
                    view = viewmatch.group("view")
                    if view.startswith("{"):
                        view = view[1:-1].strip()
                    current_node.destination = view
            # set other attributes
            colormatch = colorpattern.search(options)
            if colormatch:
                current_node.color = " ".join([c.strip() for c in
                                     colormatch.group('rgb').split(",")])
            if boldpattern.search(options):
                current_node.bold = True
            if italpattern.search(options):
                current_node.italic = True
    infile.close()
    return root


def write_latex(root, outfilename, long=False, title=None, author=None,
                pdf=None):
    """Write bookmarks to a tex file"""
    outfile = codecs.open(outfilename, "w", "utf-8")
    warnings = set()
    outfile.write("\\documentclass{article}\n")
    outfile.write("\\usepackage[utf8]{inputenc}\n")
    outfile.write("\\usepackage{pdfpages}\n")
    outfile.write("\\usepackage[\n")
    outfile.write("  pdfpagelabels=true,\n")
    if title is not None:
        outfile.write("  pdftitle={%s},\n" % escape_latex(title))
    if author is not None:
        outfile.write("  pdfauthor={%s},\n" % escape_latex(author))
    outfile.write("]{hyperref}\n")
    outfile.write("\\usepackage{bookmark}\n")
    outfile.write("\n")
    outfile.write("\\begin{document}\n")
    outfile.write("\n")
    if pdf is not None:
        outfile.write("\\pagenumbering{roman}\n")
        outfile.write("\\setcounter{page}{1}\n")
        outfile.write("\\includepdf[pages=-]{%s}\n" % pdf)
    else:
        outfile.write("%\\pagenumbering{roman}\n")
        outfile.write("%\\setcounter{page}{1}\n")
        outfile.write("%\\includepdf[pages=-]{file.pdf}\n")
    outfile.write("\n")
    for node in root:
        options = []
        if node.action == 'Launch':
            warnings.add("WARNING: The latex format cannot express the "
                         + "Launch action")
        if node.bold:
            options.append('bold')
        if node.italic:
            options.append('italic')
        if node.color is not None:
            options.append("color=[rgb]{%s}" %  ",".join(node.color.split()))
        if node.destination is not None:
            options.append("view={%s}" % node.destination)
        optstr = ", ".join(options)
        if len(optstr) > 0:
            optstr = optstr + ", "
        outfile.write("    " * ( node.level() - 1 ))
        if node.action == 'GoTo':
            if node.named is None:
                outfile.write('\\bookmark[%spage=%i,level=%i]{%s}'
                % (optstr, node.page, node.level()-1, escape_latex(node.title)))
            else:
                outfile.write('\\bookmark[%sdest=%s,level=%i]{%s}'
                % (optstr, node.named, node.level()-1, node.title))
        elif node.action == 'GoToR':
            if node.named is None:
                outfile.write('\\bookmark[%sgotor=%s, page=%i,level=%i]{%s}'
                % (optstr, node.file, node.page, node.level()-1,
                   escape_latex(node.title)))
            else:
                outfile.write('\\bookmark[%sgotor=%s, dest=%s,level=%i]{%s}'
                % (optstr, node.file, node.named, node.level()-1,
                   escape_latex(node.title)))
        elif node.action == 'URI':
            outfile.write('\\bookmark[%suri=%s,level=%i]{%s}'
            % (optstr, node.uri, node.level()-1, escape_latex(node.title)))
        outfile.write("\n")
    outfile.write("\n")
    outfile.write("\\end{document}\n")
    outfile.close()
    for warning in warnings:
        warn("")
        warn(warning)


def read_html(infilename):
    """Read in an a Djvu html file describing the bookmarks, return a root
    bookmark node. The root node itself is empty, and contains all the
    bookmarks as children."""
    root = Bookmark()

    # Define specialized handler class
    from xml.sax import ContentHandler
    class docHandler(ContentHandler):
        def __init__(self, root):
            """Initialize parser state variables """
            self.current_node = root
            self.open_element = ""
        def startElement(self, name, attrs):
            """Hook for opening XML tags """
            import re
            self.open_element = name
            if name == "li":
                self.current_node = self.current_node.newchild()
            if name == "a":
                node      = self.current_node
                link      = attrs.get("href", None)
                goto_re   = re.compile(r'#([0-9]+)')
                gotor_re  = re.compile(r'(.+)#([0-9]+)')
                goton_re  = re.compile(r'#(.+)')
                gotonr_re = re.compile(r'(.+)#(.+)')
                uri_re    = re.compile(r'(.+)')
                regexes = (goto_re, gotor_re, goton_re, gotonr_re, uri_re)
                for re in regexes:
                    match = re.match(link)
                    if match:
                        if re is goto_re:
                            node.action = "GoTo"
                            node.page = match.group(1)
                            try:
                                node.page = int(node.page)
                            except ValueError:
                                die("The Page reference "
                                    +"'%s' could not be parsed" % node.page)
                        elif re is gotor_re:
                            node.action = "GoToR"
                            node.file = match.group(1)
                            node.page = match.group(2)
                            try:
                                node.page = int(node.page)
                            except ValueError:
                                die("The Page reference "
                                    +"'%s' could not be parsed" % node.page)
                        elif re is goton_re:
                            node.action = "GoTo"
                            node.named = match.group(1)
                        elif re is gotonr_re:
                            node.action = "GoToR"
                            node.file = match.group(1)
                            node.named = match.group(2)
                        elif re is uri_re:
                            node.action = "URI"
                            node.uri = match.group(1)
                        break
        def characters(self, content):
            """Hook for XML text data """
            if self.open_element == "a":
                self.current_node.title += content
        def endElement(self, name):
            """Hook for closing XML tags """
            if name == "li":
                self.open_element = ""
                self.current_node.title = self.current_node.title.strip()
                self.current_node = self.current_node.parent()

    # Create an XML parser
    from xml.sax import make_parser
    parser = make_parser()
    parser.setContentHandler(docHandler(root))

    # Parse the infile;
    try:
        parser.parse(infilename)
    except Exception, data:
        warn("There was a fatal error in parsing the html file:")
        die(data)

    return root


def write_html(root, outfilename):
    """Write bookmarks to a Djvu html file"""
    outfile = codecs.open(outfilename, "w", "utf-8")
    def str_bm(node):
        if node.is_root():
            s  = r'<html>'+"\n"
            s += "<body>\n"
            s += "<ul>\n"
            for child in node.children():
                s +=  str_bm(child)
            s += "</ul>\n"
            s += "</body>\n"
            s += r'</html>'+"\n"
        else:
            s = "  " * node.level()
            s += '<li><a href="'
            if node.action == "GoTo":
                if node.named is not None:
                    s += "#%s" % saxutils.escape(unicode(node.named), \
                                               {'"' : '&quot;', "'" : '&apos;'})
                else:
                    s += "#%s" % node.page
            elif node.action == "GoToR":
                if node.named is not None:
                    s += "%s#%s" % ( saxutils.escape(unicode(node.file), \
                                              {'"' : '&quot;', "'" : '&apos;'}),
                                     saxutils.escape(unicode(node.named), \
                                             {'"' : '&quot;', "'" : '&apos;'}) )
                else:
                    s += "%s#%s" % ( saxutils.escape(node.file, \
                                                  {'"':'&quot;',"'": '&apos;'}),
                                     node.page)
            elif node.action == "URI":
                s += saxutils.escape(unicode(node.uri), \
                                               {'"' : '&quot;', "'" : '&apos;'})
            s += '">%s</a>' % saxutils.escape(node.title)
            if node.has_children():
                s += "\n"
                s += "  " * node.level() + "<ul>\n"
                for child in node.children():
                    s +=  str_bm(child)
                s += "  " * node.level() + "</ul>\n"
                s += "  " * node.level()
            s += "</li>\n"
        return s
    outfile.write(str_bm(root))
    outfile.close()


def read_csv(infilename):
    """Read in an jpdftweak csv file describing the bookmarks, return a root
    bookmark node. The root node itself is empty, and contains all the
    bookmarks as children."""
    linepattern = re.compile(r'''
    (?P<depth>         -?[0-9]+);
    (?P<flags>         O?B?I?);    # open, bold, italic
    (?P<title>         [^;]*);
    (?P<page>          -?[0-9]+)
    (?P<destination>   [ ][^;]+)?  # e.g. FitBV 100
    (?P<moreopts>      ;[^;]*)?    # key1=value1 key2=value2 ...
    ''', re.X)
    def unescape(s):
        """Undo the escape scheme used in the csv:
        All nonprintable characters (ascii < 32) and the characters [\:"'] are
        replaced by '\HH', where HH is the two digit ascii hex code (in upper
        case) for that character.
        """
        if s is None: return None
        result = ""
        i = 0
        while i < len(s):
            c = s[i]
            if c == "\\":
                hexcode = s[i+1:i+3]
                result += chr(int(hexcode, 16))
                i+=2
            else:
                result += c
            i += 1
        return result
    def parse_moreopts(s):
        """Parse the list of moreopts into a dictionary
        s is the direct, unescaped value of the moreopts group
        """
        # this implementation is a direct translation of the java code used in
        # the jpdftweak program itself. I think it might have a bug in handling
        # quotes that might appear inside the file attribute, but I'll stick to
        # the original implementation anyway
        result = {}
        if s is None: return result
        s = (unescape(s[1:])).strip()
        while len(s) > 0:
            pos = s.find("=\"")
            key = s[0:pos]
            value = ""
            s = s[pos+2:]
            while True:
                pos = s.find('"')
                if (pos < len(s)-1) and (s[pos+1] == '"'):
                    value += s[0:pos+1]
                    s = s[pos+2:]
                else:
                    value += s[0:pos]
                    s = s[pos+1:]
                    break
            key = key.lower()
            result[key] = value
            s = s.strip()
        return result
    root = Bookmark()
    current_node = root
    current_level = 0
    infile = codecs.open(infilename, "r", "utf-8")
    line_nr = 0
    for line in infile:
        line_nr += 1
        match = linepattern.match(line)
        if match:
            level = int(match.group("depth"))
            if level - current_level > 1:
                die("There's something wrong with the indentation "
                    +"at line %s" % line_nr)
            while current_level > level:
                current_node = current_node.parent()
                current_level -= 1
            if level == current_level:
                current_node = current_node.parent()
                current_level -= 1
            current_node = current_node.newchild()
            current_level += 1
            current_node.title       = unescape((match.group("title")))
            page = match.group("page")
            if page is not None:
                current_node.page        = int((match.group("page")).strip())
            current_node.destination = match.group("destination")
            if current_node.destination is not None:
                current_node.destination = current_node.destination.strip()
            moreopt_dict = parse_moreopts(match.group("moreopts"))
            current_node.action      = moreopt_dict.setdefault("action", "GoTo")
            current_node.open = ("O" in match.group("flags"))
            if ("B" in match.group("flags")):
                current_node.bold = True
            if ("I" in match.group("flags")):
                current_node.italic = True
            current_node.file = unescape(moreopt_dict.setdefault("file", None))
            current_node.uri = unescape(moreopt_dict.setdefault("uri", None))
            current_node.color = moreopt_dict.setdefault("color", None)
            if moreopt_dict.has_key("page"):
                # This overrides the normal page and destinations
                page = moreopt_dict["page"]
                if (page is not None) and (page.find(" ") >= 0):
                    current_node.destination = page.split(" ", 1)[1]
                    try:
                        current_node.page = int(page.split(" ", 1)[0])
                    except ValueError:
                        die("The Page reference '%s' could not be parsed"
                             % page)
        else:
            warn("Ignored line %s. Not parsable" % line_nr)
    infile.close()
    return root


def write_csv(root, outfilename):
    """Write bookmarks to a jpdftweak csv file"""
    def escape(s):
        """Apply the escape scheme used in the csv:
        All nonprintable characters (ascii < 32) and the characters [\:"'] are
        replaced by '\HH', where HH is the two digit ascii hex code (in upper
        case) for that character.
        """
        import string
        result = []
        for c in s:
            if (ord(c) < 32) or c in "\\;\"'":
                escaped_char = "\\" + (hex(ord(c))[-2:]).upper()
                if escaped_char[1] not in string.hexdigits:
                    escaped_char = escaped_char[0] + "0" + escaped_char[-1]
                result.append(escaped_char)
            else:
                result.append(c)
        return ''.join(result)
    outfile = codecs.open(outfilename, "w", "utf-8")
    for node in root:
        outfile.write(str(node.level()) + ";")
        if node.open:
            outfile.write("O")
        if node.bold:
            outfile.write("B")
        if node.italic:
            outfile.write("I")
        outfile.write(";")
        outfile.write(escape(node.title) + ";")
        if node.action == "GoTo":
            outfile.write(str(node.page))
            if (node.destination is not None) and (node.destination != ""):
                outfile.write(" " + unicode(node.destination))
        else:
            outfile.write("0")
        if (node.action != "GoTo") or (node.file is not None) \
        or (node.uri is not None) or (node.color is not None):
            moreopts_string = ""
            if (node.action != "GoTo") and (node.action is not None):
                moreopts_string += 'Action="' + str(node.action) + '" '
                if node.action in ['GoTo', 'GoToR']:
                    moreopts_string += 'Page="' + str(node.page)
                    if (node.destination is not None) \
                    and (node.destination != ""):
                        moreopts_string += " " + unicode(node.destination)
                    moreopts_string += '" '
            if (node.file is not None):
                moreopts_string += 'File="' + node.file + '" '
            if (node.uri is not None):
                moreopts_string += 'URI="' + node.uri + '" '
            if (node.color is not None):
                moreopts_string += 'Color="' + node.color + '" '
            escaped_moreopts = escape(moreopts_string.strip())
            if escaped_moreopts != "":
                outfile.write(";")
                outfile.write(escape(moreopts_string.strip()))
        outfile.write("\n")
    outfile.close()

def read_djvused(infilename):
    """Read in a djvused text file describing the bookmarks, return a root
    bookmark node. The root node itself is empty, and contains all the
    bookmarks as children."""
    startpattern = re.compile(r'\s*  \(bookmarks  \s*  ', re.X)
    titlepattern = re.compile(r'\s*  \(  "(?P<title> .*)"  \s*  ', re.X)
    targetpattern = re.compile(r'''
        \s*   "(?P<target> .*)"     (?P<endings> ( \s*\) )* )   \s* ''', re.X)
    def unescape(encoded):
        """Receive and return unicode string, unescape all octal-escaped UTF-8
        characters"""
        decoded = encoded.encode('utf-8')
        replacements = {}
        for octc in re.findall(r'\\(\d{3})', decoded):
            replacements[r'\%s' % octc] = chr(int(octc, 8))
        replacements[r'\"'] = '"'
        for code in replacements:
            decoded = decoded.replace(code, replacements[code])
        return decoded.decode('utf8')
    root = Bookmark()
    current_node = None
    infile = codecs.open(infilename, "r", "utf-8")
    line_nr = 0
    for line in infile:
        line_nr += 1
        if startpattern.match(line):
            current_node = root
            continue
        titlepattern_match = titlepattern.match(line)
        if titlepattern_match:
            current_node = current_node.newchild()
            current_node.title = unescape(titlepattern_match.group("title"))
            continue
        targetpattern_match = targetpattern.match(line)
        if targetpattern_match:
            target = targetpattern_match.group("target")
            if target.find("#") < 0: # Target is URI
                current_node.action = "URI"
                current_node.uri = target
            elif re.match(r"#[0-9]+", target): # Target is Page Reference
                current_node.action = "GoTo"
                current_node.page = int(target[1:])
            else: # Target is external
                current_node.action = "GoToR"
                current_node.file = target.split("#")[0]
                current_node.page = target.split("#")[1]
            for i in xrange(targetpattern_match.group("endings").count(")")):
                current_node = current_node.parent()
            continue
        else:
            warn("Ignored line %s. Not parsable" % line_nr)
    infile.close()
    return root

def write_djvused(root, outfilename):
    """Write bookmarks to a djvused text file"""
    def escape(source):
        """Receive and return unicode string, convert all non-ascii characters
        (or non-printables) to octal-escaped UTF-8"""
        if source is None: return ""
        encoded = []
        for character in source:
            if (ord(character) < 32) or (ord(character) >= 127):
                for byte in character.encode('utf8'):
                    encoded.append("\%03o" % ord(byte))
            else:
                if character == '"': character = r'\"'
                encoded.append(character)
        return (''.join(encoded)).decode('utf-8')
    outfile = codecs.open(outfilename, "w", "utf-8")
    def str_bm(node):
        if node.is_root():
            s = ["(bookmarks"]
        else:
            s = ['\n%s("%s"\n' % ( \
                node.level() * " ",  \
                escape(node.title) \
            )]
            target = ""
            if node.action == "GoTo":
                target = "#%s" % node.page
            elif node.action == "GoToR":
                target = "%s#%s" % (unicode(node.file), node.page)
            elif node.action == "URI":
                target = node.uri
            s.append( '%s"%s"' % ( \
                (node.level() + 1) * " ",  \
                escape(target) \
            ) )
        for child in node.children():
            s.append(str_bm(child))
        s.append(" )")
        return ''.join(s)
    outfile.write(str_bm(root))
    outfile.write("\n")
    outfile.close()

def read_pdf(infilename): 
    """ Read bookmarkds directly from a pdf file. Formatting of the bookmark
        titles is disregarded
    """
    try:
        from pdfminer.psparser  import PSKeyword, PSLiteral
        from pdfminer.pdfparser import PDFDocument, PDFParser, \
                                       PDFNoOutlines, PDFDestinationNotFound
        from pdfminer.pdftypes  import PDFStream, PDFObjRef, resolve1, \
                                       stream_value
    except ImportError:
        die("You must install the pdfminer package to read bookmarkds "
            "directly from pdf")
    def resolve_dest(dest):
        if isinstance(dest, str):
            try:
                dest = resolve1(doc.get_dest(dest))
            except PDFDestinationNotFound:
                warn("Destination not found: %s" % dest)
        elif isinstance(dest, PSLiteral):
            dest = resolve1(doc.get_dest(dest.name))
        if isinstance(dest, dict):
            dest = dest['D']
        for i, element in enumerate(dest):
            if str(element) in [r'/XYZ', r'/Fit', r'/FitH', r'/FitV', r'/FitR', 
            r'/FitB', r'/FitBH', r'/FitBV']:
                dest[i] = str(element)[1:] # strip slash
            if element is None:
                dest[i] = 'null'
        return dest
    root = Bookmark()
    current_node = root
    current_level = 0
    doc = PDFDocument()
    fp = file(infilename, 'rb')
    parser = PDFParser(fp)
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    pages = dict( (page.pageid, pageno) 
                  for (pageno,page) in enumerate(doc.get_pages()) )
    try:
        outlines = doc.get_outlines()
    except PDFNoOutlines:
        pass
    for (level,title,dest,a,se) in outlines:
        while current_level > level:
            current_node = current_node.parent()
            current_level -= 1
        if level == current_level:
            current_node = current_node.parent()
            current_level -= 1
        current_node = current_node.newchild()
        current_level += 1
        current_node.title = title
        if a:
            action = a.resolve()
            if isinstance(action, dict):
                subtype = action.get('S')
                if repr(subtype) == '/GoTo':
                    current_node.action = 'GoTo'
                    dest = resolve_dest(action['D'])
                    if type(dest) is str:
                        warn("Named string destinations are not currently"
                             + " supported ('%s')" % title)
                    else:
                        current_node.page = int(pages[dest[0].objid]) + 1
                        if dest is not None:
                            current_node.destination = \
                            u" ".join([str(d) for d in dest[1:]])
                elif repr(subtype) == '/GoToR':
                    current_node.action = 'GoToR'
                    dest = resolve_dest(action['D'])
                    current_node.fileno = int(dest[0])
                    current_node.destination = \
                                           u" ".join([str(d) for d in dest[1:]])
                    current_node.file = unicode(action['F'].resolve()['F'])
                elif repr(subtype) == '/Launch':
                    current_node.action = 'Launch'
                    dest = action['F'].resolve()
                    if repr(dest['Type']) == '/Filespec':
                        current_node.file = unicode(dest['F'])
                    else:
                        die("We can only handle /Launch links to files: %s"
                            % str(dest))
                elif repr(subtype) == '/URI':
                    current_node.action = 'URI'
                    current_node.uri = unicode(action['URI'])
                elif repr(subtype) in ['/Named', '/Sound', '/GotoE', '/Movie',
                '/Hide', '/SubmitForm', '/ResetForm', '/ImportData', 
                '/JavaScript', '/SetOCGState', '/Rendition', '/Trans', 
                '/GoTo3DView']:
                    warn("The %s action is not currently supported ('%s')" 
                         % (repr(subtype), title))
                else:
                    die("Unkown action %s" % subtype)
            else:
                die("Unexpected a -> %s" % action)
        elif dest:
            current_node.action = 'GoTo'
            dest = resolve_dest(dest)
            current_node.page = int(pages[dest[0].objid]) + 1
            current_node.destination = u" ".join([str(d) for d in dest[1:]])
        else:
            warn("level: %s" % level)
            warn("title: %s" % title)
            warn("dest : %s" % dest)
            warn("a    : %s" % a)
            warn("se   : %s" % se)
            die("Can't get action")
    parser.close()
    return root

if __name__ == "__main__":
    main()
