import sys

start = int(sys.argv[1])
end = int(sys.argv[2])
step = int(sys.argv[3])
s = 0

for i in range(start, end+1, step):
    s += i

print(s)
