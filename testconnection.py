"""
Standalone Snowflake connection test — no Streamlit required.
Run with: python test_connection_standalone.py

Reads credentials straight from .streamlit/secrets.toml, so make sure
you're running this from the same folder that contains that file.
"""

import sys
import traceback
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # pip install tomli  (for Python < 3.11)

import snowflake.connector

SECRETS_PATH = Path(".streamlit/secrets.toml")


def load_secrets():
    if not SECRETS_PATH.exists():
        sys.exit(
            f"❌ Fichier introuvable : {SECRETS_PATH.resolve()}\n"
            "   Lance ce script depuis le dossier qui contient .streamlit/secrets.toml"
        )
    with open(SECRETS_PATH, "rb") as f:
        data = tomllib.load(f)
    try:
        return data["connections"]["snowflake"]
    except KeyError:
        sys.exit("❌ Section [connections.snowflake] introuvable dans secrets.toml")


def main():
    print(f"→ snowflake-connector-python version: {snowflake.connector.__version__}")
    creds = load_secrets()
    print(f"→ Connexion à l'account '{creds.get('account')}' en tant que '{creds.get('user')}'...")

    conn_kwargs = {
        "account": creds.get("account"),
        "user": creds.get("user"),
        "password": creds.get("password"),
        "role": creds.get("role"),
        "warehouse": creds.get("warehouse"),
        "database": creds.get("database"),
        "schema": creds.get("schema"),
    }

    # Only set authenticator/private_key_file if actually present in
    # secrets.toml. Passing authenticator=None explicitly (instead of
    # omitting it) makes the connector misinterpret it as a custom
    # Okta IdP URL instead of falling back to normal password auth.
    if creds.get("authenticator"):
        conn_kwargs["authenticator"] = creds["authenticator"]
    if creds.get("private_key_file"):
        conn_kwargs["private_key_file"] = creds["private_key_file"]

    try:
        conn = snowflake.connector.connect(**conn_kwargs)
    except Exception as e:
        print("❌ Échec de la connexion.")
        print(f"   Détail : {e}")
        print("\n--- Traceback complet ---")
        traceback.print_exc()
        sys.exit(1)

    print("✅ Connexion réussie !")

    cs = conn.cursor()
    try:
        cs.execute(
            "SELECT CURRENT_VERSION(), CURRENT_ACCOUNT(), CURRENT_USER(), "
            "CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()"
        )
        version, account, user, role, warehouse, database, schema = cs.fetchone()
        print(f"   Version Snowflake : {version}")
        print(f"   Account           : {account}")
        print(f"   User              : {user}")
        print(f"   Role              : {role}")
        print(f"   Warehouse         : {warehouse}")
        print(f"   Database          : {database}")
        print(f"   Schema            : {schema}")

        print("\n→ Test de lecture de la table ARTICLES...")
        cs.execute("SELECT COUNT(*) FROM INFOCENTRE_DB.PUBLIC.ARTICLES")
        (count,) = cs.fetchone()
        print(f"✅ Table ARTICLES accessible — {count} ligne(s) trouvée(s).")

    except Exception as e:
        print("⚠️  Connexion établie, mais la requête a échoué.")
        print(f"   Détail : {e}")
    finally:
        cs.close()
        conn.close()


if __name__ == "__main__":
    main()