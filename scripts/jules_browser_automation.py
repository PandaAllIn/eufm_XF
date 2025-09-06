#!/usr/bin/env python3
"""
Jules Browser Automation - Full automation for Jules login and task delegation
"""

import time
import sys
import os
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class JulesAutomator:
    def __init__(self, headless=False, log_file=None):
        self.headless = headless
        self.log_file = log_file
        self.driver = None
        
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(log_msg + "\n")
    
    def setup_driver(self):
        """Setup Chrome WebDriver with optimal settings"""
        self.log("🔧 Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Optimizations for automation
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.log("✅ Chrome WebDriver ready")
            return True
        except Exception as e:
            self.log(f"❌ Failed to setup WebDriver: {e}")
            return False
    
    def login_to_jules(self, email, password):
        """Login to Jules with provided credentials"""
        self.log("🌐 Navigating to Jules...")
        
        try:
            self.driver.get("https://jules.google.com")
            self.log("📍 Loaded Jules homepage")
            
            # Jules automatically redirects to Google sign-in, so wait for it
            wait = WebDriverWait(self.driver, 15)
            time.sleep(3)  # Allow redirect to complete
            
            self.log(f"🔍 Current URL: {self.driver.current_url}")
            
            # Check if we're already at Google sign-in
            if "accounts.google.com" in self.driver.current_url:
                self.log("✅ Automatically redirected to Google sign-in")
            
            # Enter email
            email_field = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
            email_field.send_keys(email)
            self.log("📧 Entered email")
            
            # Click Next
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            time.sleep(2)
            
            # Enter password
            password_field = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            password_field.send_keys(password)
            self.log("🔐 Entered password")
            
            # Click Next/Sign In
            password_next = self.driver.find_element(By.ID, "passwordNext")
            password_next.click()
            
            # Wait for redirect back to Jules
            time.sleep(5)
            
            # Verify we're logged in by checking for dashboard elements
            try:
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                if "jules.google" in self.driver.current_url:
                    self.log("✅ Successfully logged into Jules")
                    return True
                else:
                    self.log("❌ Login may have failed - unexpected URL")
                    return False
            except TimeoutException:
                self.log("❌ Login timeout - page did not load")
                return False
                
        except Exception as e:
            self.log(f"❌ Login failed with error: {e}")
            return False
    
    def connect_github_repo(self, repo_url):
        """Connect GitHub repository to Jules"""
        self.log(f"🔗 Connecting GitHub repository: {repo_url}")
        
        try:
            wait = WebDriverWait(self.driver, 15)
            
            # Look for repository connection elements
            repo_selectors = [
                "//button[contains(text(), 'Connect')]",
                "//button[contains(text(), 'Add repository')]",
                "//a[contains(text(), 'GitHub')]",
                "[data-testid='connect-repo']",
                ".connect-github"
            ]
            
            # Try to find repo connection button
            for selector in repo_selectors:
                try:
                    if selector.startswith("//"):
                        repo_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    else:
                        repo_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    
                    repo_button.click()
                    self.log("🔗 Clicked repository connection button")
                    break
                except TimeoutException:
                    continue
            
            # Handle GitHub OAuth if needed
            time.sleep(3)
            
            # Look for repository URL input or selection
            try:
                # Try to find URL input
                url_input = self.driver.find_element(By.XPATH, "//input[@type='text' or @type='url']")
                url_input.clear()
                url_input.send_keys(repo_url)
                self.log("📝 Entered repository URL")
                
                # Submit
                submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Connect') or contains(text(), 'Add')]")
                submit_button.click()
                
            except NoSuchElementException:
                # Repository might be auto-detected or in a list
                self.log("🔍 Repository URL input not found - checking for auto-detection")
            
            time.sleep(5)
            self.log("✅ GitHub repository connection attempted")
            return True
            
        except Exception as e:
            self.log(f"❌ Repository connection failed: {e}")
            return False
    
    def delegate_task(self, task_prompt):
        """Delegate task to Jules with comprehensive prompt"""
        self.log("📋 Delegating task to Jules...")
        
        try:
            wait = WebDriverWait(self.driver, 15)
            
            # Look for task input areas
            task_selectors = [
                "//textarea",
                "//input[@type='text']",
                "[data-testid='task-input']",
                ".task-input",
                "#task-description"
            ]
            
            task_input = None
            for selector in task_selectors:
                try:
                    if selector.startswith("//"):
                        task_input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    else:
                        task_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    self.log(f"📝 Found task input with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not task_input:
                self.log("❌ Could not find task input field")
                return False
            
            # Clear and enter the task
            task_input.clear()
            task_input.send_keys(task_prompt)
            self.log("✅ Task prompt entered")
            
            # Submit the task
            submit_selectors = [
                "//button[contains(text(), 'Submit')]",
                "//button[contains(text(), 'Send')]",
                "//button[contains(text(), 'Start')]",
                "[data-testid='submit-task']",
                ".submit-button"
            ]
            
            for selector in submit_selectors:
                try:
                    if selector.startswith("//"):
                        submit_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    submit_button.click()
                    self.log("🚀 Task submitted to Jules")
                    return True
                except NoSuchElementException:
                    continue
            
            # If no submit button found, try Enter key
            task_input.send_keys("\n")
            self.log("⌨️ Submitted task with Enter key")
            return True
            
        except Exception as e:
            self.log(f"❌ Task delegation failed: {e}")
            return False
    
    def monitor_task_progress(self, duration_minutes=30):
        """Monitor Jules task progress for specified duration"""
        self.log(f"👁️ Monitoring task progress for {duration_minutes} minutes...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            try:
                # Look for progress indicators
                progress_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Progress') or contains(text(), 'Working') or contains(text(), 'Complete')]")
                
                if progress_elements:
                    for element in progress_elements:
                        self.log(f"📊 Progress update: {element.text}")
                
                # Check for completion indicators
                complete_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Complete') or contains(text(), 'Done') or contains(text(), 'Finished')]")
                
                if complete_elements:
                    self.log("✅ Task appears to be complete!")
                    return True
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.log(f"⚠️ Monitoring error: {e}")
            
        self.log("⏰ Monitoring period ended")
        return False
    
    def cleanup(self):
        """Clean up browser resources"""
        if self.driver:
            self.driver.quit()
            self.log("🧹 Browser cleanup complete")

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 jules_browser_automation.py <email> <password> <repo_url> [task_prompt]")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    repo_url = sys.argv[3]
    task_prompt = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Setup logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"/Users/panda/Desktop/Claude Code/eufm XF/logs/jules_automation_{timestamp}.log"
    
    automator = JulesAutomator(headless=False, log_file=log_file)
    
    try:
        if not automator.setup_driver():
            sys.exit(1)
        
        if not automator.login_to_jules(email, password):
            sys.exit(1)
        
        if not automator.connect_github_repo(repo_url):
            sys.exit(1)
        
        if task_prompt:
            if not automator.delegate_task(task_prompt):
                sys.exit(1)
            
            # Monitor for 30 minutes
            automator.monitor_task_progress(30)
        
        automator.log("🎉 Jules automation completed successfully!")
        
    except KeyboardInterrupt:
        automator.log("⚠️ Automation interrupted by user")
    except Exception as e:
        automator.log(f"❌ Automation failed: {e}")
    finally:
        automator.cleanup()

if __name__ == "__main__":
    main()