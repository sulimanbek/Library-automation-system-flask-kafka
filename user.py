class User:
    def __init__(self, first_name, user_type, user_id="", is_a_graduate=False, email="", has_smart_card=False, annual_fee_paid=False):
        self.first_name = first_name
        self.user_type = user_type
        self.user_id = user_id
        self.is_a_graduate = is_a_graduate
        self.email = email
        self.has_smart_card = has_smart_card
        self.annual_fee_paid = annual_fee_paid
        self.books_borrowed = []
        self.max_books_allowed = self.set_max_books_allowed()
        self.borrowing_days_limit = self.set_borrowing_days_limit()
        self.browsing_extension_count = 0

    def set_max_books_allowed(self):
        if self.user_type == 'faculty member':
            return 5
        else:
            return 3

    def set_borrowing_days_limit(self):
        if self.user_type == 'faculty member':
            return 30
        else:
            return 15

    def ask_user_info(self):
        print("==== User Information ====")
        self.user_type = input("Enter the user type (student/faculty member/staff/graduate): ").lower()
        if self.user_type in ['student', 'faculty member', 'staff']:
            self.first_name = input("Enter your name: ")
            self.user_id = input("Enter your ID: ")
            self.email = input('Enter your email: ')
            self.has_smart_card = input("Do you have a smart card with library card features? (yes/no): ").lower() == 'yes'
        elif self.user_type == 'graduate':
            self.first_name = input("Enter your name: ")
            self.user_id = input("Enter your ID: ")
            self.email = input('Enter your email: ')
            self.annual_fee_paid = input("Have you paid the annual fee? (yes/no): ").lower() == 'yes'
            if self.is_a_graduate:
                print("Graduates can benefit from LAS services by paying an annual fee.")
                return
        else:
            print("Invalid user type. Please enter a valid user type.")
            return
        print(f"User '{self.first_name}' of type '{self.user_type}' has been added to the LAS.")
