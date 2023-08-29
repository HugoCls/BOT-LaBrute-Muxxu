import mysql.connector
import pandas as pd

class Database():
    def __init__(self):
        # Établir une connexion à la base de données
        self.connection = mysql.connector.connect(
            host="localhost",
            port="10005",
            user="root",
            password="root",
            database="local"
        )

        # Créer un curseur pour exécuter des requêtes
        self.cursor = self.connection.cursor()

    def run(self):
        self.create_tables()

        self.insert_into_database(data = (4195904, "Changed", "Platinium", 8, 60, 7, 2, 7))
        self.insert_into_database(data = (4195102, "Hugo", "Master", 8, 60, 7, 2, 7))

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
            injuries INT,
            victories INT,
            last_heal_datetime DATETIME
        )
        """
        self.cursor.execute(create_table_query)

        # Créer une table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS attacks_logs (
            id INT PRIMARY KEY,
            rang VARCHAR(50),
            id_target INT,
            hps INT,
            strength INT,
            agility INT,
            rapidity INT,
            win BOOL,
            AI_guess FLOAT,
            FlashVars VARCHAR(150)
        )
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def log_fight(self, data):
        # Insérer des données dans la table
        insert_query = """
        INSERT INTO brutes (id, rang, id_target, hps, strength, agility, rapidity, win, AI_guess, FlashVars)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_query, data)
        self.connection.commit()

    def insert_into_database(self, data):
        # Insérer des données dans la table
        insert_query = """
        INSERT INTO brutes (id, name, rang, level, hps, strength, agility, rapidity, xp, xp_max, injuries, victories, last_heal_datetime)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        level = VALUES(level),
        rang = COALESCE(rang, VALUES(rang)),
        hps = VALUES(hps),
        strength = VALUES(strength),
        agility = VALUES(agility),
        rapidity = VALUES(rapidity),
        xp = COALESCE(xp, VALUES(xp)),
        xp_max = COALESCE(xp_max, VALUES(xp_max)),
        injuries = COALESCE(injuries, VALUES(injuries)),
        victories = COALESCE(victories, VALUES(victories)),
        last_heal_datetime = COALESCE(last_heal_datetime, VALUES(last_heal_datetime))
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