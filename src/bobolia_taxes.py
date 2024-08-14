class TaxCalculator:
    def __init__(self):
        self.tax_return = None
        self.total_income = None

    def get_tax(self, tax_return):
        self.tax_return = tax_return
        base_tax = self.determine_base_tax()
        badbob_adjustment = BadBobAdjuster(self).get_adjustment()
        total_tax = base_tax + badbob_adjustment
        after_tax_income = self.total_income - total_tax
        if after_tax_income < 20000:
            total_tax = max(0, self.total_income - 20000)
        return total_tax

    def determine_base_tax(self):
        tax_brackets = ((30000, 0),
                        (100000, .15),
                        (250000, .20),
                        (500000, .30),
                        (None, .40))

        self.total_income = self.tax_return["income"]["salary"]

        previous_maximum = 0
        offset = 0
        for maximum, rate in tax_brackets:
            if maximum is None or self.total_income <= maximum:
                return round(rate * (self.total_income - previous_maximum) + offset)
            else:
                offset = (maximum - previous_maximum) * rate + offset
                previous_maximum = maximum


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
