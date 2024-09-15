from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from time import sleep
import re

def wait(byMeth, elem_name, delay=15):
    return WebDriverWait(driver, delay).until(EC.presence_of_element_located((byMeth, elem_name)))

chk = False
try:
    with open('login.txt', 'r') as f:
        enroll = f.readline().strip()
        password = f.readline().strip()
    chk = True
    print('Login found!')
except:pass

if not chk:
    enroll = input('Enter your Enrollment number:')
    password = input('Enter your password:')
    with open('login.txt', 'w') as f:
        f.write(enroll + '\n' + password)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service,options=chrome_options)
print('Please Wait...\n\n')

driver.get('https://cms.bahria.edu.pk/Logins/Student/Login.aspx')
enroll1 = driver.find_element(By.ID, 'BodyPH_tbEnrollment')
enroll1.clear()
enroll1.send_keys(enroll)
pass1 = driver.find_element(By.ID, 'BodyPH_tbPassword')
pass1.clear()
pass1.send_keys(password)
sel = driver.find_element(By.ID,'BodyPH_ddlInstituteID')
select = Select(sel)
select.select_by_value('1')
try:
    driver.find_element(By.ID, 'BodyPH_btnLogin').click()
except:
    print("Wrong Credentials!")
sleep(1)
driver.find_element(By.LINK_TEXT,'Go To LMS').click()

window_handles = driver.window_handles
driver.switch_to.window(window_handles[-1])

driver.get('https://lms.bahria.edu.pk/Student/Assignments.php')

sleep(2)
sel1 = driver.find_element(By.ID, 'courseId')
courseIds = {x.get_attribute("value"):x.text for x in sel1.find_elements(By.TAG_NAME, "option")}

for courseId in courseIds:
    courseUrl = "https://lms.bahria.edu.pk/Student/Assignments.php?s=MjAyNDM%3D&oc="+courseId
    driver.get(courseUrl)
    res= len(re.findall('(?=(No Submission))', driver.page_source))
    if res:
        print(f"{res} Assignments due for course {courseIds[courseId]}\n")
    else:
        print(f'No Assignments due for course {courseIds[courseId]}\n')
driver.close()