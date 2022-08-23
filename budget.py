class Category:
    def __init__(self, category):
        self.category = category
        self.balance = 0
        self.ledger = []

    def deposit(self, amount, description=""):
        amount = float(amount)
        dep = {"amount": amount, "description": description}
        self.ledger.append(dep)
        try:
            self.balance = self.balance + amount
        except:
            self.balance = amount

    def withdraw(self, amount, description=""):
        amount = float(amount)
        if amount < 0:
            amount = amount * (-1)
        if self.balance >= amount:
            wit = {"amount": ((-1) * amount), "description": description}
            self.ledger.append(wit)
            self.balance = self.balance - amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, budgetobj):
        if self.balance >= amount:
            self.withdraw(amount, f"Transfer to {budgetobj.category}")
            budgetobj.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount <= self.balance:
            return True
        else:
            return False

    def __str__(self) -> str:
        how_many_stars = int((30 - len(self.category)) / 2)
        text = "*" * how_many_stars + self.category + "*" * how_many_stars + "\n"
        for item in self.ledger:
            space = len(item["description"][:23])
            if len("{:.2f}".format(item["amount"])) < 7:
                number = " " * (
                    7 - len("{:.2f}".format(item["amount"]))
                ) + "{:.2f}".format(item["amount"])
            else:
                number = "{:.2f}".format(item["amount"])

            text = text + item["description"][:23] + " " * (23 - space) + number + "\n"
        text = text + "Total: " + "{:.2f}".format(self.balance)
        return text
      
def create_spend_chart(categories):
    count = len(categories)
    # Calculate dict with amounts
    total_withdraw = 0
    withdraw_cat_amount = {}
    for category in categories:
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                total_withdraw += transaction["amount"]
                if category.category in withdraw_cat_amount:
                    withdraw_cat_amount[category.category] = (
                        withdraw_cat_amount[category.category] + transaction["amount"]
                    )
                else:
                    withdraw_cat_amount[category.category] = transaction["amount"]
    # Dict with %
    withdraw_cat_percent = {}
    for key, value in withdraw_cat_amount.items():
        withdraw_cat_percent[key] = value / total_withdraw

    # chart
    # top row
    title = "Percentage spent by category\n"

    # List with numbers "{: >3}".format(i) + "|"
    tmp_num = [i for i in range(0, 101, 10)]
    tmp_num.sort(reverse=True)

    # list None + o
    marks = []
    for category in categories:
        mark = []
        inde = int(withdraw_cat_percent[category.category] * 100)
        for i in range(0, 10 + 1):
            if inde >= tmp_num[i]:
                mark.append(" o ")
            else:
                mark.append("   ")
        marks.append(mark)

    # Make graph
    rows = [
        title,
    ]
    for i in range(0, 10 + 1):
        line = (
            "{: >3}".format(tmp_num[i])
            + "|"
            + "".join(map(lambda a: a[i], marks))
            + " \n"
        )
        rows.append(line)

    # line break
    lb = "    " + "-" * count * 3 + "-\n"
    rows.append(lb)
    print("".join(rows))

    # Find biggest category and write them in line
    quantity = 0
    for i in range(count):
        if len(categories[i].category) > quantity:
            quantity = len(categories[i].category)
    cats = []
    for category in categories:
        cat = []
        for i in range(quantity):
            if i < len(category.category):
                cat.append(" {} ".format(category.category[i]))
            else:
                cat.append("   ")
        cats.append(cat)

    # Create lines for categories
    for i in range(quantity):
        line = "    " + "".join(map(lambda a: a[i], cats)) + " \n"
        if i == quantity - 1:
            line = "    " + "".join(map(lambda a: a[i], cats)) + " "
        rows.append(line)
    ans = "".join(rows)
    return ans
  