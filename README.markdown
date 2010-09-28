# bmconverter.py

[http://github.com/goerz/bmconverter.py](http://github.com/goerz/bmconverter.py)

Author: [Michael Goerz](http://michaelgoerz.net)

`bmconverter.py` converts between the bookmark description formats used by
different pdf and djvu bookmarking tools such as [pdftk][1], the [iText
toolbox][2], [pdfWriteBookmarks][3], [jpdftweak][4], [djvused][5], and the
[DJVU Bookmark Tool][6].

This code is licensed under the [GPL](http://www.gnu.org/licenses/gpl.html)

[1]: http://www.accesspdf.com/pdftk/
[2]: http://sourceforge.net/projects/itext/files/
[3]: http://github.com/goerz/pdfWriteBookmarks
[4]: http://jpdftweak.sourceforge.net/
[5]: http://djvu.sourceforge.net/doc/index.html
[6]: http://sourceforge.net/projects/windjview/files/Bookmark%20Tool/

## Install ##

Store the `bmconverter.py` script anywhere in your `$PATH`.

## Usage ##

The script operates on text files in the various supported formats that
describe the bookmark structure in pdf or djvu files. You can then use the
appropriate tools to add the bookmarks to the pdf or djvu file.

In addition to converting between the different formats, the script can also
shift the page numbers associated with the bookmarks. This is useful if you need
to work on a file obtained from a table of contents, where the page numbers in
the pdf might not match the page numbers in the original document, for example.

When used as a module from python, this script provides a toolbox for making
arbitrary modifications to the bookmark data
    
    Usage: bmconverter.py options inputfile [outputfile]
    
    Command Line Options
    
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
    'xml', 'text', 'pdftk', 'csv', 'djvused' or 'html'
    
An example usage is 

    bmconverter.py --offset 2 --mode xml2text bm.xml bm.txt
    
All data is read and written in UTF-8 encoding, with the exception of xml files,
which are read in the encoding declared in their header, but always written in
UTF-8
    
    
### The XML Format ###
    
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
    
    
### The Text Format ###
    
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
    
    
### The pdftk Format ###
    
In the pdftk format, each bookmark is described by three lines, like this:
    
    BookmarkTitle: Page1
    BookmarkLevel: 1
    BookmarkPageNumber: 1
    
Lines not belonging to this structure are discarded.
The format is the direct output of the pdftk utility, when run as
    $ pdftk file.pdf dumpdata
    
    
### The html Format ###
    
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
    
    
### The csv Format ###
    
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
characters (`ascii < 32`) and the characters `[\:"']` are replaced by `\HH`,
where HH is the two digit ascii hex code (in upper case) for that character.
    
    
### The djvused Format ###
    
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
     ("Bookmark \"In Quotes\""
      "../external.djvu#2"
      ("Unicode \303\215\303\261\305\244\304\230\320"
       "www.google.com" ) ) )
    
Note how the target url can be the pagenumber, an external reference, or a url.
Quotes inside the title have to be escaped. Non-ascii characters are written as
escaped octal UTF-8
    
    
### Interactive Usage ###

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

inside the python interpretor.
