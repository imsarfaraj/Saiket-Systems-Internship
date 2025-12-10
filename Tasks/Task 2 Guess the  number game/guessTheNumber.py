import random

class RandomNum:
    def __init__(self):
        self.guessNum = random.randint(1, 10)

    def guessNumber(self):

        count = 1
        while True:
            try:
                num = int(input("Enter number: "))
            except ValueError:
                print("Invalid input! Please enter a NUMBER.")
                continue

            if self.guessNum == num:
                print("Congratulations, You guessed the correct number.")
                break
            else:
                if count == 5:
                    print("Game over! You used all attempts.")
                    print(f"The correct number was: {self.guessNum}")
                    break
                else:
                    count += 1

                    if num < self.guessNum:
                        print("Your guess is LOW. Try a higher number.")
                    elif num > self.guessNum:
                        print("Your guess is HIGH. Try a lower number.")

        self.playAgain()

    def playAgain(self):
        ans = input("Do You want to play again? yes/no: ").lower()
        if ans == 'yes':
            self.__init__()
            self.guessNumber()
        else:
            print("Thank you for playing")

def main():
    r = RandomNum()
    r.guessNumber()

if __name__ == '__main__':
    main()
