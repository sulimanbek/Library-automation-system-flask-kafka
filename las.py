from datetime import datetime, timedelta





class Library:
    def __init__(self):
        self.user_id = []
        self.books = []
        self.users = []
        self.borrowed_books = []
        self.reserved_books = []
        self.web_extension_count = 0
        self.kiosk_extension_count = 0
        self.extension_limit = 3
        self.fine_rate_first_week = 10
        self.fine_rate_subsequent_weeks = 20
        self.reservation_pickup_days = 2

    def add_user(self):
        user = User("", "")
        user.ask_user_info()
        self.users.append(user)

    def add_book(self):
        book = Book("", "", False, False)
        book.ask_book_info()
        self.books.append(book)

    def borrow_book(self):
        print("==== Borrow a Book ====")
        user_first_name = input("Enter your name: ")
        self.user_id = input("Enter your ID: ")
        book_title = input("Enter the book title you want to borrow: ")
        user = next((user for user in self.users if user.first_name == user_first_name), None)
        book = next((book for book in self.books if book.title == book_title), None)
        if user and book:
            borrowing_method = input("Choose borrowing method (kiosk/counter): ").lower()
            if borrowing_method == 'kiosk':
                self.pin_code = input("Enter the kiosk PIN code: ")
                self.process_borrowing(user, book, pin_code = None)
            elif borrowing_method == 'counter':
                self.process_borrowing(user, book)
            else:
                print("Invalid borrowing method. Please choose 'kiosk' or 'counter'.")
        else:
            print("User or book not found.")

    def process_borrowing(self, user, book, pin_code = None):
        if len(user.books_borrowed) < user.max_books_allowed and book.is_available:
            user.books_borrowed.append(book)
            book.is_available = False
            due_date = datetime.now() + timedelta(days=user.borrowing_days_limit)
            self.borrowed_books.append({'user': user, 'book': book, 'due_date': due_date})
            print(f"{user.first_name} has successfully borrowed '{book.title}'.")
            print(f"Due date: {due_date.strftime('%Y-%m-%d')}. Enjoy your reading!")
        else:
            print(f"Borrowing '{book.title}' is not allowed for {user.first_name}.")

    def return_book(self):
        print("==== Return a Book ====")
        user_first_name = input("Enter your name: ")
        self.user_id = input("Enter your ID: ")
        book_title = input("Enter the book title you want to return: ")
        user = next((user for user in self.users if user.first_name == user_first_name), None)
        book = next((book for book in self.books if book.title == book_title), None)
        if user and book:
            if book in user.books_borrowed:
                user.books_borrowed.remove(book)
                book.is_available = True
                self.handle_overdue_fine(user, book)
                self.borrowed_books = [item for item in self.borrowed_books if not (item['user'] == user and item['book'] == book)]
                print(f"{user.first_name} has successfully returned '{book.title}'.")
                print("Thank you for returning the book!")
            else:
                print(f"{user.first_name} did not borrow '{book.title}'.")
        else:
            print("User or book not found.")

    def handle_overdue_fine(self, user, book):
        due_date = next(item['due_date'] for item in self.borrowed_books if item['user'] == user and item['book'] == book)
        days_overdue = max(0, (datetime.now() - due_date).days)
        if days_overdue > 0:
            fine = self.calculate_fine(days_overdue)
            print(f"{user.first_name}, your book is overdue by {days_overdue} days. Please pay a fine of {fine} Turkish Lira.")

    def calculate_fine(self, days_overdue):
        if days_overdue <= 7:
            return self.fine_rate_first_week
        else:
            subsequent_weeks = (days_overdue - 7) // 7
            return self.fine_rate_first_week + (subsequent_weeks * self.fine_rate_subsequent_weeks)

    def extend_borrowing_period(self):
        print("==== Extend Borrowing Period ====")
        user_first_name = input("Enter your name: ")
        user = next((user for user in self.users if user.first_name == user_first_name), None)
        if user:
            book_title = input("Enter the book title you want to extend: ")
            book = next((book for book in user.books_borrowed if book.title == book_title), None)
            if book:
                extension_method = input("Choose extension method (web/kiosk/counter): ").lower()
                if extension_method == 'web':
                    self.extend_borrowing_period_web(user, book)
                elif extension_method == 'kiosk':
                    pin_code = input("Enter the kiosk PIN code: ")
                    self.extend_borrowing_period_kiosk(user, book, pin_code)
                elif extension_method == 'counter':
                    self.extend_borrowing_period_counter(user, book)
                else:
                    print("Invalid extension method. Please choose 'web', 'kiosk', or 'counter'.")
            else:
                print(f"You have not borrowed '{book_title}'.")
        else:
            print("User not found.")

    def extend_borrowing_period_web(self, user, book):
        if self.can_extend_borrowing_period(user, 'web'):
            if not self.is_overdue(book, user):
                new_due_date = datetime.now() + timedelta(days=user.borrowing_days_limit)
                book_due_date = next(item['due_date'] for item in self.borrowed_books if
                                     item['user'] == user and item['book'] == book)
                days_remaining = (book_due_date - datetime.now()).days
                print(f"Current due date: {book_due_date.strftime('%Y-%m-%d')}. You have {days_remaining} days remaining.")
                print(f"Extending due date to: {new_due_date.strftime('%Y-%m-%d')}")
                self.borrowed_books = [item for item in self.borrowed_books if
                                       not (item['user'] == user and item['book'] == book)]
                self.borrowed_books.append({'user': user, 'book': book, 'due_date': new_due_date})
                user.browsing_extension_count += 1
                print("Borrowing period extended successfully.")
            else:
                print("Extension is not allowed for overdue books.")
        else:
            print(f"You have reached the maximum extension limit for '{book.title}' using web.")

    def extend_borrowing_period_kiosk(self, user, book, pin_code):
        if self.can_extend_borrowing_period(user, 'kiosk'):
            if self.validate_pin_code(user, pin_code):
                self.extend_borrowing_period_web(user, book)
            else:
                print("Invalid PIN code. Extension failed.")
        else:
            print(f"You have reached the maximum extension limit for '{book.title}' using kiosk.")

    def can_extend_borrowing_period(self, user, extension_method):
        if extension_method == 'web':
            return user.browsing_extension_count < self.extension_limit
        elif extension_method == 'kiosk':
            return self.kiosk_extension_count < self.extension_limit
        else:
            return True

    def validate_pin_code(self, user, pin_code):
        if pin_code.isdigit() and len(pin_code) == 4:
            print("PIN code validation successful.")
            return True
        else:
            print("Invalid PIN code. Please enter a valid 4-digit PIN code.")
            return False


    def is_overdue(self, book, user):
        due_date = next(item['due_date'] for item in self.borrowed_books if item['user'] == user and item['book'] == book)
        return datetime.now() > due_date

    def search_and_reserve_book(self):
        print("==== Search and Reserve a Book ====")
        user_first_name = input("Enter your name: ")
        book_title = input("Enter the book title you want to search and reserve: ")
        user = next((user for user in self.users if user.first_name == user_first_name), None)
        book = next((book for book in self.books if book.title == book_title and book.is_available), None)
        if user and book:
            if book not in self.reserved_books:
                self.reserved_books.append(book)
                print(f"'{book.title}' has been reserved for {user.first_name}. You will be notified by email when the book is available.")
            else:
                print(f"'{book.title}' is already reserved by another user.")
        else:
            print("User or book not found or the book is not available.")

    def check_reserved_books(self):
        print("==== Check Reserved Books ====")
        user_first_name = input("Enter your name: ")
        self.user_id = input("Enter your ID: ")
        user = next((user for user in self.users if user.first_name == user_first_name), None)
        if user:
            reserved_books_for_user = [book.title for book in self.reserved_books if book in self.books and book.is_available]
            if reserved_books_for_user:
                print(f"{user.first_name}, you have the following reserved books:")
                for title in reserved_books_for_user:
                    print(f"- {title}")
                pickup_confirmation = input("Do you want to confirm the pickup of any reserved book? (yes/no): ").lower()
                if pickup_confirmation == 'yes':
                    self.confirm_reserved_books_pickup(user)
            else:
                print("You don't have any reserved books.")
        else:
            print("User not found.")

    def confirm_reserved_books_pickup(self, user):
        books_to_pickup = []
        for book in self.reserved_books:
            if book in self.books and book.is_available:
                books_to_pickup.append(book)
                book.is_available = False
        if books_to_pickup:
            print("The following reserved books are ready for pickup:")
            for book in books_to_pickup:
                print(f"- {book.title}")
            print("Thank you for picking up your reserved books. Enjoy your reading!")
            self.reserved_books = [book for book in self.reserved_books if book not in books_to_pickup]
        else:
            print("No reserved books available for pickup.")

    def print_menu(self):
        print("==== Library Automation System ====")
        print("1. Add a user")
        print("2. Add a book")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Extend borrowing period")
        print("6. Search and reserve a book")
        print("7. Check reserved books")
        print("8. Quit")

    def run(self):
        while True:
            self.print_menu()
            menu = input("How can we help you? Pick your option (1-8): ")
            if menu == '1':
                self.add_user()
            elif menu == '2':
                self.add_book()
            elif menu == '3':
                self.borrow_book()
            elif menu == '4':
                self.return_book()
            elif menu == '5':
                self.extend_borrowing_period()
            elif menu == '6':
                self.search_and_reserve_book()
            elif menu == '7':
                self.check_reserved_books()
            elif menu == '8':
                print("Thank you for using the Library Automation System. Goodbye!")
                pass
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")

    def extend_borrowing_period_counter(self, user, book):
        pass


# Example usage:

library = Library()
library.run()

