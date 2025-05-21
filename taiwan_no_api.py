from IPython import get_ipython
from IPython.display import display
# %%

# %%
# ✅ Download and install Chrome (Linux version for Colab)
!wget -q -O /tmp/chrome-linux.zip https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux64.zip
!unzip -q /tmp/chrome-linux.zip -d /opt/
!ln -sf /opt/chrome-linux64/chrome /usr/bin/chromium-browser
!chmod +x /usr/bin/chromium-browser

# ✅ Download and install Chromedriver (must match version above)
!wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chromedriver-linux64.zip
!unzip -q /tmp/chromedriver.zip -d /tmp/
!mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver
!chmod +x /usr/bin/chromedriver

!pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)

# ✅ Test it
driver.get("https://example.com")
print("Page title:", driver.title)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/opt/chrome-linux64/chrome"

# Create driver
driver = webdriver.Chrome(options=chrome_options)

# Create a WebDriverWait instance
wait = WebDriverWait(driver, 180) # Wait for up to 180 seconds
# Target URL
url = "https://earnings.dgbas.gov.tw/query_payroll_D.aspx"
driver.get(url)

# Add a small delay after getting the URL, sometimes helpful
time.sleep(3)
# Wait for the visible start year dropdown
start_dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "countYearBegin")))
Select(start_dropdown).select_by_value("10401")  # 2015 JAN

# Wait for the visible end year dropdown
end_dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "countYearEnd")))
Select(end_dropdown).select_by_value("11403")  # 2025 MAR

# Set cycle type (optional, if needed)
cycle_type = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cycleType")))
Select(cycle_type).select_by_value("forMonth")

# Select month (e.g., All Month)
month_dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cycleValue")))
Select(month_dropdown).select_by_value("0")  # All Month
# Select one Item
checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sITEM'][value='A02']")))
checkbox.click()

# Select one industry
checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sIND_CODE'][value='30']")))
checkbox.click()

# Select one class
checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sJob'][value='Z']")))
checkbox.click()

# Select one option
checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='sDataProp'][value='V']")))
checkbox.click()

go_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Go')]")))
go_button.click()

# Wait for the table to load
time.sleep(5)

# Locate the table within the 'tableFour' div
table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tableFour table")))
rows = table.find_elements(By.TAG_NAME, "tr")

# Parse table data into DataFrame
data = []
for row in rows:
    cols = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
    if cols:
        data.append(cols)

  # Normalize the data by keeping only the last two columns of each row
cleaned_data = [row[-2:] for row in data if len(row) >= 2]

# Create DataFrame
df = pd.DataFrame(cleaned_data, columns=["Month", "Value"])

print(df.head())
print("DataFrame shape:", df.shape)
print("First row:")
print(df.iloc[0])

df.to_excel("Taiwan.xlsx", index=False)
# Download link in Colab
from google.colab import files
files.download("Taiwan.xlsx")

# Close driver
driver.quit()
