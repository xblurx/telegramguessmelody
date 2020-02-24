import sqlite3


class SqlHandler:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all_rows(self):
        """Getting all rows"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM melodies').fetchall()

    def select_single_row(self, row_num):
        """
        Getting a row and its num
        :return first ([0]) tuple from a list that was created by cursor.execute
        """
        with self.connection:
            return self.cursor.execute('SELECT * FROM melodies WHERE id = ?', (row_num,)).fetchall()[0]

    def count_rows(self):
        """Counts all rows in db, returning length of a list"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM melodies').fetchall()
            return len(result)

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    print('sqlhandler was executed separately')
else:
    print('sqlhanadler was imported')
