# Find unused i18n keys in your project


Python program that searches through all files of specified file formats in a folder (including subfolders) to find and return keys from an internationalisation JSON file, that are not used anywhere.

Build to be used with [ng2-translate](https://github.com/ocombe/ng2-translate) but could be used in many settings.

## Installation

`
pip install -r requirements.txt
`

## Usage

**Help:**

`
python find_unused_keys.py --help
`

**Example:**
Finds unused keys from 'en.json' in '.html' and '.ts' files in the root directory '/user/code/project'.

`
python find_unused_keys.py -r /user/code/project -k en.json -f .html -f .ts
`

Opensourced by [injurymap](https://www.injurymap.com)
