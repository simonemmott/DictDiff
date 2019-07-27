from unittest import TestCase
from dictdiff import  apply, add, remove, update, show, _split_path
import logging
import json
logger = logging.getLogger(__name__)
            
            
class ApplyTests(TestCase):
    
    def test_split_path(self):
        self.assertEqual([''], _split_path(''))
        self.assertEqual(['name'], _split_path('name'))
        self.assertEqual(['name', 'attr'], _split_path('name.attr'))
        self.assertEqual(['name', '[0]'], _split_path('name[0]'))
        self.assertEqual(['[0]'], _split_path('[0]'))
        self.assertEqual(['[0]', '[1]'], _split_path('[0][1]'))
        self.assertEqual(['name', '[1]', 'attr'], _split_path('name[1].attr'))
        
    def test_update_empty_dict(self):
        src = {}
        diff = [
            add('name', 'NAME'),
            add('desc', 'DESC'),
        ]
        expected = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        result = apply(src, diff)
        self.assertEqual(expected, result)
        
    def test_update_dict(self):
        src = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        diff = [
            update('name', 'NAME', 'NAME_UPD'),
            add('data', 'DATA'),
        ]
        expected = {
            'name': 'NAME_UPD',
            'desc': 'DESC',
            'data': 'DATA'
        }
        result = apply(src, diff)
        self.assertEqual(expected, result)
        
    def test_update_dict_with_dict(self):
        src = {
            'name': 'NAME',
            'data': {
                'attr': 'ATTR',
                'value': 'VALUE'
            }
        }
        diff = [
            update('name', 'NAME', 'NAME_UPD'),
            update('data.attr', 'ATTR', 'ATTR_UPD'),
            remove('data.value', 'VALUE'),
            add('data.new', 'NEW')
        ]
        expected = {
            'name': 'NAME_UPD',
            'data': {
                'attr': 'ATTR_UPD',
                'new': 'NEW'
            }
        }
        result = apply(src, diff)
        self.assertEqual(expected, result)

    def test_update_dict_with_list_extend(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        diff = [
            update('name', 'NAME', 'NAME_UPD'),
            update('data[0]', 'A', 'A_UPD'),
            add('data[3]', 'D'),
            add('data[4]', 'Z'),
        ]
        expected = {
            'name': 'NAME_UPD',
            'data': ['A_UPD', 'B', 'C', 'D', 'Z']
        }
        result = apply(src, diff)
        self.assertEqual(expected, result)

    def test_update_dict_with_list_reduce(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        diff = [
            update('name', 'NAME', 'NAME_UPD'),
            update('data[0]', 'A', 'A_UPD'),
            remove('data[2]', 'C'),
        ]
        expected = {
            'name': 'NAME_UPD',
            'data': ['A_UPD', 'B']
        }
        result = apply(src, diff)
        self.assertEqual(expected, result)

        