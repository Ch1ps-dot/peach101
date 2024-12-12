import os, sys

def pingpong():
    cnt = 0
    while(True):
        recv = input()
        if (recv == "ping"):
            cnt = cnt + 1
            print("pong")
            if( cnt == 3): 
                print("pwn!")
                break

        else:
            print("Oops")
            break
    print("Game Over")

if __name__ == "__main__":
    pingpong()