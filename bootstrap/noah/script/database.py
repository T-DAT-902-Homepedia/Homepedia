import mysql.connector


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="homepedia"
    )


def close_connection(connection, cursor):
    if connection.is_connected():
        cursor.close()
        connection.close()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS famille
                   (
                       id      INT PRIMARY KEY AUTO_INCREMENT,
                       famille VARCHAR(255) NOT NULL
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS univers
                   (
                       id         INT PRIMARY KEY AUTO_INCREMENT,
                       univers    VARCHAR(255) NOT NULL,
                       famille_id INT          NOT NULL,
                       FOREIGN KEY (famille_id) REFERENCES famille (id)
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS maille
                   (
                       id     INT PRIMARY KEY AUTO_INCREMENT,
                       maille VARCHAR(255) NOT NULL
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS maille_univers
                   (
                       maille_id  INT NOT NULL,
                       univers_id INT NOT NULL,
                       PRIMARY KEY (maille_id, univers_id),
                       FOREIGN KEY (maille_id) REFERENCES maille (id),
                       FOREIGN KEY (univers_id) REFERENCES univers (id)
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS client
                   (
                       id VARCHAR(255) PRIMARY KEY
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS produit
                   (
                       id        INT PRIMARY KEY AUTO_INCREMENT,
                       libelle   VARCHAR(255) NOT NULL,
                       maille_id INT          NOT NULL,
                       FOREIGN KEY (maille_id) REFERENCES maille (id)
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS ticket
                   (
                       id         VARCHAR(255) PRIMARY KEY,
                       client_id  VARCHAR(255) NOT NULL,
                       mois_vente INT          NOT NULL,
                       FOREIGN KEY (client_id) REFERENCES client (id)
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS ticket_produits
                   (
                       id         INT PRIMARY KEY AUTO_INCREMENT,
                       ticket_id  VARCHAR(255)   NOT NULL,
                       produit_id INT            NOT NULL,
                       prix_net   DECIMAL(10, 2) NOT NULL,
                       FOREIGN KEY (ticket_id) REFERENCES ticket (id),
                       FOREIGN KEY (produit_id) REFERENCES produit (id)
                   )
                   """)

    connection.commit()
    close_connection(connection, cursor)


if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)
