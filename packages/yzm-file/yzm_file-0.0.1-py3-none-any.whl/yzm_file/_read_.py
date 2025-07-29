#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from typing import Sequence, Literal

import pandas as pd
from pandas import DataFrame
from yzm_log import Logger

'''
 * @Author       : Zheng-Min Yu
 * @Description  : file Read
'''


class Read:
    """
    Read file content
    """

    def __init__(
        self,
        sep='\t',
        line_terminator="\n",
        encoding: str = "utf-8",
        orient: str = "records",
        lines: bool = True,
        header: int | Sequence[int] | None | Literal["infer"] = "infer",
        sheet_name=0,
        low_memory: bool = False,
        log_file: str = "file",
        is_verbose: bool = False,
        is_form_log_file: bool = False
    ):
        """
        Read file initialization information, public information
        :param sep: file separator
        :param line_terminator: file line break
        :param encoding: file encoding
        :param orient: Indicates the expected JSON string format, which is valid only when reading a json file
        :param lines: Read the file as a json object per line
        :param header: The first row header situation
        :param sheet_name: Specify the sheet number when reading Excel
        :param low_memory: Process files in internal chunks to reduce memory usage during parsing
        :param log_file: Path to form a log file
        :param is_verbose: Is log information displayed
        :param is_form_log_file: Is a log file formed
        """
        self.log = Logger(name="file", log_path=log_file, is_form_file=is_form_log_file)
        self.sep = sep
        self.line_terminator = line_terminator
        self.encoding = encoding
        self.orient = orient
        self.lines = lines
        self.header = header
        self.is_verbose = is_verbose
        self.sheet_name = sheet_name
        self.low_memory = low_memory

    def get_content(self, file: str) -> DataFrame | list[DataFrame]:
        """
        Get file content
        :param file: File path information
        :return:
        """
        if self.is_verbose:
            self.log.debug(f"Start reading {file} file...")

        if str(file).endswith(".txt") or str(file).endswith(".bed") or str(file).endswith(".tsv"):
            return pd.read_table(file, sep=self.sep, header=self.header, encoding=self.encoding, low_memory=self.low_memory)
        elif str(file).endswith(".csv"):
            return pd.read_csv(file, sep=',', header=self.header, encoding=self.encoding, low_memory=self.low_memory)
        elif str(file).endswith(".xls") or str(file).endswith(".xlsx"):
            return pd.read_excel(file, sheet_name=self.sheet_name, header=self.header if isinstance(self.header, int) else 0)
        elif str(file).endswith(".html") or str(file).endswith(".htm"):
            return pd.read_html(file, encoding=self.encoding)
        elif str(file).endswith(".json"):
            return pd.read_json(file, orient=self.orient, lines=self.lines, encoding=self.encoding)
        else:
            raise ValueError("Unsupported file type")

    def read_file(self, *files) -> list[DataFrame]:
        """
        Read multiple files
        :param files:
        :return:
        """
        files_return = []
        for file in files:
            files_return.append(self.get_content(file))
        return files_return

    def file_concat_output(self, *files, output_file, join="inner", index=False, encoding="utf_8_sig") -> None:
        """
        Merge two files and export the file
        :param files:
        :param output_file:
        :param join: How to merge files
        :param index:
        :param encoding: Encoding of output files
        :return:
        """
        file_content = self.read_file(*files)

        if self.is_verbose:
            self.log.debug(f"Start merging files {files} ...")

        pd_concat = pd.concat(file_content, join=join, ignore_index=True)
        pd.DataFrame(pd_concat).to_csv(output_file, encoding=encoding, sep=self.sep, index=index)
