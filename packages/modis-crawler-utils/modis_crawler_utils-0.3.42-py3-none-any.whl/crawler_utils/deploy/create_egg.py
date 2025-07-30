import configparser
import errno
import glob
import os
import shutil
import sys
import tempfile
from subprocess import check_call

from setuptools import find_packages

setup_py = 'setup.py'


def retry_on_eintr(function, *args, **kw):
    """Run a function and retry it while getting EINTR errors"""
    while True:
        try:
            return function(*args, **kw)
        except IOError as e:
            if e.errno != errno.EINTR:
                raise


def get_value_from_file(file_name, error_message):
    result = None
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            result = f.read()
    except:
        print(error_message)

    return result


def get_args(kwargs):
    name = kwargs.get('name', None)
    if not name:
        raise ValueError('argument "name" must be filled')

    config = configparser.ConfigParser()
    config.read('scrapy.cfg')
    settings = config['settings']['default']

    extra_data_files = kwargs.get('data_files', '').split(",")

    extra_files = list(filter(lambda file: os.path.exists(file),
                              extra_data_files + ['VERSION', 'args_and_settings.json', 'Pipfile', 'Pipfile.lock',
                                                  'pyproject.toml', 'poetry.lock']))

    return {
        'name': name,
        'version': kwargs.get('version', get_value_from_file("VERSION",
                                                             "file with crawler version was not found")),
        'description': kwargs.get('description', None),
        'long_description': kwargs.get('long_description',
                                       get_value_from_file("README.md",
                                                           "file with long description was not found")),
        'long_description_content_type': kwargs.get('long_description_content_type', None),
        'url': kwargs.get('url', None),
        'author': kwargs.get('author', 'MODIS @ ISP RAS'),
        'author_email': kwargs.get('author_email', 'yatskov@ispras.ru'),
        'maintainer': kwargs.get('maintainer', 'Yatskov Alexander'),
        'maintainer_email': kwargs.get('maintainer_email', 'yatskov@ispras.ru'),
        'packages': kwargs.get('packages', find_packages()),
        'data_files': [('', extra_files)],
        'install_requires': kwargs.get('install_requires', None),
        'python_requires': kwargs.get('python_requires', '>=3.6'),
        'license': kwargs.get('license', 'BSD'),
        'classifiers': kwargs.get('classifiers', None),
        'entry_points': kwargs.get('entry_points', {'scrapy': ['settings = ' + settings]})
    }


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
        kwargs = get_args(
            {kw[0]: kw[1] for kw in [ar.split('=') for ar in argv if ar.find('=') > 0]})
    else:
        kwargs = get_args(argv)

    print("INFO - args parsed successfully")

    create_setup_file(kwargs)
    print("INFO - setup.py created")

    temp_dir = tempfile.mkdtemp(prefix="building-egg-")
    out = open(os.path.join(temp_dir, "stdout"), "wb")
    err = open(os.path.join(temp_dir, "stderr"), "wb")
    retry_on_eintr(check_call,
                   [sys.executable, 'setup.py', 'clean', '-a', 'bdist_egg', '-d', temp_dir],
                   stdout=out, stderr=err)
    out.close()
    err.close()
    egg = glob.glob(os.path.join(temp_dir, '*.egg'))[0]
    shutil.copyfile(egg, kwargs.get('name') + ".egg")
    print("INFO - egg file created")


def create_setup_file(args):
    setup_file = open(setup_py, "w")
    setup_file.write('#!/usr/bin/env python\nfrom setuptools import setup\n\n')
    setup_file.write('setup(\n')
    for arg in args:
        arg_value = args.get(arg)
        if arg_value:
            if isinstance(arg_value, list) or isinstance(arg_value, dict):
                setup_file.write(arg + "=" + str(arg_value) + ",\n")
            elif "\n" in arg_value:
                setup_file.write(arg + "='''" + str(arg_value) + "''',\n")
            else:
                setup_file.write(arg + "='" + str(arg_value) + "',\n")
    setup_file.write(')')


if __name__ == '__main__':
    main()
