class TaxCalculator:
    def __init__(self):
        self.tax_return = None
        self.total_income = None

    def get_tax(self, tax_return):
        self.tax_return = tax_return
        tax = self.determine_base_tax()
        tax += self.determine_badbob_adjustment()
        return tax

    def determine_badbob_adjustment(self):
        class1 = sum(self.tax_return["badbobs"]["class1"])
        class1_adjustment = class1 /2
        class2 = sum(self.tax_return["badbobs"]["class2"])
        if class2<1001:
            class2_adjustment = 0
        elif class2<10001:
            class2_adjustment = self.total_income * 0.05
        elif class2<50001:
            class2_adjustment = self.total_income * 0.1
        else:
            class2_adjustment = self.total_income * 0.15
        return class1_adjustment + class2_adjustment

    def determine_base_tax(self):
        self.total_income = self.tax_return["income"]["salary"]
        tax = self.total_income * 0.15
        after_tax_income = self.total_income - tax
        if after_tax_income < 30000:
            tax = self.total_income - 30000
        return tax
