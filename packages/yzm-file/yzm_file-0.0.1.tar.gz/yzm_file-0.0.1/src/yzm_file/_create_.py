#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pandas as pd
from yzm_log import Logger
from pandas import DataFrame

'''
 * @Author       : Zheng-Min Yu
 * @Description  : file Create
'''


class Create:
    """
    初始化文件
    """

    def __init__(
        self,
        sep='\t',
        line_terminator="\n",
        encoding: str = 'utf_8_sig',
        index: bool = False,
        header: bool = True,
        sheet_name='new_sheet',
        log_file: str = "file",
        is_form_log_file: bool = True
    ):
        """
        Initialization creation information, public information
        :param sep: File Separator
        :param line_terminator: File Line Break
        :param encoding: Document code
        :param index: Whether there is a row index
        :param header: Whether there is a title
        :param sheet_name: sheet name
        :param log_file: Path to form a log file
        :param is_form_log_file: Is a log file formed
        """
        self.log = Logger(name="file", log_path=log_file, is_form_file=is_form_log_file)
        self.sep = sep
        self.line_terminator = line_terminator
        self.encoding = encoding
        self.index = index
        self.header = header
        self.sheet_name = sheet_name

    def to_file(self, df: DataFrame, file: str) -> None:
        """
        :param df: DataFrame
        :param file: File path plus name
        """
        self.log.debug(f"create a file: {file}")
        # 导出文件
        if str(file).endswith(".txt") or str(file).endswith(".bed") or str(file).endswith(".tsv"):
            df.to_csv(file, sep=self.sep, lineterminator=self.line_terminator, header=self.header, encoding=self.encoding, index=self.index)
        elif str(file).endswith(".csv"):
            df.to_csv(file, sep=',', lineterminator=self.line_terminator, header=self.header, encoding=self.encoding, index=self.index)
        elif str(file).endswith(".xls") or str(file).endswith(".xlsx"):
            df.to_excel(file, sheet_name=self.sheet_name, header=self.header, index=self.index)
        else:
            with open(file, 'w', encoding='UTF-8') as f:
                df.to_string(f)

    def rename(self, df: DataFrame, columns: list, output_file: str = None) -> None:
        """
        Modify the file column name
        :param df: source document
        :param columns: New column name
        :param output_file: Output file path
        :return:
        """
        # 重新命名
        self.log.debug(f"Modify the file column name: {columns}")
        df.columns = columns
        # 保存
        if output_file is not None:
            self.to_file(df, output_file)

    def drop_columns(self, df: DataFrame, columns: list, output_file: str = None) -> None:
        """
        Delete File Column Name
        :param df: source document
        :param columns: Delete column names
        :param output_file: Output file path
        :return:
        """
        # 删除列
        self.log.debug(f"Delete file column names: {columns}")
        df.drop(columns, axis=1, inplace=True)
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def add_content(self, df: DataFrame, list_content: list, columns=None, is_log: bool = False, output_file: str = None) -> None:
        """
        Add content to the created file
        :param df: DataFrame
        :param list_content: A column of content information in array form
        :param columns: column information
        :param output_file: Output file path
        :param is_log: Do you want to print the log
        :return:
        """
        # 添加内容
        if columns is None:
            columns: list = list(df.columns)
        if is_log:
            self.log.debug(f"Add content {list_content} ...")
        df.loc[len(df)] = pd.Series(list_content, index=columns)
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def add_difference_column(self, df: DataFrame, column: str, a: str, b: str, output_file: str = None) -> None:
        """
        Add a subtraction column (column=a - b)
        :param df: DataFrame
        :param column: A new column name added
        :param a: minuend
        :param b: subtrahend
        :param output_file: Output file path
        :return:
        """
        self.log.debug(f"Add a subtraction column: {column}")
        df[column] = df[a] - df[b]
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def add_rank_group_by(self, df: DataFrame, group: list, column: str, output_file: str = None) -> None:
        """
        添加五个 rank 列
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要秩的列
        :param output_file: Output file path
        :return:
        """
        self.log.debug(f"添加五个 rank 列: {group}, {column}")
        # 添加排名
        for method in ['average', 'min', 'max', 'dense', 'first']:
            df[f'{method}_rank'] = df.groupby(group)[column].rank(method)
        # 保存文件
        if output_file is not None:
            self.to_file(df, output_file)

    def sum_group_by(self, df: DataFrame, group: list, column: str, output_file: str = None) -> DataFrame:
        """
        Calculate the total number of columns by grouping
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要和的列
        :param output_file: Output file path
        :return:
        """
        # 总和
        self.log.debug(f"Calculate the total number of columns by grouping: {group}, {column}")
        column_sum = df.groupby(group)[column].sum().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_sum")
        column_sum.columns = new_column
        # 保存文件
        if output_file is not None:
            self.to_file(column_sum, output_file)
        return column_sum

    def count_group_by(self, df: DataFrame, group: list, column: str, output_file: str = None) -> DataFrame:
        """
        Calculate the number of columns by grouping
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要数量的列
        :param output_file: Output file path
        :return:
        """
        # 总和
        self.log.debug(f"Calculate the total number of columns by grouping: {group}, {column}")
        column_sum = df.groupby(group)[column].count().reset_index()
        group.append(f"{column}_count")
        column_sum.columns = group
        # 保存文件
        if output_file is not None:
            self.to_file(column_sum, output_file)
        return column_sum

    def calculation_group_by(self, df: DataFrame, group: list, column: str, on: str, output_file: str = None, add_merge_files: list = None) -> DataFrame:
        """
        Performing a series of numerical calculations through grouping
        :param df: DataFrame
        :param group: 分组的列
        :param column: 需要秩的列
        :param on: 合并的列
        :param output_file: Output file path
        :param add_merge_files: 添加 merge 文件
        :return:
        """
        # 总和
        self.log.debug(f"Performing a series of numerical calculations through grouping: {group}, {column}")
        # 个数大小
        column_size = df.groupby(group)[column].size().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_size")
        column_size.columns = new_column
        # 平均值
        column_mean = df.groupby(group)[column].mean().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_mean")
        column_mean.columns = new_column
        # 方差 (size == 1 的值为 NaN)
        column_var = df.groupby(group)[column].var().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_var")
        column_var.columns = new_column
        # 标准误差 (size == 1 的值为 NaN)
        column_sem = df.groupby(group)[column].sem().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_sem")
        column_sem.columns = new_column
        # 标准偏差 (size == 1 的值为 NaN)
        column_std = df.groupby(group)[column].std().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_std")
        column_std.columns = new_column
        # 中位数值
        column_median = df.groupby(group)[column].median().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_median")
        column_median.columns = new_column
        # 最小值
        column_min = df.groupby(group)[column].min().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_min")
        column_min.columns = new_column
        # 最大值
        column_max = df.groupby(group)[column].max().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_max")
        column_max.columns = new_column
        # 总和
        column_sum = self.sum_group_by(df, group, column)
        # 乘积
        column_prod = df.groupby(group)[column].prod().reset_index()
        new_column = group.copy()
        new_column.append(f"{column}_prod")
        column_prod.columns = new_column
        # 保存文件
        all_merge_files: list = [column_size, column_mean, column_var, column_sem, column_std,
                                 column_median, column_min, column_max, column_sum, column_prod]

        if output_file is not None:
            if add_merge_files is not None:
                all_merge_files.extend(add_merge_files)
                return self.merge_files(all_merge_files, on=on, output_file=output_file)
            else:
                return self.merge_files(all_merge_files, on=on, output_file=output_file)
        else:
            return self.merge_files(all_merge_files, on=on)

    def merge_files(self, files: list, on: str, output_file: str = None) -> DataFrame:
        """
        将文件进行合并
        :param files: 多个文件
        :param on: 关键 key
        :param output_file: Output file path
        :return:
        """
        # 总和
        size = len(files)
        self.log.debug(f"Merge files: {size}, {on}")
        new_file = files[0]
        i = 1
        while i < size:
            self.log.debug(f"Merge files {i} 次")
            new_file = pd.merge(new_file, files[i], on=on)
            i += 1
        # 保存文件
        if output_file is not None:
            self.to_file(new_file, output_file)
        return new_file
