import subprocess
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def setup_chrome():
    # Download and install Chrome
    subprocess.run([
        "wget", "-q", "-O", "/tmp/chrome-linux.zip",
        "https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux64.zip"
    ])
    subprocess.run(["unzip", "-q", "/tmp/chrome-linux.zip", "-d", "/opt/"])
    subprocess.run(["ln", "-sf", "/opt/chrome-linux64/chrome", "/usr/bin/chromium-browser"])
    subprocess.run(["chmod", "+x", "/usr/bin/chromium-browser"])

    # Download and install Chromedriver
    subprocess.run([
        "wget", "-q", "-O", "/tmp/chromedriver.zip",
        "https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chromedriver-linux64.zip"
    ])
    subprocess.run(["unzip", "-q", "/tmp/chromedriver.zip", "-d", "/tmp/"])
    subprocess.run(["mv", "/tmp/chromedriver-linux64/chromedriver", "/usr/bin/chromedriver"])
    subprocess.run(["chmod", "+x", "/usr/bin/chromedriver"])

def run_scraper():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
    wait = WebDriverWait(driver, 180)

    url = "https://earnings.dgbas.gov.tw/query_payroll_D.aspx"
    driver.get(url)
    time.sleep(3)

    # Select dropdown values
    Select(wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "countYearBegin")))).select_by_value("10401")
    Select(wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "countYearEnd")))).select_by_value("11403")
    Select(wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cycleType")))).select_by_value("forMonth")
    Select(wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cycleValue")))).select_by_value("0")

    # Click checkboxes
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sITEM'][value='A02']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sIND_CODE'][value='30']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sJob'][value='Z']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sDataProp'][value='V']"))).click()

    # Click Go
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Go')]"))).click()
    time.sleep(5)

    # Extract table
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tableFour table")))
    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows:
        cols = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if cols:
            data.append(cols)

    cleaned_data = [row[-2:] for row in data if len(row) >= 2]
    df = pd.DataFrame(cleaned_data, columns=["Month", "Value"])

    print(df.head())
    print("DataFrame shape:", df.shape)

    df.to_excel("Taiwan.xlsx", index=False)
    driver.quit()

def main():
    setup_chrome()
    run_scraper()

if __name__ == "__main__":
    main()
