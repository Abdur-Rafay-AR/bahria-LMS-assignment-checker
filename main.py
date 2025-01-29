import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import re
import os

def wait(driver, byMeth, elem_name, delay=15):
    return WebDriverWait(driver, delay).until(EC.presence_of_element_located((byMeth, elem_name)))

def get_assignments(enroll, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH", "chromedriver.exe"))
    
    results = []
    
    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        driver.get('https://cms.bahria.edu.pk/Logins/Student/Login.aspx')
        wait(driver, By.ID, 'BodyPH_tbEnrollment').send_keys(enroll)
        wait(driver, By.ID, 'BodyPH_tbPassword').send_keys(password)
        Select(wait(driver, By.ID, 'BodyPH_ddlInstituteID')).select_by_value('1')
        wait(driver, By.ID, 'BodyPH_btnLogin').click()

        wait(driver, By.LINK_TEXT, 'Go To LMS').click()
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://lms.bahria.edu.pk/Student/Assignments.php')

        course_select = wait(driver, By.ID, 'courseId')
        course_ids = {option.get_attribute("value"): option.text for option in course_select.find_elements(By.TAG_NAME, "option")}

        for course_id, course_name in course_ids.items():
            course_url = f"https://lms.bahria.edu.pk/Student/Assignments.php?s=MjAyNDM%3D&oc={course_id}"
            driver.get(course_url)
            assignments_due = len(re.findall('(?=(No Submission))', driver.page_source))
            results.append({
                "course": course_name,
                "assignments_due": assignments_due,
                "status": "Pending" if assignments_due else "Completed"
            })
    
    return results

# Streamlit UI
st.set_page_config(page_title="LMS Assignment Checker", page_icon="📚", layout="wide")
st.markdown("""
    <style>
        .title-text { text-align: center; font-size: 32px; font-weight: bold; color: var(--text-color); }
        .container { padding: 20px; border-radius: 10px; background: var(--background-color); }
        .status-box { padding: 10px; border-radius: 5px; margin: 10px 0; font-weight: bold; }
        .pending { background-color: rgba(255, 75, 75, 0.2); border-left: 4px solid #ff4b4b; }
        .completed { background-color: rgba(46, 204, 113, 0.2); border-left: 4px solid #2ecc71; }
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #f8f9fa;
                --background-color: #2c3e50;
            }
        }
        @media (prefers-color-scheme: light) {
            :root {
                --text-color: #2c3e50;
                --background-color: #f8f9fa;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">📚 Bahria LMS Assignment Checker</p>', unsafe_allow_html=True)
st.write("Enter your credentials to check pending assignments")

with st.form("credentials_form"):
    enroll = st.text_input("Enrollment Number", placeholder="Enter your enrollment number")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    submitted = st.form_submit_button("🔍 Check Assignments")

if submitted:
    if not enroll or not password:
        st.error("Please fill both enrollment number and password")
    else:
        with st.spinner("Checking assignments..."):
            try:
                progress_bar = st.progress(0)
                results = get_assignments(enroll, password)
                
                st.subheader("📌 Assignment Status")
                cols = st.columns(2)
                
                for index, result in enumerate(results[1:], start=1):
                    status_class = "pending" if result['assignments_due'] else "completed"
                    cols[index % 2].markdown(f"""
                    <div class="status-box {status_class}">
                        <h4 style="margin: 0">{result['course']}</h4>
                        <p style="margin: 5px 0">Assignments Due: {result['assignments_due']}</p>
                        <p style="margin: 0">Status: <strong>{result['status']}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    progress_bar.progress((index + 1) / len(results))
                
                total_due = sum(item['assignments_due'] for item in results[1:])
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; text-align: center; background: linear-gradient(45deg, #2c3e50, #1abc9c); color: #fff">
                    <h3>Total Assignments Pending</h3>
                    <p style="font-size: 24px; font-weight: bold;">{total_due}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align: center; color: red; font-weight: bold;">⚠️ This is an unofficial interface and not affiliated with Bahria University</p>', unsafe_allow_html=True)
st.markdown("""
    <div style="position: fixed; bottom: 0; width: 100%; background-color: black; color: #f8f9fa; text-align: center; padding: 10px 0; left: 0;">
        <p style="margin: 0; font-size: 14px;">Developed by <strong>Abdur Rafay</strong>. Check out the source code on <a href="https://github.com/Abdur-Rafay-AR/bahria-LMS-assignment-checker" target="_blank" style="color: #1abc9c;">GitHub</a>.</p>
    </div>
""", unsafe_allow_html=True)
