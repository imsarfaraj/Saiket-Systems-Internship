import re
import shutil
from pathlib import Path

# Your text file to operate on
FILE_PATH = Path("fileHandlingTXT")

class fileHandlingOperations:

    def __init__(self):
        self.word = None

    def userInput(self):
        self.word = input("Enter word to find: ").strip()

    def readFile(self):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\n----- FILE CONTENT -----\n")
                print(content)
                print("\n----- END OF FILE -----\n")
        except FileNotFoundError:
            print(f"File not found: {FILE_PATH}. Please create it in the program folder.")

    def findWord(self):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                if not self.word:
                    print("No search word provided.")
                    return

                if self.word.lower() in content.lower():
                    print("Word is found (case-insensitive search).")
                else:
                    print("Word is not found.")
        except FileNotFoundError:
            print(f"File not found: {FILE_PATH}.")

    def findAndReplaceWord(self):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()

            search = self.word
            if not search:
                print("No search word provided.")
                return

            pattern = re.compile(r'\b' + re.escape(search) + r'\b', flags=re.IGNORECASE)
            matches = list(pattern.finditer(content))

            if not matches:
                print(f"'{self.word}' not found in the file (case-insensitive, whole-word search).")
                return

            print(f"Found {len(matches)} occurrence(s) of '{self.word}'. Showing up to first 5 contexts:\n")
            lines = content.splitlines()
            shown = 0

            for m in matches:
                if shown >= 5:
                    break
                char_index = m.start()
                cumulative = 0
                for i, line in enumerate(lines):
                    cumulative += len(line) + 1
                    if char_index < cumulative:
                        start = max(0, i-1)
                        end = min(len(lines), i+2)
                        ctx = "\n".join(lines[start:end])
                        print(f"--- Line {i+1} ---\n{ctx}\n")
                        shown += 1
                        break

            ans = input("Do you want to replace this word everywhere? (yes/no): ").strip().lower()
            if ans not in ('yes', 'y'):
                print("No changes made.")
                return

            new_word = input("Enter new word: ").strip()
            if not new_word:
                print("No replacement word entered. Aborting.")
                return

            try:
                backup_path = FILE_PATH.with_suffix(FILE_PATH.suffix + ".bak")
                shutil.copy(FILE_PATH, backup_path)
                print(f"Backup created: {backup_path}")
            except Exception as e:
                print("Warning: could not create backup:", e)

            def replace_match(m):
                orig = m.group(0)
                if orig.isupper():
                    return new_word.upper()
                if orig.istitle():
                    return new_word.capitalize()
                if orig.islower():
                    return new_word.lower()
                return new_word

            updated_content = pattern.sub(replace_match, content)

            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            print("Replacement completed successfully.")

        except FileNotFoundError:
            print(f"File not found: {FILE_PATH}.")
        except Exception as e:
            print("An error occurred during find & replace:", e)


def main():
    files = fileHandlingOperations()

    while True:
        print("----- MENU -----\n"
              "1. Read File\n"
              "2. Find Word\n"
              "3. Find and Replace Word\n"
              "4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        match choice:
            case "1":
                files.readFile()

            case "2":
                files.userInput()
                files.findWord()

            case "3":
                files.userInput()
                files.findAndReplaceWord()

            case "4":
                print("Exiting program... Thank you!")
                break

            case _:
                print("Invalid choice. Please try again.")

        isContinue = input("Do you want to do something more? (yes/no): ").strip().lower()
        if isContinue not in ('yes', 'y'):
            print("Exiting program... Thank you!")
            break


if __name__ == '__main__':
    main()
