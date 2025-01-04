from expense import Expense
import calendar
import datetime
import csv
import os

format = "%d/%m/%Y"


def main():
    print("Running expense tracker...")
    expenses_file_path = "expenses.csv"

    # Set the monthly budget
    budget = set_budget()

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new expense")
        print("2. View summary of expenses")
        print("3. Update budget")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            expense = get_user_expense()
            save_expense_to_file(expense, expenses_file_path)
        elif choice == "2":
            summarize_expenses(expenses_file_path, budget)
        elif choice == "3":
            budget = set_budget()
            print(f"New budget set to ${budget:.2f}")
        elif choice == "4":
            print("Exiting expense tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def set_budget():
    budget_file = "budget.txt"
    # Check if the budget file exists
    if os.path.exists(budget_file):
        with open(budget_file, "r") as f:
            try:
                budget = float(f.read().strip())
                print(f"Loaded saved budget: ${budget:.2f}")
                return budget
            except ValueError:
                print("Invalid data in budget file. Resetting budget.")

    # If file doesn't exist or is invalid, ask user to set a budget
    while True:
        try:
            budget = float(input("Please set your monthly budget: "))
            if budget > 0:
                return budget
            else:
                print("Budget must be a positive number. Try again.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_user_expense():
    print("Getting user expense")
    expense_desc = input("Enter expense description: ")
    expense_amount = float(input("Enter expense amount: "))
    # catch date error 
    expense_date = input("Date of expense dd/mm/yyyy: ")
    expense_date = datetime.datetime.strptime(expense_date, format)
     
    expense_categories = ["🍔 Food", "🏠 Home", "✨ Others", "🎉 Fun"]

    while True:
        print("select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"   {i}. {category_name}")

        value_range = f"[0 - {len(expense_categories)}] "
        selected_index = int(input(f"Enter a category number {value_range}: "))

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                description=expense_desc,
                category=selected_category,
                amount=expense_amount,
                date=expense_date,
            )
            return new_expense
        else:
            print("Invalid category !")


def save_expense_to_file(expense: Expense, expenses_file_path):
    print(f"...Saving users expenses: {expense} to {expenses_file_path}")
    with open(expenses_file_path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [expense.description, expense.amount, expense.category, expense.date]
        )


def summarize_expenses(expenses_file_path, budget):
    print("...Summarizing user expenses")
    expenses = []

    if not os.path.exists(expenses_file_path):
        print("No expenses file found. Please add expenses first.")
        return

    with open(expenses_file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 4:
                print(f"Skipping invalid row: {row}")
                continue
            expense_description, expense_amount, expense_category, expense_date = row
            try:
                line_expense = Expense(
                    description=expense_description,
                    category=expense_category,
                    amount=float(expense_amount),
                    date=expense_date,
                )
                expenses.append(line_expense)
            except ValueError:
                print(f"Skipping malformed row: {row}")

    if not expenses:
        print("No valid expenses to summarize.")
        return

    # Calculate expenses by category
    amount_by_category = {}
    for expense in expenses:
        key = expense.category.strip()  # remove trailing or leading whitespaces
        amount_by_category[key] = amount_by_category.get(key, 0) + expense.amount

    print("\nExpenses by category 📉: ")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    # Calculate total spent
    total_spent = sum(expense.amount for expense in expenses)
    print(f"\n💵Total spent: ${total_spent:.2f}")

    # Calculate remaining budget
    remaining_budget = budget - total_spent
    print(f"💵Budget remaining: ${remaining_budget:.2f}")

    # Daily budget calculation
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(pink(f"👌Recommended Daily Budget: ${daily_budget:.2f}"))
    else:
        print("⚠️ No remaining days in the current month to calculate daily budget.")


def pink(text):
    return f"\033[95m{text}\033[0m"


def generate_report(expenses, report_file_path):
    with open(report_file_path, "w") as f:
        f.write("Expense Report\n")
        f.write("=" * 40 + "\n")
        f.write("Expenses by Category:\n")
        amount_by_category = {}
        for expense in expenses:
            amount_by_category[expense.category] = (
                amount_by_category.get(expense.category, 0) + expense.amount
            )
        for category, total in amount_by_category.items():
            f.write(f"  {category}: ${total:.2f}\n")
        f.write("\nTotal Expenses: ${:.2f}\n".format(sum(e.amount for e in expenses)))


if __name__ == "__main__":
    main()
