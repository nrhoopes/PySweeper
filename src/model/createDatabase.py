import sqlite3
from sqlite3 import Error
import os

class pyData:
    def __init__(self) -> None:
        self.conn = self.__createConnection(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scoreDatabase.db'))

    def __createConnection(self, databaseFile):
        conn = None
        try:
            conn = sqlite3.connect(databaseFile)
            print("SQLITE VERSION: " + sqlite3.version)
        except Error as e:
            print(e)
            quit()
        finally:
            if(conn):
                conn.execute(''' CREATE TABLE IF NOT EXISTS normalScores (
                    scoreNum INTEGER PRIMARY KEY NOT NULL,
                    username TEXT NOT NULL,
                    score INTEGER NOT NULL
                );
                ''')
            conn.commit()

            return conn

    def insertScore(self, username, score):
        maxScoreID = self.conn.execute(''' SELECT MAX(scoreNum) FROM normalScores;''')
        
        status = self.conn.execute(''' INSERT INTO normalScores (scoreNum, username, score) VALUES (?, ?, ?);
        ''', (list(maxScoreID)[0][0], username, score))

        self.conn.commit()

        return status

    def retrieveTop10Scores(self):
        return self.conn.execute(''' SELECT * FROM normalScores ORDER BY score ASC LIMIT 10;''')
