#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from yzm_log import Logger

import gzip
import os
import shutil
from multiprocessing.dummy import Lock

'''
 * @Author       : Zheng-Min Yu
 * @Description  : file StaticMethod
'''


class StaticMethod:
    """
    文件或者路径的静态方法
    """

    def __init__(
        self,
        log_file: str = "file",
        is_verbose: bool = False,
        is_form_log_file: bool = False
    ):
        """
        file static method
        :param log_file: Path to form a log file
        :param is_verbose: Is log information displayed
        :param is_form_log_file: Is a log file formed
        """
        self.log = Logger(name="file", log_path=log_file, is_form_file=is_form_log_file)
        self.is_verbose = is_verbose

    def read_file_line(self, path: str, mode: str = 'r', encoding: str = "utf-8") -> list[str]:
        """
        Read file by line
        :param path:
        :param mode:
        :param encoding:
        :return:
        """
        content = []

        if self.is_verbose:
            self.log.info(f"Start reading file {path}")

        with open(path, mode, encoding=encoding) as f:
            while True:
                line = f.readline().strip()
                content.append(line)
                if not line:
                    break
        return content

    def write_file_line(self, path: str, content: list, line: str = '\n', mode: str = 'a', encoding: str = "utf-8") -> None:
        """
        Write a file (write by line, and it will not be cleared if the original file is called again by default)
        :param path:
        :param content:
        :param line:
        :param mode:
        :param encoding:
        :return:
        """
        if self.is_verbose:
            self.log.info(f"Start writing file {path}")

        with open(path, mode, encoding=encoding) as f:
            for li in content:
                f.write(li + line)

    def read_write_line(
        self,
        path: str,
        output: str, callback,
        column=None,
        rm: str = 'r',
        om: str = 'w',
        encoding: str = "utf-8",
        buffering: int = 256,
        newline: str = "\n"
    ) -> None:
        """
        Write one file to another
        :param column: Output column name
        :param path: Enter a path
        :param output: output path
        :param callback: A callback function that returns the input data
        :param rm: Read mode
        :param om: Output mode
        :param encoding: encoding
        :param buffering: Number of loaded lines in the output file
        :param newline: The newline character of the output file
        :return:
        """
        with open(output, om, encoding=encoding, buffering=buffering, newline=newline) as w:
            with open(path, rm, encoding=encoding) as f:
                if column:
                    name: str = "\t".join(column)

                    if self.is_verbose:
                        self.log.debug(f"Add Column Name: {name}")

                    w.write(f"{name}\n")
                while True:
                    line: str = str(f.readline().strip())
                    if not line:
                        break
                    new_line: list = callback(line)
                    if new_line and len(new_line) != 0 and new_line != "":
                        content = "\t".join(new_line)
                        w.write(f"{content}\n")

    def get_contents(self, path: str) -> list[str]:
        """
        Obtain all files and folders under the specified path
        :param path: path
        :return: files and folders
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")
        return list(os.listdir(path))

    def entry_contents(self, path: str, type_: int = 0) -> list[str]:
        """
        Obtain all files and (or) folders under the specified path
        :param path: path
        :param type_: judge file or dir
        :return: files and (or) folders
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")

        contents: list = []
        with os.scandir(path) as it:
            for entry in it:
                entry: os.DirEntry
                if type_ == 0:
                    contents.append(entry.name)
                elif type_ == 1 and entry.is_file():
                    contents.append(entry.name)
                elif type_ == 2 and entry.is_dir():
                    contents.append(entry.name)
                else:
                    raise ValueError("type input error, type is 0 or 1 or 2.")
        return contents

    def entry_contents_path(self, path: str, type_: int = 0) -> list[str]:
        """
        Obtain all files and (or) folders under the specified path
        :param path: path
        :param type_: judge file or dir
        :return: files and (or) folders path
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")

        contents: list = []
        with os.scandir(path) as it:
            for entry in it:
                entry: os.DirEntry
                if type_ == 0:
                    contents.append(entry.path)
                elif type_ == 1:
                    if entry.is_file():
                        contents.append(entry.path)
                elif type_ == 2:
                    if entry.is_dir():
                        contents.append(entry.path)
                else:
                    raise ValueError("type input error, type is 0 or 1 or 2.")
        return contents

    def get_files(self, path: str) -> list[str]:
        """
        Obtain all files in the specified path
        :param path: path
        :return: files
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")

        files: list = []
        with os.scandir(path) as it:
            for entry in it:
                entry: os.DirEntry
                if entry.is_file():
                    files.append(entry.name)
        return files

    def get_files_path(self, path: str) -> list[str]:
        """
        Obtain all files in the specified path
        :param path: path
        :return: file paths
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")

        files: list = []
        with os.scandir(path) as it:
            for entry in it:
                entry: os.DirEntry
                if entry.is_file():
                    files.append(entry.path)
        return files

    def get_dirs(self, path: str) -> list[str]:
        """
        Obtain all files in the specified path
        :param path:  path
        :return: dirs
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")

        dirs: list = []
        with os.scandir(path) as it:
            for entry in it:
                entry: os.DirEntry
                if entry.is_dir():
                    dirs.append(entry.name)
        return dirs

    def get_dirs_path(self, path: str) -> list[str]:
        """
        Obtain all files in the specified path
        :param path: path
        :return: dirs
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")

        dirs: list = []
        with os.scandir(path) as it:
            for entry in it:
                entry: os.DirEntry
                if entry.is_dir():
                    dirs.append(entry.path)
        return dirs

    def entry_contents_dict(self, path: str, type_: int = 0, suffix: str = None) -> dict:
        """
        Obtain all files in the specified path
        :param path: path
        :param type_: type_
        :param suffix: Filter criteria
        :return: files and (or) dirs
        """
        if self.is_verbose:
            self.log.info(f"Starting to retrieve content under this path: {path}")

        files: list = []
        dirs: list = []
        contents: list = []
        dict_: dict = {}
        with os.scandir(path) as it:
            for entry in it:
                entry: os.DirEntry
                # 判断是否满足情况
                if suffix is None or entry.name.endswith(suffix):
                    if type_ == 0:
                        contents.append(entry.name)
                        dict_.update({entry.name: entry.path})
                    elif type_ == 1:
                        # 此处判断不能和 type_ == 1 连写，因为需要进行提示 ValueError("type input error, type is 0 or 1 or 2.")
                        if entry.is_file():
                            files.append(entry.name)
                            dict_.update({entry.name: entry.path})
                    elif type_ == 2:
                        if entry.is_dir():
                            dirs.append(entry.name)
                            dict_.update({entry.name: entry.path})
                    else:
                        raise ValueError("type input error, type is 0 or 1 or 2.")
        dict_.update({"name": contents if type_ == 0 else files if type_ == 1 else dirs})
        return dict_

    def entry_files_dict(self, path: str) -> dict:
        """
        Obtain all files in the specified path
        :param path: path
        :return: files
        """
        return self.entry_contents_dict(path, 1)

    def entry_dirs_dict(self, path: str) -> dict:
        """
        Obtain all files in the specified path
        :param path: path
        :return: dirs
        """
        return self.entry_contents_dict(path, 2)

    def unzip_gz(self, gz_file: str, generate_file: str = None, is_force: bool = False) -> list:
        if generate_file:
            if os.path.exists(generate_file) and is_force:
                self.log.warning(f"{generate_file} The file already exists, it has been moved by default")
            else:
                if self.is_verbose:
                    self.log.info(f"Start unzip file {gz_file}")

                w = open(generate_file, 'wb')
                f = gzip.open(gz_file, 'rb')
                read = f.read()
                # Form a file
                w.write(read)
                # Obtaining Content Information
                file_content: list = read.decode().rstrip().split("\n")
                f.close()
                w.close()

                if self.is_verbose:
                    self.log.info(f"End of unzip file  {gz_file}")

                return file_content
        f = gzip.open(gz_file, 'rb')
        # Obtaining Content Information
        file_content: list = f.read().decode().rstrip().split("\n")
        f.close()
        return file_content

    def download_file(self, url: str, filename: str, chunk_size: int = 1024, is_force: bool = False) -> None:
        """
        download file
        :param url: Download URL
        :param filename: The downloaded file name
        :param chunk_size: The size of the download stream
        :param is_force: Whether to force coverage
        :return:
        """
        if os.path.exists(filename) and is_force:
            self.log.warning(f"{filename} The file already exists, it has been downloaded by default")
        else:
            if self.is_verbose:
                self.log.info(f"Download {url} file")

            response_data_file = requests.get(url, stream=True)

            if self.is_verbose:
                self.log.info(f"Create {filename} file")

            with open(filename, 'wb') as f:
                for chunk in response_data_file.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)

            if self.is_verbose:
                self.log.info(f"Download {url}===>{filename} file completed")

    def copy_file(self, source_file: str, target_file: str, is_force: bool = False) -> None:
        """
        copy file
        :param source_file: source file
        :param target_file: target file
        :param is_force: Whether to force coverage
        :return:
        """
        if is_force:
            self.log.warning(f"{source_file} ====> {target_file} The file already exists, it has been copied by default")
        else:
            if self.is_verbose:
                self.log.info(f"Start copying file {source_file}")
            shutil.copy(source_file, target_file)
            if self.is_verbose:
                self.log.info(f"End of copying file  {source_file}")

    def move_file(self, source_file: str, target_file: str, is_force: bool = False) -> None:
        """
        move file
        :param source_file: source file
        :param target_file: target file
        :param is_force: Whether to force coverage
        :return:
        """
        if is_force:
            self.log.warning(f"{source_file} ====> {target_file} The file already exists, it has been moved by default")
        else:
            if self.is_verbose:
                self.log.info(f"Start moving file {source_file}")

            shutil.move(source_file, target_file)

            if self.is_verbose:
                self.log.info(f"End of moving file  {source_file}")

    def makedirs(self, dirs: str, is_lock: bool = False) -> None:
        lock = Lock()

        if is_lock:
            lock.locked()

        if not os.path.exists(dirs):

            if self.is_verbose:
                self.log.info(f"Create {dirs} folder")

            os.makedirs(dirs)

        if is_lock:
            lock.release()
