import unittest

import bobolia_taxes

tax_50K = 3000


class BoboliaTaxTests(unittest.TestCase):
    def setUp(self):
        self.tax_calculator = bobolia_taxes.TaxCalculator()
        self.tax_return = None

    def make_return(self, args):
        tax_return = {"income": {"salary": 0},
                      "badbobs": {"class1": (),
                                  "class2": ()}}
        if "income" in args:
            tax_return["income"].update(args["income"])
        if "badbobs" in args:
            tax_return["badbobs"].update(args["badbobs"])
        self.tax_return = tax_return

    def make_simple_return(self, salary):
        self.make_return({"income": {"salary": salary}})

    def get_tax(self):
        return self.tax_calculator.get_tax(self.tax_return)

    def test_class_1_badbobs(self):
        self.make_return({"income": {"salary": 50000},
                          "badbobs": {"class1": (100,)}}
                         )
        self.assertEqual(tax_50K + 50, self.get_tax())

    def test_class_2_badbob_purchases_under_1001(self):
        self.make_return({"income": {"salary": 50000},
                          "badbobs": {"class2": (400, 600)}}
                         )
        self.assertEqual(tax_50K, self.get_tax())

    def test_class_2_badbob_purchases_under_10001(self):
        self.make_return({"income": {"salary": 50000},
                          "badbobs": {"class2": (10000,)}}
                         )
        self.assertEqual(tax_50K + 2500, self.get_tax())

    def test_class_2_badbob_purchases_under_50001(self):
        self.make_return({"income": {"salary": 50000},
                          "badbobs": {"class2": (10000, 40000)}}
                         )
        self.assertEqual(tax_50K + 5000, self.get_tax())

    def test_class_2_badbob_purchases_over_50000(self):
        self.make_return({"income": {"salary": 50000},
                          "badbobs": {"class2": (10000, 40000, 1000)}}
                         )
        self.assertEqual(tax_50K + 7500, self.get_tax())

    def test_badbobs_do_not_reduce_after_tax_income_below_20000(self):
        self.make_return({"income": {"salary": 20000},
                          "badbobs": {"class2": (10000,)}}
                         )
        self.assertEqual(0, self.get_tax())

    def test_0_30_tax_bracket(self):
        self.make_simple_return(15000)
        self.assertEqual(0, self.get_tax())
        self.make_simple_return(30000)
        self.assertEqual(0, self.get_tax())

    def test_30_100_tax_bracket(self):
        self.make_simple_return(30001)
        self.assertEqual(0, self.get_tax())
        self.make_simple_return(50000)
        self.assertEqual(tax_50K, self.get_tax())
        self.make_simple_return(100000)
        self.assertEqual(10500, self.get_tax())

    def test_100_250_tax_bracket(self):
        self.make_simple_return(100001)
        self.assertEqual(10500, self.get_tax())
        self.make_simple_return(200000)
        self.assertEqual(30500, self.get_tax())
        self.make_simple_return(250000)
        self.assertEqual(40500, self.get_tax())

    def test_250_500_tax_bracket(self):
        self.make_simple_return(250001)
        self.assertEqual(40500, self.get_tax())
        self.make_simple_return(500000)
        self.assertEqual(115500, self.get_tax())

    def test_500_up_tax_bracket(self):
        self.make_simple_return(500001)
        self.assertEqual(115500, self.get_tax())
        self.make_simple_return(1000000)
        self.assertEqual(315500, self.get_tax())


if __name__ == '__main__':
    unittest.main()
