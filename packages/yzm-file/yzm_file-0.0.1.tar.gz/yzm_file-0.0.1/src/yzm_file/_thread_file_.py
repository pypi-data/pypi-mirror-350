#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from asyncio import Future
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional, Sequence, Literal, Any

from pandas import DataFrame
from yzm_log import Logger

from ._util_ import path, collection
from ._static_method_ import StaticMethod
from ._read_ import Read

'''
 * @Author       : Zheng-Min Yu
 * @Description  : file ThreadFile
'''


class ThreadFile:

    def __init__(
        self,
        base_path: Optional[path] = None,
        files: Optional[collection] = None,
        thread: int = 16,
        wait_number: int = 5,
        log_file: str = "file",
        is_verbose: bool = False,
        is_form_log_file: bool = False,
        sep='\t',
        line_terminator="\n",
        encoding: str = "utf-8",
        orient: str = "records",
        lines: bool = True,
        header: int | Sequence[int] | None | Literal["infer"] = "infer",
        sheet_name=0,
        low_memory: bool = False
    ):
        """
        Multi thread read file
        :param base_path: The base path for storing files
        :param files: Absolute path to multiple files
        :param thread: Number of threads
        :param wait_number: Number of times waiting for results (one second at a time)
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
        self.base_path = base_path
        self.files = files
        self.thread = thread
        self.wait_number = wait_number
        self.static_method = StaticMethod(log_file, is_form_log_file=is_form_log_file)
        self.read = Read(
            sep=sep,
            line_terminator=line_terminator,
            encoding=encoding,
            orient=orient,
            lines=lines,
            header=header,
            sheet_name=sheet_name,
            low_memory=low_memory,
            log_file=log_file,
            is_verbose=is_verbose,
            is_form_log_file=is_form_log_file
        )
        self.log = Logger(name="file", log_path=log_file, is_form_file=is_form_log_file)
        self.results: list = []
        # get exec files
        self.new_files = self.get_files()
        # add tasks
        self.tasks = self.add_tasks()
        # run
        self.run()

    def read_file(self, file: path) -> DataFrame:
        return self.read.get_content(file)

    def get_result(self, future: Future) -> None:
        self.results.append(future.result())

    def run(self) -> None:
        for task in as_completed(self.tasks):
            task.add_done_callback(self.get_result)

    def get_files(self) -> list[str] | list[Any]:
        file_size: int = 0
        if self.files is not None:
            file_size: int = len(list(self.files))

        if self.base_path is None and file_size == 0:
            self.log.error("At least one of the `base_path` and `files` parameters has a parameter")
            raise ValueError("At least one of the `base_path` and `files` parameters has a parameter")

        new_files = []
        if isinstance(self.base_path, path):
            new_files = self.static_method.get_files_path(self.base_path)
        return new_files

    def add_tasks(self) -> list[Any]:
        with ProcessPoolExecutor(self.thread) as executor:
            future_list = [executor.submit(self.read_file, file) for file in self.new_files]
        return future_list
