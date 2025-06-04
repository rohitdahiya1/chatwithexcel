import streamlit as st
import pandas as pd
import pandasai as pai
from pandasai_openai import AzureOpenAI
import matplotlib.pyplot as plt


AZURE_API_KEY       = ""
AZURE_ENDPOINT      = ""
AZURE_DEPLOYMENT    = ""
AZURE_API_VERSION   = ""

llm = AzureOpenAI(
    api_token=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    deployment_name=AZURE_DEPLOYMENT,
    api_version=AZURE_API_VERSION
)
pai.config.set({"llm": llm})

country_df = pai.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "sales": [5000, 3200, 2900, 4100, 2300, 2100, 2500, 2600, 4500, 7000]
    
})

region_df = pai.DataFrame({
    "country": [
        "United States", "United Kingdom", "France", "Germany", "Italy",
        "Spain", "Canada", "Australia", "Japan", "China"
    ],
    "region": [
        "North America", "Europe", "Europe", "Europe", "Europe",
        "Europe", "North America", "Oceania", "Asia", "Asia"
    ],
    "population_millions": [331, 67, 65, 83, 60, 47, 38, 26, 126, 1441]
})

target_df = pai.DataFrame({
    "region": [
        "North America",
        "Europe",
        "Asia",
        "Oceania"
    ],
    "sales_target": [
        7000,    # Quarterly target for North America
        12000,   # Quarterly target for Europe
        10000,   # Quarterly target for Asia
        3000     # Quarterly target for Oceania
    ]
})



response = pai.chat('What is the total population region wise',country_df,region_df,target_df) # one question related to one table only
#response = pai.chat('how many regions are there where sales is greater then 2600 ',country_df,region_df,target_df) #one question related to joining two tables
#response = pai.chat('how many regions are there where sales is greater then 2600, and also tell me the sum of the population of all regions ',country_df,region_df,target_df) # one question related to joining two tables and one independent question 
#response = pai.chat('Which regions have exceeded or fallen short of their sales targets, and by how much?',country_df,region_df,target_df) # one question related to joining three tables

# response = pai.chat('What is the total sales by region, show in bargraph',country_df,region_df)
print("the generated code is", response.last_code_executed)
print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")  # Convert response to dictionary for better readability
print(response)
