import sys
import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

# Aggiungi il percorso della directory 'modules' al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

# Importa i moduli personalizzati
from core.username import verifyUsername
from utils.userAgent import getRandomUserAgent
from export.file_operations import createSaveDirectory
from export.csv import saveToCsv
from export.pdf import saveToPdf
from utils.permute import Permute

# Carica le variabili d'ambiente
load_dotenv()

# Funzione per generare possibili username
def generate_usernames(first_name, last_name, company):
    usernames = []
    if first_name and last_name:
        # Combinazioni base
        usernames.append(f"{first_name}{last_name}")
        usernames.append(f"{first_name}.{last_name}")
        usernames.append(f"{last_name}{first_name}")
        usernames.append(f"{first_name[0]}{last_name}")
        usernames.append(f"{last_name}{first_name[0]}")
        usernames.append(f"{first_name}_{last_name}")
        usernames.append(f"{last_name}_{first_name}")
        
        # Combinazioni con iniziali
        usernames.append(f"{first_name[0]}_{last_name}")
        usernames.append(f"{last_name}_{first_name[0]}")
        usernames.append(f"{first_name[0]}.{last_name}")
        usernames.append(f"{last_name}.{first_name[0]}")
        
        # Combinazioni con numeri (es. anno di nascita)
        usernames.append(f"{first_name}{last_name}123")
        usernames.append(f"{first_name}.{last_name}123")
        usernames.append(f"{first_name}_{last_name}123")
        
        # Combinazioni con azienda
        if company:
            usernames.append(f"{first_name}{last_name}{company}")
            usernames.append(f"{first_name}.{last_name}@{company}")
            usernames.append(f"{last_name}.{first_name}@{company}")
            usernames.append(f"{first_name[0]}{last_name}@{company}")
            usernames.append(f"{first_name}.{last_name}.{company}")
    return usernames

# Funzione principale per l'app Streamlit
def main():
    st.title("Blackbird Username Finder")

    # Sezione di input
    st.sidebar.title("Input Data")
    first_name = st.sidebar.text_input("Nome", "")
    last_name = st.sidebar.text_input("Cognome", "")
    company = st.sidebar.text_input("Azienda", "")
    permute = st.sidebar.checkbox("Permutazioni", value=False)
    output_csv = st.sidebar.checkbox("Output CSV", value=False)
    output_pdf = st.sidebar.checkbox("Output PDF", value=False)

    if st.sidebar.button("Cerca Username"):
        # Genera i possibili username
        usernames = generate_usernames(first_name, last_name, company)
        
        # Permutazioni degli username se richiesto
        if permute and usernames:
            permute_class = Permute(usernames)
            usernames = permute_class.gather("all")

        if not usernames:
            st.write("Nessun username generato. Inserisci nome e cognome.")
            return

        # Mostra i risultati
        st.write("Risultati ricerca per gli username:")
        found_accounts = []
        for user in usernames:
            st.write(f"Cercando per {user}...")
            # Esegui la verifica degli username
            result = verifyUsername(user)
            if result:
                st.write(f"Trovato: {user} - {result}")
                found_accounts.append((user, result))
            else:
                st.write(f"Nessun risultato per: {user}")

        # Salvataggio dei risultati
        if output_csv and found_accounts:
            createSaveDirectory()
            saveToCsv(found_accounts, "username_results.csv")
            st.write("Risultati salvati in CSV.")

        if output_pdf and found_accounts:
            createSaveDirectory()
            saveToPdf(found_accounts, "username_results.pdf")
            st.write("Risultati salvati in PDF.")

if __name__ == "__main__":
    main()
