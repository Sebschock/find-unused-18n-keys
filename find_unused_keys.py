#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import codecs
import click


@click.command()
@click.option('--path_to_root', '-r', prompt='Path to project',
              help='Path to root directory of project.')
@click.option('--path_to_keys', '-k', prompt='Path to JSON key file',
              help='Path to json i18n file.')
@click.option('--file_format', '-f', multiple=True, default=['.html', '.ts'],
              help='File format to search through'
                   '(e.g. -f .html -.ts)')
def find_unused_keys(path_to_root, path_to_keys, file_format):
    """
    Find unused i18n keys in your project in order to clean up your i18n file.

    The program searches through all files of specified file formats (default
    .ts and .html) in root folder (and subfolders) to find keys from a JSON
    file, that are not used anywhere.


    Example:

    "python find_unused_keys.py -r /user/project -k en.json -f .html -f .ts"
    finds unused keys from 'en.json' in '.html' and '.ts' files in the root
    directory '/user/project'.
    """
    f = Finder(path_to_root, path_to_keys, file_format)
    unused_keys = sorted(f.unused_keys)
    for unused_key in unused_keys:
        click.echo(unused_key)

    click.echo('\nSearched through: %i files' % len(f.file_names))
    click.echo('Found %i unused keys in %s \n' % (len(unused_keys),
                                                  path_to_keys))


class Finder():
    file_names = []
    dirs = []
    keys = []
    result = {}

    def __init__(self, path_to_root, path_to_keys, file_format):
        self.path_to_root = path_to_root
        self.path_to_keys = path_to_keys
        self.file_format = file_format
        self.file_names = []
        self.get_filenames()
        self.get_keys()
        self.find_unused_keys()

    def get_keys(self):
        with open(self.path_to_keys) as keys_file:
            json_keys_file = json.load(keys_file)
            self.keys = json_keys_file.keys()

    def get_filenames(self):
        for path, subdirs, files in os.walk(self.path_to_root):
            for full_file_name in files:
                file_name, file_extension = os.path.splitext(full_file_name)
                if file_extension in self.file_format and \
                        full_file_name != '.DS_Store':
                    self.file_names.append(os.path.join(path, full_file_name))

    def find_unused_keys(self):
        for file_name in self.file_names:
            with codecs.open(file_name, 'r', 'utf-8') as f:
                for line in f:
                    for key in self.keys:
                        if key in line:
                            self.save_line_to_result(key, line, file_name)

    def save_line_to_result(self, key, line, file_name):
        if key not in self.result:
            self.result[key] = {
                "number_of_appearances": 0,
                "file_names": [],
                "lines": []
            }

        self.result[key]["number_of_appearances"] += 1
        self.result[key]["file_names"].append(file_name)
        self.result[key]["lines"].append(line)

    @property
    def unused_keys(self):
        unused_keys = []
        for key in self.keys:
            if key not in self.result:
                unused_keys.append(key)
        return unused_keys

if __name__ == '__main__':
    find_unused_keys()
