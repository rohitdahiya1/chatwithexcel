#pip install 'vanna[chromadb,openai,postgres]'

from vanna.openai import OpenAI_Chat
from openai import AzureOpenAI
from vanna.chromadb import ChromaDB_VectorStore
import pymssql
import pandas as pd


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        # Azure OpenAI client initialization
        azure_client = AzureOpenAI(
            api_key="",
            api_version="",
            azure_endpoint="",
            azure_deployment=""
        )

        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=azure_client, config=config)



vn = MyVanna(config={'model': 'gpt-4o'})


SERVER = 'it-genaisupport.database.windows.net'
USERNAME = 'it-genaisupport'
PASSWORD = 'itgenai@123'
DATABASE = 'it-genaisupport'


def connect_to_mssql_with_pymssql():
    try:
        conn = pymssql.connect(
            server=SERVER,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE
        )
        return conn
    except Exception as e:
        print("Failed to connect to SQL Server:", e)
        return None


def run_sql(sql):
    conn = connect_to_mssql_with_pymssql()
    if conn:
        df = pd.read_sql(sql, conn)
        conn.close()
        return df
    return None


df_information_schema = run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")


if df_information_schema is not None:
    plan = vn.get_training_plan_generic(df_information_schema)
    print(plan)
else:
    print("Failed to retrieve schema.")

vn.train(plan=plan)

# The following are methods for adding training data. Make sure you modify the examples to match your database.
# DDL statements are powerful because they specify table names, colume names, types, and potentially relationships
vn.train(ddl="""
    CREATE TABLE IF NOT EXISTS my-table (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""")

# Sometimes you may want to add documentation about your business terminology or definitions.
vn.train(documentation="Our business defines OTIF score as the percentage of orders that are delivered on time and in full")

# You can also add SQL queries to your training data. This is useful if you have some queries already laying around. You can just copy and paste those from your editor to begin generating new SQL.
vn.train(sql="SELECT * FROM my-table WHERE name = 'John Doe'")


# df=vn.get_training_data() #to get all the training data

## Asking the AI
"Whenever you ask a new question, it will find the 10 most relevant pieces of training data and use it as part of the LLM prompt to generate the SQL."
vn.ask(question= "",
    print_results = True,
    auto_train = True,
    visualize= True,
    allow_llm_to_see_data = False)

# vn.generate_sql("What are the top 10 albums by sales?")
# vn.remove_training_date(id="id") to remove particular training data
# vn.get_similar_question_sql("Which artists have tracks in the 'Rock' genre?")
# vn.run_sql("SELECT COUNT(*) AS TotalTables FROM sqlite_master WHERE type = 'table'")




