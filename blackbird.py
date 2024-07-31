import streamlit as st
import os
from dotenv import load_dotenv
from itertools import permutations

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

# Funzione di esempio per la verifica dell'username
def verifyUsername(username, config):
    # Implementa qui la logica per verificare l'username
    st.write(f"Verifica dell'username: {username}")
    # Simulazione di risultati trovati
    found_accounts = {"platform1": f"{username}@platform1.com", "platform2": f"{username}@platform2.com"}
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
        return [username for username in usernames]

# Streamlit App
def main():
    st.title("Strumento di Verifica Username")

    # Configurazione
    config = Config()  # Crea un'istanza della configurazione

    # Input dell'utente
    username_input = st.text_input("Inserisci Username")
    permute_input = st.checkbox("Permuta Username", value=False)
    permuteall_input = st.checkbox("Permuta Tutti gli Username", value=False)
    
    if username_input:
        config.username = [username_input]
        config.permute = permute_input
        config.permuteall = permuteall_input
        
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

if __name__ == "__main__":
    main()
