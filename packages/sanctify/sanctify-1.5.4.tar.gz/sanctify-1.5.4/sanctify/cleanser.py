# External Imports
from typing import Iterable

import pandas as pd
from frozendict import frozendict
import demoji

# Internal Imports
from sanctify.constants import Constants, DefaultColumns, PrimitiveDataTypes
from sanctify.utils import convert_stringified_list_to_list, replace_dict_keys


class Cleanser:
    """
    The Cleanser class is responsible for validating and checking if a column is present and should be used.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        column_mapping_schema: frozendict | dict,
        data_type_schema: frozendict | dict = None,
    ) -> None:
        """
        Initializes the Cleanser object.

        Args:
            df (pd.DataFrame): The input DataFrame to be cleansed.
            column_mapping_schema (frozendict): The mapping schema for column names.
        """
        self.df = df
        self.mandatory_column_headers = []
        self.column_mapping_schema: frozendict[str:dict] = column_mapping_schema
        self.data_type_schema = data_type_schema
        self.input_vs_standard_column_mapping = self.extract_input_vs_standard_column_mapping()

    def check_if_all_columns_mapping_exist_in_df(self) -> None | ValueError:
        """
        Checks if all columns specified in the column mapping schema exist in the DataFrame.

        Returns:
            None: If all columns are present.

        Raises:
            ValueError: If any mandatory column is missing.
        """
        self.mandatory_column_headers = self.input_vs_standard_column_mapping.keys()

        missing_columns = set(self.mandatory_column_headers) - set(self.df.columns.to_list())
        if len(missing_columns) == 0:
            return None
        else:
            raise ValueError(f"Missing mandatory columns: ({', '.join(missing_columns)})")

    def extract_input_vs_standard_column_mapping(self) -> frozendict:
        """
        Extracts the input vs standard column mapping from the column mapping schema.

        Returns:
            frozendict: The input vs standard column mapping.
        """
        input_vs_standard_column_mapping = {}
        for input_column_name, column_config in self.column_mapping_schema.items():
            input_vs_standard_column_mapping[input_column_name] = column_config.get(
                Constants.STANDARD_COLUMN.value, input_column_name
            )
        return frozendict(input_vs_standard_column_mapping)

    def remove_trailing_spaces_from_column_headers(self) -> pd.DataFrame:
        """
        Removes trailing spaces from column headers in the DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with trailing spaces removed from column headers.
        """
        self.df.columns = self.df.columns.str.strip()
        return self.df

    def drop_unmapped_columns(self) -> pd.DataFrame:
        """
        Drops columns from the DataFrame that are not present in the mandatory column headers.

        Returns:
            pd.DataFrame: The DataFrame with unmapped columns dropped.
        """
        self.mandatory_column_headers = self.input_vs_standard_column_mapping.keys()
        columns_to_keep = self.mandatory_column_headers
        self.df = self.df[columns_to_keep]
        return self.df

    def drop_fully_empty_rows(self, inplace: bool = True) -> pd.DataFrame:
        """
        Drops rows from the DataFrame that are fully empty.

        Args:
            inplace (bool): Whether to drop rows in-place or return a new DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with fully empty rows dropped.
        """
        if inplace is True:
            self.df.dropna(how="all", inplace=inplace)
        else:
            self.df = self.df.dropna(how="all", inplace=inplace)

        return self.df

    def drop_rows_with_errors(self, inplace: bool = True, ignore_columns_list: Iterable = []) -> pd.DataFrame:
        """
        Drops all rows where the 'Error' column is not an empty string.

        Args:
            inplace (bool): If True, modify the DataFrame in-place. If False, return a new DataFrame.
            ignore_columns_list (list, tuple, set): If provided, only rows where the 'Error' column contains any of the other column names will be dropped

        Returns:
            pd.DataFrame: The cleaned DataFrame with rows dropped where the 'Error' column is not an empty string.
        """
        # Check if 'Error' column exists, and if not, create it with empty strings
        if DefaultColumns.ERROR.value not in self.df.columns:
            self.df[DefaultColumns.ERROR.value] = ""

        if isinstance(ignore_columns_list, Iterable) and len(ignore_columns_list) > 0:
            # Get list of column names to consider erroring out except from the ignore_columns_list and the default columns list
            columns_to_consider_erroring_out = (
                set(self.df.columns.to_list())
                - set(ignore_columns_list)
                - set([member.value for member in DefaultColumns])
            )

            # Create a mask for rows where the 'Error' column contains any of the strings in columns_to_consider_erroring_out
            mask = (
                self.df[DefaultColumns.ERROR.value].fillna("").str.contains("|".join(columns_to_consider_erroring_out))
            )

        else:
            # No columns to ignore, use an empty mask
            mask = self.df[DefaultColumns.ERROR.value].fillna("") != ""

        if inplace:
            # Modify the DataFrame in-place
            self.df.drop(self.df[mask].index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
        else:
            # Create a new DataFrame with rows excluded based on the mask
            df = self.df[~mask].copy()
            df.reset_index(drop=True, inplace=True)
            return df

        return self.df

    def remove_trailing_spaces_from_each_cell_value(self) -> pd.DataFrame:
        """
        Removes trailing spaces from each cell value in the DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with trailing spaces removed from each cell value.
        """
        self.df = self.df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return self.df

    def replace_column_headers(self, inplace: bool = True) -> tuple[pd.DataFrame, frozendict]:
        """
        Replaces column headers in the DataFrame based on the input vs standard column mapping.

        Args:
            inplace (bool): Whether to replace column headers in-place or return a new DataFrame.

        Returns:
            tuple[pd.DataFrame, frozendict]: The DataFrame with updated column headers
                and the updated column mapping schema.
        """
        if inplace is True:
            self.df.rename(columns=self.input_vs_standard_column_mapping, inplace=inplace)
        else:
            self.df = self.df.rename(columns=self.input_vs_standard_column_mapping, inplace=inplace)

        self.df.rename(columns=self.input_vs_standard_column_mapping, inplace=True)
        self.mandatory_column_headers = self.input_vs_standard_column_mapping.values()
        updated_column_mapping_schema = frozendict(
            replace_dict_keys(
                original_dict=self.column_mapping_schema,
                key_mapping=self.input_vs_standard_column_mapping,
            )
        )
        self.column_mapping_schema = updated_column_mapping_schema
        return self.df, updated_column_mapping_schema

    def mark_all_duplicates(self, columns: list[str], drop_duplicates: bool = False) -> pd.DataFrame:
        """
        INPLACE: Marks all duplicates based on the specified columns and populates the 'Error' column.

        Args:
            columns (list[str]): The list of column names to check for duplicates.
            drop_duplicates (bool): Whether to drop the duplicate rows or keep them. Default is False.

        Returns:
            pd.DataFrame: The DataFrame with duplicates marked and the 'Error' column populated.
        """
        if DefaultColumns.ERROR.value not in self.df.columns:
            self.df[DefaultColumns.ERROR.value] = ""

        if drop_duplicates is True:
            self.df.drop_duplicates(subset=columns, keep="first", inplace=True, ignore_index=True)
        else:
            duplicate_rows = self.df.duplicated(subset=columns, keep="first")

            error_message = f"Duplicate entry for {', '.join(columns)} passed"
            self.df.loc[duplicate_rows, DefaultColumns.ERROR.value] += " | " + error_message

        return self.df

    def drop_fully_duplicate_rows(self, inplace: bool = True) -> pd.DataFrame:
        """
        Drops rows from the DataFrame that are fully duplicates.

        Args:
            inplace (bool): Whether to drop rows in-place or return a new DataFrame.

        Returns:
            pd.DataFrame: The DataFrame with fully duplicate rows dropped.
        """
        if inplace is True:
            self.df.drop_duplicates(inplace=inplace, ignore_index=True)
        else:
            self.df = self.df.drop_duplicates(inplace=inplace, ignore_index=True)

        return self.df

    def modify_error_column_to_set_all_except_mandatory_to_blank(
        self, df: pd.DataFrame = None, use_standard_column_names: bool = True
    ) -> pd.DataFrame:
        """
        Modifies the 'Error' column in a DataFrame by setting all values to empty strings, except for specific columns that are considered for erroring out.

        Args:
            df (pd.DataFrame, optional): The DataFrame to modify the 'Error' column. If not provided, the DataFrame stored in the `Cleanser` object will be used.
            use_standard_column_names (bool, optional): A boolean flag indicating whether to use standard column names or raw column names from the column mapping schema.

        Returns:
            pd.DataFrame: The modified DataFrame with the 'Error' column updated.
        """
        if df is None:
            df = self.df

        ignore_columns_list = self.get_optional_column_names_from_column_mapping(
            return_standard_column_names=use_standard_column_names
        )

        # Check if 'Error' column exists, and if not, create it with empty strings
        if DefaultColumns.ERROR.value not in df.columns:
            return df

        if len(ignore_columns_list) > 0:
            # Get list of column names to consider erroring out except from the ignore_columns_list and the default columns list
            columns_to_consider_erroring_out = (
                set(df.columns.to_list()) - set(ignore_columns_list) - set([member.value for member in DefaultColumns])
            )

            # Create a mask for rows where the 'Error' column contains any of the strings in columns_to_consider_erroring_out
            mask = df[DefaultColumns.ERROR.value].fillna("").str.contains("|".join(columns_to_consider_erroring_out))

        else:
            # No columns to ignore, use an empty mask
            mask = df[DefaultColumns.ERROR.value].fillna("") != ""

        # Set all rows in the 'Error' column to empty strings except for those specified in columns_to_consider_erroring_out
        df.loc[~mask, DefaultColumns.ERROR.value] = ""

        return df

    def get_optional_column_names_from_column_mapping(
        self, return_standard_column_names: bool = True
    ) -> set | KeyError:
        """
        Retrieves the names of optional columns from the column mapping schema.

        Args:
            return_standard_column_names (bool, optional): A flag indicating whether to return the column names in their standard form or in their raw form. Defaults to True.

        Returns:
            set: A set of column names representing the optional columns from the column mapping schema. The column names can be in their standard form or in their raw form, depending on the value of the return_standard_column_names parameter.

        Example Usage:
            # Initialize the Cleanser object
            cleanser = Cleanser(df, column_mapping_schema)

            # Get the optional column names in their standard form
            optional_columns_standard = cleanser.get_optional_column_names_from_column_mapping(return_standard_column_names=True)

            # Get the optional column names in their raw form
            optional_columns_raw = cleanser.get_optional_column_names_from_column_mapping(return_standard_column_names=False)
        """
        optional_column_names = set()
        for raw_column_name, column_config in self.column_mapping_schema.items():
            if column_config.get(Constants.IS_OPTIONAL.value, False) is True:
                standard_column = column_config.get(Constants.STANDARD_COLUMN.value)
                if return_standard_column_names is True and standard_column is not None:
                    optional_column_names.add(column_config.get(Constants.STANDARD_COLUMN.value))
                else:
                    optional_column_names.add(raw_column_name)
        return optional_column_names

    def merge_data_type_schema_into_column_mapping_schema(self) -> frozendict:
        """
        Merges a data type schema into a column mapping schema.

        Updates the column configuration in the column mapping schema with the corresponding data type configuration from the data type schema.

        Returns:
            A frozendict representing the merged column mapping schema, where the keys are the raw column names and the values are the updated column configurations.
        """
        merged_column_mapping_schema: dict[str:dict] = dict(self.column_mapping_schema)
        for _, column_config in merged_column_mapping_schema.items():
            data_type = column_config.get(Constants.DATA_TYPE.value, {})
            column_config |= self.data_type_schema.get(data_type, {})
        return frozendict(merged_column_mapping_schema)

    def coalesce_rows(self, merge_on: str, agg_col_modifier: str = "Child ") -> None:
        """
        ### Modifies Dataframe in place!

        Merge rows in a DataFrame based on a specified column and aggregate the values of other columns.

        Args:
            merge_on (str): The column name to merge the rows on.
            agg_col_modifier (str, optional): A prefix to add to the new columns that will contain the aggregated values. Defaults to "Child ".

        Returns:
            None

        Example Usage:
            # Initialize the Cleanser object
            cleanser = Cleanser(df=df, column_mapping_schema=column_mapping_schema)

            # Call the coalesce_rows method
            cleanser.coalesce_rows(merge_on="merge_column", agg_col_modifier="Child ")

            # The DataFrame will be modified with merged rows and aggregated values in new columns
        """

        def agg_function(values):
            if len(values) > 1:
                return list(values)
            return ""

        aggregated_df = self.df.groupby(merge_on).first().reset_index()

        for col in self.df.columns:
            if col in self.mandatory_column_headers and (
                not self.column_mapping_schema[col].get(Constants.COALESCE_CHILD_REQUIRED, True)
            ):
                continue
            if col == merge_on:
                continue

            agg_col_name = f"{agg_col_modifier}{col}"
            aggregated_df[agg_col_name] = (
                self.df.groupby(merge_on)[col].agg(lambda x: agg_function(x)).reset_index()[col]
            )
            aggregated_df[agg_col_name] = aggregated_df[agg_col_name].astype(str, errors="ignore")

        self.df = aggregated_df
        self.df.reset_index()

    def explode_rows(self, agg_col_modifier: str = "Child ", remove_agg_cols: bool = False) -> pd.DataFrame:
        """
        Explodes rows in the DataFrame based on specified aggregation columns.

        Args:
            agg_col_modifier (str, optional): The prefix used to identify the aggregation columns. Default is "Child ".
            remove_agg_cols (bool, optional): Whether to remove the aggregation columns after exploding the rows. Default is False.

        Returns:
            pd.DataFrame: New DataFrame with exploded rows.

        Example Usage:
            cleanser = Cleanser(df, column_mapping_schema)
            exploded_df = cleanser.explode_rows(agg_col_modifier="Child ", remove_agg_cols=False)
        """
        agg_cols_map = {}
        for col in self.df.columns:
            if col.startswith(agg_col_modifier):  # Child Account
                agg_cols_map[col] = col.removeprefix(
                    agg_col_modifier
                )  # Behaviour: agg_cols_map["Child Account"] = "account"
                self.df[col] = self.df[col].apply(
                    convert_stringified_list_to_list
                )  # Behaviour: apply on "Child Account"

        self.df = self.df.explode(list(agg_cols_map.keys())).reset_index(drop=True)

        # Replace empty data in current col with non-empty data from subcol
        for subcol, col in agg_cols_map.items():
            non_empty_mask = self.df[subcol].apply(lambda x: bool(x) and any(x))
            self.df.loc[non_empty_mask, col] = self.df.loc[non_empty_mask, subcol]

        # Remove aggregated columns
        if remove_agg_cols is True:
            self.df = self.df.drop(columns=list(agg_cols_map.keys()), inplace=False)

        return self.df

    def merge_same_data_type_column(self, merge_column_data_type: str) -> pd.DataFrame:
        same_data_type_columns = [
            raw_column
            for raw_column, column_config in self.column_mapping_schema.items()
            if merge_column_data_type.lower() == column_config.get(Constants.DATA_TYPE.value).lower()
        ]

        for col in same_data_type_columns[1:]:
            self.df[same_data_type_columns[0]] = (
                self.df[same_data_type_columns[0]].replace("", pd.NA).combine_first(self.df[col])
            )
            self.column_mapping_schema[col][Constants.DATA_TYPE.value] = PrimitiveDataTypes.STRING.value
            self.column_mapping_schema[col].pop(Constants.STANDARD_COLUMN.value, None)
        self.input_vs_standard_column_mapping = self.extract_input_vs_standard_column_mapping()

        return self.df

    def remove_emojis(self) -> pd.DataFrame:
        self.df = self.df.map(lambda x: demoji.replace(x, "") if isinstance(x, str) else x)
        return self.df