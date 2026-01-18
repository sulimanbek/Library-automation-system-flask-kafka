class Book:
    def __init__(self, title, author, is_a_textbook, is_a_periodical):
        self.title = title
        self.author = author
        self.is_a_textbook = is_a_textbook
        self.is_a_periodical = is_a_periodical
        self.is_available = True

    def ask_book_info(self):
        print("==== Book Information ====")
        self.title = input("Enter the book title: ")
        self.author = input("Enter the author: ")
        while True:
            is_a_textbook_input = input("Is it a textbook? (yes/no): ").lower()
            if is_a_textbook_input == 'yes':
                self.is_a_textbook = True
                print("This book is a textbook.")
                break
            elif is_a_textbook_input == 'no':
                self.is_a_textbook = False
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        while True:
            is_a_periodical_input = input("Is it a periodical? (yes/no): ").lower()
            if is_a_periodical_input == 'yes':
                self.is_a_periodical = True
                print("This book is a periodical.")
                break
            elif is_a_periodical_input == 'no':
                self.is_a_periodical = False
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        print(f"Book '{self.title}' by {self.author} has been added to the library.")

