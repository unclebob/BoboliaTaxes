class TaxCalculator:
    def __init__(self):
        self.tax_return = None

    def get_tax(self, tax_return):
        self.tax_return = tax_return
        tax = self.determine_base_tax()
        tax += self.determine_badbob_adjustment()
        return tax

    def determine_badbob_adjustment(self):
        return sum(self.tax_return["badbobs"]["class1"]) / 2

    def determine_base_tax(self):
        total_income = self.tax_return["income"]["salary"]        
        tax = total_income * 0.15
        after_tax_income = total_income - tax
        if after_tax_income < 30000:
            tax = total_income - 30000
        return tax
