class wordCount:
    def __init__(self):
        self.num_of_word = None
        self.num_of_lines = None
        self.num_of_char = None
        self.freq = None

    def countNumberOfWord(self):
        try:
            with open('wordCount.txt', 'r') as f:
                self.num_of_word = 0
                for line in f:
                    words = line.split()
                    self.num_of_word += len(words)
                print("Total number of words:", self.num_of_word)
        except FileNotFoundError:
            print("Error: 'wordCount.txt' file not found.")

    def numberOfLines(self):
        try:
            with open('wordCount.txt', 'r') as f:
                self.num_of_lines = 0
                for line in f:
                    self.num_of_lines += 1
                print(f"Total number of lines: {self.num_of_lines}")
        except FileNotFoundError:
            print("Error: 'wordCount.txt' file not found.")

    def totalNumberOfChar(self):
        try:
            with open('wordCount.txt', 'r') as f:
                self.num_of_char = 0
                for line in f:
                    self.num_of_char += len(line.strip("\n"))
                print(f"Total number of characters: {self.num_of_char}")
        except FileNotFoundError:
            print("Error: 'wordCount.txt' file not found.")

    def frequencyOfWord(self):
        try:
            with open('wordCount.txt', 'r') as f:
                self.freq = {}
                for line in f:
                    words = line.split()
                    for w in words:
                        w = w.lower()
                        if w in self.freq:
                            self.freq[w] += 1
                        else:
                            self.freq[w] = 1

                sorted_list = sorted(self.freq.items(), key=lambda x: x[1], reverse=True)
                top5 = sorted_list[:5]

                print("\nTop 5 repeated words:")
                for word, count in top5:
                    print(f"'{word}' -> {count} times")

        except FileNotFoundError:
            print("Error: 'wordCount.txt' file not found.")


def main():
    count_word = wordCount()
    count_word.countNumberOfWord()
    count_word.numberOfLines()
    count_word.totalNumberOfChar()
    count_word.frequencyOfWord()


if __name__ == "__main__":
    main()
