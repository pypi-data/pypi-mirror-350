import datetime
import os
import hashlib
import json

DATA_DIR = "journal_data"
JOURNAL_FILE = os.path.join(DATA_DIR, "journal.txt")
MD_EXPORT_FILE = os.path.join(DATA_DIR, "journal.md")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

def init():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        pwd = input("🔐 Set a password for your journal: ")
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        with open(CONFIG_FILE, "w") as f:
            json.dump({"password": hashed}, f)
        print("✅ Password set.\n")

def check_password():
    if not os.path.exists(CONFIG_FILE):
        return True
    pwd = input("🔐 Enter your journal password: ")
    hashed_input = hashlib.sha256(pwd.encode()).hexdigest()
    with open(CONFIG_FILE) as f:
        stored = json.load(f)["password"]
    if hashed_input != stored:
        print("❌ Incorrect password. Exiting.")
        exit()
    return True

def add_entry(text, tags):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tag_str = " ".join(f"#{tag}" for tag in tags)
    entry = f"[{timestamp}] {tag_str}\n{text}\n{'-'*40}\n"
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    print("✅ Entry added.")

def view_entries():
    if not os.path.exists(JOURNAL_FILE):
        print("No entries yet.")
        return
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        print(f.read())

def search_entries(keyword_or_tag):
    if not os.path.exists(JOURNAL_FILE):
        print("No entries found.")
        return
    found = False
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        entries = f.read().split('-' * 40 + '\n')
        for entry in entries:
            if keyword_or_tag.lower() in entry.lower():
                print(entry)
                print('-' * 40)
                found = True
    if not found:
        print("No matching entries found.")

def export_to_markdown():
    if not os.path.exists(JOURNAL_FILE):
        print("Nothing to export.")
        return
    with open(JOURNAL_FILE, "r", encoding="utf-8") as src:
        entries = src.read().split('-' * 40 + '\n')
    with open(MD_EXPORT_FILE, "w", encoding="utf-8") as md:
        for entry in entries:
            if entry.strip():
                md.write(f"### {entry.strip().splitlines()[0]}\n")
                md.write('\n'.join(entry.strip().splitlines()[1:]))
                md.write("\n\n---\n")
    print(f"📦 Exported to {MD_EXPORT_FILE}")

def main():
    init()
    check_password()

    while True:
        print("\n📓 What do you want to do?")
        print("1. Add entry")
        print("2. View entries")
        print("3. Search entries")
        print("4. Export to markdown")
        print("5. Exit")

        choice = input("Enter choice [1-5]: ")

        if choice == "1":
            text = input("📝 Write your journal entry:\n")
            tags = input("🏷️ Enter tags separated by spaces (optional): ").split()
            add_entry(text, tags)
        elif choice == "2":
            view_entries()
        elif choice == "3":
            keyword = input("🔍 Enter a keyword or tag to search: ")
            search_entries(keyword)
        elif choice == "4":
            export_to_markdown()
        elif choice == "5":
            print("👋 Exiting. See you next time!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
