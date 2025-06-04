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





response = pai.chat('What is the total sales by region, show in bargraph',country_df,region_df)
print("the type of response is" ,type(response))
print("########################################")
print("the generated code is", response.last_code_executed)
print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")  # Convert response to dictionary for better readability
print(response)
