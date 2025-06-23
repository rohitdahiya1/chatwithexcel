#pip install 'vanna[chromadb,openai,postgres]'
#pip install psycopg2
#pip install psycopg2-binary

from vanna.openai import OpenAI_Chat
from openai import AzureOpenAI
from vanna.chromadb import ChromaDB_VectorStore
import pandas as pd
import psycopg2
import urllib.parse as urlparse


# Parse PostgreSQL connection URL
DATABASE_URL = "postgres://avnadmin:AVNS_x8Um2fuCxKqrsAD@pg-23fd6e-rohitdahiya38-a9d8.b.aivencloud.com:18226/defaultdb1?sslmode=require"
url = urlparse.urlparse(DATABASE_URL)

PG_CONFIG = {
    'dbname': url.path[1:],
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'port': url.port,
    'sslmode': 'require'
}


# Azure OpenAI + Vanna setup
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        azure_client = AzureOpenAI(
            api_key="abf9b7951ac44ec187265d7054b8e804",
            api_version="2024-08-01-preview",
            azure_endpoint="https://corp-openai-poc-tas-sm-01.openai.azure.com/",
            azure_deployment="gpt-4o"
        )
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=azure_client, config=config)


vn = MyVanna(config={'model': 'gpt-4o'})


vn.connect_to_postgres(
    host='pg-23fd696e-rohitdahiya308-a9d8.b.aivencloud.com',
    dbname='defaultdb',
    user='avnadmin',
    password='AVNS_x8Um2fuCaTcbxKqrsAD',
    port='18626'
)

# The information schema query may need some tweaking depending on your database. This is a good starting point.
# df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

# # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
# plan = vn.get_training_plan_generic(df_information_schema)

# # If you like the plan, then uncomment this and run it to train
# vn.train(plan=plan)

# The following are methods for adding training data. Make sure you modify the examples to match your database.

# DDL statements are powerful because they specify table names, colume names, types, and potentially relationships
# vn.train(ddl="""
#     CREATE TABLE IF NOT EXISTS my-table (
#         id INT PRIMARY KEY,
#         name VARCHAR(100),
#         age INT
#     )
# """)

# Sometimes you may want to add documentation about your business terminology or definitions.
# vn.train(documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full")

# You can also add SQL queries to your training data. This is useful if you have some queries already laying around. You can just copy and paste those from your editor to begin generating new SQL.
# vn.train(sql="SELECT * FROM my-table WHERE name = 'John Doe'")


vn.ask(
    question="List all orders along with customer names and order dates."
    # print_results=True,
    # auto_train=False,
    # visualize=False,
    # allow_llm_to_see_data=False
)


#Which customers have registered in the last 30 days?
#What is the total number of orders placed so far?
#List all orders along with customer names and order dates.
#Which customers have placed orders worth more than $500 in a single transaction?
#Which customer has purchased the highest quantity of products in total across all their orders, and what is the total quantity?




