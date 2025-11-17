import json

MOCKUP_DB_INIT_JSON_FILENAME = "mockup_db_init.json"
MOCKUP_DB_JSON_FILENAME = "mockup_db.json"

def load_data_from_db() -> dict:
    with open(MOCKUP_DB_JSON_FILENAME) as f:
        return json.load(f)

def store_data_on_db(data) -> None:
    with open(MOCKUP_DB_INIT_JSON_FILENAME, "w+") as f:
        json.dump(data, f)