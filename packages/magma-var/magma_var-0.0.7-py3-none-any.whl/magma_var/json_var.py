from magma_var.utils import check_directory
from glob import glob
import os
import json


class JsonVar:
    def __init__(self, volcano_code: str, start_date: str, end_date: str, json_dir: str = None, current_dir: str = None, verbose: bool = False):
        self.volcano_code = volcano_code.upper()
        self.start_date = start_date
        self.end_date = end_date

        self.output_dir, self.figures_dir, self.magma_dir = check_directory(current_dir)

        if json_dir is None:
            json_dir = os.path.join(self.magma_dir, 'json')
        self.json_dir = json_dir

        self.verbose = verbose
        self.data = []
        self.dates = []

    def concat(self, json_files: list[str]) -> dict:
        for json_file in json_files:
            data = json.load(open(json_file))
            self.data = self.data + data['data']

            if self.verbose:
                print(f'ℹ️ Read {json_file}')

        if self.verbose:
            print('=' * 60)

        return self.data

    def get(self):
        volcano_json_dir: str = os.path.join(self.json_dir, self.volcano_code)
        json_files = glob(os.path.join(volcano_json_dir, '*.json'))

        if self.verbose:
            print(f'ℹ️ Volcano JSON dir :: {volcano_json_dir}')
            print(f'ℹ️ Total JSON files :: {len(json_files)}')
            print('=' * 60)

        if len(json_files) > 0:
            data = self.concat(json_files)
