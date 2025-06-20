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


SERVER = ''
USERNAME = ''
PASSWORD = ''
DATABASE = ''


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



