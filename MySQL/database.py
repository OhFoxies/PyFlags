import mysql.connector
import json

try:
    with open("config/config.json", 'r') as config:
        config = json.load(config)
except FileNotFoundError:
    print("Config file not found.")
    input("Press enter to close the program.")
    quit()
create_table = f"CREATE TABLE `{config['MySQL']['database']}`.`userdata` (`player_ID` VARCHAR(19) NOT " \
               f"NULL , `lang` VARCHAR(2) NOT NULL ," \
               f"`flags_lang` VARCHAR(2) NOT NULL , `points` INT NOT NULL , PRIMARY KEY (`player_ID`))"
create_database = f"CREATE DATABASE {config['MySQL']['database']}"

while True:
    try:
        try:
            user_data = mysql.connector.connect(
                host=config['MySQL']['host'],
                user=config['MySQL']['username'],
                password=config['MySQL']['password'],
                database=config['MySQL']['database'])
            cursor = user_data.cursor()
        except mysql.connector.errors.ProgrammingError:
            base = mysql.connector.connect(
                host=config['MySQL']['host'],
                user=config['MySQL']['username'],
                password=config['MySQL']['password'])
            base_cursor = base.cursor()
            base_cursor.execute(create_database)
            base_cursor.execute(create_table)
            del base_cursor, base
            continue
    except mysql.connector.errors.DatabaseError:
        print("Database doesnt exists.")
        input("Press enter to close")
        quit()
    break
