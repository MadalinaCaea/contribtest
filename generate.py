# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import jinja2 as j2
import json
import sys

log = logging.getLogger(__name__)


def list_files(folder_path):
    # takes a folder path and iterates over its files, selecting only rst files
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        # yield os.path.join(folder_path, name), base
        yield folder_path+'/'+name, base


def read_file(file_path):
    # takes a file path to a document that contains data to be rendered
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line.rstrip('\n\r\t')
    return json.loads(raw_metadata), content


def write_output(name, html, *args):
    # takes a name and the html generated and creates the proper static page
    # TODO should not use sys.argv here, it breaks encapsulation
    if not os.path.exists(args[0]):
        os.makedirs(args[0])
    with open(os.path.join(args[0], name+'.html'),'w') as f:
        f.write(html)


def generate_site(folder_path, *args):
    # takes a folder path containing the data and the layout for the site
    # takes the folder where the pages will be created
    # creates a jinja environment, generates the site from the data and the layout
    log.info("Generating site from %r", folder_path)
    jinja_env = j2.Environment(loader=j2.FileSystemLoader(os.path.join(folder_path,'layout')))
    for file_path, name in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(**data)
        write_output(name, html, args[0])
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    logging.basicConfig()
    main()
