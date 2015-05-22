import os
import shutil
import json
import sys

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
        try:
            html_md_text = markdown.markdown(md_text, [ 'markdown.extensions.fenced_code',
                                                        'markdown.extensions.extra',
                                                        'markdown.extensions.codehilite'])
        except UnicodeDecodeError:
            print(path)
            raise
            
    return html_md_text
    
    
def generate_section(files):
    """
    Generate site's subsection. 
    
    Autofill /<section's index.html> with file's "description" parameter.
    A section is determined simply by checking if a "file" (see "files" variable
    in site-variables.json) has the optional parameter "index" set to true. 
    
    If "index" is set to true, then the optional parameter "section" is used to 
    partition the "files" array based off files having the same "section" value.       
    """
    join = os.path.join
    root = sitevars.get('root', "")
    
    root_path = join(THIS_FILE, root)
    
    section_names = set()
    # logic is reversed from the description b/c this makes more sense
    for f in files:
        if "section" in f:
            section_names.add(f["section"])
    
    sections = {name:[] for name in sections_names}
    nonsections = []
    
    for f in files:
        if 'section' in f:
            sections[f['section']].append(f)
        else:
            nonsections.append(f)
    
    '''for section, files in sections:
        # search for index
        with open()
    '''
    
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
        sitevars['site_title'] = md_file['title']
        
        if 'ad' in md_file: 
            sitevars['ad'] = md_file['ad']
               
        with open(html_path, 'w') as index_html:
            html = template('index.tpl', 
                            sitevars=sitevars,
                            body=html_md_text,
                            get_url=get_url)
                            
            index_html.write(html)

gen = generate_static


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

    shutil.copytree(STATIC_DIR, path, 
                    ignore=shutil.ignore_patterns('.git', '.gitignore'))


@route('/css/<path:path>', name='css')
def css(path):
    """
    Return static css files
    """
    return static_file(path, CSS_PATH, mimetype='text/css')

@route('/')
@route('/<path:path>')
#@view('index.html')
def static(path=""):
    """
    # TODO
    """
    print(path)
    path, filename = os.path.split(path)
    if not path:
        path = filename
        filename = "index.html"
        
    print(path, filename)
    #html_md_text = md_to_html(p)
    #return template('index.tpl', sitevars=SITEVARS, body=html_md_text)
    return static_file(filename, os.path.join(STATIC_DIR, path))


if len(sys.argv) == 2 and sys.argv[1]:
    run(host='localhost', reloader=True, port=8088, debug=True)