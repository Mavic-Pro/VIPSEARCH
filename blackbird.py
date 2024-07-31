import os
import streamlit as st
from rich.console import Console
import logging
from datetime import datetime

from dotenv import load_dotenv
from modules.core.username import verifyUsername
from modules.utils.userAgent import getRandomUserAgent
from modules.export.file_operations import createSaveDirectory
from modules.export.csv import saveToCsv
from modules.export.pdf import saveToPdf
from modules.utils.permute import Permute

load_dotenv()

# Inizializzazione configurazione
console = Console()
log_path = "logs/log.txt"

def setup_logging():
    if not os.path.exists("logs/"):
        os.makedirs("logs/")
    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

def generate_usernames(first_name, last_name, company):
    usernames = []
    if first_name and last_name:
        usernames.append(f"{first_name}{last_name}")
        usernames.append(f"{first_name}.{last_name}")
        usernames.append(f"{last_name}{first_name}")
        usernames.append(f"{first_name[0]}{last_name}")
        usernames.append(f"{last_name}{first_name[0]}")
        if company:
            usernames.append(f"{first_name}{last_name}{company}")
            usernames.append(f"{first_name}.{last_name}@{company}")
    return usernames

def main():
    st.title("Blackbird Username Finder")

    st.sidebar.title("Input Data")
    first_name = st.sidebar.text_input("Nome", "")
    last_name = st.sidebar.text_input("Cognome", "")
    company = st.sidebar.text_input("Azienda", "")

    permute = st.sidebar.checkbox("Permutazioni", value=False)
    output_csv = st.sidebar.checkbox("Output CSV", value=False)
    output_pdf = st.sidebar.checkbox("Output PDF", value=False)

    if st.sidebar.button("Cerca Username"):
        setup_logging()
        
        # Genera i possibili username
        usernames = generate_usernames(first_name, last_name, company)

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
            console.print(f"Searching for {user}")
            # Esegui la verifica degli username
            result = verifyUsername(user)
            if result:
                st.write(f"Found: {user} - {result}")
                found_accounts.append((user, result))

        if output_csv and found_accounts:
            createSaveDirectory()
            saveToCsv(found_accounts)
            st.write("Salvato in CSV.")

        if output_pdf and found_accounts:
            createSaveDirectory()
            saveToPdf(found_accounts, "username")
            st.write("Salvato in PDF.")

if __name__ == "__main__":
    main()
