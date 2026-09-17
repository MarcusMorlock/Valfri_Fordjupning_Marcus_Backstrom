# Valfri_Fordjupning_Marcus_Backstrom
## Valfri fördjupning inom Python för Data Science


# Sensor Data Validation Pipeline (`sensor_pipeline`)

En modulär Python-pipeline för automatisk städning, validering och kvalitetssäkring av sensordata. Projektet kombinerar **Pandas** för deterministisk felkorrigering med **Pydantic** för strikt schemavalidering och felhantering (Human-in-the-Loop).

## Systemkrav & Beroenden

* **Python:** `>= 3.13`
* **Huvudbibliotek:**
  * `pydantic >= 2.0.0`
  * `pandas >= 2.0.0`

## Installation & Setup

### Klona repot och navigera till projektmappen:
git clone https://github.com/MarcusMorlock/Valfri_Fordjupning_Marcus_Backstrom.git

cd Valfri_Fordjupning_Marcus_Backstrom

### Skapa och aktivera virtuell miljö:
python -m venv .venv

source .venv/Scripts/activate

### Installera projektet:
pip install -e .

### För att köra hela pipelinen från CLI:
python -m src

# Hur Pipelinen Fungerar
- Generering (generate_data.py): Skapar 5 JSON-filer i mappen data/ med olika feltyper (korrekt data, stavfel, saknade värden, orimliga temperaturer).

- Datainläsning (io.py): Läser in JSON-filerna till Pandas DataFrames.

- Auto-korrigering (transform.py): Rättar automatiskt till kända stavfel i regionnamn (t.ex. "orebro" -> "Örebro").

- Schemavalidering (schemas.py & validate.py): Validerar varje rad mot Pydantic-modellen TemperatureRead. Rader med orimliga temperaturer eller saknade fält flaggas.

- Human-in-the-Loop Output: Returnerar en strukturerad DataFrame med spårbarhetskolumner (auto_cleaned, flagged_for_manual_review, original_region).


# Projektstruktur
- data/ – Genererade JSON-filer (skapas automatiskt vid körning)

- src/

- __init__.py – Exporterar moduler

- __main__.py – Entrépunkt för CLI (python -m src)

- generate_data.py – Skapar mock-data

- io.py – Läser och skriver data

- log_config.py – Loggningsinställningar

- schemas.py – Pydantic-modeller och datamodellering

- transform.py – Pandas-städning och auto-correct

- validate.py – Valideringskörning per dataset

- pyproject.toml – Paket- och beroendekonfiguration
  
- README.md – Projektdokumentation