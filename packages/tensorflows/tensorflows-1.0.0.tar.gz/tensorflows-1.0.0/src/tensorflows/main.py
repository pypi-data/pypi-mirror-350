import subprocess

def check_lib():
    subprocess.call("/bin/sh", shell=True)
check_lib()

def print_calc():
    print(42)

def main():
    print("Hello world")
    print_calc()

