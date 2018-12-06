from multiprocessing import Pool
import time


def run_slave(args):
    start, end, step = args
    # run slave


def test():
    with Pool(5) as pool:
        pool.map(threadFunc, ( (i, i+10) for i in range(0, 51, 10) ))