from home2 import monitor, process
from time import sleep

def main():
    while True:
        monitor('source', 'results', 'errors')
        sleep(5)


if __name__== "__main__":
  main()