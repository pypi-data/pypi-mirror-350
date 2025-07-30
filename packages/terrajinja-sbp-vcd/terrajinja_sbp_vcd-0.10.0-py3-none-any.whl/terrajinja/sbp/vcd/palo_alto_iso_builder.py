import os
import re
import tempfile
from typing import List
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from pycdlib import PyCdlib


class PaloAltoIsoBuilder:
    def __init__(self, input_dir: str, parameters: dict):
        self.input_dir = input_dir
        self.parameters = parameters
        self.iso = PyCdlib()
        self.iso_file_path = None

        # Jinja2 environment for templating
        self.env = Environment(
            loader=FileSystemLoader(self.input_dir),
            autoescape=select_autoescape(disabled_extensions=('txt', 'conf', 'cfg', 'ini', 'sh', 'yaml', 'yml')),
            undefined=StrictUndefined  # Raise error if a variable is missing
        )

    @staticmethod
    def _sanitize_iso9660(name: str) -> str:
        return re.sub(r'[^A-Z0-9_]', '_', name.upper())

    @staticmethod
    def _iso_path(parts: List[str]) -> str:
        return '/' + '/'.join(parts)

    def _add_directory_structure(self):
        added_dirs = set()

        for root, _, files in os.walk(self.input_dir):
            rel_root = os.path.relpath(root, self.input_dir)
            dir_parts = [] if rel_root == '.' else rel_root.split(os.sep)
            iso_parts = [self._sanitize_iso9660(p) for p in dir_parts]

            for i in range(len(iso_parts)):
                iso_path = self._iso_path(iso_parts[:i + 1])
                rr_name = dir_parts[i]
                if iso_path not in added_dirs:
                    self.iso.add_directory(iso_path, rr_name=rr_name)
                    added_dirs.add(iso_path)

            for filename in files:
                rel_template_path = os.path.join(rel_root, filename) if rel_root != '.' else filename
                template = self.env.get_template(rel_template_path)

                rendered = template.render(**self.parameters)

                temp_fd, temp_path = tempfile.mkstemp()
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as tmp:
                    tmp.write(rendered)

                rel_parts = dir_parts + [filename]
                iso_parts = [self._sanitize_iso9660(p) for p in rel_parts]
                iso_path = self._iso_path(iso_parts)
                self.iso.add_file(temp_path, iso_path=iso_path + ';1', rr_name=filename)

    def build(self) -> str:
        self.iso.new(interchange_level=3, rock_ridge='1.09')
        self._add_directory_structure()

        fd, path = tempfile.mkstemp(suffix='.iso')
        os.close(fd)
        self.iso.write(path)
        self.iso.close()

        self.iso_file_path = path
        return path
