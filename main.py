import streamlit as st 
from datetime import datetime
# import pandas as pd
import gspread 
from google.oauth2 import service_account
# import slack 

# Clear cell.
def update_page():
	# Update.
	sheet_url = st.secrets["private_gsheets_url"]
	sheet = client.open_by_url(sheet_url).sheet1
	sheet.insert_row(entry_line, index=2)
	st.success('Data has been written to Google Sheets!')
	st.session_state['particular'] = ""
	st.session_state['amount'] = 0
	st.session_state['remark'] = ""

# Get current time.
now_n = datetime.now()
now_strf = now_n.strftime('%Y/%m/%d')

# Connect slack.
# slack_client = slack.WebClient(token = st.secrets['slack_credentials']['SLACK_TOKEN'])

# Create a connetion object.
credentials = service_account.Credentials.from_service_account_info(
	st.secrets["gcp_service_account"],
	scopes=["https://www.googleapis.com/auth/spreadsheets"],)

# conn = connect(credentials=credentials)
client = gspread.authorize(credentials)

st.title("TLCM Bills")

col01, col02 = st.columns(2)

sel_date = col01.date_input('Date: ', datetime.now())
bill_date = sel_date.strftime("%d/%m/%Y")

particular = col02.text_input('Particular', key='particular', value="")

amount = st.number_input('Amount: ', key='amount', min_value=0)
remark = st.text_input('Remark:', key='remark', value="")
mode = st.selectbox('Mode', ('UPI', 'Net Banking', 'Cash'))


# Write to spreadsheet.
entry_line = [bill_date, particular, amount, mode, remark]

st.button('Enter', on_click=update_page)