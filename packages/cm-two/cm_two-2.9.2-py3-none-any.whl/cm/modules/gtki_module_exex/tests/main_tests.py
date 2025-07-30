from gtki_module_exex import main
import unittest
from wsqluse.wsqluse import Wsqluse


class TestCase(unittest.TestCase):
    data_list = (
        ['1', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
        ['2', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
        ['3', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
        ['4', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
        ['5', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
        ['6', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
        ['7', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
        ['8', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
         'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'],
    )

    @unittest.SkipTest
    def test_create_excel(self):
        inst = main.CreateExcel('main_test.xls', self.data_list)
        inst.create_document()

    @unittest.SkipTest
    def tests_create_acts_excel(self):
        amount_info = 'Итого 5000 (3 взвешивания)'
        inst = main.CreateExcelActs('main_acts.xls', self.data_list,
                                    amount_info)
        inst.create_document()


    def tests_creat_daily_report(self):
        inst = main.CreateExcelDailyReport('ishb_daily_new.xls',
                                           ar_port=52250,
                                           ar_ip="localhost")
        inst.create_document()

if __name__ == '__main__':
    unittest.main()
