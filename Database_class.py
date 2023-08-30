import mysql.connector
import pandas as pd
from datetime import datetime

class Database():
    def __init__(self):
        # Établir une connexion à la base de données
        self.connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            #password="your_password",
            database="local"
        )

        # Créer un curseur pour exécuter des requêtes
        self.cursor = self.connection.cursor()

    def run(self):
        self.create_tables()

        df = self.get_table(table_name="brutes")

        print(df)

        self.save_database()

    def create_tables(self):
        # Créer une table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS brutes (
            id INT PRIMARY KEY,
            name VARCHAR(50),
            rang VARCHAR(50),
            level INT,
            hps INT,
            strength INT,
            agility INT,
            rapidity INT,
            xp INT,
            xp_max INT,
            victories INT,
            last_update DATETIME
        )
        """
        self.cursor.execute(create_table_query)

        # Créer une table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS attacks_logs (
            date_time DATETIME,
            id INT,
            rang VARCHAR(50),
            id_target INT,
            hps INT,
            strength INT,
            agility INT,
            rapidity INT,
            AI_guess FLOAT,
            FlashVars VARCHAR(150),
            win BOOL
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def delete_tables(self):
        query = """
        DROP TABLE brutes
        """
        self.cursor.execute(query)
        self.connection.commit()
        
        query = """
        DROP TABLE attacks_logs
        """
        self.cursor.execute(query)
        self.connection.commit()

    def log_fight(self, data):
        data = (datetime.utcnow(),) + data
        # Insérer des données dans la table
        insert_query = """
        INSERT INTO attacks_logs (date_time, id, rang, id_target, hps, strength, agility, rapidity, AI_guess, FlashVars, win)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_query, data)
        self.connection.commit()

    def insert_into_database(self, data):
        data = data + (datetime.utcnow(),)
        # Insérer des données dans la table
        insert_query = """
        INSERT INTO brutes (id, name, rang, level, hps, strength, agility, rapidity, xp, xp_max, victories, last_update)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        level = VALUES(level),
        rang = COALESCE(rang, VALUES(rang)),
        hps = VALUES(hps),
        strength = VALUES(strength),
        agility = VALUES(agility),
        rapidity = VALUES(rapidity),
        xp = COALESCE(xp, VALUES(xp)),
        xp_max = COALESCE(xp_max, VALUES(xp_max)),
        victories = COALESCE(victories, VALUES(victories)),
        last_update = COALESCE(last_update, VALUES(last_update))
        """
        self.cursor.execute(insert_query, data)
        self.connection.commit()
    
    def delete_from_database(self, id):
        delete_query = "DELETE FROM brutes WHERE id = %s"
        self.cursor.execute(delete_query, (id,))
        self.connection.commit()

    def get_table(self, table_name):
        # Obtenir les noms des colonnes de la table
        self.cursor.execute(f"DESCRIBE {table_name}")
        columns = [column[0] for column in self.cursor.fetchall()]

        # Obtenir les données de la table
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()

        # Créer un DataFrame avec les données et les noms des colonnes
        df = pd.DataFrame(rows, columns=columns)
        
        return df
    
    def custom_query(self, query, table_name):
        # Obtenir les noms des colonnes de la table
        self.cursor.execute(f"DESCRIBE {table_name}")
        columns = [column[0] for column in self.cursor.fetchall()]

        # Obtenir les données de la table
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Créer un DataFrame avec les données et les noms des colonnes
        df = pd.DataFrame(rows, columns=columns)
        
        return df
    
    def save_database(self):
        # Nom du fichier de sortie
        output_file = "data/backup.sql"

        # Ouvrir le fichier en mode écriture
        with open(output_file, "w") as file:
            # Récupérer la liste des tables
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()

            # Parcourir chaque table et générer le contenu SQL
            for table in tables:
                table_name = table[0]

                if table_name in ["brutes","attacks_logs"]:
                    file.write(f"--- Table: {table_name}\n")

                    # Obtenir la structure de la table
                    self.cursor.execute(f"SHOW CREATE TABLE {table_name}")
                    create_table_query = self.cursor.fetchone()[1]

                    # Écrire la structure de la table dans le fichier
                    file.write(create_table_query + ";\n")

                    # Obtenir les données de la table
                    self.cursor.execute(f"SELECT * FROM {table_name}")
                    rows = self.cursor.fetchall()
                    
                    # Générer les requêtes d'insertion
                    for row in rows:
                        insert_query = f"INSERT INTO {table_name} VALUES {row};\n"
                        file.write(insert_query)