from playwright.sync_api import sync_playwright
import os

# Example: Automating interaction with static HTML files using file:// URLs

html_file_path = os.path.abspath('path/to/your/file.html')
file_url = f'file://{html_file_path}'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    page.goto(file_url)
    page.screenshot(path='static_page.png', full_page=True)
    
    # Interaction examples (uncomment/modify as needed)
    # page.click('text=Click Me')
    # page.fill('#name', 'John Doe')
    
    browser.close()

print("Static HTML automation completed!")
