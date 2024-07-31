import sys
import os
from flask import Flask, request, render_template, send_file
from datetime import datetime
from dotenv import load_dotenv
from io import BytesIO
import pandas as pd
import pdfkit

# Aggiungi il percorso della directory 'src/modules' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src/modules")))

# Importa i moduli personalizzati
try:
    from core.username import verifyUsername
    from utils.userAgent import getRandomUserAgent
    from export.file_operations import createSaveDirectory
    from export.csv import saveToCsv
    from export.pdf import saveToPdf
    from utils.permute import Permute
except ModuleNotFoundError as e:
    print(f"Errore nell'importazione dei moduli: {e}")
    sys.exit()

# Carica le variabili d'ambiente
load_dotenv()

app = Flask(__name__)

# Funzione per generare possibili username
def generate_usernames(first_name, last_name, company):
    usernames = set()
    if first_name and last_name:
        # Combinazioni base
        usernames.update([
            f"{first_name}{last_name}",
            f"{first_name}.{last_name}",
            f"{last_name}{first_name}",
            f"{first_name[0]}{last_name}",
            f"{last_name}{first_name[0]}",
            f"{first_name}_{last_name}",
            f"{last_name}_{first_name}"
        ])
        
        # Combinazioni con iniziali
        usernames.update([
            f"{first_name[0]}_{last_name}",
            f"{last_name}_{first_name[0]}",
            f"{first_name[0]}.{last_name}",
            f"{last_name}.{first_name[0]}"
        ])
        
        # Combinazioni con numeri
        usernames.update([
            f"{first_name}{last_name}123",
            f"{first_name}.{last_name}123",
            f"{first_name}_{last_name}123"
        ])
        
        # Combinazioni con azienda
        if company:
            usernames.update([
                f"{first_name}{last_name}{company}",
                f"{first_name}.{last_name}@{company}",
                f"{last_name}.{first_name}@{company}",
                f"{first_name[0]}{last_name}@{company}",
                f"{first_name}.{last_name}.{company}"
            ])
    return list(usernames)

# Route principale per la pagina web
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        company = request.form.get("company")
        permute = request.form.get("permute") == "on"
        output_csv = request.form.get("output_csv") == "on"
        output_pdf = request.form.get("output_pdf") == "on"

        if not first_name or not last_name:
            return render_template("index.html", error="Nome e Cognome sono richiesti.")

        # Genera i possibili username
        usernames = generate_usernames(first_name, last_name, company)
        
        # Permutazioni degli username se richiesto
        if permute and usernames:
            permute_class = Permute(usernames)
            usernames = permute_class.gather("all")

        if not usernames:
            return render_template("index.html", error="Nessun username generato. Inserisci nome e cognome.")

        # Verifica gli username
        found_accounts = []
        for user in usernames:
            try:
                result = verifyUsername(user)
                if result:
                    found_accounts.append((user, result))
            except Exception as e:
                found_accounts.append((user, f"Errore: {e}"))

        # Salvataggio dei risultati
        if output_csv and found_accounts:
            csv_output = BytesIO()
            df = pd.DataFrame(found_accounts, columns=["Username", "Risultato"])
            df.to_csv(csv_output, index=False)
            csv_output.seek(0)
            return send_file(csv_output, as_attachment=True, download_name="username_results.csv", mimetype="text/csv")

        if output_pdf and found_accounts:
            pdf_output = BytesIO()
            html_content = "<h1>Risultati della Ricerca</h1><ul>"
            for user, result in found_accounts:
                html_content += f"<li>{user}: {result}</li>"
            html_content += "</ul>"
            pdfkit.from_string(html_content, pdf_output)
            pdf_output.seek(0)
            return send_file(pdf_output, as_attachment=True, download_name="username_results.pdf", mimetype="application/pdf")

        return render_template("index.html", results=found_accounts)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
