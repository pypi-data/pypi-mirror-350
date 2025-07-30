from magma_var.utils import save
from magma_var import MagmaVar
import re
import os
import json
import pandas as pd
import requests
from typing import Self


class Download(MagmaVar):
    url_filter = 'https://magma.esdm.go.id/api/v1/magma-var/filter'
    url_volcano = 'https://magma.esdm.go.id/api/v1/home/gunung-api'

    def __init__(self, token: str, volcano_code: str, start_date: str, end_date: str,
                 current_dir: str = None, verbose: bool = False, url_filter: str = None, url_volcano: str = None):
        super().__init__(token, volcano_code, start_date, end_date, current_dir, verbose)

        self.url_filter = url_filter or self.url_filter
        self.url_volcano = url_volcano or self.url_volcano

        self.json_dir = os.path.join(self.magma_dir, 'json')
        os.makedirs(self.json_dir, exist_ok=True)

        self.volcano_dir = os.path.join(self.json_dir, self.volcano_code)
        os.makedirs(self.volcano_dir, exist_ok=True)

        self.filename = f"{self.volcano_code}_{self.start_date}_{self.end_date}"
        self.json_filename = f"{self.filename}.json"
        self.files: list[str] = []
        self._events: list[dict[str, str]] = []
        self._df: pd.DataFrame = pd.DataFrame()

        if self.verbose:
            print(f'ℹ️ JSON Directory: {self.json_dir}')
            print(f'ℹ️ Volcano Directory: {self.volcano_dir}')

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, values: list[dict[str, str]]):
        self._df = pd.DataFrame(values)

    @property
    def events(self) -> list[dict[str, str]]:
        self._events.sort(key=lambda x: x['index'], reverse=True)
        return self._events

    @events.setter
    def events(self, values: list[dict[str, str]]):
        self._events = values

    def download(self, params: dict = None) -> dict:
        """Download VAR from Filter URL

        Args:
            params (dict): Page paramater to pass

        Returns:
            response (dict): Dictionary of response
        """
        volcano_code = self.volcano_code
        start_date = self.start_date
        end_date = self.end_date

        payload: str = json.dumps({
            "code": volcano_code,
            "start_date": start_date,
            "end_date": end_date,
        })

        try:
            response = requests.request("GET", self.url_filter, headers=self.headers,
                                        data=payload, params=params).json()

            if 'errors' in response.keys():
                raise ValueError(f'❌ Download Error :: {response["errors"]}')

            return response
        except Exception as e:
            raise ValueError(f'❌ Failed to download JSON :: {e}')

    def download_per_page(self, response: dict) -> list[str]:
        """Download VAR per page from Filter URL

        Args:
            response (dict): Dictionary of response

        Returns:
            list of filenames
        """
        pages: list[str] = []
        last_page = response['last_page']

        if self.verbose:
            print(f'ℹ️ Downloading from page 2 to {last_page}')
            print('=' * 60)

        for page in range(2, last_page + 1):
            filename = f'{self.json_filename}_{page}.json'
            json_per_page = os.path.join(self.volcano_dir, filename)

            if os.path.exists(json_per_page):
                if self.verbose:
                    print(f'✅ Skip. JSON for page #{page} exists :: {json_per_page}')
                pages.append(json_per_page)
                continue

            response = self.download({'page': page})
            save(json_per_page, response)

            pages.append(json_per_page)

            if self.verbose:
                print(f'✅ JSON for page #{page} downloaded :: {json_per_page}')
                print('=' * 60)

        self.files = self.files + pages
        return pages

    def download_first_page(self) -> dict:
        """Download first page to be used as reference

        Returns:
            response (dict): Dictionary of response
        """
        first_page_json = os.path.join(self.volcano_dir, f'{self.json_filename}_1.json')

        if os.path.isfile(first_page_json):
            if self.verbose:
                print(f'✅ JSON First Page exists :: {first_page_json}')
            self.files.append(first_page_json)
            return json.load(open(first_page_json))

        if self.verbose:
            print(f'⌛ Downloading JSON First Page :: {first_page_json}')

        response = self.download()

        # Check if response is success
        if 'data' not in response.keys():
            raise ValueError(f'❌ Error download first page :: {response}')

        save(first_page_json, response)

        if self.verbose:
            print(f'✅ JSON First Page downloaded :: {first_page_json}')

        self.files.append(first_page_json)

        return response

    @staticmethod
    def _extracted(date: str, description: str, event_name: str = None, count: int = None,
                   amplitudo: str = None, sp_time: str = None, duration: str = None, dominant: str = None):

        amp_min = None
        amp_max = amplitudo
        sp_min = None
        sp_max = sp_time
        duration_min = None
        duration_max = duration

        if amplitudo is not None:
            amps = amplitudo.split('-')
            if len(amps) == 2:
                amp_min, amp_max = amplitudo.split('-')

        if sp_time is not None:
            sp_times = sp_time.split('-')
            if len(sp_times) == 2:
                sp_min, sp_max = sp_time.split('-')

        if duration is not None:
            durations = duration.split('-')
            if len(durations) == 2:
                duration_min, duration_max = durations

        return {
            'date': date,
            'description': description,
            'event_name': event_name,
            'count': count,
            'amplitude_min': float(amp_min) if amp_min is not None else None,
            'amplitude_max': float(amp_max) if amp_max is not None else None,
            'sp_min': float(sp_min) if sp_min is not None else None,
            'sp_max': float(sp_max) if sp_max is not None else None,
            'duration_min': float(duration_min) if duration_min is not None else None,
            'duration_max': float(duration_max) if duration_max is not None else None,
            'dominant': float(dominant) if dominant is not None else None,
        }

    def extract(self) -> Self:
        extracted_list: list[dict[str, str]] = []

        for event in self.events:
            date = event['date']
            text: str = event['event'].strip()

            name_match_pattern = r'gempa\s+(.+?)\s+dengan'
            if 'Harmonik' in text:
                name_match_pattern = r'kali\s+(.+?)\s+dengan'

            count_match = re.search(r'(\d+)\s+kali', text)
            name_match = re.search(name_match_pattern, text)
            amp_match = re.search(r'amplitudo\s+([\d\-.]+)\s+mm', text)
            sp_match = re.search(r'S-P\s+([\d\-.]+)\s+detik', text)
            duration_match = re.search(r'lama\s+gempa\s+([\d\-.]+)\s+detik', text)
            dominant_match = re.search(r'dominan\s+([\d\-.]+)\s+mm', text)

            try:
                if count_match and name_match and amp_match:
                    data = {
                        'count': int(count_match.group(1)),
                        'event_name': name_match.group(1).strip(),
                        'amplitudo': amp_match.group(1),
                        'sp': sp_match.group(1) if sp_match else None,
                        'duration': duration_match.group(1) if duration_match else None,
                        'dominant': dominant_match.group(1) if dominant_match else None
                    }

                    extracted_list.append(Download._extracted(
                        date=date,
                        description=text,
                        event_name=data['event_name'],
                        count=int(data['count']),
                        amplitudo=data['amplitudo'],
                        sp_time=data['sp'],
                        duration=data['duration'],
                        dominant=data['dominant']
                    ))
                else:
                    extracted_list.append(Download._extracted(
                        date=date,
                        description=text,
                    ))
            except Exception as e:
                print(f'❌ {date} :: {text}')
                print(e)

        self.df = extracted_list

        return self

    def transform(self) -> Self:
        """Transform all json files

        Returns:
            self: Self
        """
        index = 0
        for file in self.files:
            response = json.load(open(file))
            datas = response['data']
            for data in datas:
                noticenumber: str = data['laporan_terakhir']['noticenumber']
                year = noticenumber[0:4]
                month = noticenumber[4:6]
                day = noticenumber[6:8]
                descriptions: list[str] = data['laporan_terakhir']['gempa']['deskripsi']
                for description in descriptions:
                    index = index + 1
                    events: dict[str, str] = {
                        'index': int(index),
                        'date': f'{year}-{month}-{day}',
                        'event': description
                    }
                    self.events.append(events)
        return self

    def var(self) -> Self:
        """Download VAR from Filter URL and save it to JSON files

        Returns:
            self: Self
        """
        response = self.download_first_page()
        if self.verbose:
            print(f'ℹ️ Total Data :: {response['total']}')

        self.download_per_page(response)

        if self.verbose:
            print('ℹ️ JSON Files :: ', len(self.files))

        self.transform().extract()

        if len(self.events) != len(self.df):
            if self.verbose:
                print(f'⚠️ Events length not equal to DataFrame length :: {len(self.events)} vs {len(self.df)}')
            print(f'⚠️ Please kindly to check the results.')

        return self

    def _to(self, type: str, filename: str = None, verbose: bool = True) -> str:
        """Save wrapper

        Args:
            type (str): Type of wrapper. 'csv' or 'excel'
            filename (str, optional): Name of file. Defaults to None.
            verbose (bool, optional): Print verbose output. Defaults to True.

        Returns:
            Saved path location
        """
        to_dir = os.path.join(self.magma_dir, type)
        os.makedirs(to_dir, exist_ok=True)

        file_type = 'csv' if type == 'csv' else 'xlsx'

        _filename = filename if filename is not None else self.filename
        path = os.path.join(to_dir, f'{_filename}.{file_type}')

        self.df.to_csv(path, index=False) if type == 'csv' else self.df.to_excel(path, index=False)

        if verbose:
            print(f'🗃️ Saved to :: {path}')

        return path

    def to_csv(self, filename: str = None, verbose: bool = True) -> str:
        """Save to CSV files

        Args:
            filename (str, optional): CSV filename. Defaults to None.
            verbose (bool, optional): For debugging. Defaults to True.

        Returns:
            str: CSV file location
        """
        return self._to(type='csv', filename=filename, verbose=verbose)

    def to_excel(self, filename: str = None, verbose: bool = True) -> str:
        """Save to Excel Files

        Args:
            filename (str, optional): Excel filename. Defaults to None.
            verbose (bool, optional): For debugging. Defaults to True.
        """
        return self._to(type='xlsx', filename=filename, verbose=verbose)
