import xlsxwriter

from gtki_module_exex import mixins
import unittest


class TestCase(unittest.TestCase):
    def test_template_creator(self):
        class TestTemplateCreator(mixins.TemplateCreator):
            workbook = xlsxwriter.Workbook('template_test.xlsx')
            worksheet = workbook.add_worksheet()

        inst = TestTemplateCreator()
        inst.create_template()
        inst.workbook.close()


    def test_data_filler(self):
        class TestDataFiller(mixins.DataFiller):
            workbook = xlsxwriter.Workbook('data_filler.xlsx')
            worksheet = workbook.add_worksheet()
            data_list = (
                ['1', 'В060ХА702', 'Физлицо', 'Физлицо', 100, 50, 50, 'ПО',
                 'Прочее', '2022-05-01 12:00', '2022-05-10 13:00', 'Тест'])

        inst = TestDataFiller()
        inst.create_rows_from_data_list()
        inst.workbook.close()



if __name__ == '__main__':
    unittest.main()
