from multiprocessing import Pool
from subprocess import Popen
from random import randrange


def params():
    start = randrange(0, 99, 1)
    stop = randrange(100, 10000000, 1)
    step = randrange(1, 100, 1)
    return start, stop, step


def run_slave(args):
    p = Popen(['python', 'slave.py'] + [str(x) for x in args])
    while p.poll() is None:
        pass
    print('pid={pid}\n'.format(pid=p.pid))


def run_pool(amount):
    """
    Variant 1 - run processes in Pool. When each process finished, - it prints its pid
    :param amount: pool size
    """
    with Pool(amount) as pool:
        pool.map(run_slave, [params() for _ in range(amount)])


def run_list(amount):
    """
    Variant 2 - Create a list of processes. In loop check every process on whether its finished or not.
    Print the pid of the process who finished first.
    :param amount: size of process list
    """
    processes = list()
    for _ in range(amount):
        processes.append(Popen(['python', 'slave.py'] + [str(x) for x in params()]))
    res = True
    while res:
        for p in processes:
            if p.poll() is not None:
                print('pid={pid}'.format(pid=p.pid))
                res = False
                break

if __name__ == '__main__':
    print("Variant 1")
    run_pool(3)
    print("Variant 2")
    run_list(3)