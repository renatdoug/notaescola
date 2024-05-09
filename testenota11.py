import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from streamlit_gsheets import GSheetsConnection
from googleapiclient.errors import HttpError
import os.path
import json
import requests

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Sheet1",
    ttl="10m",
    usecols=[0, 1],
    nrows=3,
)

# Print results.
for row in df.itertuples():
    st.write(f"{row.nome} has a :{row.nota}:")
