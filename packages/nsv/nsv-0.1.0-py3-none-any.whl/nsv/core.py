from .reader import Reader
from .writer import Writer

def load(file_obj):
    """Load NSV data from a file-like object."""
    r = Reader(file_obj)
    return r.metadata, list(r)

def loads(s):
    """Load NSV data from a string."""
    if s.startswith('---\n'):  # empty head
        header, body = '', s[4:]
    else:
        header, body = s.split(f'\n{META_SEPARATOR}\n', 1)  # will raise ValueError here if no separator
    metadata = []
    for line in header.split('\n'):
        metadata.append(line)
    data = []
    acc = []
    for i, line in enumerate(body.split('\n')[:-1]):
        if line:
            acc.append(Reader.unescape(line))
        else:
            data.append(acc)
            acc = []
    return metadata, data

def dump(data, file_obj, metadata=None):
    """Write elements to an NSV file."""
    w = Writer(file_obj, metadata)
    w.write_rows(data)
    return file_obj

def dumps(data, metadata=None):
    """Write elements to an NSV string."""
    lines = [*(metadata or ()), META_SEPARATOR]
    for i, row in enumerate(data):
        for cell in row:
            lines.append(Writer.escape(cell))
        lines.append('')
    return '\n'.join(lines) + '\n'

META_SEPARATOR = '---'
