from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, lit, sequence, explode, to_date, expr, last_day
from typing import List, Dict


class DateChecker:
    """
    Generates a range of dates based on frequency (daily or monthly).
    """
    def __init__(self, start_date: str, end_date: str, frequency: str = "daily", exclude_date: list = None) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.exclude_date = exclude_date
        self.spark = SparkSession.getActiveSession()

    def generate_date_range(self) -> DataFrame:
        """
        Generate date range based on frequency.
        
        Returns:
            DataFrame: DataFrame containing the generated dates.
        """
        if self.frequency == "daily":
            df = self.spark.createDataFrame(
                [(self.start_date, self.end_date)], ["start_date", "end_date"]
            ).select(
                explode(
                    sequence(
                        to_date(col("start_date")),
                        to_date(col("end_date")),
                        expr("interval 1 day")
                    )
                ).alias("check_date")
            )
        elif self.frequency == "monthly":
            df = self.spark.createDataFrame(
                    [(self.start_date, self.end_date)], ["start_date", "end_date"]
                ).select(
                    explode(
                        sequence(
                            last_day(to_date(col("start_date"))),
                            last_day(to_date(col("end_date"))),
                            expr("interval 1 month")
                        )
                    ).alias("as_at_dt")
                )
            df = df.select(last_day(col("as_at_dt")).alias("check_date"))
        else:
            raise ValueError("Invalid frequency. Supported values are 'daily' and 'monthly'.")
        
        df = df.filter(~df['check_date'].isin(self.exclude_date))
        return df


class TableDateValidator:
    """
    Validates missing dates for a single table.
    """
    def __init__(
        self, table_name: str,
        start_date: str,
        end_date: str,
        frequency: str = "daily",
        date_col: str = "as_at_dt",
        custom_filter: str = None,
        exclude_date: list = None
    ) -> None:
    
        self.table_name = table_name
        self.date_col = date_col
        self.spark = SparkSession.getActiveSession()
        self.date_checker = DateChecker(start_date, end_date, frequency, exclude_date)
        self.custom_filter = custom_filter

    def check_missing_dates(self) -> DataFrame:
        """
        Check for missing dates in the table.
        
        Returns:
            DataFrame: DataFrame containing missing dates.
        """
        df = self.spark.table(self.table_name)
        if self.custom_filter:
            df = df.filter(self.custom_filter)
        
        if self.date_col not in df.columns:
            raise ValueError(f"Column '{self.date_col}' not found in table '{self.table_name}'.")
        
        date_range_df = self.date_checker.generate_date_range()
        missing_dates_df = date_range_df.join(
            df.withColumn(self.date_col, to_date(col(self.date_col))),
            col(self.date_col) == date_range_df.check_date,
            how="left_anti"
        )
        return missing_dates_df.orderBy(col('check_date'))


class MultipleTablesValidator:
    """
    Orchestrates missing dates validation across multiple tables.
    """
    def __init__(self, table_configs: List[Dict[str, str]]) -> None:
        self.table_configs = table_configs

    def run_checks(self) -> None:
        """
        Run checks for all table configurations.
        
        Raises:
            ValueError: If missing dates are found in any table.
        """
        all_missing_dates = []
        for config in self.table_configs:
            table_name = config["table_name"]
            start_date = config["start_date"]
            end_date = config["end_date"]
            frequency = config.get("frequency","daily") # Optional
            date_col = config.get("date_col","as_at_dt") # Optional
            custom_filter = config.get("custom_filter",None) # Optional
            exclude_date = config.get("exclude_date",None) # Optional
            try:
                validator = TableDateValidator(table_name, start_date, end_date, frequency, date_col, custom_filter, exclude_date)
                missing_dates = validator.check_missing_dates()
                if missing_dates.count() > 0:
                    print(f"Missing dates in table '{table_name}' ({frequency}):")
                    missing_dates.show(truncate=False)
                    all_missing_dates.append((table_name, missing_dates))
                else:
                    print(f"No missing dates found in table '{table_name}' ({frequency}).")
            except Exception as e:
                print(f"Error checking table '{table_name}': {e}")

        if all_missing_dates:
            raise ValueError("Missing dates detected in one or more tables.")
