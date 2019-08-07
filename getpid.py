"""
getpid's operations section
"""
import os
import time

import click
import psutil

from simdash.database import database

@click.command()
@click.option('--d', help='database name, should end in .db')
@click.option('--u', help='username')
@click.option('--system/--pid', help='see the usage per pid or for the whole system', default=False)
def cli(d, u, system):
    """Implements the command line running of get_pids"""
    while True:
        print("start time %s" %time.time())
        if system:    
            get_sys_info(d)
        else:
            get_pids(d, u)
        print("finish time %s" %time.time())
        time.sleep(5)

def get_sys_info(db):
    """
    Get information about the System's usage of CPU load, load avg, and swap and physical memory.

    Args:
        db: path to the database file
    """
    the_db = database.Database(str(db))
    if  not the_db.check_if_table_exists("sys_usage"):
        cols = ['logic_time', 'real_time', 'cpu_load', 'num_cpus',  'load_avg', 'used_phys_mem',
                'total_phys_mem', 'used_swap_mem', 'total_swap_mem']
        dtypes = ["FLOAT", "INT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT"]
        vtypes = ["Q", "T", "Q", "Q", "Q", "Q", "Q", "Q", "Q"]
        the_db.make_table("sys_usage", cols, dtypes, vtypes)
    the_tab = the_db.get_table("sys_usage")
    load_avg = os.getloadavg()[0]
    swap_mem = psutil.swap_memory()
    total_swap = swap_mem[0]
    used_swap = swap_mem[1]
    phys_mem = psutil.virtual_memory()
    used_phys = phys_mem[3]
    free_phys = phys_mem[4]
    total_phys = phys_mem[3]+phys_mem[4]
    num_cpus = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq(percpu=True)
    cpu_sum = 0.0
    for cpu in cpu_freq:
        total = cpu[2]-cpu[1]
        used = float(cpu[0]-cpu[1])
        cpu_sum += used/total
    the_tab.append(cpu_load=cpu_sum, num_cpus=num_cpus, load_avg=load_avg, used_phys_mem=used_phys,
                   total_phys_mem=total_phys, used_swap_mem=used_swap, total_swap_mem=total_swap)

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
