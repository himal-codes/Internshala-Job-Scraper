import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Target: Internshala Python Internships
url = "https://internshala.com/internships/python-internship"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

print("🕵️‍♂️ Sending the Master Spy to Internshala...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get all job cards
    jobs = soup.find_all('div', class_='individual_internship')
    
    print(f"🔥 SUCCESS! We found {len(jobs)} internships.")
    
    internship_list = []
    
    for job in jobs:
        try:
            # 1. Get Title (Safe extraction)
            title_tag = job.find('h3', class_='job-internship-name')
            title = title_tag.text.strip() if title_tag else "Unknown Role"

            # 2. Get Company (FIXED: Using 'p' tag instead of 'div')
            company_tag = job.find('p', class_='company-name')
            company = company_tag.text.strip() if company_tag else "Unknown Company"

            # 3. Get Location
            location_tag = job.find('div', class_='locations')
            location = location_tag.text.strip() if location_tag else "Remote/Unknown"

            # 4. Get Stipend (The Money)
            stipend_tag = job.find('span', class_='stipend')
            stipend = stipend_tag.text.strip() if stipend_tag else "Unpaid/Hidden"
            
            # 5. Get Apply Link
            link_tag = job.find('a', class_='job-title-href')
            link = "https://internshala.com" + link_tag['href'] if link_tag else "No Link"

            internship_list.append({
                "Role": title,
                "Company": company,
                "Location": location,
                "Stipend": stipend,
                "Apply Link": link
            })
            
        except Exception as e:
            # If one job fails, just skip it and keep going
            continue

    # Save to Excel
    if len(internship_list) > 0:
        print(f"💾 Saving {len(internship_list)} jobs to 'internshala_jobs.xlsx'...")
        df = pd.DataFrame(internship_list)
        df.to_excel("internshala_jobs.xlsx", index=False)
        print("🚀 MISSION COMPLETE! Open the Excel file now.")
    else:
        print("⚠️ Found the boxes, but couldn't extract text. Show Gems the errors.")

else:
    print("❌ Blocked. Status Code:", response.status_code)