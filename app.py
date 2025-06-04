import streamlit as st
import pandas as pd
import pandasai as pai
from pandasai_openai import AzureOpenAI
import matplotlib.pyplot as plt

st.set_page_config(page_title="Country Sales Chat (Upload Your Own)", layout="centered")
st.title("🌐 Country Sales Chat (Upload Your Own)")

st.markdown(
    """
    Upload a **CSV** or **Excel** file containing your sales (or any tabular) data. 
    After uploading, type a natural-language prompt (e.g. “Which are the top 5 countries by sales?”) 
    and click **Run**. Charts and DataFrames will display inline.
    """
)

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

# ——————————————
# 1) File Uploader
# ——————————————
uploaded_file = st.file_uploader(
    label="Upload your CSV or Excel file here",
    type=["csv", "xlsx"],
    help="Accepted formats: .csv or .xlsx"
)

if uploaded_file is not None:
    try:
        # Attempt to read as CSV first; if that fails, try Excel
        try:
            pandas_df = pd.read_csv(uploaded_file)
        except Exception:
            uploaded_file.seek(0)  # reset buffer pointer
            pandas_df = pd.read_excel(uploaded_file)

        # Convert to pandasAI DataFrame
        df = pai.DataFrame(pandas_df)

        st.subheader("🔎 Sample of Your Data")
        st.dataframe(pandas_df.head())

        # ——————————————
        # 2) Prompt Input
        # ——————————————
        user_prompt = st.text_input(
            "Ask a question about this data (e.g., “Which are the top 5 countries by sales?”) ",
            ""
        )

        # ——————————————
        # 3) Run pandasAI chat when button clicked
        # ——————————————
        if st.button("🚀 Run"):
            if not user_prompt.strip():
                st.error("Please enter a question before clicking Run.")
            else:
                with st.spinner("Thinking..."):
                    # Clear any existing matplotlib figures
                    plt.close("all")

                    try:
                        answer = df.chat(user_prompt)
                        print(type(answer))

                        # 1) If pandasAI returned a DataFrame, render it
                        if isinstance(answer, pd.DataFrame):
                            st.subheader("📊 DataFrame Result")
                            st.dataframe(answer)

                        # 2) Otherwise, show textual answer
                        else:
                            st.subheader("📋 Answer")
                            st.write(answer)

                        # 3) Display any matplotlib figures inline
                        for fig_num in plt.get_fignums():
                            fig = plt.figure(fig_num)
                            st.subheader("📈 Chart")
                            st.pyplot(fig)

                        # Close all figures to avoid re-rendering on next run
                        plt.close("all")

                    except Exception as e:
                        st.error(f"Error during pandasAI execution:\n{e}")

    except Exception as file_e:
        st.error(f"Could not read the uploaded file. Please make sure it's a valid CSV or Excel.\nDetails: {file_e}")
else:
    st.info("🔘 Please upload a CSV or Excel file to get started.")
