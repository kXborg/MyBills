import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from datetime import datetime
import gspread 
from google.oauth2 import service_account


def main():
	# Get current time.
	now_n = datetime.now()
	now_strf = now_n.strftime('%Y/%m/%d')

	# Connect slack.
	# slack_client = slack.WebClient(token = st.secrets['slack_credentials']['SLACK_TOKEN'])
	# conn = connect(credentials=credentials)
	# Create a connetion object.
	credentials = service_account.Credentials.from_service_account_info(
			st.secrets["gcp_service_account"],
			scopes=["https://www.googleapis.com/auth/spreadsheets"],)
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

	if st.button('Enter'):
		# Update.
		sheet_url = st.secrets["private_gsheets_url"]
		sheet = client.open_by_url(sheet_url).sheet1
		sheet.insert_row(entry_line, index=2)
		st.success('Data has been written to Google Sheets!')
		st.session_state['particular'] = ""
		st.session_state['amount'] = 0
		st.session_state['remark'] = ""


if __name__ == '__main__':
	with open('config.yaml') as file:
		config = yaml.load(file, Loader=SafeLoader)


	authenticator = stauth.Authenticate(
	    config['credentials'],
	    config['cookie']['name'],
	    config['cookie']['key'],
	    config['cookie']['expiry_days'],
	)

	name, authentication_status, username = authenticator.login('Login', 'main')

	if authentication_status:
		authenticator.logout('Logout', 'main')
		main()
	elif authentication_status == False:
		st.error('Username/password is incorrect')
	elif authentication_status == None:
		st.warning('Please enter your username and password')



