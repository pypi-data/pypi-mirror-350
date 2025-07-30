import os
import tempfile
import time

import nsv
from io import StringIO

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'samples')
SAMPLES_DATA = {
    'empty': (["v:1.0"], []),
    'empty_one': (["v:1.0"], [[]]),
    'empty_two': (["v:1.0"], [[], []]),
    'empty_three': (["v:1.0"], [[], [], []]),
    'basic': (["v:1.0"], [["r1c1", "r1c2", "r1c3"], ["r2c1", "r2c2", "r2c3"]]),
    'comments': (
        ["v:1.0", "# This is a comment", "// Another comment", "-- And another"], [["r1c1", "r1c2"], ["r2c1", "r2c2"]]),
    'empty_fields': (["v:1.0"], [["r1c1", "", "r1c3"], ["r2c1", "", "r2c3"]]),
    'empty_sequence': (["v:1.0"], [["r1c1", "r1c2"], [], ["r3c1", "r3c2"]]),
    'empty_sequence_end': (["v:1.0"], [["r1c1", "r1c2"], ["r2c1", "r2c2"], []]),
    'empty_sequence_start': (["v:1.0"], [[], ["r2c1", "r2c2"], ["r3c1", "r3c2"]]),
    'special_chars': (
        ["v:1.0"],
        [["field with spaces", "field,with,commas", "field\twith\ttabs"],
         ["field\"with\"quotes", "field'with'quotes", "field\\with\\backslashes"],
         ["field\nwith\nnewlines", "field, just field"]]
    ),
    'multiple_empty_sequences': (
        ["v:1.0"],
        [[],
         ["r2c1", "r2c2"],
         [],
         [],
         ["r5c1", "r5c2", "r5c3"],
         []]
    ),
    'multiline_encoded': (
        ["v:1.0"],
        [["line1\nline2", "r1c2", "r1c3"], ["anotherline1\nline2\nline3", "r2c2"]],
    )
}


def dump_then_load(data):
    return nsv.loads(nsv.dumps(data))


def load_then_dump(s):
    return nsv.dumps(*nsv.loads(s))


def load_sample(name):
    file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
    with open(file_path, 'r') as f:
        metadata, data = nsv.load(f)
    return metadata, data


def loads_sample(name):
    file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
    with open(file_path, 'r') as f:
        metadata, data = nsv.loads(f.read())
    return metadata, data


def dump_sample(name):
    metadata, data = SAMPLES_DATA[name]
    with tempfile.TemporaryDirectory() as output_dir:
        output_path = os.path.join(output_dir, f'output_{name}.nsv')
        with open(output_path, 'w') as f:
            if metadata:
                nsv.dump(data, f, metadata=metadata)
            else:
                nsv.dump(data, f)
        with open(output_path, 'r') as f:
            s = f.read()
    return s


def dumps_sample(name):
    metadata, data = SAMPLES_DATA[name]
    return nsv.dumps(data, metadata)
