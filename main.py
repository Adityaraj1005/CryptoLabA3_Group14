#Main entry point for project
import os
from utils.logger import write_log
from utils.file_analysis import analyze_file

def menu():
    while True:
        print("\n===== CryptoLabX =====")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Encrypt - Coming Soon")
            write_log("Encrypt")

        elif choice == "2":
            print("Decrypt - Coming Soon")
            write_log("Decrypt")

        elif choice == "3":
            print("Attack - Coming Soon")
            write_log("Attack")

        elif choice == "4":
            filename = input("Enter filename (e.g., sample1.txt): ")
            filepath = os.path.join("datasets", filename)

            if os.path.exists(filepath):
                analyze_file(filepath)
                write_log("Analyze")
            else:
                print("File not found.")

        elif choice == "5":
            write_log("Exit")
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
