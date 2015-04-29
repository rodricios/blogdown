import os

from tinydb import TinyDB

from bottle import request, route, run, view,\
            static_file, TEMPLATE_PATH


def json_to_html_ul(d,tag=""):
    tag = "<ul>"

    for key in d:
        tag += "<li>" + key

        if type(d[key])==type({}):
            tag += json_to_html_ul(d[key],"") + "</li>"
        else:
            tag += "</li>"

    tag += "</ul>"
    return tag
