from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json, time, random, math

# Load Json Data
with open("config.json") as js:
    data = json.load(js)
    baseUsername = str(data['startofusername'])
    password = str(data['password'])
    accountnumber = int(data['accountstocreate'])
    numbersafterusername = int(data['Digits'])

options = webdriver.ChromeOptions()
# Disable Google Password Manager
prefs = {"credentials_enable_service": False,
     "profile.password_manager_enabled": False}

options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


url = "https://www.roblox.com/signup"
print("Creating {} Accounts".format(accountnumber))

def genNumber():
    ph_no = []
    for i in range(numbersafterusername): 
        ph_no.append(str(random.randint(0, 9))) 
    return str().join(ph_no)

def Signup(secondDriver: webdriver.Chrome, username: str):
    # Write Log
    with open("log.txt", 'a') as log:
        write = "Successfully Created Account: " + username
        print(write)
        log.write(write)
        log.write("\n")
        log.close()
    # CLick Signup Button
    sigup_button = secondDriver.find_element(By.ID, "signup-button")
    webdriver.ActionChains(secondDriver).move_to_element(sigup_button).click().perform()
    time.sleep(100)
    

def createAccount(driver):
    # Set Month
    month = Select(driver.find_element(By.ID, "MonthDropdown"))
    month.select_by_value('Jan')
    # Set Day
    day = Select(driver.find_element(By.ID, "DayDropdown"))
    day.select_by_value('01')
    # Set Year
    year = Select(driver.find_element(By.ID, "YearDropdown"))
    year.select_by_index(len(year.options)-1)
    sign_pass = driver.find_element(By.ID, "signup-password")
    sign_pass.send_keys(password)
    sign_user = driver.find_element(By.ID, "signup-username")
    username = baseUsername + genNumber()
    sign_user.send_keys(username)
    time.sleep(0.7)
    # Is Username In Use
    if len(driver.find_element(By.ID, "signup-usernameInputValidation").text) == 0:
        Signup(driver, username)
    else:
        print("Generating New Number Set")
        sign_user.clear()
        time.sleep(0.2)
        username = baseUsername + genNumber()
        sign_user.send_keys(username)
        Signup(driver, username)

# Enter Account Making Loop
for i in range(100):
    firstDriver = webdriver.Chrome(options=options)
    stealth(firstDriver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    firstDriver.get(url)
    # Wait Until Driver Has Started
    element_present = EC.presence_of_element_located((By.ID, 'signup'))
    WebDriverWait(firstDriver, math.inf).until(element_present)
    createAccount(firstDriver)
    time.sleep(1)