import logging 
from abc import ABC, abstractmethod
from typing import Union
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

class DataStrategy(ABC):
    #Abstract class defining strategy for handling data
    @abstractmethod
    def handle_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass

class DataPreProcessStrategy(DataStrategy):


    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:

        try:
            data = data.drop([
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date",
                "order_estimated_delivery_date",
                "order_purchase_timestamp"
            ], axis=1)

            data["product_weight_g"].fillna(data["product_weight_g"].median(), inplace=True)
            data["product_length_cm"].fillna(data["product_weight_g"].median(), inplace=True)
            data["product_height_cm"].fillna(data["product_weight_g"].median(), inplace=True)
            data["product_width_cm"].fillna(data["product_weight_g"].median(), inplace=True)
            data["review_comment_message"].fillna("No review", inplace=True)

            data = data.select_dtypes(include=[np.number])
            cols_to_drop = ["customer_zip_code_prefix", "order_item_id"]
            data = data.drop(cols_to_drop, axis=1)
            return data

        except Exception as e:
            logging.error("Error in processing data: {}".format(e))
            raise e


# Pure Python equivalent. Input: a list of row dictionaries, with numbers
# already converted to int or float. Output: a new list of row dictionaries.
# def handle_data_without_libraries(rows):
#     date_columns = {
#         "order_approved_at",
#         "order_delivered_carrier_date",
#         "order_delivered_customer_date",
#         "order_estimated_delivery_date",
#         "order_purchase_timestamp",
#     }
#     columns_to_remove = date_columns | {
#         "customer_zip_code_prefix", "order_item_id"
#     }
#     columns_to_fill = (
#         "product_weight_g", "product_length_cm",
#         "product_height_cm", "product_width_cm",
#     )
#
#     def is_missing(value):
#         return value is None or value != value  # NaN is unequal to itself.
#
#     def median(values):
#         ordered = sorted(values)
#         middle = len(ordered) // 2
#         if len(ordered) % 2:
#             return ordered[middle]
#         return (ordered[middle - 1] + ordered[middle]) / 2
#
#     medians = {}
#     for column in columns_to_fill:
#         present = [
#             row[column] for row in rows
#             if column in row and not is_missing(row[column])
#         ]
#         medians[column] = median(present) if present else None
#
#     cleaned_rows = []
#     for row in rows:
#         cleaned = row.copy()  # Leave the original input unchanged.
#         for column in date_columns:
#             cleaned.pop(column, None)
#         for column in columns_to_fill:
#             if column in cleaned and is_missing(cleaned[column]):
#                 cleaned[column] = medians[column]
#         if "review_comment_message" in cleaned and is_missing(
#             cleaned["review_comment_message"]
#         ):
#             cleaned["review_comment_message"] = "No review"
#
#         # select_dtypes works on whole columns, so use the same set of
#         # numeric columns for every output row.
#         if not cleaned_rows:
#             numeric_columns = {
#                 key for source_row in rows for key, value in source_row.items()
#                 if key not in columns_to_remove
#                 and isinstance(value, (int, float))
#                 and not isinstance(value, bool)
#             }
#         numeric_row = {
#             column: cleaned.get(column) for column in numeric_columns
#         }
#         cleaned_rows.append(numeric_row)
#     return cleaned_rows

class DataDivideStrategy(DataStrategy):

    def handle_data(self, data:pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        try:
            x = data.drop(["review_score"], axis=1)
            y = data["review_score"]
            X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error("Error in dividing data: {}".format(e))
            raise e

class DataCleaning:

    def __init__(self, data: pd.DataFrame, strategy: DataStrategy):
        self.data = data
        self.strategy = strategy

    def handle_data(self) -> Union[pd.DataFrame, pd.Series]:
        try:
            return self.strategy.handle_data(self.data)
        except Exception as e:
            logging.error("Error in handling data{}".format(e))
            raise e


