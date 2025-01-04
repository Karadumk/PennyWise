class Expense:
    def __init__(self, description, category, amount, date) -> None:
        self.description = description
        self.category = category
        self.amount = amount
        self.date = date

    def __repr__(self) -> str:
        return f"<Expense: {self.description}, {self.category} ${self.amount:.2f}, {self.date}>"
