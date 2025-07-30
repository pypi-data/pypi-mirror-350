import csv
import os
from pathlib import Path
from typing import Any


class CsvWriterTools:
    def __init__(self, csv_file:str, is_dict_row:bool=False):
        self.csv_file = csv_file
        self.is_dict_row=is_dict_row
        self.csv_file_input = None
        self.writer = None
        self._open()

    def _open(self):
        os.makedirs(Path(self.csv_file).parent, exist_ok=True)
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        self.csv_file_input = open(self.csv_file, mode='a', encoding='utf-8',
                                   newline='' if not self.is_dict_row else '\n')

    def add_header(self, header_list: list[str]):
        if self.is_dict_row:
            self.writer = csv.DictWriter(self.csv_file_input, fieldnames=header_list)
            self.writer.writeheader()
        else:
            self.writer = csv.writer(self.csv_file_input)
            self.writer.writerow(header_list)

    def add_row(self, row_data:list[Any]|dict[str, Any]):
        self.writer.writerow(row_data)

    def add_rows(self, row_list:list[list[Any]|dict[str, Any]], auto_close:bool=True):
        self.writer.writerows(row_list)
        if auto_close:
            self.csv_file_input.close()

    def close(self):
        self.csv_file_input.close()


if __name__ == '__main__':
    csv_tool = CsvWriterTools('tmp.csv', is_dict_row=True)
    csv_tool.add_header(['id', 'username', 'age'])
    csv_tool.add_row({
        'id':1, 'username':'chen', 'age':34
    })
    csv_tool.add_rows([
        {
            'id': 2, 'username': 'chen2', 'age': 32
        },
        {
            'id': 3, 'username': 'chen3', 'age': 33
        },
        {
            'id': 4, 'username': 'chen4', 'age': 35
        },
    ])
    pass