from unittest import TestCase
from dictdiff import diff, _added, _removed, _updated, show
import logging
import json
logger = logging.getLogger(__name__)
            
            
class DiffTests(TestCase):
    
    def test_no_difference(self):
        src = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        comp = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        d = diff(src, comp)
        self.assertEqual(0, len(d))
        
    def test_added(self):
        self.assertEqual({'path': 'PATH', 'new_value': 'NEW'}, _added('PATH', 'NEW'))
        
    def test_removed(self):
        self.assertEqual({'path': 'PATH', 'old_value': 'OLD'}, _removed('PATH', 'OLD'))
        
    def test_updated(self):
        self.assertEqual({'path': 'PATH', 'old_value': 'OLD', 'new_value': 'NEW'}, _updated('PATH', 'OLD', 'NEW'))
        
    def test_all_removed(self):
        src = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        comp = {}
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_removed('name', 'NAME') in d)
        self.assertTrue(_removed('desc', 'DESC') in d)
        
    def test_all_new(self):
        src = {}
        comp = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_added('name', 'NAME') in d)
        self.assertTrue(_added('desc', 'DESC') in d)
        
    def test_new_property(self):
        src = {
            'name': 'NAME'
        }
        comp = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_added('desc', 'DESC') in d)
        
    def test_removed_property(self):
        src = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        comp = {
            'name': 'NAME'
        }
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_removed('desc', 'DESC') in d)
        
    def test_updated_property(self):
        src = {
            'name': 'NAME',
            'desc': 'DESC'
        }
        comp = {
            'name': 'NAME_UPD',
            'desc': 'DESC_UPD'
        }
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD') in d)
        self.assertTrue(_updated('desc', 'DESC', 'DESC_UPD') in d)
        
    def test_new_dict(self):
        src = None
        comp = {
            'name': 'NAME_UPD',
            'desc': 'DESC_UPD'
        }
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_added('', {'name': 'NAME_UPD','desc': 'DESC_UPD'}) in d)
        
    def test_delete_dict(self):
        src = {
            'name': 'NAME_UPD',
            'desc': 'DESC_UPD'
        }
        comp = None
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_removed('', {'name': 'NAME_UPD','desc': 'DESC_UPD'}) in d)
        
    def test_new_dict_with_dict(self):
        src = None
        comp = {
            'name': 'NAME_UPD',
            'data': {
                'attr1': 'VALUE_1',
                'attr2': 'VALUE_2'
            }
        }
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_added('', {
            'name': 'NAME_UPD',
            'data': {
                'attr1': 'VALUE_1',
                'attr2': 'VALUE_2'
            }
        }) in d)
        
    def test_update_dict_with_dict(self):
        src = {
            'name': 'NAME',
            'data': {
                'attr1': 'VALUE_1',
                'attr2': 'VALUE_2'
            }
        }
        comp = {
            'name': 'NAME_UPD',
            'data': {
                'attr1': 'VALUE_1_UPD',
                'attr2': 'VALUE_2_UPD'
            }
        }
        d = diff(src, comp)
        self.assertEqual(3, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD' ) in d)
        self.assertTrue(_updated('data.attr1', 'VALUE_1', 'VALUE_1_UPD' ) in d)
        self.assertTrue(_updated('data.attr2', 'VALUE_2', 'VALUE_2_UPD' ) in d)
        
    def test_remove_dict_with_dict(self):
        src = {
            'name': 'NAME_UPD',
            'data': {
                'attr1': 'VALUE_1',
                'attr2': 'VALUE_2'
            }
        }
        comp = None
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_removed('', {
            'name': 'NAME_UPD',
            'data': {
                'attr1': 'VALUE_1',
                'attr2': 'VALUE_2'
            }
        }) in d)
        
    def test_new_dict_with_list(self):
        src = None
        comp = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_added('', {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }) in d)
        
    def test_update_dict_with_list_extend(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        comp = {
            'name': 'NAME_UPD',
            'data': ['A', 'Z', 'Y', 'D']
        }
        d = diff(src, comp)
        self.assertEqual(4, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD' ) in d)
        self.assertTrue(_updated('data[1]', 'B', 'Z' ) in d)
        self.assertTrue(_updated('data[2]', 'C', 'Y' ) in d)
        self.assertTrue(_added('data[3]', 'D' ) in d)
        
    def test_update_dict_with_list_reduce(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        comp = {
            'name': 'NAME_UPD',
            'data': ['A', 'Z']
        }
        d = diff(src, comp)
        self.assertEqual(3, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD' ) in d)
        self.assertTrue(_updated('data[1]', 'B', 'Z' ) in d)
        self.assertTrue(_removed('data[2]', 'C' ) in d)
        
    def test_update_dict_with_list_clear(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        comp = {
            'name': 'NAME_UPD',
            'data': []
        }
        d = diff(src, comp)
        self.assertEqual(4, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD' ) in d)
        self.assertTrue(_removed('data[0]', 'A' ) in d)
        self.assertTrue(_removed('data[1]', 'B' ) in d)
        self.assertTrue(_removed('data[2]', 'C' ) in d)
        
    def test_update_dict_with_list_null(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        comp = {
            'name': 'NAME_UPD',
            'data': None
        }
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD' ) in d)
        self.assertTrue(_updated('data', ['A', 'B', 'C'], None ) in d)
        
    def test_update_dict_with_list_removed(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        comp = {
            'name': 'NAME_UPD',
        }
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD') in d)
        self.assertTrue(_removed('data', ['A', 'B', 'C']) in d)
        
    def test_update_dict_with_list_removed(self):
        src = {
            'name': 'NAME',
            'data': ['A', 'B', 'C']
        }
        comp = {
            'name': 'NAME_UPD',
        }
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD') in d)
        self.assertTrue(_removed('data', ['A', 'B', 'C']) in d)
        
    def test_no_changes_dict_with_list_of_dict(self):
        src = {
            'name': 'NAME',
            'data': [
                {
                    'name': 'NAME_1',
                    'data': 'DATA_1'
                },
                {
                    'name': 'NAME_2',
                    'data': 'DATA_2'
                },
                {
                    'name': 'NAME_3',
                    'data': 'DATA_3'
                }
            ]
        }
        comp = {
            'name': 'NAME',
            'data': [
                {
                    'name': 'NAME_1',
                    'data': 'DATA_1'
                },
                {
                    'name': 'NAME_2',
                    'data': 'DATA_2'
                },
                {
                    'name': 'NAME_3',
                    'data': 'DATA_3'
                }
            ]
        }
        d = diff(src, comp)
        self.assertEqual(0, len(d))
        
    def test_update_dict_with_list_of_dict_reduce(self):
        src = {
            'name': 'NAME',
            'data': [
                {
                    'name': 'NAME_1',
                    'data': 'DATA_1'
                },
                {
                    'name': 'NAME_2',
                    'data': 'DATA_2'
                },
                {
                    'name': 'NAME_3',
                    'data': 'DATA_3'
                }
            ]
        }
        comp = {
            'name': 'NAME_UPD',
            'data': [
                {
                    'name': 'NAME_1_UPD',
                    'data': 'DATA_1_UPD'
                },
                {
                    'name': 'NAME_2',
                    'data': 'DATA_2'
                }
            ]
        }
        d = diff(src, comp)
        self.assertEqual(4, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD') in d)
        self.assertTrue(_updated('data[0].name', 'NAME_1', 'NAME_1_UPD') in d)
        self.assertTrue(_updated('data[0].data', 'DATA_1', 'DATA_1_UPD') in d)
        self.assertTrue(_removed('data[2]', {'name': 'NAME_3','data': 'DATA_3'}) in d)
        
    def test_update_dict_with_list_of_dict_extend(self):
        src = {
            'name': 'NAME',
            'data': [
                {
                    'name': 'NAME_1',
                    'data': 'DATA_1'
                },
                {
                    'name': 'NAME_2',
                    'data': 'DATA_2'
                },
                {
                    'name': 'NAME_3',
                    'data': 'DATA_3'
                }
            ]
        }
        comp = {
            'name': 'NAME',
            'data': [
                {
                    'name': 'NAME_1',
                    'data': 'DATA_1'
                },
                {
                    'name': 'NAME_2',
                    'data': 'DATA_2'
                },
                {
                    'name': 'NAME_3',
                    'data': 'DATA_3'
                },
                {
                    'name': 'NAME_4',
                    'data': 'DATA_4'
                }
            ]
        }
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_added('data[3]', {'name': 'NAME_4','data': 'DATA_4'}) in d)
        
    def test_update_list_extend(self):
        src = ['A', 'B', 'C']
        comp = ['A', 'Z', 'C', 'D']
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_updated('[1]', 'B', 'Z') in d)
        self.assertTrue(_added('[3]', 'D') in d)
        
    def test_update_list_reduce(self):
        src = ['A', 'B', 'C']
        comp = ['A', 'Z']
        d = diff(src, comp)
        self.assertEqual(2, len(d))
        self.assertTrue(_updated('[1]', 'B', 'Z') in d)
        self.assertTrue(_removed('[2]', 'C') in d)
        
    def test_update_value(self):
        src = 'VALUE'
        comp = 'UPDATED'
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_updated('', 'VALUE', 'UPDATED') in d)
        
    def test_new_value(self):
        src = None
        comp = 'VALUE'
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_added('', 'VALUE') in d)
        
    def test_delete_value(self):
        src = 'VALUE'
        comp = None
        d = diff(src, comp)
        self.assertEqual(1, len(d))
        self.assertTrue(_removed('', 'VALUE') in d)
        
    def test_update_list_of_lists(self):
        src = [
            ['A', 'B', 'C'],
            ['X', 'Y', 'Z'],
            ['1', '2', '3'],
        ]
        comp = [
            ['A1', 'B', 'C', 'D'],
            ['X1', 'Y'],
            ['1A', '2', '3'],
            ['D', 'E']
        ]
        d = diff(src, comp)
        self.assertEqual(6, len(d))
        self.assertTrue(_updated('[0][0]', 'A', 'A1') in d)
        self.assertTrue(_added('[0][3]', 'D') in d)
        self.assertTrue(_updated('[1][0]', 'X', 'X1') in d)
        self.assertTrue(_removed('[1][2]', 'Z') in d)
        self.assertTrue(_updated('[2][0]', '1', '1A') in d)
        self.assertTrue(_added('[3]', ['D', 'E']) in d)
        
        
        
        
        
        
        
        
        
        

        