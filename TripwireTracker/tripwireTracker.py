import os
import pandas as pd
import streamlit as st
from openpyxl import Workbook
import base64
from io import BytesIO

# Set the page configuration for the Streamlit application, including the title and icon.
st.set_page_config(
    page_title="Iberia Advisory Tripewire Tracker",
    page_icon="📊",
    layout="wide"
)

# Display the Iberia Advisory image on the Streamlit application.
st.image("./Images/iberia-logo.png")

################
# AUTHENICATION
################

# Define a function check_password() that handles user authentication.
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True
    
# Check the user password using the check_password() function and sets the is_logged_in flag to True if the password is correct.
if check_password():
    is_logged_in = True

    # Streamlit UI
    st.title('Tripwire Tracker App')

    # Upload Onboarding Tracker Excel file
    tracker_file = st.file_uploader("Upload Onboarding Tracker Excel File", type=["xlsx"])
    hourly_cost_file = st.file_uploader("Upload Hourly Cost Excel File", type=["xlsx"])
    hourly_cost_sheet_name = st.text_input("Enter Hourly Cost Sheet Name:")

    if tracker_file is not None and hourly_cost_file is not None:
        # Read the uploaded Excel files into Pandas DataFrames
        tracker_df = pd.read_excel(tracker_file, sheet_name='Tripwire Tracker')
        hourly_cost_df = pd.read_excel(hourly_cost_file, sheet_name=hourly_cost_sheet_name)

        # Set the header row as the column names for Onboarding Tracker
        tracker_df.columns = tracker_df.iloc[4]
        tracker_df = tracker_df[5:]
        tracker_df.reset_index(drop=True, inplace=True)
        tracker_df = tracker_df[["Employee Name", "SES Y/N - recommend allowing to exceed tripwire"]]

        # Set the header row as the column names for Hourly Cost
        hourly_cost_df.columns = hourly_cost_df.iloc[6]
        hourly_cost_df = hourly_cost_df[7:]
        hourly_cost_df.reset_index(drop=True, inplace=True)
        hourly_cost_df = hourly_cost_df[["Name", "PLC Desc", "Hourly Cost $/hr", "Above Tripwire Rate?"]]

        # Read LCAT Normalization data from Onboarding Tracker
        lcat_df = pd.read_excel(tracker_file, sheet_name='LCAT Normalization')
        lcat_df = lcat_df[["Vendor LCATs", "Correct LCAT Syntax"]]

        # Remove middle initials from names in both DataFrames
        tracker_df["Employee Name"] = tracker_df["Employee Name"].str.replace(r' [A-Z]\b', '', regex=True)
        hourly_cost_df["Name"] = hourly_cost_df["Name"].str.replace(r' [A-Z]\b', '', regex=True)

        # Filter Data
        filtered_tripwire_df = tracker_df[tracker_df["SES Y/N - recommend allowing to exceed tripwire"] == "Y"]
        names_above_tripwire = hourly_cost_df[hourly_cost_df["Above Tripwire Rate?"] == "Yes"]["Name"]
        names_allow_exceed_tripwire = filtered_tripwire_df[
            filtered_tripwire_df["SES Y/N - recommend allowing to exceed tripwire"] == "Y"]["Employee Name"]
        names_not_in_tripwire = names_above_tripwire[~names_above_tripwire.isin(names_allow_exceed_tripwire)]

        # Remove newline characters from the "PLC Desc" column in hourly_cost_df
        hourly_cost_df["PLC Desc"] = hourly_cost_df["PLC Desc"].str.strip()

        # Create a dictionary to map "Vendor LCATs" to "Correct LCAT Syntax"
        lcat_mapping = lcat_df.set_index("Vendor LCATs")["Correct LCAT Syntax"].to_dict()

        # Map the "PLC Desc" column in hourly_cost_df to get corrected LCAT syntax
        hourly_cost_df["Correct LCAT Syntax"] = hourly_cost_df["PLC Desc"].map(lcat_mapping)

        # Filter again
        filtered_hourly_cost_df = hourly_cost_df[hourly_cost_df["Name"].isin(names_not_in_tripwire)]

        # Output
        result_df = filtered_hourly_cost_df[["Name", "PLC Desc", "Correct LCAT Syntax", "Hourly Cost $/hr", "Above Tripwire Rate?"]]

        # Display the resulting DataFrame
        st.subheader("Processed Data")
        st.dataframe(result_df)

#         # Input field for Excel file name
#         excel_filename = st.text_input("Enter Excel File Name (without extension)", "filtered_hourly_cost")

#         # Save to Excel button
#         if st.button('Save Data to Excel'):
#             # Get the path to the user's downloads folder
#             downloads_folder = os.path.expanduser("~/Downloads")
#             excel_file_path = os.path.join(downloads_folder, f"{excel_filename}.xlsx")

#             with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
#                 result_df.to_excel(writer, index=False)

#             st.success(f"Data saved to '{excel_file_path}'")

        # Input field for Excel file name
        excel_filename = st.text_input("Enter Excel File Name (without extension)", "filtered_hourly_cost")

        # Save to Excel button
        if st.button('Save Data to Excel'):
            # Save the filtered dataframe to an Excel file in memory
            excel_buffer = BytesIO()
            result_df.to_excel(excel_buffer, index=False)
            excel_data = excel_buffer.getvalue()

            # Generate a download link for the Excel file
            b64 = base64.b64encode(excel_data).decode('utf-8')
            excel_filename = f"{excel_filename}.xlsx"
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{excel_filename}">Download Excel File</a>'
            st.markdown(href, unsafe_allow_html=True)

