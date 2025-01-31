import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  
import re
import os

def wait(driver, byMeth, elem_name, delay=15):
    return WebDriverWait(driver, delay).until(EC.presence_of_element_located((byMeth, elem_name)))

def get_assignments(enroll, password, progress_callback):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install()) 
    
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

        total_courses = len(course_ids)
        for index, (course_id, course_name) in enumerate(course_ids.items()):
            if course_name == "Select Course":
                continue
            course_url = f"https://lms.bahria.edu.pk/Student/Assignments.php?s=MjAyNDM%3D&oc={course_id}"
            driver.get(course_url)
            assignments_due = 0
            rows = driver.find_element(By.CSS_SELECTOR, ".table.table-hover").find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                if 'No Submission' in row.text and 'Deadline Exceeded' not in row.text:
                    assignments_due += 1
            results.append({
                "course": course_name,
                "assignments_due": assignments_due,
                "status": "Pending" if assignments_due else "Completed"
            })
            progress_callback(0.95 * (index / total_courses))
    
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
        @media (max-width: 768px) {
            .title-text { font-size: 24px; }
            .status-box { font-size: 14px; }
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
                results = get_assignments(enroll, password, progress_bar.progress)
                
                st.subheader("📌 Assignment Status")
                cols = st.columns(2)
                
                for index, result in enumerate(results, start=1):
                    status_class = "pending" if result['assignments_due'] else "completed"
                    cols[index % 2].markdown(f"""
                    <div class="status-box {status_class}">
                        <h4 style="margin: 0">{result['course']}</h4>
                        <p style="margin: 5px 0">Assignments Due: {result['assignments_due']}</p>
                        <p style="margin: 0">Status: <strong>{result['status']}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                
                total_due = sum(item['assignments_due'] for item in results)
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; text-align: center; background: linear-gradient(45deg, #0b1c26, #0a4d3b); color: #fff">
                    <h3>Total Assignments Pending</h3>
                    <p style="font-size: 24px; font-weight: bold;">{total_due}</p>
                </div>
                """, unsafe_allow_html=True)
                
                progress_bar.progress(1.0)  # Indicate completion
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown('<p style="text-align: center; color: red; font-weight: bold;">⚠️ This is an unofficial interface and not affiliated with Bahria University</p>', unsafe_allow_html=True)

developer_name = "Abdur Rafay"
github_url = "https://github.com/Abdur-Rafay-AR/bahria-LMS-assignment-checker"

st.markdown(f"""
    <div style="position:relative; bottom:0; background-color: black; color: #f8f9fa; text-align: center; padding: 10px 0; width: 50%; margin: 0 auto; border-radius: 10px;">
        <p style="margin: 0; font-size: 14px;">Developed by <strong>{developer_name}</strong>. Check out the source code on <a href="{github_url}" target="_blank" style="color: #1abc9c;">GitHub</a>.</p>
    </div>
""", unsafe_allow_html=True)
