import unittest
from banking_system_impl import BankingSystemImpl


class Level3Tests(unittest.TestCase):
    """
    The test suit below includes 10 tests for Level 3.

    All have the same score.
    You are not allowed to modify this file,
    but feel free to read the source code
    to better understand what is happening in every specific case.
    """

    failureException = Exception


    @classmethod
    def setUp(cls):
        cls.system = BankingSystemImpl()

    def test_level_3_case_01_basic_pay(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 2000), 2000)
        self.assertEqual(self.system.pay(3, 'account1', 100), 'payment1')
        self.assertEqual(self.system.pay(4, 'account1', 200), 'payment2')
        self.assertEqual(self.system.deposit(5, 'account1', 100), 1800)

    def test_level_3_case_02_basic_pay_cashback(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
        self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
        self.assertEqual(self.system.pay(5, 'account1', 100), 'payment1')
        self.assertEqual(self.system.pay(6, 'account2', 200), 'payment2')
        self.assertEqual(self.system.pay(7, 'account2', 300), 'payment3')
        self.assertEqual(self.system.pay(8, 'account1', 400), 'payment4')
        self.assertEqual(self.system.deposit(9, 'account1', 100), 1600)
        self.assertEqual(self.system.deposit(10, 'account2', 100), 600)
        self.assertEqual(self.system.deposit(86400010, 'account1', 100), 1710)
        self.assertEqual(self.system.deposit(86400011, 'account2', 100), 710)

    def test_level_3_case_03_basic_pay_and_get_status_1(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 2000), 2000)
        self.assertEqual(self.system.pay(3, 'account1', 100), 'payment1')
        self.assertEqual(self.system.get_payment_status(4, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(86400002, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(86400003, 'account1', 'payment1'), 'CASHBACK_RECEIVED')

    def test_level_3_case_04_basic_pay_and_get_status_2(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
        self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
        self.assertEqual(self.system.pay(5, 'account1', 100), 'payment1')
        self.assertEqual(self.system.pay(6, 'account2', 200), 'payment2')
        self.assertEqual(self.system.get_payment_status(9, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(10, 'account2', 'payment2'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(86400003, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(86400004, 'account2', 'payment2'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(86400005, 'account1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400006, 'account2', 'payment2'), 'CASHBACK_RECEIVED')

    def test_level_3_case_05_pay_edge_cases(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertEqual(self.system.deposit(2, 'account1', 2000), 2000)
        self.assertEqual(self.system.pay(3, 'account1', 900), 'payment1')
        self.assertIsNone(self.system.pay(4, 'account2', 900))
        self.assertIsNone(self.system.pay(5, 'account1', 1101))
        self.assertEqual(self.system.pay(6, 'account1', 1100), 'payment2')
        self.assertEqual(self.system.pay(86400006, 'account1', 40), 'payment3')
        self.assertEqual(self.system.deposit(86400007, 'account1', 100), 100)

    def test_level_3_case_06_get_payment_status_edge_cases(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
        self.assertEqual(self.system.deposit(4, 'account2', 1000), 1000)
        self.assertEqual(self.system.pay(5, 'account1', 100), 'payment1')
        self.assertEqual(self.system.pay(6, 'account2', 200), 'payment2')
        self.assertEqual(self.system.get_payment_status(9, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertIsNone(self.system.get_payment_status(10, 'account3', 'payment2'))
        self.assertIsNone(self.system.get_payment_status(11, 'account1', 'payment3'))
        self.assertIsNone(self.system.get_payment_status(12, 'account1', 'payment2'))

    def test_level_3_case_07_pay_is_reflected_in_top_spenders(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertTrue(self.system.create_account(3, 'account3'))
        self.assertEqual(self.system.deposit(4, 'account1', 1000), 1000)
        self.assertEqual(self.system.deposit(5, 'account2', 1000), 1000)
        self.assertEqual(self.system.deposit(6, 'account3', 1000), 1000)
        self.assertEqual(self.system.pay(7, 'account2', 100), 'payment1')
        self.assertEqual(self.system.pay(8, 'account2', 100), 'payment2')
        self.assertEqual(self.system.transfer(9, 'account3', 'account1', 100), 900)
        expected = ['account2(200)', 'account3(100)', 'account1(0)']
        self.assertEqual(self.system.top_spenders(10, 3), expected)

    def test_level_3_case_08_all_operations_1(self):
        self.assertTrue(self.system.create_account(1, 'account1'))
        self.assertTrue(self.system.create_account(2, 'account2'))
        self.assertEqual(self.system.deposit(3, 'account1', 2000), 2000)
        self.assertEqual(self.system.pay(4, 'account1', 1000), 'payment1')
        self.assertEqual(self.system.pay(100, 'account1', 1000), 'payment2')
        self.assertIsNone(self.system.get_payment_status(101, 'non-existing', 'payment1'))
        self.assertIsNone(self.system.get_payment_status(102, 'account2', 'payment1'))
        self.assertEqual(self.system.get_payment_status(103, 'account1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.deposit(86400003, 'account1', 100), 100)
        self.assertEqual(self.system.get_payment_status(86400004, 'account1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.deposit(86400005, 'account1', 100), 220)
        self.assertEqual(self.system.deposit(86400099, 'account1', 100), 320)
        self.assertEqual(self.system.deposit(86400100, 'account1', 100), 440)

    def test_level_3_case_09_all_operations_2(self):
        self.assertTrue(self.system.create_account(1, 'acc1'))
        self.assertTrue(self.system.create_account(2, 'acc2'))
        self.assertTrue(self.system.create_account(3, 'acc3'))
        self.assertTrue(self.system.create_account(4, 'acc4'))
        self.assertTrue(self.system.create_account(5, 'acc5'))
        self.assertTrue(self.system.create_account(6, 'acc6'))
        self.assertTrue(self.system.create_account(7, 'acc7'))
        self.assertTrue(self.system.create_account(8, 'acc8'))
        self.assertTrue(self.system.create_account(9, 'acc9'))
        self.assertTrue(self.system.create_account(10, 'acc10'))
        self.assertIsNone(self.system.deposit(11, 'acc0', 7492))
        self.assertEqual(self.system.deposit(12, 'acc1', 5620), 5620)
        self.assertEqual(self.system.deposit(13, 'acc2', 9057), 9057)
        self.assertEqual(self.system.deposit(14, 'acc3', 5323), 5323)
        self.assertEqual(self.system.deposit(15, 'acc4', 9128), 9128)
        self.assertEqual(self.system.deposit(16, 'acc5', 5363), 5363)
        self.assertEqual(self.system.deposit(17, 'acc6', 8896), 8896)
        self.assertEqual(self.system.deposit(18, 'acc7', 8871), 8871)
        self.assertEqual(self.system.deposit(19, 'acc8', 8206), 8206)
        self.assertEqual(self.system.deposit(20, 'acc9', 9165), 9165)
        self.assertEqual(self.system.pay(21, 'acc1', 478), 'payment1')
        self.assertEqual(self.system.pay(22, 'acc2', 443), 'payment2')
        self.assertEqual(self.system.pay(23, 'acc3', 148), 'payment3')
        self.assertEqual(self.system.pay(24, 'acc4', 434), 'payment4')
        self.assertEqual(self.system.pay(25, 'acc5', 168), 'payment5')
        self.assertEqual(self.system.pay(26, 'acc6', 460), 'payment6')
        self.assertEqual(self.system.pay(27, 'acc7', 259), 'payment7')
        self.assertEqual(self.system.pay(28, 'acc8', 357), 'payment8')
        self.assertEqual(self.system.pay(29, 'acc9', 381), 'payment9')
        self.assertIsNone(self.system.pay(30, 'acc10', 314))
        self.assertEqual(self.system.get_payment_status(31, 'acc1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(32, 'acc2', 'payment2'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(33, 'acc3', 'payment3'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(34, 'acc4', 'payment4'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(35, 'acc5', 'payment5'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(36, 'acc6', 'payment6'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(37, 'acc7', 'payment7'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(38, 'acc8', 'payment8'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(39, 'acc9', 'payment9'), 'IN_PROGRESS')
        self.assertIsNone(self.system.get_payment_status(40, 'acc10', 'payment10'))
        expected = ['acc1(478)', 'acc6(460)', 'acc2(443)', 'acc4(434)', 'acc9(381)', 'acc8(357)', 'acc7(259)', 'acc5(168)', 'acc3(148)', 'acc10(0)']
        self.assertEqual(self.system.top_spenders(41, 10), expected)
        self.assertIsNone(self.system.deposit(86400021, 'acc0', 959))
        self.assertEqual(self.system.deposit(86400022, 'acc1', 985), 6136)
        self.assertEqual(self.system.deposit(86400023, 'acc2', 176), 8798)
        self.assertEqual(self.system.deposit(86400024, 'acc3', 467), 5644)
        self.assertEqual(self.system.deposit(86400025, 'acc4', 454), 9156)
        self.assertEqual(self.system.deposit(86400026, 'acc5', 702), 5900)
        self.assertEqual(self.system.deposit(86400027, 'acc6', 921), 9366)
        self.assertEqual(self.system.deposit(86400028, 'acc7', 797), 9414)
        self.assertEqual(self.system.deposit(86400029, 'acc8', 531), 8387)
        self.assertEqual(self.system.deposit(86400030, 'acc9', 496), 9287)
        self.assertEqual(self.system.get_payment_status(86400031, 'acc1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400032, 'acc2', 'payment2'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400033, 'acc3', 'payment3'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400034, 'acc4', 'payment4'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400035, 'acc5', 'payment5'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400036, 'acc6', 'payment6'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400037, 'acc7', 'payment7'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400038, 'acc8', 'payment8'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400039, 'acc9', 'payment9'), 'CASHBACK_RECEIVED')
        self.assertIsNone(self.system.get_payment_status(86400040, 'acc10', 'payment10'))

    def test_level_3_case_10_all_operations_3(self):
        self.assertTrue(self.system.create_account(1, 'acc1'))
        self.assertTrue(self.system.create_account(2, 'acc2'))
        self.assertTrue(self.system.create_account(3, 'acc3'))
        self.assertTrue(self.system.create_account(4, 'acc4'))
        self.assertTrue(self.system.create_account(5, 'acc5'))
        self.assertTrue(self.system.create_account(6, 'acc6'))
        self.assertTrue(self.system.create_account(7, 'acc7'))
        self.assertTrue(self.system.create_account(8, 'acc8'))
        self.assertTrue(self.system.create_account(9, 'acc9'))
        self.assertTrue(self.system.create_account(10, 'acc10'))
        self.assertIsNone(self.system.deposit(11, 'acc0', 6255))
        self.assertEqual(self.system.deposit(12, 'acc1', 6460), 6460)
        self.assertEqual(self.system.deposit(13, 'acc2', 6555), 6555)
        self.assertEqual(self.system.deposit(14, 'acc3', 6648), 6648)
        self.assertEqual(self.system.deposit(15, 'acc4', 7372), 7372)
        self.assertEqual(self.system.deposit(16, 'acc5', 5964), 5964)
        self.assertEqual(self.system.deposit(17, 'acc6', 6559), 6559)
        self.assertEqual(self.system.deposit(18, 'acc7', 8653), 8653)
        self.assertEqual(self.system.deposit(19, 'acc8', 8284), 8284)
        self.assertEqual(self.system.deposit(20, 'acc9', 8832), 8832)
        self.assertEqual(self.system.pay(21, 'acc1', 134), 'payment1')
        self.assertEqual(self.system.pay(22, 'acc2', 493), 'payment2')
        self.assertEqual(self.system.pay(23, 'acc3', 493), 'payment3')
        self.assertEqual(self.system.pay(24, 'acc4', 256), 'payment4')
        self.assertEqual(self.system.pay(25, 'acc5', 425), 'payment5')
        self.assertEqual(self.system.pay(26, 'acc6', 373), 'payment6')
        self.assertEqual(self.system.pay(27, 'acc7', 158), 'payment7')
        self.assertEqual(self.system.pay(28, 'acc8', 211), 'payment8')
        self.assertEqual(self.system.pay(29, 'acc9', 469), 'payment9')
        self.assertIsNone(self.system.pay(30, 'acc10', 205))
        self.assertEqual(self.system.get_payment_status(31, 'acc1', 'payment1'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(32, 'acc2', 'payment2'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(33, 'acc3', 'payment3'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(34, 'acc4', 'payment4'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(35, 'acc5', 'payment5'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(36, 'acc6', 'payment6'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(37, 'acc7', 'payment7'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(38, 'acc8', 'payment8'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(39, 'acc9', 'payment9'), 'IN_PROGRESS')
        self.assertIsNone(self.system.get_payment_status(40, 'acc10', 'payment10'))
        expected = ['acc2(493)', 'acc3(493)', 'acc9(469)', 'acc5(425)', 'acc6(373)', 'acc4(256)', 'acc8(211)', 'acc7(158)', 'acc1(134)', 'acc10(0)']
        self.assertEqual(self.system.top_spenders(41, 10), expected)
        self.assertIsNone(self.system.deposit(86400021, 'acc0', 745))
        self.assertEqual(self.system.deposit(86400022, 'acc1', 313), 6641)
        self.assertEqual(self.system.deposit(86400023, 'acc2', 890), 6961)
        self.assertEqual(self.system.deposit(86400024, 'acc3', 213), 6377)
        self.assertEqual(self.system.deposit(86400025, 'acc4', 519), 7640)
        self.assertEqual(self.system.deposit(86400026, 'acc5', 296), 5843)
        self.assertEqual(self.system.deposit(86400027, 'acc6', 447), 6640)
        self.assertEqual(self.system.deposit(86400028, 'acc7', 875), 9373)
        self.assertEqual(self.system.deposit(86400029, 'acc8', 485), 8562)
        self.assertEqual(self.system.deposit(86400030, 'acc9', 98), 8470)
        self.assertEqual(self.system.get_payment_status(86400031, 'acc1', 'payment1'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400032, 'acc2', 'payment2'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400033, 'acc3', 'payment3'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400034, 'acc4', 'payment4'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400035, 'acc5', 'payment5'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400036, 'acc6', 'payment6'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400037, 'acc7', 'payment7'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400038, 'acc8', 'payment8'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(86400039, 'acc9', 'payment9'), 'CASHBACK_RECEIVED')
        self.assertIsNone(self.system.get_payment_status(86400040, 'acc10', 'payment10'))
        self.assertEqual(self.system.pay(86400041, 'acc1', 286), 'payment10')
        self.assertEqual(self.system.pay(86400042, 'acc2', 365), 'payment11')
        self.assertEqual(self.system.pay(86400043, 'acc3', 225), 'payment12')
        self.assertEqual(self.system.pay(86400044, 'acc4', 483), 'payment13')
        self.assertEqual(self.system.pay(86400045, 'acc5', 194), 'payment14')
        self.assertEqual(self.system.pay(86400046, 'acc6', 386), 'payment15')
        self.assertEqual(self.system.pay(86400047, 'acc7', 392), 'payment16')
        self.assertEqual(self.system.pay(86400048, 'acc8', 290), 'payment17')
        self.assertEqual(self.system.pay(86400049, 'acc9', 249), 'payment18')
        self.assertIsNone(self.system.pay(86400050, 'acc10', 177))
        expected = ['acc2(858)', 'acc6(759)', 'acc4(739)', 'acc3(718)', 'acc9(718)', 'acc5(619)', 'acc7(550)', 'acc8(501)', 'acc1(420)', 'acc10(0)']
        self.assertEqual(self.system.top_spenders(86400051, 10), expected)
        self.assertEqual(self.system.get_payment_status(172800036, 'acc9', 'payment18'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(172800037, 'acc8', 'payment17'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(172800038, 'acc7', 'payment16'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(172800039, 'acc6', 'payment15'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(172800040, 'acc5', 'payment14'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(172800041, 'acc4', 'payment13'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(172800042, 'acc3', 'payment12'), 'IN_PROGRESS')
        self.assertEqual(self.system.get_payment_status(172800043, 'acc2', 'payment11'), 'CASHBACK_RECEIVED')
        self.assertEqual(self.system.get_payment_status(172800044, 'acc1', 'payment10'), 'CASHBACK_RECEIVED')