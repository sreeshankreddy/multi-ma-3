"""
Table extraction module for documents.
Handles extraction and conversion of tables to structured formats.
"""

import os
from typing import List, Dict, Any, Optional
import pdfplumber
import pandas as pd
import re


class TableExtractor:
    """
    Extracts tables from PDF documents and converts them to structured formats.
    Supports multiple extraction methods and table conversions.
    """

    @staticmethod
    def extract_tables_from_pdf(pdf_path: str) -> List[pd.DataFrame]:
        """
        Extract all tables from a PDF file.

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            List[pd.DataFrame]: List of extracted tables as DataFrames.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        tables = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()

                    if page_tables:
                        for table in page_tables:
                            # Convert table to DataFrame
                            if table:
                                # First row is usually headers
                                headers = table[0]
                                data = table[1:]
                                df = pd.DataFrame(data, columns=headers)
                                df['source_page'] = page_num + 1
                                tables.append(df)

            return tables

        except Exception as e:
            raise Exception(f"Error extracting tables from PDF: {str(e)}")

    @staticmethod
    def extract_tables_with_page_info(pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract tables with detailed page and position information.

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            List[Dict]: Table information including page number and position.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        tables_info = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extract table settings
                    table_settings = {
                        "vertical_strategy": "lines",
                        "horizontal_strategy": "lines"
                    }

                    page_tables = page.extract_tables(table_settings)

                    if page_tables:
                        for table_idx, table in enumerate(page_tables):
                            if table:
                                headers = table[0]
                                data = table[1:]
                                df = pd.DataFrame(data, columns=headers)

                                tables_info.append({
                                    'table_index': table_idx,
                                    'page_number': page_num + 1,
                                    'dataframe': df,
                                    'row_count': len(df),
                                    'column_count': len(df.columns),
                                    'columns': list(df.columns)
                                })

            return tables_info

        except Exception as e:
            raise Exception(f"Error extracting tables with info: {str(e)}")

    @staticmethod
    def extract_tables_from_page(pdf_path: str, page_num: int) -> List[pd.DataFrame]:
        """
        Extract tables from a specific page.

        Args:
            pdf_path (str): Path to PDF file.
            page_num (int): Page number (1-indexed).

        Returns:
            List[pd.DataFrame]: Tables from the specified page.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        tables = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                if page_num < 1 or page_num > len(pdf.pages):
                    raise ValueError(f"Invalid page number: {page_num}")

                page = pdf.pages[page_num - 1]
                page_tables = page.extract_tables()

                if page_tables:
                    for table in page_tables:
                        if table:
                            headers = table[0]
                            data = table[1:]
                            df = pd.DataFrame(data, columns=headers)
                            tables.append(df)

            return tables

        except Exception as e:
            raise Exception(f"Error extracting tables from page {page_num}: {str(e)}")

    @staticmethod
    def convert_table_to_csv(df: pd.DataFrame, output_path: str) -> None:
        """
        Convert DataFrame table to CSV file.

        Args:
            df (pd.DataFrame): Input DataFrame.
            output_path (str): Path to save CSV file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)

    @staticmethod
    def convert_table_to_json(df: pd.DataFrame, output_path: str) -> None:
        """
        Convert DataFrame table to JSON file.

        Args:
            df (pd.DataFrame): Input DataFrame.
            output_path (str): Path to save JSON file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_json(output_path, orient='records', indent=2)

    @staticmethod
    def convert_table_to_html(df: pd.DataFrame, output_path: str) -> None:
        """
        Convert DataFrame table to HTML file.

        Args:
            df (pd.DataFrame): Input DataFrame.
            output_path (str): Path to save HTML file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_html(output_path, index=False)

    @staticmethod
    def get_table_statistics(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get statistics about a table.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            Dict: Table statistics.
        """
        stats = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
            'text_columns': df.select_dtypes(include=['object']).columns.tolist()
        }

        return stats

    @staticmethod
    def clean_table_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean table data: remove empty rows/columns, trim whitespace.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        # Remove completely empty rows
        df = df.dropna(how='all')

        # Remove completely empty columns
        df = df.dropna(axis=1, how='all')

        # Strip whitespace from string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        return df

    @staticmethod
    def merge_tables(tables: List[pd.DataFrame], how: str = 'outer') -> pd.DataFrame:
        """
        Merge multiple tables.

        Args:
            tables (List[pd.DataFrame]): List of DataFrames to merge.
            how (str): Merge method ('outer', 'inner', 'left', 'right').

        Returns:
            pd.DataFrame: Merged DataFrame.
        """
        if not tables:
            return pd.DataFrame()

        merged = tables[0]
        for table in tables[1:]:
            merged = pd.merge(merged, table, how=how)

        return merged

    @staticmethod
    def extract_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract and convert numeric columns.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with converted numeric columns.
        """
        df_copy = df.copy()

        for col in df_copy.columns:
            # Try to convert to numeric
            df_copy[col] = pd.to_numeric(df_copy[col], errors='ignore')

        return df_copy

    @staticmethod
    def detect_table_headers(df: pd.DataFrame) -> List[str]:
        """
        Detect and return table headers.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            List[str]: List of column headers.
        """
        return list(df.columns)

    @staticmethod
    def find_empty_cells(df: pd.DataFrame) -> Dict[str, List[int]]:
        """
        Find empty cells in table.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            Dict: Dictionary mapping column names to list of row indices with empty cells.
        """
        empty_cells = {}

        for col in df.columns:
            empty_rows = df[df[col].isnull()].index.tolist()
            if empty_rows:
                empty_cells[col] = empty_rows

        return empty_cells

    @staticmethod
    def table_to_dict(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Convert table to list of dictionaries.

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            List[Dict]: List of row dictionaries.
        """
        return df.to_dict('records')

    @staticmethod
    def export_all_tables(pdf_path: str, output_dir: str, format: str = 'csv') -> List[str]:
        """
        Extract all tables from PDF and export in specified format.

        Args:
            pdf_path (str): Path to PDF file.
            output_dir (str): Directory to save exported tables.
            format (str): Export format ('csv', 'json', 'html').

        Returns:
            List[str]: List of exported file paths.
        """
        os.makedirs(output_dir, exist_ok=True)
        tables = TableExtractor.extract_tables_from_pdf(pdf_path)
        exported_files = []

        for idx, table in enumerate(tables):
            filename = f"table_{idx + 1}.{format}"
            filepath = os.path.join(output_dir, filename)

            if format == 'csv':
                TableExtractor.convert_table_to_csv(table, filepath)
            elif format == 'json':
                TableExtractor.convert_table_to_json(table, filepath)
            elif format == 'html':
                TableExtractor.convert_table_to_html(table, filepath)

            exported_files.append(filepath)

        return exported_files
