import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path




# Carregar as credenciais do ambiente de execução (configuração específica do ambiente)
credentials = Credentials.from_service_account_info({
  "type": "service_account",
  "project_id": "digitacaonotas",
  "private_key_id": "9141920045fa5fe712e251daa42466bbd9d13c57",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9GPab0x/EFrB4\nZyDImktqFf7rVjf3tu/qGRxJT47S8fE+nz9mCie6bfH8MqYH344+mnbR5/nyZUGy\nrWXuZ2DnJRNX9hqe8RNBnSPO5t1jRN1psecdiPJzDXqZ/mE/nGAwDfdpJLRn2PLN\nl2srNOXNShVhx2Y/c852CucGM8VKm6ZsFh9STRkQLhdOm4jdK0yfMNRmaDS1FVA3\nYNjbLpt3DOW/nDJw3kDC95jqS7+JVmF0/2HNkQnLznfaHlnQEtLrNQNL6IRunIUx\n1iateTDQavF/JN8aOfchwWFNObuqxYWOlDAm6kgB2ghM+WB4tA3RwyY9cOYBrcvv\nz8YZ3lyHAgMBAAECggEAAodaiBiGRjlsQE/wvX4CucQNiQwgHeBRmQNsJp05WOzP\nWXnVTGhtjsd4z7/FpJ+156edJMJBzDhtoBWqVUo6OFBKNlTq/Wq8sGK8X3OK5l1X\nY9oMyY8fq6/ODra68JgHJhCQJgg0BjRKgVSGPfYSuwoQlLwoske6k3pV2I/JeNPr\nvsivourYKvmabeUBzffiZ/T/CwC7/KUON1qRpcrUEZd+eF3hq14ODopLOXHdsW41\nP0nyWv6GqYGughgqIsAIUkQhxMRoRSoM62Vbs3BB5QhBENIPKRG3r9e+T9BNKIHH\nbYHWM6tgJpk7JNtrVyOkoV+XmHQd/A4kh+Ek9nxMgQKBgQDfcN6qmzdKn8liIjL1\nzIf4Rg1M1yNKHr+cMVW0TbHJLAGecdnfgkIgFvMcx1gHGgz05inktGCy0Bc9/yFn\n/jeWydeZ+T2SSGuqAB/IVVmNhK4yPNwdfBWxQzJ0Fs1YeUK7KFnC+tF0aalnUfsF\nlOVhvsF4T4hOyUxkcy/YD5JUIQKBgQDYpvb0ElCce8s8J8hbC/A4AIOD0irsDcr+\nkNsP4g8H6uTvtpSC8I9TjtJP0CSx+vECusSmiTdVdG32RQAmIZwtjgMVKwHOhVK3\nQHhbEtlCpEKAjTOdETU6UEt2v2qVqqK1G+XrCcCL+maRai3aFYc7fhXX+pyEAgMP\nB/6tEUobpwKBgBERQBDsFkce+XUDg7z+yIwQXce2zz1EKAK4SgGhxajGMcF2lNvb\nyU1GM3/JQlIYjVDPm/eaR6ChAIV9zYFyC7D67fsW7LsVyRONOuBElLiYn+26dF3U\nMpv9tAbmDv1pFc3SATlBi2pG/+eifXgprXPP7FtSR+ksuycZHVh1qAnBAoGBAJfJ\nKj1HU5i+ll231YQMMilaGsnRBedJpo2BOSjAjR1T8T8MoLG4DgJRjoECZ6MWF6J8\n7WdrvQuuvZeLMhaE96Fm3DwJXIOvHotqrKfJ5dLtt/XOd3m0Y6FOPgCdDPR8ju/p\n8sQfmfm33gJE7IjdClig9nbRirRloHT4efIQqeYDAoGAJdFSPVWr/94E4uxEcvCm\nUNwRUJ9ii7Kn99o3cuFhIYS/bwvaySg3uvXqYxX8aoEmfMFSqI9gx3mgSHLOFWN+\nxkc3w+3grhdiz8hsltmSo0rrVnl5kIP3HUmtLC1ND1Kc92xkmwQuyYR8fo1BHLKx\nAvfMvJwWGkQPSsiHEY50umI=\n-----END PRIVATE KEY-----\n",
  "client_email": "digitarnotas@digitacaonotas.iam.gserviceaccount.com",
  "client_id": "117384486449011450121",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/digitarnotas%40digitacaonotas.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

# Definir o escopo de autorização para acessar o Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# O ID da planilha do Google Sheets que você deseja acessar ou modificar
SAMPLE_SPREADSHEET_ID = "1OahlvKuGODaTet_Y-OL6s82eufuYfVo6jPxSgxCxsd4"

# Criar o cliente do Google Sheets
service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()

def main():
    st.title("Adicionar Nota dos Alunos")

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
