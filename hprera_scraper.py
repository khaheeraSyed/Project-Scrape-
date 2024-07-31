import requests
from bs4 import BeautifulSoup

# URL of the HPRERA Public Dashboard
url = "http://hprera.nic.in/PublicDashboard"

# Sending a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Finding the "Registered Projects" table
    registered_projects_table = soup.find("table", {"id": "tblRegisteredProjects"})

    # Extracting the first 6 project RERA numbers
    rera_links = registered_projects_table.find_all("a")[:6]
    rera_numbers = [link.text for link in rera_links]

    # Creating a list to store the project details
    project_details = []

    # Loop through each RERA number and scrape the detail page
    for rera_number in rera_numbers:
        detail_url = f"http://hprera.nic.in/ProjectDetails?id={rera_number}"
        detail_response = requests.get(detail_url)
        
        # Check if the detail page request was successful
        if detail_response.status_code == 200:
            detail_soup = BeautifulSoup(detail_response.content, "html.parser")
            
            # Extracting the GSTIN, PAN, Name, and Permanent Address
            gstin = detail_soup.find("span", {"id": "lblGSTINNo"}).text.strip() if detail_soup.find("span", {"id": "lblGSTINNo"}) else "N/A"
            pan = detail_soup.find("span", {"id": "lblPANNo"}).text.strip() if detail_soup.find("span", {"id": "lblPANNo"}) else "N/A"
            name = detail_soup.find("span", {"id": "lblProjectName"}).text.strip() if detail_soup.find("span", {"id": "lblProjectName"}) else "N/A"
            permanent_address = detail_soup.find("span", {"id": "lblPermanentAddress"}).text.strip() if detail_soup.find("span", {"id": "lblPermanentAddress"}) else "N/A"
            
            # Adding the project details to the list
            project_details.append({
                "RERA Number": rera_number,
                "GSTIN": gstin,
                "PAN": pan,
                "Name": name,
                "Permanent Address": permanent_address
            })
        else:
            print(f"Failed to retrieve details for RERA Number: {rera_number}")

    # Finally Printing the project details
    for project in project_details:
        print(project)
else:
    print("Failed to retrieve the main page.")
