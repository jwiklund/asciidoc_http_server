A web server for asciidoc files
===============================

This project aims to be a python based asciidoc web server which turns asciidoc
text files into html code on the fly.
Its being started like this:

`asciidoc_http_server --port 8080 --root /path/to/asciidoc/files`

If you now browse localhost:8080/ you will be provided with a list of links
representing asciidoc files (ending with '.asciidoc.txt') located in 
_/path/to/asciidoc/files_.

By navigating to one of these links asciidoc will be started on the fly
returning a html rendered web page.

use cases
---------

* make your asciidoc content available on the web
* have a lightweight wiki like system together with synchronize tools like
  dropbox or sparkleshare
* quick evaluate your current changes on asciidoc files in a browser

wish list
---------

* switch between source/html
* support generated files like for plantuml
* support more markup languages like e.g. markdown
* online asciidoc editing (like a wiki)
* support "real" http servers like apache or nginx

