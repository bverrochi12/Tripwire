# Tripwire Tracker App

The Tripwire Tracker App is a Python script designed to process data from Excel files and filter information based on specific criteria. It leverages the Pandas library to manipulate data efficiently.

---

Deployed links:

Updated with "Final Approval" column: 

https://tripwire.streamlit.app/



Original version using "SES Y/N - recommend allowing to exceed tripwire" column: 

https://tripwiretracker.streamlit.app/

---

## Table of Contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Functionality](#functionality)
- [How to Run](#how-to-run)
- [Output](#output)

---

### Dependencies <a name="dependencies"></a>

The following Python libraries are required to run this app:
- os
- pandas
- openpyxl

You can install them using pip if they are not already installed:

    pip install pandas openpyxl

---

## Usage

The Tripwire Tracker App is designed to perform the following tasks:

    - Read data from an Excel file containing tripwire information.
    - Read data from an Excel file containing hourly cost information.
    - Normalize LCAT (Labor Category) data.
    - Remove middle initials from employee names.
    - Filter data based on specific criteria.
    - Map LCAT information to correct syntax.
    - Generate a final output.

---

## Functionality

Here's an overview of the functionality of each section of the app:
Data Import

- **Tripwire Tracker:** Reads tripwire information from the "Onboarding_Tracker" Excel file.
    
- **Hourly Cost:** Reads hourly cost information from the "hourly_cost" Excel file.
    
- **LCAT Normalization:** Reads LCAT data from the "Onboarding_Tracker.xlsx" Excel file.

---

### Data Preprocessing

**Remove Middle Initials:** Removes middle initials from employee names in both DataFrames.


### Filtering Data

**Filter Tripwire Data:** Finds names in the tripwire data where "SES Y/N - recommend allowing to exceed tripwire" is "Y".

**Filter Hourly Cost Data:** Finds names in the hourly cost data where "Above Tripwire Rate?" is "Yes".

**Filter Names for Allowance:** Finds names in the tripwire data where "SES Y/N - recommend allowing to exceed tripwire" is "Y".

**Find Names Not in Tripwire:** Finds names in the hourly cost data that are not in the filtered tripwire data.

### Mapping of LCAT

**Map LCAT:** Maps the "PLC Desc" column in the hourly cost data to get corrected LCAT syntax.

---

## How to Run

To run the Tripwire Tracker App, follow these steps:

    - Ensure you have the required dependencies installed (pandas and openpyxl).
    - Place the Excel files ("Onboarding_Tracker.xlsx" and "hourly_cost.xlsx") in the same directory as the script.
    - Run the script, and it will process the data and provide the output.

---

### Output

Creates a final DataFrame with desired columns showing the filtered and mapped data and prints the result.

---
---
