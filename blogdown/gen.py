import os
import shutil
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
    
    
def generate_static(**sitevars):
    # % rebase('base.html', navmenu=navmenu)
    # get root directory of md files
    join = os.path.join
    root = sitevars.get('root', "")
    
    root_path = join(THIS_FILE, root)
    index_md_path = join(root_path, sitevars['index'])
    index_html_path = index_md_path.replace('.md', '.html')
    
    # /root/index.md
    html_md_text = md_to_html(index_md_path)
    #print("html_md_text", html_md_text)
    # /root/index.html
    with open(index_html_path, 'w') as output_file:
        rendered_html = template('index.tpl', sitevars=SITEVARS, 
                                body=html_md_text, get_url=get_url)
        #print("rendered_html", rendered_html)
        output_file.write(rendered_html)
        
    for md_file in sitevars['files']:
        md_path = join(root_path, md_file['path'])
        html_path = md_path.replace('.md', '.html')
        
        html_md_text = md_to_html(md_path)
        
        with open(html_path, 'w') as index_html:
            html = template('index.tpl', 
                            sitevars=sitevars,
                            body=html_md_text,
                            get_url=get_url)
                            
            index_html.write(html)

gen = generate_static


@route('/css/<path:path>', name='css')
def css(path):
    """
    Return static css files
    """
    return static_file(path, CSS_PATH, mimetype='text/css')


def dump(path):
    """Save necessary github-pages files and subfolders to specified path.

    :param path: path where new github-pages will be located
    """
    if os.path.exists(path):
        override = raw_input("\n" + path +
                             " exists already. This action will override " +
                             "the existing folder's contents.\ny/n?\n")

        if override.lower() == "y":
            shutil.rmtree(path)
        else:
            print("Goodbye!")
            sys.exit()

    shutil.copytree(STATIC_DIR, path)
