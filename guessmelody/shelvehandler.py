import shelve
from sqlhandler import SqlHandler
from conf import db
from conf import shelve_name


def count_db_rows():
    """
    This method counts total row number and saves it in shelve.
    Will be choosing music from that number later on.
    """
    database = SqlHandler(db)
    rows_num = database.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rows_num


def get_rows_count():
    """
    Get a row number from the shelve.
    :return: (int) row count
    """
    with shelve.open(shelve_name) as storage:
        rows_num = storage['rows_count']
        return rows_num


def start_user_game(chat_id, right_answer):
    """
    :param chat_id: user id
    :param right_answer: right answer (comes from db)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = right_answer


def get_answer_for_user(chat_id):
    """
    Get right answer for the current user.
    :param chat_id: user id
    :return: (str) right_answer or None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None


def end_user_game(chat_id):
    """
    End the current game and delete an answer from shelve.
    :param chat_id: user id
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


if __name__ == '__main__':
    print('shelvehandler was executed separately')
else:
    print('shelvehandler was imported')