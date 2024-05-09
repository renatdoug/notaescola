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

# The ID of your spreadsheet.
SAMPLE_SPREADSHEET_ID = "1S1oID1RUYCyYxq2ZRcAmY0XVx1PaO7EJTtRLNDoLLPM"

def get_credentials():
    creds = None
    # Load credentials from the provided JSON data
    creds_data = {
        "type": "service_account",
        "project_id": "digitacaonotas",
        "private_key_id": "5c1b2b39dff8f490c4e36b7963b1bb7adc1de745",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCuKiKhkY201VGh\n5oSfQZ+xwQvBc+e+B5WfFg6/lwXmXvFT0cX5lOObJR8ll+azHWKJNNwdYWGciTrK\nuxPj2JRpgCsd0XYXwB8oRPhRTsIMOZRx9bTPWxByl6NkxIM9ryhWXjaB5WyaNsot\nWlDBtYIf7pbD3O6wfDXeyn8Ws28dLWNYLrSkT8pnNewVV2mQtdZI3sjuwdaeGcpc\n91c88P/6haM7LsNdubXzDcggSNee98OhkD39gXiLhgFq3JMoP6tEM4M6thQUFMmx\nZOFu2SnxtUn0Pt0TlMjPrMOwD7kHkfZhq4qSBWSIydjNKCzalTjMXWOsX/BCg5RG\nshGVb4LfAgMBAAECggEAFLZqG/Dle2YLKUfy6cWyKj+dGEqietUIFD1ZT6u0Retw\no9lExCPS1baad6wTAaYy+8JPkybrpuQjG80X1ncBX3KgrhElDDoK+o0JQxIsvatz\nXgIsmKRp1lb2VZuRSBq2n17g+J3CRqzRaoddJ0xgx09mmrCBqnd7KJ3Ic3ivdDap\nJ1sf+uquvvbQ4UDCxt5j94nKP1KPfO2d6ENgQDF+230DHI+cg6ENIw7P17SLPgue\njSlPK20/vmFiIr3fCLFV3BrrRsmOplxEkEJa6qRywW6NEofHa3wQoR4JB4PvobQg\n/rOvcBeYXO2+vkHkCsj5u+28nkvyigCjeAlRA1wCMQKBgQDp4bm4y9LcqJloiFK7\nhX/Z38whgfOslgunWXcIzfoClPM1PEkEt/uqEqb6N64qHlg+pB9n+Wq4iMllXFR2\nOtSIazHg0CRs3EqAA+wfH4id1MA1qktYFWlnSFBbHddW3TMFpDaZDJhzdaN5Y1Xr\nlvhR0mYEcvijeaTUBD5t/B9ECwKBgQC+oqiB/IfpBsFOZ3RawlITE4zpvKjj9JMA\n26Zj/pMretw/TZJ6azm3607c71uVLV0V8hSo7WlaAP3j2oD1wbizH+18yN/pCyfN\nXzPw+9dujkxNE5irclQ8xLHvH0tD0+27G8R9x6ylxmspnKVP5CEwIItsOuVVp5dt\nZn2W9sJM/QKBgQCjIPUYRtoxXEt8FLGX5/qP7cAEkw5yD0nblNQoyPobeObV99F6\nQBWBv3bFybZp3DZyoqjhLZ9ZTNckIq0qtcftys7EXok5gMFZ3uJ/ps/0PiM+iyP4\nMR8OkeqyUvMSvEBNLAeE4rsmtSOrlDSmmOtkrprHeaWg6ESmOLuOnS71lwKBgAlF\nObKQiD9xv6bDayoatwkMc1bOgNwNAbUR+WZ1c8yyfdFqQUxIuJbUD5K45Rg9C4DM\ns+p/GRdyYuZYstrAn+2+CLt/vTvE+huHnKwEYzaSHu3EnTEBL02BNzHssKlMvgvS\nTtza/+9T1dRBNNzMuDxx6LXLq2ld7AQ67rKPr2U1AoGBAIpEjwZGeIdlDeHVPMDy\ntrWxUEX/fz5pvrXUYe+hjmiQMSlGRHmnYDsGJFWrOsbwuinusqBkcm2Il/Q1AlvC\nqFF6e8XHpkBVaKdt8WIioRm6kKN+tx8OqqNZsGBoqpt2iUopIIKhp+y1vu0Lk65H\n4JSYz5cVpoPf6S0N6QJpXoYn\n-----END PRIVATE KEY-----\n",
  "client_email": "digitarnotas@digitacaonotas.iam.gserviceaccount.com",
  "client_id": "117384486449011450121",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/digitarnotas%40digitacaonotas.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

def get_credentials():
    creds = Credentials.from_service_account_info(creds_data, scopes=SCOPES)
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

