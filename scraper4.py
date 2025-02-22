import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_website():
    url = "https://www.sparkl.me/learn/ib/economics-sl/normative-vs-positive-economics/revision-notes/1802"  # Replace with the target website
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        soup = BeautifulSoup(response.text, "html.parser")
        classRemove = ("left-section__header","left-section__footer","main-pdf-btn","mobile-action-container","mobile-flash_card-modal d-none","modal fade","menu-container","flashcard-main d-none","flashcard-section d-none","coming-soon-section d-none","sparkl-extra-content","faq-section","mobile-left-section")
        for tag in soup.find_all("header"):
            tag.decompose()  # Completely removes the tag from the tree
        for tag in soup.find_all("footer"):
            tag.decompose()
        for tag in soup.find_all("script"):
            tag.decompose()  # Completely removes the tag from the tree
        for tag in soup.find_all("noscript"):
            tag.decompose()
        for tag in soup.find_all("nav"):
            tag.decompose()
        for tag in soup.find_all("img"):
            tag.decompose()
        for tag in soup.find_all("div", class_=classRemove):
            tag.decompose()

        topics_dict = {}

# Find all main topics
        for topic_container in soup.find_all("div", class_="topic-list-container"):
            main_topic_number = topic_container.find("span", class_="topic-title").text.strip()
            main_topic_name = topic_container.find_all("span", class_="topic-title")[1].text.strip()

            topics_dict[main_topic_number] = {"name": main_topic_name, "subtopics": {}}

    # Find all subtopics
            for subtopic in topic_container.find_all("div", class_="accordion-item"):
                subtopic_number = subtopic.find("span", class_="sub-topic-title-number").text.strip()
                subtopic_name = subtopic.find("span", class_="sub-topic-title-name").text.strip()
                topics_dict[main_topic_number]["subtopics"][subtopic_number] = {"name": subtopic_name, "sub-subtopics": {}}

        # Find all sub-subtopics
                for sub_subtopic in subtopic.find_all("div", class_="sub-topic-subpart-container"):
                    sub_subtopic_number = sub_subtopic.find("span", class_="sub-topic-subpart-title-number").text.strip()
                    sub_subtopic_name = sub_subtopic.find("span", class_="sub-topic-subpart-title-name").text.strip()
                    topics_dict[main_topic_number]["subtopics"][subtopic_number]["sub-subtopics"][sub_subtopic_number] = sub_subtopic_name

# Print dictionary
        print(json.dumps(topics_dict, indent=4, ensure_ascii=False))

# Save dictionary as JSON
        with open("scrape4_left.json", "w", encoding="utf-8") as json_file:
            json.dump(topics_dict, json_file, indent=4, ensure_ascii=False)

############################################################################################
#####################################################################################
        content_dict = {}

# Get main topic (h1)
        main_topic_tag = soup.find("h1")
        if not main_topic_tag:
            raise ValueError("No <h1> main topic found in the document.")

        main_topic = main_topic_tag.text.strip()
        content_dict[main_topic] = {}

# Initialize section and subsection
        current_section = None
        current_subsection = None

# Iterate through elements
        for tag in soup.find_all(["h2", "h3", "p", "ul", "div", "table"]):
            if tag.name == "h2":
                current_section = tag.text.strip()
                content_dict[main_topic][current_section] = {}
                current_subsection = None  # Reset subsection when a new section starts

            elif tag.name == "h3":
                if not current_section:
                    print(f"Warning: Found h3 '{tag.text.strip()}' without an h2. Assigning to 'Miscellaneous'.")
                    current_section = "Miscellaneous"
                    content_dict[main_topic][current_section] = {}

                current_subsection = tag.text.strip()
                content_dict[main_topic][current_section][current_subsection] = []

            elif tag.name in ["p", "div"]:
                if not current_section:
                    print(f"Warning: Found content '{tag.text.strip()[:30]}...' without an h2. Skipping.")
                    continue
                if not current_subsection:
                    print(f"Warning: Found content under section '{current_section}' without an h3. Assigning to 'General'.")
                    current_subsection = "General"
                    content_dict[main_topic][current_section][current_subsection] = []

                content_dict[main_topic][current_section][current_subsection].append(tag.text.strip())

            elif tag.name == "ul":
                list_items = [li.text.strip() for li in tag.find_all("li")]
                if current_section and current_subsection:
                    content_dict[main_topic][current_section][current_subsection].extend(list_items)
                else:
                    print(f"Warning: Found list without valid section/subsection. Skipping.")

            elif tag.name == "table":
                table_data = []
                for row in tag.find_all("tr"):
                    cells = [cell.text.strip() for cell in row.find_all(["th", "td"])]
                    table_data.append(cells)

                if current_section and current_subsection:
                    content_dict[main_topic][current_section][current_subsection].append({"table": table_data})
                else:
                    print(f"Warning: Found table but missing section/subsection. Skipping.")

# Save structured data as JSON
        with open("scrape4_text.json", "w", encoding="utf-8") as json_file:
            json.dump(content_dict, json_file, indent=4, ensure_ascii=False)

# Print structured content
        print(json.dumps(content_dict, indent=4, ensure_ascii=False))

        main_content = soup.body.prettify()

        with open("scrape4.html", "w", encoding="utf-8") as file:
            file.write(main_content)
        # Extract only the relevant parts (body content)
        return str(main_content)  # Convert HTML to string for frontend rendering
    
    except requests.exceptions.RequestException as e:
        return f"<p>Error fetching content: {e}</p>"
