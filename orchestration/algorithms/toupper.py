import sys

input = ""
for line in sys.stdin.readlines():
	input = input + line
output = input.upper()
sys.stdout.write(output)
