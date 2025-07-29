#
#
from pygments import highlight, lexers, formatters
import pickle
import shutil
import glob
import json
import os
import re


def read_file(f, split=False):
    """Read text file.

    :param f: Filename.
    :type f: str

    :return: File content.
    :rtype: Object
    """
    with open(f, 'r') as m:
        data = m.read().splitlines() if split else m.read()

    return data


def write_file(f, c, mode='w', join=False):
    """Write text file.

    :param f: Filename.
    :type f: str

    :param c: Content to write.
    :type c: Object
    """
    if join:
        c = '\n'.join(c)

    with open(f, mode) as m:
        data = m.write(c)

    return None


def read_pickle(f):
    """Read pickle binary file.

    :param f: Filename.
    :type f: str

    :return: File content.
    :rtype: Object
    """
    with open(f, 'rb') as msg:
        c = pickle.load(msg)

    return c


def write_pickle(f, c):
    """Write pickle binary file.

    :param f: Filename.
    :type f: str

    :param c: Content to write.
    :type c: Object
    """
    with open(f, 'wb') as msg:
        pickle.dump(c, msg)

    return None


def write_json(f, c):
    """.
    """
    with open(f, 'w') as msg:
        json.dump(c, msg)

    return None


def read_json(f):
    """.
    """
    with open(f) as msg:
        data = json.load(msg)

    return data


def list_dir(p):
    """.

    :param p: .
    :type p: str

    :return: .
    :rtype: list
    """
    p = os.path.join(p, '*')

    dirs = glob.glob(p)

    dirs = sorted([x for x in dirs if os.path.isdir(x)])

    return dirs


def last_file(p):
    """.

    :param p: .
    :type p: str

    :return: .
    :rtype: str
    """
    files = glob.glob(p)

    file = max(files, key=os.path.getctime)

    return file


def pretty_json(data):
    """.
    """
    print (highlight(json.dumps(data,sort_keys=True,indent=4), lexers.JsonLexer(), formatters.TerminalFormatter()))

    return data


def pysed(f, s, r, d=None):
    """.
    """
    data = read_file(f)
    data = data.replace(s, str(r))

    f = d if d else f

    write_file(f, data)

    return None


def grep(f, s, mode='in', first=False):
    """.
    """
    data = read_file(f, True)

    if mode == 'in':
        data = [x for x in data if s in x]
    elif mode == 'start':
        data = [x for x in data if x.startswith(s)]

    if first:
        data = data[0]

    return data


def mkdir(path):
    """.
    """
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)

    return None


def rmdir(path):
    """.
    """
    if os.path.isdir(path):
        shutil.rmtree(path)

    return None


def rmfile(path):
    """.
    """
    if os.path.isfile(path):
        os.remove(path)

    return None


def sort_anum(data):
    """ Sort the given iterable in the way that humans expect.
    """
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]

    return sorted(data, key = alphanum_key)
