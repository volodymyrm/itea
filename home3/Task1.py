import sys


def inverse():
    """
    To use function, run the following command in console:
    $ python Task1.py <filename>
    :return: inverse file <filename>
    """
    filename = sys.argv[1]
    try:
        with open(filename, 'r+') as file:
            length = file.seek(0, 2)
            for j in range(length-1):
                file.seek(0,0)
                for i in range(length - 1 - j):
                    buf = list(file.read(2))
                    temp = buf[0]
                    buf[0] = buf[1]
                    buf[1] = temp
                    file.seek(file.tell() - 2, 0)
                    file.write("".join(buf))
                    file.seek(i + 1, 0)
    except FileNotFoundError:
        print('No such file found')

inverse()
