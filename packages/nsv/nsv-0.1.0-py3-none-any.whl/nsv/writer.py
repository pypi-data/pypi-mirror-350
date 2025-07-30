from typing import Optional


class Writer:
    META_SEPARATOR = '---'

    def __init__(self, file_obj, metadata: Optional[list[str]] = None):
        self._file_obj = file_obj
        self.metadata = metadata if metadata else ()
        self._write_header()

    def _write_header(self):
        for line in self.metadata:
            self._file_obj.write(f'{line}\n')
        self._file_obj.write(f'{Writer.META_SEPARATOR}\n')

    def write_row(self, row):
        if row:
            chunk = ''.join(f'{Writer.escape(str(cell))}\n' if cell else '\\\n' for cell in row)
            self._file_obj.write(chunk)
        self._file_obj.write('\n')

    def write_rows(self, rows):
        for row in rows:
            self.write_row(row)

    @staticmethod
    def escape(s):
        if s == '':
            return '\\'
        return s.replace("\\", "\\\\").replace("\n", "\\n")  # i know
