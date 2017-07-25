import os
import pathlib

import requests
from urllib.request import Request as urllib_request, urlopen as urllib_open
import sys
from datetime import datetime


class Downloader:
    PROJECT = sys.path[0]
    UTILITIES = os.path.join(PROJECT, 'utilities')
    DOWNLOADS = os.path.join(UTILITIES, 'downloads')
    DOWNLOADS_PATH = pathlib.Path(DOWNLOADS)

    def __init__(self):
        self.enabled = False
        self.current = ''
        self._req = None
        self.queue = []
        self.ensure_paths()
        self.start_time = datetime.now()
        self.end_time = datetime.now()

    def ensure_paths(self):
        self._ensure_path(Downloader.UTILITIES)
        self._ensure_path(Downloader.DOWNLOADS)

    @staticmethod
    def _ensure_path(string: str):
        path = pathlib.Path(string)
        if Downloader._is_filepath(str(path)):
            path = path.parent

        if not path.is_dir():
            path.mkdir()

    @staticmethod
    def _is_filepath(string: str):
        return len(os.path.splitext(os.path.basename(string))[1]) > 0

    def url_to_queue(self, url: str):
        if not self.queue.__contains__(url):
            self.queue.append(url)

    def urls_to_queue(self, urls: list):
        for url in urls:
            self.url_to_queue(url)

    def start(self):
        if not self.enabled and len(self.queue) > 0:
            self.start_time = datetime.now()
            print(f'DOWNLOADS\t-\tSTART\t-\t({len(self.queue)})\t-\t{self.start_time}')
            self.enabled = True
            self._get_next()
        else:
            print(f'ERROR  -  DOWNLOADS START  -  ALREADY RUNNING!!!')

    def _update_current(self):
        try:
            self.current = self.queue.pop(0)
            print(f'# Queue Size\t-\tUpdated\t-\t{len(self.queue)}')
        except Exception as error:
            print(f'Error Updating Current: {self.current}')
            self.stop()
            self.start()

    def stop(self):
        self.current = ''
        self.enabled = False
        self.end_time = datetime.now()
        print(f'DOWNLOADS\t-\tSTOP\t-\t({len(self.queue)})\t-\t{self.end_time}')
        self._log_start_stop(f'DOWNLOADS\t-\t-STOP\t-\t({len(self.queue)})', self.start_time, self.end_time)

    @staticmethod
    def _log_start_stop(string: str, start: datetime, stop: datetime):
        print(f'\n# TIMELOG\t{string}\n'
              f'Start:\t{start}\n'
              f'Stop:\t{stop}\n'
              f'Time:\t{stop - start}\n'
              )

    def _get_next(self):
        if len(self.queue) > 0:
            self._update_current()
            if self.current != '':
                self._download_current()
        else:
            self.stop()

    @staticmethod
    def _download_http(url: str):
        return requests.get(url, allow_redirects=True)

    @staticmethod
    def _download_ftp(url: str):
        data = bytes('', encoding='utf-8')
        req = urllib_request(url)

        try:
            with urllib_open(req) as response:
                data = response.read()
        except Exception as error:
            print(f'ERROR\t-\t{url}\n{error}')
            data = None
        finally:
            return data

    @staticmethod
    def _download_generic(url: str):
        if url.startswith('http'):
            return Downloader._download_http(url)
        elif url.startswith('ftp'):
            return Downloader._download_ftp(url)
        return bytes('', encoding='utf-8')

    def _download_current(self):
        src = self.current
        base = os.path.basename(src)
        start_time = datetime.now()
        print(f'Starting Download:\t{base}\t-\t{start_time}')
        fn, ext = os.path.splitext(base)
        if ext.isupper():
            ext = ext.lower()
        dst = os.path.join(Downloader.DOWNLOADS, f'{fn}{ext}')
        dst_path = pathlib.Path(dst)

        data = Downloader._download_generic(src)
        dst_path.write_bytes(data)

        end_time = datetime.now()
        self._log_start_stop(f'Finished Download:\t{base}', start_time, end_time)
        self._get_next()


class URLS:
    def __init__(self):
        self.natality = self.create_set('ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/DVS/natality/Nat', '.zip', 1968, 2015, 1994, [1968, 1989])
        self.mortality_multiple = self.create_set('ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/DVS/mortality/mort', '.zip', 1968, 2015, 1968)

    def create_set(self, prefix: str, ext: str, min_year: int, max_year: int, us_append_year: int, capitalized_ext_years=None) -> list:
        outs = []
        if isinstance(capitalized_ext_years, type(None)):
            capitalized_ext_years = []
        for year in range(min_year, max_year+1):
            if year == us_append_year:
                ext = f'us{ext}'
            if capitalized_ext_years.__contains__(year):
                _ext = ext.upper()
                if _ext.startswith('US'):
                    _ext = f'us{_ext[2:]}'
                url = f'{prefix}{year}{_ext}'
            else:
                url = f'{prefix}{year}{ext}'

            outs.append(url)
        return outs

    @staticmethod
    def __get_joined_for_log__(data: list) -> str:
        return '\n'.join(data)

    def __do_log__(self):
        return f'URLS\n' \
               f'Natality:\n{self.__get_joined_for_log__(self.natality)}\n' \
               f'Mortality:\n{self.__get_joined_for_log__(self.mortality_multiple)}\n'


def run():
    urls = URLS()
    d = Downloader()
    d.urls_to_queue(urls.natality)
    d.urls_to_queue(urls.mortality_multiple)
    d.start()
