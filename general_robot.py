import pandas as pd
import time
import undetected_chromedriver as uc
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_click_date import click_date
from utils import calculate_date_offsets, is_public_holiday_malaysia
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shared import get_chrome_driver
import os

# def is_alert_present(driver):
#     try:
#         alert = driver.switch_to.alert  # Attempt to switch to the alert
#         alert.accept()
#         return True  # If successful, alert is present
#     except NoAlertPresentException:
#         return False  # No alert is present
def is_alert_present(driver, timeout=2):
    try:
        start_time = time.time()  # Track start time
        # Wait for the alert to be present within the specified timeout
        print(f"Checking for alert at {start_time}")
        driver.implicitly_wait(0)  # Disable implicit wait
        print(1)
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        print(2)
        alert = driver.switch_to.alert  # Switch to the alert
        print(3)
        driver.implicitly_wait(5)  # Restore implicit wait
        print(4)
        alert.accept()  # Accept the alert if needed
        print(5)
        print(f"Alert found and handled at {time.time()}, took {time.time() - start_time:.2f} sec")
        return True  # Alert was present and handled
    except TimeoutException:
        print(f"Alert found and handled at {time.time()}, took {time.time() - start_time:.2f} sec")
        return False  # No alert was present within the timeout
def open_chrome_and_login(username,password):
    driver = get_chrome_driver()
    print(driver.capabilities["browserVersion"])
    # Step 1: Go to the website's login page
    driver.get("https://www.publicmutualutcconnect.com.my/Login")
    driver.maximize_window()
    # Step 2: Locate the username and password fields
    user_id_input = driver.find_element(By.ID, "LoginVM_UserName")
    password_field = driver.find_element(By.ID, "LoginVM_Password")
    user_id_input.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "btnLogin")
    login_button.click()
    return driver
def click_acknowledge(driver):
    wait = WebDriverWait(driver, 10)
    # Check if the modal title element is present
    modal_title_elements = driver.find_elements(By.ID, "infoModalLabel")
    if modal_title_elements:  # Check if the modal title exists
        modal_title = modal_title_elements[0]  # Get the first element
        if "Warning" in modal_title.text:
            # Locate the button and click it if it exists
            proceed_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-secondary[onclick='updateWarningModal()']")))
            proceed_button.click()
    else:
        print("Warning modal is not present.")
def return_result_in_dict(driver):
    fund_total_return_div = driver.find_element(By.ID, "ucCompare_divFundTotalReturn")
    labels = fund_total_return_div.find_elements(By.TAG_NAME, "label")
    fund_info_list = [label.text.strip() for label in labels]
    def parse_list_to_dict(data_list):
        result_dict = {}
        for item in data_list:
            key = item.split(' ')[0]  # Extract the key (first part)
            value = item.split(': ')[1]  # Extract the value (after ": ")
            result_dict[key] = value  # Assign to dictionary
        return result_dict
    parsed_dict = parse_list_to_dict(fund_info_list)
    return parsed_dict
def click_from_calendar(driver):
    calendar_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".input-group-append[data-target='#ucCompare_datetimepickerfrom']"))
    )
    time.sleep(5)
    calendar_icon.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".bootstrap-datetimepicker-widget"))
    )
def click_to_calendar(driver):
    calendar2_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".input-group-append[data-target='#ucCompare_datetimepickerto']"))
    )
    calendar2_icon.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".bootstrap-datetimepicker-widget"))
    )
def wait_for_button_to_be_enabled(driver, timeout=10):
    """
    Waits for the button with id 'ddGraphCompare' to be enabled (i.e., not disabled).

    Parameters:
        driver: The Selenium WebDriver instance.
        timeout: Maximum time to wait for the button to be enabled.

    Returns:
        The WebElement if the button is enabled within the timeout period.
    """
    try:
        # Wait for the button to be clickable, which implies it’s enabled
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "ddGraphCompare"))
        )
        return element  # Return the enabled button element
    except :
        print("Button did not become enabled within the specified time.")
        return None
def wait_for_image_to_appear(driver, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "imgUTCLogo"))
        )
        return element  # Return the element once it appears
    except :
        print("Image did not appear within the specified time.")
        return None
def format_date(value):
    return value.strftime("%d%b%Y")
def add_collected_date_to_data(data, all_date, results):
    for key, date in all_date.items():
        # Format date string
        formatted_date = format_date(date)

        # Retrieve the results for the current period
        success = results.get(key, {})

        # Prepare row data
        # row = {
        #     "Period": f"{key}|{formatted_date}"
        # }
        row = {
            "Period": f"{key}"
        }
        row.update(success)

        # Append to the data list
        data.append(row)

    # Handle 'selected_to_date' if it exists in results
    if 'selected_to_date' in results:
        selected_to_date = results['selected_to_date']
        for column, value in selected_to_date.items():
            # Add a row where the column (e.g., PeAGFF) is used, and Selected_To_Date is a key
            row = {
                "Period": "Selected_To_Date",  # Fixed value as the row identifier
                column: value                 # Add the value under the corresponding column
            }
            # Append to the data list
            data.append(row)



