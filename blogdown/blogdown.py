"""
blogdown
"""
import os

from tinydb import TinyDB

from bottle import request, route, run, view,\
            static_file, install, TEMPLATE_PATH


####### PATH CONSTANTS #######
THIS_FILE = os.path.dirname(__file__)

TEMPLATE_DIR = os.path.join(THIS_FILE, "template")

DIRS = os.path.join(TEMPLATE_DIR, "dirs")

CSS_PATH = os.path.join(TEMPLATE_DIR, 'css')

JS_PATH = os.path.join(TEMPLATE_DIR, 'js')

IMG_PATH = os.path.join(TEMPLATE_DIR, 'img')

###ADD TO BOTTLE.PY TEMPLATE##
TEMPLATE_PATH.insert(0, TEMPLATE_DIR)
##### END PATH CONSTANTS #####


def load_tinydb_plugin(callback):
    def wrapper(*args, **kwargs):
        """
        Get site's file/folder structure
        """
        folders = [f for f in os.listdir(DIRS)]
        #for db in
        kwargs['folders'] = folders
        return callback(*args, **kwargs)
        #db = TinyDB('./db/posts.json')
    return wrapper

#install(load_tinydb_plugin)

@route('/', apply=[load_tinydb_plugin])
@view('index.html')
def index(folders):
    """
    Return index.html
    """
    devmode = True
    return {'navmenu':folders, 'devmode':devmode}


@route('/posts')
@view('posts.html')
def posts():
    """
    Return posts.html
    """
    return


@route('/static')
@view('static.html')
def static():
    """
    # TODO
    """
    return


@route('/css/<path:path>')
def css(path):
    """
    Return static css files
    """
    return static_file(path, CSS_PATH)


@route('/js/<path:path>')
def js(path):
    """
    Return static css files
    """
    return static_file(path, JS_PATH)


@route('/img/<path:path>')
def img(path):
    """
    Return static img files
    """
    return static_file(path, IMG_PATH)


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


run(host='localhost', reloader=True, port=8088, debug=True)


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
