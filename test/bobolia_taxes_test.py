import unittest

import badbob_adjuster
import tax_bracketter
import tax_calculator

tax_50K = 3000


class BoboliaTaxTests(unittest.TestCase):
    def setUp(self):
        self.tax_bracketter = tax_bracketter.TaxBracketter()
        self.badbob_adjuster = badbob_adjuster.BadBobAdjuster()
        self.tax_calculator = tax_calculator.TaxCalculator(
            self.tax_bracketter, self.badbob_adjuster)
        self.tax_return = None

    def make_return(self, args):
        tax_return_data = {"income": {"salary": 0},
                           "badbobs": {"class1": (),
                                       "class2": ()}}
        if "income" in args:
            tax_return_data["income"].update(args["income"])
        if "badbobs" in args:
            tax_return_data["badbobs"].update(args["badbobs"])
        self.tax_return = tax_calculator.TaxReturn(tax_return_data)

    def make_simple_return(self, salary):
        self.make_return({"income": {"salary": salary}})

    def get_tax(self):
        return self.tax_calculator.get_tax(self.tax_return)

    def assert_tax_with_badbobs(self, income, badbobs, tax):
        self.make_return({"income": {"salary": income},
                          "badbobs": badbobs})
        self.assertEqual(tax, self.get_tax())

    def test_class_1_badbobs(self):
        self.assert_tax_with_badbobs(50000,
                                     {"class1": (100,)},
                                     tax_50K + 50)

    def test_class_2_badbob_purchases_under_1001(self):
        self.assert_tax_with_badbobs(50000,
                                     {"class2": (400, 600)},
                                     tax_50K)

    def test_class_2_badbob_purchases_under_10001(self):
        self.assert_tax_with_badbobs(50000,
                                     {"class2": (10000,)},
                                     tax_50K + 2500)

    def test_class_2_badbob_purchases_under_50001(self):
        self.assert_tax_with_badbobs(50000,
                                     {"class2": (10000, 40000)},
                                     tax_50K + 5000)

    def test_class_2_badbob_purchases_over_50000(self):
        self.assert_tax_with_badbobs(50000,
                                     {"class2": (10000, 40000, 1000)},
                                     tax_50K + 7500)

    def test_badbobs_do_not_reduce_after_tax_income_below_20000(self):
        self.assert_tax_with_badbobs(20000,
                                     {"class2": (10000,)},
                                     0)

    def assert_tax_for(self, income, tax):
        self.make_simple_return(income)
        self.assertEqual(tax, self.get_tax())

    def test_0_30_tax_bracket(self):
        self.assert_tax_for(15000, 0)
        self.assert_tax_for(30000, 0)

    def test_30_100_tax_bracket(self):
        self.assert_tax_for(30001, 0)
        self.assert_tax_for(50000, tax_50K)
        self.assert_tax_for(100000, 10500)

    def test_100_250_tax_bracket(self):
        self.assert_tax_for(100001, 10500)
        self.assert_tax_for(200000, 30500)
        self.assert_tax_for(250000, 40500)

    def test_250_500_tax_bracket(self):
        self.assert_tax_for(250001, 40500)
        self.assert_tax_for(500000, 115500)

    def test_500_up_tax_bracket(self):
        self.assert_tax_for(500001, 115500)
        self.assert_tax_for(1000000, 315500)


if __name__ == '__main__':
    unittest.main()
