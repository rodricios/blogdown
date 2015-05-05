"""
blogdown
"""
import os
import json
import markdown
from tinydb import TinyDB
from bottle import request, route, run, view,\
            static_file, install, TEMPLATE_PATH,\
            template, app

get_url = app[0].get_url

####### PATH CONSTANTS #######
THIS_FILE = os.path.dirname(__file__)

TEMPLATE_DIR = os.path.join(THIS_FILE, "template")

STATIC_DIR = os.path.join(THIS_FILE, "static")

DIRS = os.path.join(TEMPLATE_DIR, "dirs")

CSS_PATH = os.path.join(TEMPLATE_DIR, 'css')

FILES_PATH = os.path.join(TEMPLATE_DIR, 'files')

JS_PATH = os.path.join(TEMPLATE_DIR, 'js')

IMG_PATH = os.path.join(TEMPLATE_DIR, 'img')

###ADD TO BOTTLE.PY TEMPLATE##
TEMPLATE_PATH.insert(0, TEMPLATE_DIR)
TEMPLATE_PATH.insert(1, STATIC_DIR)
##### END PATH CONSTANTS #####

###### LOAD SITE-VARIABLES ######
SITEVARS = json.load(open(os.path.join(TEMPLATE_DIR, 'site-variables.json'),'r'))

    
def md_to_html(path):
    """
    Given path(s) to markdown file (as list), return html equivalent.
    """
    with open(path, 'r') as index_md:
        md_text = index_md.read()
        html_md_text = markdown.markdown(md_text)
    return html_md_text
    
    
def load_site_variables(callback):
    def wrapper(*args, **kwargs):
        """
        Get site variables (located in /templates/site-variables.json)
        """
        kwargs['sitevars'] = SITEVARS
        return callback(*args, **kwargs)
    return wrapper


@route('/', apply=[load_site_variables])
@view('index.tpl')
def index(sitevars):
    """
    Return index.tpl
    """
    devmode = True
    return {"devmode": devmode, "sitevars": sitevars}


@route('/posts')
@view('posts.html')
def posts():
    """
    Return posts.html
    """
    return


@route('/static/<path:path>')
def static(path):
    """
    # TODO
    """
    path, filename = os.path.split(path)
    
    #html_md_text = md_to_html(p)
    #return template('index.tpl', sitevars=SITEVARS, body=html_md_text)
    return static_file(filename, os.path.join(STATIC_DIR, path))


@route('/css/<path:path>', name='css')
def css(path):
    """
    Return static css files
    """
    
    return static_file(path, CSS_PATH, mimetype='text/css')


@route('/files/<path:path>')
def files(path):
    """
    Return static file attachments
    """
    return static_file(path, FILES_PATH)


@route('/js/<path:path>')
def js(path):
    """
    Return static css files
    """
    return static_file(path, JS_PATH, mimetype='text/js')


@route('/img/<path:path>')
def img(path):
    """
    Return static img files
    """
    return static_file(path, IMG_PATH)


run(host='localhost', reloader=True, port=8088, debug=True)


@route('/new/<type>/<path:path>')
def new(type, path):
    """
    Client api to make new folder and/or post
    """

    print("making new", type, path)

    if type == "folder":
        folders, filename = os.path.split(path)

        try:
            os.makedirs(os.path.join(DIRS, folders))
            print("created new folder[s]", folders)

        except (WindowsError, Exception):
            print("failed making new folder[s]", folders)
            return {'result':'failure'}

    with open(os.path.join(DIRS, path), 'w') as newfile:
        pass

    print("created new file", path)
    return {'result':'success'}


@route('/save-site')
def save_site():
    """
    # TODO
    """
    site = request.json['site']
    return

def json_to_html_ul(d,tag=""):
    """

    """
    tag = "<ul>"

    for key in d:
        tag += "<li>" + key

        if type(d[key])==type({}):
            tag += json_to_html_ul(d[key],"") + "</li>"
        else:
            tag += "</li>"

    tag += "</ul>"
    return tag
