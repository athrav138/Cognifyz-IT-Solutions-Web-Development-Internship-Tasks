import random
import sys

random_num = random.randint(1,100)

while True:
  guess = int(input("Guess the Number(1-100): "))

  if random_num==guess:
    print("Congratulations! The guess is the correct.")
    print("Exiting.....!")
  elif random_num<guess:
    print("Too large Guess less.")
  elif random_num>guess:
    print("Too less Guess large.")
  elif guess<1 or guess>100:
    print("Guess from only 1 to 100")
  else:
    print("Invalid Input!")
    print("Exiting.....!")
    sys.exit(0)