"""
Script to automatically take screenshots of all 3 tabs of the Streamlit Web App
using headless Chrome via Selenium with exact Streamlit selectors.
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def capture_streamlit_tabs():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,920")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_api_traffic_forecasting", "figures")
    os.makedirs(output_dir, exist_ok=True)
    
    print("Launching headless Chrome...")
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "http://localhost:8501"
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait for Streamlit to render tabs (div with data-testid="stTab")
        print("Waiting for Streamlit tabs to render...")
        wait = WebDriverWait(driver, 20)
        tabs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="stTab"]')))
        print(f"Found {len(tabs)} tabs!")
        
        # Give extra time for Plotly charts in Tab 1 to render
        time.sleep(4)
        
        # Tab 1 Screenshot
        tab1_path = os.path.join(output_dir, "web_tab1_forecast.png")
        driver.save_screenshot(tab1_path)
        print(f"Captured Tab 1: {tab1_path} ({os.path.getsize(tab1_path)} bytes)")
        
        # Tab 2 Screenshot
        if len(tabs) >= 2:
            print("Clicking Tab 2...")
            driver.execute_script("arguments[0].click();", tabs[1])
            time.sleep(3.5)
            tab2_path = os.path.join(output_dir, "web_tab2_anomalies.png")
            driver.save_screenshot(tab2_path)
            print(f"Captured Tab 2: {tab2_path} ({os.path.getsize(tab2_path)} bytes)")
            
        # Tab 3 Screenshot
        if len(tabs) >= 3:
            print("Clicking Tab 3...")
            driver.execute_script("arguments[0].click();", tabs[2])
            time.sleep(3.5)
            tab3_path = os.path.join(output_dir, "web_tab3_raw_benchmarks.png")
            driver.save_screenshot(tab3_path)
            print(f"Captured Tab 3: {tab3_path} ({os.path.getsize(tab3_path)} bytes)")
            
        print("All 3 screenshots captured successfully!")
        return tab1_path, tab2_path, tab3_path
        
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_streamlit_tabs()
