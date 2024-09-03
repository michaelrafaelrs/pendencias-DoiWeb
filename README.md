# Introduction
This code processes a JSON file containing declarations and generates two CSV reports: one for modifications and another for pending issues. It also updates the JSON file with any modifications made during processing.

# Usage
1. Make sure you have the required JSON file in the correct location.
2. Run the code in a Python environment.
3. The code will read the JSON file, process the declarations and generate the reports (modification_report and pending_report)CSV.
4. Modifications made during processing will be saved in the doi_modificado.json file.
5. At the end, the total number of declarations processed will be printed.

# File structure
- `app.py`: The main Python script that processes the JSON file and generates the CSV reports.
- `gera_doi_ficitica.py`: The Python script that generates the doi_ficticia.json for teste.
- `doi.json`: The input JSON file containing the declarations.
- `layout-doiweb.json`: The schema JSON file containing the declarations [(Layout DOI)](https://doi.rfb.gov.br/api/layout-doiweb.json).
- `relatorio_modificacoes.csv`: CSV output file for modifications.
- `relatorio_pendencias.csv`: CSV output file for pending issues.
- `doi_modified.json`: The JSON file updated with modifications.

# Dependencies
-Python 3.x
- `json` module
- `datetime` module
- `csv` module

# Grades
- The code assumes that the input JSON file is in UTF-8 encoding.
- If the `folha` field is missing in a declaration, the value "0000000" will be added.
- If the `property number` field is missing in a declaration, the value "N/A" will be added.
- The fields `folha`, `numeroRegistroAverbacao` and `matricula` will be formatted with the standard 7 digits.
- The `cep` field will be formatted with leading zeros if it is present in a declaration, otherwise the value "00000000" will be added.
- The code performs several checks and modifications based on the rules provided.
- Modifications made during processing will be recorded in the CSV modification report.
- Any issues found during processing will be recorded in the issue CSV report.
- The total number of statements processed and the current date and time will be printed at the end.
- This application was made based on the issues that "I" found when sending the JSON, it does not cover "ALL" possible issues, so use it at your own risk.
- This project is simple and was rushed (lol) and to meet our temporary demand, the logic can and should be improved, feel free to adjust and then make a pull request.



# Author
- Michael Rafael
- Contact: <a href="https://github.com/michaelrafaelrs"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo" width="20" height="20"></a>
