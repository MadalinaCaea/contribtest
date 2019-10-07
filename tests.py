from unittest import TestCase
import generate as gen

class Tests(TestCase):
    def test_list_files(self):
        expected_result = [('test/source/contact.rst', 'contact'), ('test/source/index.rst', 'index')]
        actual_result = []
        for el in gen.list_files('test/source'):
             actual_result.append(el)

        self.assertEqual(actual_result,expected_result)

    def test_list_no_rst_file(self):
        expected_result = [('test/source/contact.rst', 'contact'), ('test/source/index.rst', 'index')]
        actual_result = []
        file = open('test/source/text.txt','w')
        f = file.close()
        for el in gen.list_files('test/source'):
            actual_result.append(el)

        self.assertEqual(actual_result, expected_result)

    def test_read_file(self):
        expected_result = ({"title": "Contact us!", "layout": "base.html"},
                           "Write an email to contact@example.com.")
        actual_result = gen.read_file('test/source/contact.rst')

        self.assertEqual(actual_result[0]['title'] , expected_result[0]['title'])
        self.assertEqual(actual_result[0]['layout'], expected_result[0]['layout'])
        self.assertEqual(actual_result[1], expected_result[1])

    def test_read_empty_file(self):
        expected_result = ({},"")
        f = open('empty.rst','w')
        f.write("{}")
        f.close()
        actual_result = gen.read_file('empty.rst')
        self.assertEqual(actual_result[0], expected_result[0])
        self.assertEqual(actual_result[1], expected_result[1])
