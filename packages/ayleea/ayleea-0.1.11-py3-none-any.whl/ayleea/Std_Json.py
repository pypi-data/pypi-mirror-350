#!python3
# coding=utf-8
"""
FilePath     : Std_Json.py
Description  : 定义Std_Json类，用于处理大模型训练使用的标准json数据
Author       : Ayleea zhengyalin@xiaomi.com
Date         : 2024-09-13 13:00:21
Version      : 0.1.0
"""
import json
import random
from copy import deepcopy
from pathlib import Path
from typing import Union, List, Dict, Any, Optional, Generator, Callable, Tuple, Mapping
import pandas as pd

# 不对std_json中的item进行set判断不需要进行dumps序列化操作
class Std_Json:
    """
    形如[{}....]的json数据
    """

    def __init__(self, std_json: Union['Std_Json', List[Dict], Dict, str, Path, None] = None):
        """
        Initialize Std_Json with optional data input.

        Args:
            std_json: Input data in various supported formats
        """
        self.std_data: List[Dict] = []
        if std_json is not None:
            self.load(std_json)

    def load(self, std_json: Union['Std_Json', List[Dict], Dict, str, Path]) -> None:
        """
        Load data from various sources with robust type checking.

        Args:
            std_json: Data source to load from

        Raises:
            TypeError: If input type is not supported
        """
        if isinstance(std_json, Std_Json):
            self.std_data = deepcopy(std_json.std_data)
        elif isinstance(std_json, list):
            self.std_data = [dict(item) for item in std_json]  # Ensure deep copy of dictionaries
        elif isinstance(std_json, (str, Path)):
            with open(std_json, "r", encoding="utf-8") as f:
                if std_json.endswith("jsonl"):
                    data=[json.loads(line) for line in f.readlines() if line.strip()]
                else:
                    data = json.load(f)
                if isinstance(data, list):
                    self.std_data = data
                elif isinstance(data, dict):
                    self.std_data = [data]
                else:
                    raise TypeError("JSON file must contain a list/dict of objects")
        elif isinstance(std_json, dict):
            self.std_data = [dict(std_json)]  # Ensure deep copy
        else:
            raise TypeError("std_json must be Std_Json, list, dict, str, or Path")

    def add(self, std_json: Union['Std_Json', List[Dict], Dict, str, Path]) -> None:
        """
        Add new data to the existing dataset.

        Args:
            std_json: Data to be added
        """
        if isinstance(std_json, Std_Json):
            self.std_data.extend(deepcopy(std_json.std_data))
        else:
            new_std_json = Std_Json(std_json)
            self.std_data.extend(new_std_json.std_data)

    def save(self, std_json_file: Union[str, Path], type:str="json",**kwargs) -> None:
        """
        Save data to a JSON file with customizable JSON dump options.

        Args:
            std_json_file: File path to save
            type: file type
            **kwargs: Additional JSON dump options
        """
        with open(std_json_file, "w", encoding="utf-8") as f:
            if type == 'json':
                json.dump(self.std_data, f, ensure_ascii=False, indent=4, **kwargs)
            elif type == "jsonl":
                f.writelines([json.dumps(item, ensure_ascii=False) + "\n" for item in self.std_data])
            else:
                raise ValueError("Unsupported type")

    def sort_by_key(self, key: Optional[Callable] = None, reverse: bool = False) -> None:
        """
        Sort data using a key function.

        Args:
            key: Function to extract comparison key
            reverse: Sort in descending order if True
        """
        if key is None:
            key = lambda x: str(x)  # Default to string representation
        self.std_data.sort(key=key, reverse=reverse)

    def remove(self, item: Union[int, Dict]) -> None:
        """
        Remove an item by index or content.

        Args:
            item: Index or dictionary to remove

        Raises:
            ValueError: If index is out of bounds
        """
        if isinstance(item, int):
            try:
                del self.std_data[item]
            except IndexError:
                raise ValueError(f"Index {item} is out of bounds")
        else:
            self.std_data = [x for x in self.std_data if x != item]

    def copy(self):
        return Std_Json(self)

    def iter_data(self, batch_size: Optional[int] = None) -> Generator[List[Dict], None, None]:
        """
        Generate data in batches or one at a time.

        Args:
            batch_size: Number of items to yield at once. If None, yields individual items.

        Yields:
            Items or batches of items
        """
        if batch_size is None:
            yield from self.std_data
        else:
            for i in range(0, len(self.std_data), batch_size):
                yield self.std_data[i:i + batch_size]

    def filter(self, predicate: Callable[[Dict], bool]) -> 'Std_Json':
        """
        Filter data based on a predicate function.

        Args:
            predicate: Function returning True for items to keep

        Returns:
            Filtered Std_Json instance
        """
        filtered_data = [item for item in self.std_data if predicate(item)]
        return Std_Json(filtered_data)

    def map(self, transform: Callable[[Dict], Dict]) -> 'Std_Json':
        """
        Transform each item in the dataset.

        Args:
            transform: Function to transform each item

        Returns:
            Transformed Std_Json instance
        """
        transformed_data = [transform(item) for item in self.std_data]
        return Std_Json(transformed_data)

    def sample(self, n: Union[int, float], seedNum: Optional[int] = None, return_remaining: bool = False) \
            -> Union['Std_Json', Tuple['Std_Json', 'Std_Json']]:
        """
        Sample random items with more flexible options.

        Args:
            n: Number or proportion of items to sample
            seedNum: Random seed for reproducibility
            return_remaining: If True, returns a tuple of sampled and remaining data

        Returns:
            Sampled data, or tuple of sampled and remaining data
        """
        if n <= 0:
            raise ValueError("Sample size must be greater than 0")
        elif 0 < n <= 1:
            n = int(len(self.std_data) * n)
        else:
            n=int(n)

        n = min(n,len(self.std_data))
        # if n > len(self.std_data):
        #     raise ValueError("Sample size cannot exceed total data size")

        if seedNum is not None:
            random.seed(seedNum)

        sampled_data = random.sample(self.std_data, n)

        if return_remaining:
            remaining_data = [item for item in self.std_data if item not in sampled_data]
            return Std_Json(sampled_data), Std_Json(remaining_data)

        return Std_Json(sampled_data)

    def set(self, sort_key=False, ori=False):
        res_set = set()
        for item in self.std_data:
            res_set.add(json.dumps(item, ensure_ascii=False, sort_keys=sort_key))
        new_std_data = [json.loads(item) for item in res_set]
        if ori:
            self.std_data = deepcopy(new_std_data)
        return Std_Json(new_std_data)

    def _convert_dtypes(self, df: pd.DataFrame, dtype_map: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Convert DataFrame column types based on provided mapping or automatic inference.

        Args:
            df: Input DataFrame
            dtype_map: Dictionary mapping column names to their desired types

        Returns:
            DataFrame with converted types
        """
        if dtype_map:
            for col, dtype in dtype_map.items():
                if col in df.columns:
                    try:
                        if dtype == bool:
                            # Handle special case for boolean conversion
                            df[col] = df[col].map({'True': True, 'False': False, '1': True, '0': False,
                                                   True: True, False: False, 1: True, 0: False})
                        else:
                            df[col] = df[col].astype(dtype)
                    except (ValueError, TypeError) as e:
                        print(f"Warning: Could not convert column '{col}' to type {dtype}. Error: {str(e)}")
        return df

    def _validate_data(self, df: pd.DataFrame, validators: Dict[str, Callable[[pd.Series], bool]]) -> List[
        Dict[str, List[int]]]:
        """
        Validate DataFrame using provided validation functions.

        Args:
            df: Input DataFrame
            validators: Dictionary mapping column names to validation functions

        Returns:
            List of validation errors
        """
        validation_errors = []
        for col, validator in validators.items():
            if col in df.columns:
                invalid_rows = df.index[~df[col].apply(validator)].tolist()
                if invalid_rows:
                    validation_errors.append({
                        'column': col,
                        'invalid_rows': invalid_rows
                    })
        return validation_errors

    def from_excel(self, file_path: Union[str, Path],
                   sheet_name: Optional[Union[str, int, List[str], List[int]]] = 0,
                   dtype_map: Optional[Dict[str, Any]] = None,
                   validators: Optional[Dict[str, Callable[[Any], bool]]] = None,
                   header_rows: Union[int, List[int]] = 0,
                   skip_blank_lines: bool = True,
                   **kwargs) -> Optional[Dict[str, List[Dict[str, Any]]]]:
        """
        Enhanced import from Excel with type conversion, validation, and multi-sheet support.

        Args:
            file_path: Path to the Excel file
            sheet_name: Name(s) or index(es) of sheet(s) to read
            dtype_map: Dictionary mapping column names to their desired types
            validators: Dictionary mapping column names to validation functions
            header_rows: Row number(s) to use as column names
            skip_blank_lines: Whether to skip blank lines
            **kwargs: Additional arguments to pass to pandas.read_excel()

        Returns:
            Dictionary mapping sheet names to data if multiple sheets are read

        Raises:
            ValueError: If validation fails or file is empty
        """
        try:
            # Handle multiple header rows
            if isinstance(header_rows, list):
                kwargs['header'] = header_rows

            # Read Excel file
            dfs = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)

            # Convert to dict if single sheet was read
            if not isinstance(dfs, dict):
                dfs = {0: dfs}

            result = {}
            for sheet, df in dfs.items():
                if df.empty:
                    raise ValueError(f"Sheet '{sheet}' is empty")

                # Skip blank lines if requested
                if skip_blank_lines:
                    df = df.dropna(how='all')

                # Convert data types
                if dtype_map:
                    df = self._convert_dtypes(df, dtype_map)

                # Validate data
                if validators:
                    errors = self._validate_data(df, validators)
                    if errors:
                        raise ValueError(f"Validation errors in sheet '{sheet}': {errors}")

                # Convert NaN values to None
                df = df.where(pd.notnull(df), None)

                # Convert to list of dictionaries
                result[str(sheet)] = df.to_dict(orient='records')

            # If single sheet was requested, update std_data
            if isinstance(sheet_name, (str, int)) or sheet_name is None:
                self.std_data = list(result.values())[0]
                return None

            return result

        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")

    def to_excel(self, file_path: Union[str, Path],
                 sheet_mapping: Optional[Union[str, Mapping[str, List[Dict]]]] = None,
                 index: bool = False,
                 column_order: Optional[List[str]] = None,
                 column_widths: Optional[Dict[str, int]] = None,
                 **kwargs) -> None:
        """
        Enhanced export to Excel with multi-sheet support and formatting options.

        Args:
            file_path: Path to save the Excel file
            sheet_mapping: Sheet name or dictionary mapping sheet names to data
            index: Whether to write row numbers
            column_order: List of columns in desired order
            column_widths: Dictionary mapping column names to their widths
            **kwargs: Additional arguments to pass to pandas.DataFrame.to_excel()
        """
        if not self.std_data and not sheet_mapping:
            raise ValueError("No data to export")

        # Create Excel writer
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            if isinstance(sheet_mapping, str):
                # Single sheet export
                df = pd.DataFrame(self.std_data)
                sheet_name = sheet_mapping
                self._write_sheet(df, writer, sheet_name, index, column_order, column_widths, **kwargs)
            elif isinstance(sheet_mapping, dict):
                # Multi-sheet export
                for sheet_name, data in sheet_mapping.items():
                    df = pd.DataFrame(data)
                    self._write_sheet(df, writer, sheet_name, index, column_order, column_widths, **kwargs)
            else:
                # Default single sheet export
                df = pd.DataFrame(self.std_data)
                self._write_sheet(df, writer, 'Sheet1', index, column_order, column_widths, **kwargs)

    def _write_sheet(self, df: pd.DataFrame, writer: pd.ExcelWriter, sheet_name: str,
                     index: bool, column_order: Optional[List[str]], column_widths: Optional[Dict[str, int]],
                     **kwargs) -> None:
        """Helper method to write and format a single sheet."""
        # Reorder columns if specified
        if column_order:
            df = df.reindex(columns=column_order)

        # Write DataFrame to Excel
        df.to_excel(writer, sheet_name=sheet_name, index=index, **kwargs)

        # Apply column widths if specified
        if column_widths:
            worksheet = writer.sheets[sheet_name]
            for idx, column in enumerate(df.columns):
                if column in column_widths:
                    worksheet.column_dimensions[chr(65 + idx)].width = column_widths[column]

    def from_csv(self, file_path: Union[str, Path],
                 encoding: str = 'utf-8',
                 dtype_map: Optional[Dict[str, Any]] = None,
                 validators: Optional[Dict[str, Callable[[Any], bool]]] = None,
                 header_rows: Union[int, List[int]] = 0,
                 skip_blank_lines: bool = True,
                 **kwargs) -> None:
        """
        Enhanced import from CSV with type conversion and validation.

        Args:
            file_path: Path to the CSV file
            encoding: File encoding
            dtype_map: Dictionary mapping column names to their desired types
            validators: Dictionary mapping column names to validation functions
            header_rows: Row number(s) to use as column names
            skip_blank_lines: Whether to skip blank lines
            **kwargs: Additional arguments to pass to pandas.read_csv()
        """
        try:
            # Handle multiple header rows
            if isinstance(header_rows, list):
                kwargs['header'] = header_rows

            # Read CSV file
            df = pd.read_csv(file_path, encoding=encoding, **kwargs)
            if df.empty:
                raise ValueError("CSV file is empty")

            # Skip blank lines if requested
            if skip_blank_lines:
                df = df.dropna(how='all')

            # Convert data types
            if dtype_map:
                df = self._convert_dtypes(df, dtype_map)

            # Validate data
            if validators:
                errors = self._validate_data(df, validators)
                if errors:
                    raise ValueError(f"Validation errors: {errors}")

            # Convert NaN values to None
            df = df.where(pd.notnull(df), None)

            # Convert DataFrame to list of dictionaries
            self.std_data = df.to_dict(orient='records')

        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

    def to_csv(self, file_path: Union[str, Path],
               encoding: str = 'utf-8',
               index: bool = False,
               column_order: Optional[List[str]] = None,
               **kwargs) -> None:
        """
        Enhanced export to CSV with column ordering.

        Args:
            file_path: Path to save the CSV file
            encoding: File encoding
            index: Whether to write row numbers
            column_order: List of columns in desired order
            **kwargs: Additional arguments to pass to pandas.DataFrame.to_csv()
        """
        if not self.std_data:
            raise ValueError("No data to export")

        df = pd.DataFrame(self.std_data)

        # Reorder columns if specified
        if column_order:
            df = df.reindex(columns=column_order)

        df.to_csv(file_path, encoding=encoding, index=index, **kwargs)

    def __add__(self, other: "Std_Json"):
        if not isinstance(other, Std_Json):
            raise TypeError("Operand must be a Std_Json object")
        sum_std_json = self.copy()
        sum_std_json.std_data.extend(deepcopy(other.std_data))
        return sum_std_json

    def __sub__(self, other: "Std_Json"):
        # 将数据转换为集合进行操作
        self_set = {json.dumps(item, sort_keys=True) for item in self.std_data}
        other_set = {json.dumps(item, sort_keys=True) for item in other.std_data}
        diff_set = self_set - other_set
        return Std_Json([json.loads(item) for item in diff_set])

    def __and__(self, other: "Std_Json"):
        print("and")
        if not isinstance(other, Std_Json):
            raise TypeError("Operand must be a Std_Json object")
        temp_std_json = self.set()
        common_data = [item for item in temp_std_json if item in other.std_data]
        return Std_Json(common_data)

    def __or__(self, other: "Std_Json"):
        print("or")
        if not isinstance(other, Std_Json):
            raise TypeError("Operand must be a Std_Json object")
        combined_json = self.set()
        for item in deepcopy(other.std_data):
            if item not in combined_json.std_data:
                combined_json.std_data.append(item)
        return combined_json

    def __len__(self):
        return len(self.std_data)

    def __getitem__(self, index):
        try:
            return self.std_data[index]
        except IndexError:
            raise IndexError(f"Index {index} is out of bounds")

    def __repr__(self):
        return json.dumps(self.std_data, ensure_ascii=False, indent=4)

    def __iter__(self):
        return iter(self.std_data)


if __name__ == "__main__":
    pass