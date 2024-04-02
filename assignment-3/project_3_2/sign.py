from oracle import *
from helper import *

def get_signature(m, n):
  return (Sign(lowest_divisor(m)) * Sign(m//lowest_divisor(m)) * pow(Sign(1), -1, n)) % n


def main():
  with open('project_3_2/input.txt', 'r') as f:
    n = int(f.readline().strip())
    msg = f.readline().strip()

  Oracle_Connect()    

  m = ascii_to_int(msg)
  sigma = get_signature(m, n) 

  print(sigma)

  Oracle_Disconnect()

if __name__ == '__main__':
  main()
