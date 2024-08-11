class TaxCalculator:
    def __init__(self):
        self.tax_return = None
        self.total_income = None

    def get_tax(self, tax_return):
        self.tax_return = tax_return
        base_tax = self.determine_base_tax()
        badbob_adujustment = BadBobAdjuster(self).get_adjustment()
        total_tax = base_tax + badbob_adujustment
        after_tax_income = self.total_income - total_tax
        if after_tax_income < 20000:
            total_tax = max(0, self.total_income - 20000)
        return total_tax

    def determine_base_tax(self):
        self.total_income = self.tax_return["income"]["salary"]
        tax = self.total_income * 0.15
        after_tax_income = self.total_income - tax
        if after_tax_income < 30000:
            tax = max (0, self.total_income - 30000)
        return tax


class BadBobAdjuster:
    def __init__(self, tax_calculator):
        self.tax_calculator = tax_calculator

    def get_adjustment(self):
        class1_adjustment = self.class1_adjustment()
        class2_adjustment = self.get_class2_badbob_adjustment()
        return class1_adjustment + class2_adjustment

    def get_class2_badbob_adjustment(self):
        class2 = sum(self.tax_calculator.tax_return["badbobs"]["class2"])
        class2_rate = self.get_class2_rate(class2)

        return class2_rate * self.tax_calculator.total_income

    def get_class2_rate(self, class2):
        class2_rate = 0
        class2_table = ((1001, 0),
                        (10001, 0.05),
                        (50001, 0.1),
                        ("max", 0.15))
        for row in class2_table:
            if row[0] == "max" or class2 < row[0]:
                class2_rate = row[1]
                break
        return class2_rate

    def class1_adjustment(self):
        class1 = sum(self.tax_calculator.tax_return["badbobs"]["class1"])
        return class1 / 2
