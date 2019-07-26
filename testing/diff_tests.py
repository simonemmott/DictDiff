from unittest import TestCase
from dictdiff import diff, _added, _removed, _updated
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
        print(json.dumps(d, indent=4))
        self.assertEqual(2, len(d))
        self.assertTrue(_updated('name', 'NAME', 'NAME_UPD') in d)
        self.assertTrue(_updated('desc', 'DESC', 'DESC_UPD') in d)
        

        