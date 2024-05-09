# example/st_app.py

import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import json

#url = "https://docs.google.com/spreadsheets/d/1OahlvKuGODaTet_Y-OL6s82eufuYfVo6jPxSgxCxsd4/edit?usp=sharing"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet = "portugues", usecols = list(range(3))) # ou pode ser usecols = [0,1] # para o paramento worksheet usa o valor do id caso planilha publica, e o nome da planilha se for privada
st.dataframe(data)

st.subheader("Alunos com Falta supeior a 2")
sql = '''
SELECT
     portugues Faltas
FROM
     portugues
WHERE
     "Faltas" > 2
ORDER BY
     "nome" DESC;
'''


df_alunos = conn.query(sql = sql)

st.dataframe(df_alunos)