import unittest

from parse import outputing


class Tests(unittest.TestCase):
    def test1(self):
        read_file = open('test1.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('res1.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(result, answer)

    def test2(self):
        read_file = open('test2.txt', 'r')
        text = read_file.read()
        read_file.close()
        result = outputing(text)
        read_file = open('res2.txt', 'r')
        answer = read_file.read()
        read_file.close()
        self.assertEqual(result, answer)

if __name__ == '__main__':
    unittest.main()