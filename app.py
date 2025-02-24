'''import streamlit as st
import pandas as pd
import os
from io import BytesIO

#Set up our App
st.set_page_config(page_title="💽 Smart Data Transformer", layout='wide')
st.title("💽 Smart Data Transformer")
st.write("Transfrom your files between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("Upload your files(CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file_ext}")
            continue


        #Display info about the file
        st.write(f"**📂 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size/1024}")

        st.write("🔍 Preview the Head of the Dataframe")
        st.dataframe(df.head())


        #Options for data cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")


        #Choose Specific Columns to keep or convert
        st.subheader("🎯Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        #Create some Visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])


        #Convert the file -> CSV to Excel
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)


        #Download Button
            st.download_button(
                label= f"⬇️ Download {file.name} as {conversion_type}",
                data = buffer,
                file_name = file_name,
                mime = mime_type
                )


st.success("🎉 All files processed!") 
'''

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Apply dark theme
st.set_page_config(page_title="Smart Data Transformer", layout="wide")
sns.set_theme(style="darkgrid")

# Custom CSS for Full Dark Theme
st.markdown(
    """
    <style>
        body { background-color: #DDA0DD; color: white; }
        .stApp { background-color: #121212; }
        .stButton > button { border-radius: 10px; font-weight: bold; padding: 10px 15px; background-color: #FF5722; color: white; border: none; cursor: pointer; }
        .stButton > button:hover { background-color: #FFC107; color: black; transform: scale(1.05); }
        .stDataFrame { background-color: #DDA0DD; color: white; }
        [data-testid="stSidebar"] {
            background-color: #DDA0DD;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        div[data-testid="stSidebar"] label {
            color: white !important;
        }
        div.stRadio label {
            color: white !important;
        }
        div.stNumberInput label {
            color: white !important;
        }
        div.stAlert {
            color: white !important;
        }
            h1 {
            text-align: center;
            font-size: 36px;
            color: #800080; /* Purple color */
        }
        @keyframes glow {
            100% { color: rgb(155, 55, 119); }
            0% { color: rgb(73, 46, 173); } 
        }
        .glow-text {
            animation: glow 1.5s infinite alternate;
        }
        [data-testid="stSidebar"] {
            background-color: #8B5081 !important; 
        }
        [data-testid="stSidebarNav"] {
            background-color: #800080 !important; 
        }
        h2, h3 , h5, h6 {
            color: #ffffff !important;  /* Ensure headings stay visible */
        }
        div[data-testid="stFileUploader"] { background-color: black !important; color: white !important; border: 2px solid white !important; padding: 10px; border-radius: 10px; text-align: center; }
        div.stFileUploader label {
            color: white !important;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📂 Upload & Transform", "🛠️ Data Cleaner", "📊 Insights & Visualization"])

# Initialize df in session_state if it doesn't exist
if "df" not in st.session_state:
    st.session_state.df = None

# Main Content Based on Selection

if page == "🏠 Home":
    st.markdown("""
        <h1 style='text-align: center; color: #800080; size: 36px;'>
            🤖 <span style='animation: glow 1.5s infinite alternate;'>AI-Powered Data Transformer</span> 🚀
        </h1>
        <style>
            @keyframes glow {
                100% { color:rgb(155, 55, 119) }
                0% { color:rgb(73, 46, 173)} 
            }
        </style>
    """, unsafe_allow_html=True)


    st.markdown("""
        <div style="text-align: center; font-size: 18px; color: #ddd; padding: 15px; border-radius: 10px; background-color: #222831;">
            <p>📂 <b>Upload</b> your dataset</p>
            <p>🛠️ <b>Clean & Transform</b> data effortlessly</p>
            <p>📊 <b>Visualize</b> insights with interactive charts</p>
        </div>
    """, unsafe_allow_html=True)

elif page == "📂 Upload & Transform":
    st.markdown("""
    <h1 style='text-align: center; font-size: 36px; color: #800080;'>
        📂 <span class='glow-text'>Upload & Transform Data</span>
    </h1>
    <style>
        @keyframes glow {
            100% { color: rgb(155, 55, 119); }
            0% { color: rgb(73, 46, 173); } 
        }
        .glow-text {
            animation: glow 1.5s infinite alternate;
        }
    </style>
                """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            st.session_state.df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            st.session_state.df = pd.read_excel(uploaded_file)
    
    if st.session_state.df is not None:
        st.subheader("🔍 Data Preview")
        st.dataframe(st.session_state.df.head())  
        st.subheader("📊 Summary Statistics")
        st.write(st.session_state.df.describe())
        st.subheader("⚠️ Missing Values")
        st.write(st.session_state.df.isnull().sum())

elif page == "🛠️ Data Cleaner":
    st.markdown("""
    <h1 style='text-align: center; font-size: 36px; color: #800080;'>
        🛠️ <span class='glow-text'>Data Cleaning</span>
    </h1>
    <style>
        @keyframes glow {
            100% { color: rgb(155, 55, 119); }
            0% { color: rgb(73, 46, 173); } 
        }
        .glow-text {
            animation: glow 1.5s infinite alternate;
        }
    </style>
""", unsafe_allow_html=True)

    if st.session_state.df is not None:
        clean_option = st.radio("Select Cleaning Method", ["Fill Missing Values", "Drop Missing Values"])
        
        if clean_option == "Fill Missing Values":
            fill_value = st.number_input("Enter value to fill missing data:", value=0)
            st.session_state.df.fillna(fill_value, inplace=True)
            st.success("Missing values filled!")
        elif clean_option == "Drop Missing Values":
            drop_option = st.radio("Drop rows or columns?", ["Rows", "Columns"])
            if drop_option == "Rows":
                st.session_state.df.dropna(axis=0, inplace=True)
            else:
                st.session_state.df.dropna(axis=1, inplace=True)
            st.success("Missing values dropped!")
        
        st.subheader("Cleaned Data Preview")
        st.dataframe(st.session_state.df.head())
    else:
        st.markdown("""
    <div style='background-color: #8B5081; padding: 10px; border-radius: 5px;'>
        <h4 style='color: #F3EDF2;'>⚠️ Warning: Please upload a dataset first.</h4>
    </div>
""", unsafe_allow_html=True)


elif page == "📊 Insights & Visualization":
    st.markdown("""
    <h1 style='text-align: center; font-size: 36px; color: #800080;'>
        📊 <span class='glow-text'>Data Insights & Visualization</span>
    </h1>
    <style>
        @keyframes glow {
            100% { color: rgb(155, 55, 119); }
            0% { color: rgb(73, 46, 173); } 
        }
        .glow-text {
            animation: glow 1.5s infinite alternate;
        }
    </style>
""", unsafe_allow_html=True)

    if st.session_state.df is not None:
        st.subheader("Data Preview")
        st.dataframe(st.session_state.df.head())
        
        # Bar Chart Example
        st.subheader("Bar Chart")
        fig, ax = plt.subplots()
        sns.barplot(x=st.session_state.df.columns[0], y=st.session_state.df.iloc[:, 1], data=st.session_state.df, ax=ax, palette="rocket")
        st.pyplot(fig)
    else:
        st.markdown("""
    <div style='background-color: #8B5081 ; padding: 10px; border-radius: 5px;'>
        <h4 style='color: #F3EDF2;'>⚠️ Warning: Please upload a dataset first.</h4>
    </div>
""", unsafe_allow_html=True)











