import streamlit as st
import pandas as pd
import os
from io import BytesIO
import base64

#set up our app
st.set_page_config(page_title="Data Sweeper", layout ='wide')

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
image_base64 = get_base64_image("Meer.jpg") 
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="data:image/jpg;base64,{image_base64}" style="border-radius: 50%; width: 320px; height: 300px;">
    </div>
    
    <h1 style="text-align: center; font-size: 50px; font-family: 'Poiret One'; color: #white;">
        Data Sweeper by Meer
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("Transform your files from CSV to XLSX and Vise Versa formats with built-in data cleaning and visualization")

uploaded_files = st.file_uploader ("Upload your (CSV or Excel);", type=["csv","xlsx"], accept_multiple_files=True)

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
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")
        
        #show 5 rows of our df
        st.write("Preview teh Head of the DataFrame")
        st.dataframe(df.head())

        #Options for data clean
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            
            with col2:
                if st.button(f"Fill missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled")

        #Choose specific Columns to Keep or Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #Create some Visualizations
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.area_chart(df.select_dtypes(include='number').iloc[:,:2])

        #Convert the File -> CSV to XLSX
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel" ], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type =="CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            
            elif conversion_type =="Excel":
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            #Download Button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )


st.success("Congratulation! All files processed now")