def generate_series():
    data = []
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')

    driver = open_chrome_and_login(username, password)
    wait_for_image_to_appear(driver, 10)
    print("Image appear")
    try:
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.QuickAccess[href='/fund-analytics']"))
        )
        print("able to click fund analytics")
    except:
        pass

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    fund_analytics_link = driver.find_element(By.CSS_SELECTOR, "a.QuickAccess[href='/fund-analytics']")
    fund_analytics_link.click()
    time.sleep(5)

    # switch to next tab
    driver.switch_to.window(driver.window_handles[1])
    wait_for_button_to_be_enabled(driver, 30)
    driver.get(
        "https://utcole.publicmutualutcconnect.com.my/PM.Web.UTCFunds/FundCompareGraph/144;178;176;163;170/UNIT%20TRUST")
    # remaining_e_fund = ["170;163;176", "181","178","144","188"]
    fund_number_string = os.environ.get('FUND_NUMBER')
    # result = [item.strip() for item in fund_number_string.split(",")]
    remaining_e_fund = [item.strip() for item in fund_number_string.split(",")]
    time.sleep(4)
    element = driver.find_element(By.CSS_SELECTOR,
                                  "input.form-control.datetimepicker-input[data-target='#ucCompare_datetimepickerto']")
    date_to_text = element.get_attribute("value")
    print(date_to_text)
    date_to_text = datetime.datetime.strptime(date_to_text, "%d-%b-%Y")
    all_date = calculate_date_offsets(date_to_text)

    time.sleep(4)
    click_acknowledge(driver)
    '''
    # results = {}
    # for key, value in all_date.items():
    #     print(f"{key}: {value}")
    #     click_from_calendar(driver)
    #     click_date(value, driver)
    #
    #     show_button = driver.find_element(By.ID, "ucCompare_btnShow")
    #     show_button.click()
    #     element = driver.find_element(By.CSS_SELECTOR,
    #                                   "input.form-control.datetimepicker-input[data-target='#ucCompare_datetimepickerfrom']")
    #     date_text = element.get_attribute("value")
    #
    #     print(date_text)
    #     time.sleep(5)
    #     success = return_result_in_dict(driver)
    #     print(success)
    #     results[key] = success
    #     driver.refresh()
    # add_collected_date_to_data(data, all_date, results)
    '''
    for i in remaining_e_fund:
        fund_link = f"https://utcole.publicmutualutcconnect.com.my/PM.Web.UTCFunds/FundCompareGraph/{i}/UNIT%20TRUST"
        driver.get(fund_link)
        time.sleep(4)
        click_acknowledge(driver)

        element = driver.find_element(By.CSS_SELECTOR,
                                      "input.form-control.datetimepicker-input[data-target='#ucCompare_datetimepickerto']")
        date_to_text_element = element.get_attribute("value")
        print(date_to_text_element)
        date_to_text = datetime.datetime.strptime(date_to_text_element, "%d-%b-%Y")
        all_date = calculate_date_offsets(date_to_text)

        results = {}
        for index, (key, value) in enumerate(all_date.items()):
            print(f"{key}: {value}")
            click_from_calendar(driver)
            click_date(value, driver)

            show_button = driver.find_element(By.ID, "ucCompare_btnShow")
            show_button.click()
            if is_alert_present(driver):
                break
            else:
                print("No alert is present")
            element = driver.find_element(By.CSS_SELECTOR,
                                          "input.form-control.datetimepicker-input[data-target='#ucCompare_datetimepickerfrom']")
            date_text = element.get_attribute("value")

            print(date_text)
            success = return_result_in_dict(driver)
            fund_name = next(iter(success))
            print(success)
            results[key] = success
            driver.refresh()
        results["selected_to_date"] = {fund_name:date_to_text_element}
        add_collected_date_to_data(data, all_date, results)
        print()
    fund_arrangement_string = os.environ.get('FUND_ARRANGEMENT')
    # result = [item.strip() for item in fund_number_string.split(",")]
    fund_arrangement = [item.strip() for item in fund_arrangement_string.split(",")]
    my_order = ["Period"] + fund_arrangement

    df = pd.DataFrame(data)

    # Preserve original order without using categorical for now
    df['Period'] = df['Period'].astype(str)

    # Capture the order after converting to string
    period_order = df['Period'].unique()

    # Use groupby to consolidate rows with the same Period, taking the first non-null value
    consolidated_df = df.groupby("Period", as_index=False).first()

    # Fill missing values
    consolidated_df.fillna("N/A", inplace=True)

    # Reorder using the captured order
    consolidated_df = consolidated_df.set_index('Period').reindex(period_order).reset_index()

    df = consolidated_df[my_order]
    file_name = os.environ.get('FILE_NAME')
    df.to_csv(file_name + ".csv", index=False)  # Save the data to a CSV file
    if driver:
        driver.quit()




if __name__ == "__main__":
    print("run job")
    if is_public_holiday_malaysia():
        print("Today is a public holiday in Malaysia.")
    else:
        import pytz
        from send_email import send_email_with_attachment
        malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
        today_date = datetime.datetime.now(malaysia_tz).strftime("%d %b %Y")  # Format: 10 Nov 2024
        body = "This is the extracted data from the website. Please refer to the date in the excel file."
        from_email = ""
        app_password = ""  # Use the app password generated in your Google account
        generate_series()
        # generate_normal_series(2)
        # generate_normal_series()
        # generate_prs_series()
        # generate_e_series()
        file_name = os.environ.get('FILE_NAME')
        attachment_path = file_name+".csv"  # Replace with the actual file path
        subject = f"{today_date} Extracted Data"
        subject = subject + " " + file_name

        to_email = ""
        send_email_with_attachment(subject, body, to_email, from_email, app_password, attachment_path)

#
# docker tag general_1 asia-southeast1-docker.pkg.dev/fyp2-366317/hcproject/general_1:latest
# docker push asia-southeast1-docker.pkg.dev/fyp2-366317/hcproject/general_1:latest
#
# docker tag general_1 us-central1-docker.pkg.dev/hc-fund-automation/hc-docker/general_1:latest
# docker push us-central1-docker.pkg.dev/hc-fund-automation/hc-docker/general_1:latest
