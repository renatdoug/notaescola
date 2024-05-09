import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import json
import requests

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1S1oID1RUYCyYxq2ZRcAmY0XVx1PaO7EJTtRLNDoLLPM"

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Carrega as credenciais do arquivo credenciaisweb.json no GitHub
            cred_url = "https://raw.githubusercontent.com/renatdoug/notaescola/main/credenciaisweb.json"
            response = requests.get(cred_url)
            if response.status_code == 200:
                creds_data = response.json()
                creds = Credentials(
                    creds_data["token"],
                    refresh_token=creds_data["refresh_token"],
                    token_uri=creds_data["token_uri"],
                    client_id=creds_data["client_id"],
                    client_secret=creds_data["client_secret"],
                    scopes=SCOPES
                )
            else:
                st.error("Erro ao carregar as credenciais.")

        # Salva as credenciais no arquivo 'token.json' para uso posterior
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def main():
    st.title("Adicionar Nota dos Alunos")

    # Autenticação e autorização do Google Sheets
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Obter a lista de abas (nome das disciplinas) da planilha
    spreadsheet = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    abas = [aba["properties"]["title"] for aba in spreadsheet["sheets"]]

    # Permitir que o usuário escolha a aba (nome da disciplina)
    aba_escolhida = st.selectbox("Escolha a aba (nome da disciplina):", abas)

    # Adicionar campo para nome do professor
    nome_professor = st.text_input("Digite seu nome (professor):")
    
    # Obter a chave de acesso única para a aba escolhida
    # Você pode criar um dicionário ou banco de dados para armazenar essas chaves
    chaves_acesso = {
        "Página1": "mat",
        "Página3": "port",
        "História": "chave_hist"
        # Adicione outras disciplinas e chaves de acesso conforme necessário
    }

    if nome_professor and aba_escolhida in chaves_acesso:
        chave_acesso = st.text_input(f"Digite a chave de acesso para {aba_escolhida}:")
        if chave_acesso == chaves_acesso[aba_escolhida]:
            # Definir o range baseado na aba escolhida
            range_aba = f"{aba_escolhida}!A1:B12"

            try:
                # Ler os dados existentes da planilha na aba escolhida
                result = sheet.values().get(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_aba
                ).execute()
                
                if "values" in result:
                    valores = result["values"]
                    # Criar dicionário para mapear nome do aluno com a nota
                    notas_alunos = {linha[0]: linha[1] for linha in valores[1:] if linha}
            
                    # Exibir lista de alunos com input para adicionar a nota
                    for aluno, nota in notas_alunos.items():
                        st.write(f"{aluno}: {nota}")
                        nova_nota = st.number_input(f"Inserir nova nota para {aluno}", value=float(nota), step=0.1, format="%.1f", key=f"nota_input_{aluno}")
                        if nova_nota < 0 or nova_nota > 10:
                            st.error(f"A nota deve ser um valor entre 0 e  10.")
                        else:
                            notas_alunos[aluno] = nova_nota
                
                    if st.button("Atualizar Notas"):
                        # Atualizar a planilha com as novas notas
                        valores_atualizados = [["Nome", "Nota"]] + [[aluno, nota] for aluno, nota in notas_alunos.items()]
                        result_update = sheet.values().update(
                            spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=range_aba,
                            valueInputOption="USER_ENTERED",
                            body={"values": valores_atualizados},
                        ).execute()
            
                        # Desabilitar o botão de atualização após o primeiro salvamento
                        st.success("Notas atualizadas com sucesso!")
                        st.experimental_rerun()
                        st.button("Atualizar Notas", disabled=True)
                else:
                    st.error("A planilha não possui valores.")
            
            except HttpError as err:
                st.error(f"Erro ao ler dados da planilha: {err}")
        else:
            st.error("Chave de acesso incorreta. Apenas o professor autorizado pode acessar.")
    elif nome_professor:
        st.error("A disciplina selecionada não possui chave de acesso definida para o professor.")
    else:
        st.warning("Por favor, preencha o nome do professor.")

if __name__ == "__main__":
    main()
