import streamlit as st 
import streamlit as st
import subprocess
"""

# Tenders Web Scraper
In this website you will find some python scripts to scrape tenders from different websites. They will return a csv file with the tenders of your interest
with description and link. 

"""
first_variable = st.text_input("Enter your name")

if first_variable:
    ret = subprocess.run(["python", "script.py", first_variable])
    st.write(ret)




# keywords = st.text_input("Enter the keywords in lower case you are interested in searching for separated by commas")
# keywords = keywords.split(",") 

# weeks = st.number_input("Enter the number of weeks you want to search for")

# def runWebScrapers():
#     subprocess.run(["python", "F:\Desktop\Proyectos\Tender-Web-Scraper\aysa.py", keywords, weeks])

# st.button("Run script", on_click=runWebScrapers)