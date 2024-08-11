import unittest

import bobolia_taxes


def make_return(args):
    tax_return = {"income": {"salary": 0},
                  "badbobs": {"class1": (),
                              "class2": ()}}
    if "income" in args:
        tax_return["income"].update(args["income"])
    if "badbobs" in args:
        tax_return["badbobs"].update(args["badbobs"])
    return tax_return


class BoboliaTaxTests(unittest.TestCase):
    def setUp(self):
        self.tax_calculator = bobolia_taxes.TaxCalculator()

    def test_15pct_tax_rate(self):
        tax_return = make_return({"income": {"salary": 50000}})
        self.assertEqual(7500, self.tax_calculator.get_tax(tax_return))

    def test_no_tax_for_30K_and_below(self):
        tax_return = make_return({"income": {"salary": 30000}})
        self.assertEqual(0, self.tax_calculator.get_tax(tax_return))

    def test_no_after_tax_income_less_than_30K(self):
        tax_return = make_return({"income": {"salary": 30001}})
        self.assertEqual(1, self.tax_calculator.get_tax(tax_return))
        tax_return = make_return({"income": {"salary": 35000}})
        self.assertEqual(5000, self.tax_calculator.get_tax(tax_return))

    def test_class_1_badbobs(self):
        tax_return = make_return({"income": {"salary": 50000},
                                  "badbobs": {"class1": (100,)}}
                                 )
        self.assertEqual(7550, self.tax_calculator.get_tax(tax_return))

    def test_class_2_badbob_purchases_under_1001(self):
        tax_return = make_return({"income": {"salary": 50000},
                                  "badbobs": {"class2": (400, 600)}}
                                 )
        self.assertEqual(7500, self.tax_calculator.get_tax(tax_return))

    def test_class_2_badbob_purchases_under_10001(self):
        tax_return = make_return({"income": {"salary": 50000},
                                  "badbobs": {"class2": (10000,)}}
                                 )
        self.assertEqual(7500 + 2500, self.tax_calculator.get_tax(tax_return))

    def test_class_2_badbob_purchases_under_50001(self):
        tax_return = make_return({"income": {"salary": 50000},
                                  "badbobs": {"class2": (10000,40000)}}
                                 )
        self.assertEqual(7500 + 5000, self.tax_calculator.get_tax(tax_return))

    def test_class_2_badbob_purchases_over_50000(self):
        tax_return = make_return({"income": {"salary": 50000},
                                  "badbobs": {"class2": (10000,40000,1000)}}
                                 )
        self.assertEqual(7500 + 7500, self.tax_calculator.get_tax(tax_return))

    def test_badbobs_do_not_reduce_after_tax_income_below_20000(self):
        tax_return = make_return({"income": {"salary": 20000},
                                  "badbobs": {"class2": (10000,)}}
                                 )
        self.assertEqual(0, self.tax_calculator.get_tax(tax_return))

if __name__ == '__main__':
    unittest.main()
