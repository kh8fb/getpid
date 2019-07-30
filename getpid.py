"""
getpid's operations section
"""
import time

import click
import psutil

from simdash.database import database

@click.command()
@click.option('--d', help='database name, should end in .db')
@click.option('--u', help='username')
def cli(d, u):
    """Implements the command line running of get_pids"""
    while True:
        print("start time %s" %time.time())
        get_pids(d, u)
        time.sleep(5)
        print("finish time %s" %time.time())


def get_pids(db, username):
    """
    Find all of the processes ocurring under this user and add their information to the database.

    Will find the cpu_percent of the current action, as well as the uss or how much space
    would be freed by removing that specific PID.  This information will be stored in the
    database file.

    Args:
        db: database file name and path, should end in .db
        username: name of the user
    """
    the_db = database.Database(str(db))
    user = str(username)
    for proc in psutil.process_iter(attrs=['pid', 'memory_percent', 'cpu_percent', 'username']):
        dic = proc.as_dict()
        if user == dic['username']:
            pid = f"{user}pid{str(dic['pid'])}"
            mem_inf = dic['memory_percent']
            cols = ['logic_time', 'real_time', 'mem_percent', 'cpu_percent']
            dtypes = ["FLOAT", "INT", "INT", "FLOAT"]
            vtypes = ["Q", "T", "Q", "Q"]
            cpu_pcnt = dic['cpu_percent']
            if the_db.check_if_table_exists(pid):
                tab = the_db.get_table(pid)
                tab.append(mem_percent=mem_inf, cpu_percent=cpu_pcnt)
            else:
                the_db.make_table(pid, cols, dtypes, vtypes)
                tab = the_db.get_table(pid)
                tab.append(mem_percent=mem_inf, cpu_percent=cpu_pcnt)
