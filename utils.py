from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# Function to calculate different date offsets based on the given date
def calculate_date_offsets(input_date: datetime):
    offsets = {
        "1-Day": (input_date - timedelta(days=1)).date(),
        "1-Week": (input_date - timedelta(weeks=1)).date(),
        "2-Week": (input_date - timedelta(weeks=2)).date(),
        "3-Week": (input_date - timedelta(weeks=3)).date(),
        "1-Month": (input_date - relativedelta(months=1)).date(),
        "3-Month": (input_date - relativedelta(months=3)).date(),
        "6-Month": (input_date - relativedelta(months=6)).date(),
        "9-Month": (input_date - relativedelta(months=9)).date(),
        "1-Year": (input_date - relativedelta(years=1)).date(),
        "2-Year": (input_date - relativedelta(years=2)).date(),
        "3-Year": (input_date - relativedelta(years=3)).date(),
    }
    return offsets

def get_yesterday_date():
    return datetime.now() - timedelta(days=1)

# Test function to verify the outputs
def test_calculate_date_offsets():
    # Test date - for consistency, using a fixed date
    import datetime as dt
    test_date = datetime(2024, 10, 31)
    results = calculate_date_offsets(test_date)

    # Expected results
    expected_results = {
        "yesterday": dt.date(2024, 10, 30),
        "1_week_before": dt.date(2024, 10, 24),
        "2_weeks_before": dt.date(2024, 10, 17),
        "1_month_before": dt.date(2024, 9, 30),
        "3_months_before": dt.date(2024, 7, 31),
        "6_months_before": dt.date(2024, 4, 30),
        "9_months_before": dt.date(2024, 1, 31),
        "1_year_before": dt.date(2023, 10, 31),
        "2_years_before": dt.date(2022, 10, 31),
        "3_years_before": dt.date(2021, 10, 31),
    }

    # Compare each result to the expected output
    test_results = {}
    for key, value in results.items():
        test_results[key] = (value == expected_results[key])

    return test_results


import holidays


def is_public_holiday_malaysia():
    """
    Check if today is a public holiday in Malaysia, including regional holidays.

    Args:
        region (str): The region code for Malaysia (e.g., "MY", "MY-01" for Johor).
                      Default is "MY" (all national and regional holidays).

    Returns:
        bool: True if today is a public holiday in the specified region, False otherwise.
    """
    # Get today's date
    import datetime
    today = datetime.date.today()

    # Define Malaysia holidays with the given region
    malaysia_holidays = holidays.Malaysia()

    # Check if today is a holiday
    return today in malaysia_holidays


# Run the test function
if __name__ == "__main__":
    test_results = test_calculate_date_offsets()
    print(test_results)
