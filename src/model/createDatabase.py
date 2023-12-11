import sqlite3
from sqlite3 import Error
import os

class pyData:
    def __init__(self) -> None:
        # Create a connection immediately
        self.conn = self.__createConnection(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scoreDatabase.db'))

    # Private method __createConnection
    # Arguments:
    #   - databaseFile: The filepath for the SQLite database
    #
    # Will either connect to or create the SQLite database for the leaderboard
    # and will also attempt to create the tables for the scores if needed or if
    # they were for some reason deleted.
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

    # Public method insertScore
    # Arguments:
    #   - username: The username of the player to insert the score of
    #   - score: The score that the player achieved.
    #
    # Used to insert a new highscore into the database.
    def insertScore(self, username, score):
        maxScoreID = self.conn.execute(''' SELECT MAX(scoreNum) FROM normalScores;''')
        for i in maxScoreID:
            maxScoreID = list(i)[0]
            break
        
        # Each score has an ID as a primary key which increments each time a new score is added,
        # however if no previous score exists, it is automatically set to 1.
        if maxScoreID is not None:
            status = self.conn.execute(''' INSERT INTO normalScores (scoreNum, username, score) VALUES (?, ?, ?);
            ''', (maxScoreID + 1, username, score))
        else:
            status = self.conn.execute(''' INSERT INTO normalScores (scoreNum, username, score) VALUES (?, ?, ?);
            ''', (1, username, score))

        self.conn.commit()

        return status

    # Public method retrieveTop10Scores
    # 
    # Reaches into the databse and retrieves the top 10 scores for the scoreboard.
    def retrieveTop10Scores(self):
        return self.conn.execute(''' SELECT * FROM normalScores ORDER BY score ASC LIMIT 10;''')
