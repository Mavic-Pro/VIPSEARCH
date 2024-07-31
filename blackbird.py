import streamlit as st
import os
import csv
import pandas as pd
from dotenv import load_dotenv
from itertools import permutations
from fpdf import FPDF

# Carica variabili d'ambiente se necessario
load_dotenv()

# Configurazione basata su variabili d'ambiente
class Config:
    def __init__(self):
        self.username = None
        self.permute = False
        self.permuteall = False
        self.csv = False
        self.pdf = False
        self.verbose = False
        self.no_update = False
        self.filter = None
        self.no_nsfw = False
        self.dump = False
        self.proxy = None
        self.timeout = 30
        self.max_concurrent_requests = 30
        self.email = None
        self.email_file = None
        self.username_file = None
        self.console = None
        self.dateRaw = None
        self.datePretty = None
        self.userAgent = None
        self.usernameFoundAccounts = None
        self.emailFoundAccounts = None
        self.currentUser = None
        self.currentEmail = None

# Funzione di verifica dell'username (esempio)
def verifyUsername(username, config):
    # Implementa qui la logica per verificare l'username
    st.write(f"Verifica dell'username: {username}")
    # Simulazione di risultati trovati
    found_accounts = {
        "platform1": f"{username}@platform1.com",
        "platform2": f"{username}@platform2.com"
    }
    return found_accounts

# Funzione di permutazione degli username
def permute_usernames(usernames, permuteall=False):
    if permuteall:
        permuted = set()
        for r in range(1, len(usernames) + 1):
            for p in permutations(usernames, r):
                permuted.add(''.join(p))
        return list(permuted)
    else:
        return usernames

# Funzione per salvare i risultati in CSV
def saveToCsv(found_accounts, filename):
    filepath = f"{filename}.csv"
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Platform', 'Account'])
        for user, accounts in found_accounts.items():
            for platform, account in accounts.items():
                writer.writerow([user, platform, account])
    st.write(f"Risultati salvati in {filepath}")

# Funzione per salvare i risultati in PDF
def saveToPdf(found_accounts, filename):
    filepath = f"{filename}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Risultati di Verifica Username", ln=True, align='C')
    
    for user, accounts in found_accounts.items():
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Username: {user}", ln=True)
        for platform, account in accounts.items():
            pdf.cell(200, 10, txt=f"  {platform}: {account}", ln=True)
    
    pdf.output(filepath)
    st.write(f"Risultati salvati in {filepath}")

# Streamlit App
def main():
    st.title("Strumento di Verifica Username")

    # Configurazione
    config = Config()  # Crea un'istanza della configurazione

    # Input dell'utente
    username_input = st.text_input("Inserisci Username")
    permute_input = st.checkbox("Permuta Username", value=False)
    permuteall_input = st.checkbox("Permuta Tutti gli Username", value=False)
    save_csv = st.checkbox("Salva in CSV", value=False)
    save_pdf = st.checkbox("Salva in PDF", value=False)

    if username_input:
        config.username = [username_input]
        config.permute = permute_input
        config.permuteall = permuteall_input
        config.csv = save_csv
        config.pdf = save_pdf

        # Permutazioni se necessario
        if config.permute or config.permuteall:
            st.write("Permutazioni in corso...")
            permuted_usernames = permute_usernames(config.username, config.permuteall)
        else:
            permuted_usernames = config.username

        # Verifica degli username
        all_found_accounts = {}
        for user in permuted_usernames:
            config.currentUser = user
            found_accounts = verifyUsername(user, config)
            all_found_accounts[user] = found_accounts
        
        # Mostra i risultati
        st.write("Risultati trovati:")
        for user, accounts in all_found_accounts.items():
            st.write(f"Username: {user}")
            for platform, account in accounts.items():
                st.write(f"  {platform}: {account}")

        # Salva i risultati se richiesto
        if config.csv:
            saveToCsv(all_found_accounts, "username_results")
        if config.pdf:
            saveToPdf(all_found_accounts, "username_results")

if __name__ == "__main__":
    main()
