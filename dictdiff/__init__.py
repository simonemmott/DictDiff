import logging
import json

logger = logging.getLogger(__name__)


def _added(path, new_value):
    return {
        'path': path,
        'new_value': new_value
    }    
        
def _removed(path, old_value):
    return {
        'path': path,
        'old_value': old_value
    }    
        
def _updated(path, old_value, new_value):
    return {
        'path': path,
        'new_value': new_value,
        'old_value': old_value
    }  
    
def _dict_diff(path, src, comp):
    path = path+'.' if len(path) > 0 else path
    d = []
    found_keys = []
    for key, value in src.items():
        if key in comp:
            found_keys.append(key)
            d.extend(diff(value, comp[key], path=path+key))
        else:
            d.append(_removed(path+key, value))
    for key in comp.keys()-found_keys:
        d.append(_added(path+key, comp[key]))
    return d

def _list_diff(path, src, comp): 
    d = []
    len_src = len(src)
    len_comp = len(comp)
    length = len_src if len_src >= len_comp else len_comp
    for index in range(length):
        if index < len_src and index < len_comp:
            d.extend(diff(src[index], comp[index], path=path+'['+str(index)+']'))
        elif index >= len_src and index < len_comp:
            d.append(_added(path+'['+str(index)+']', comp[index]))
        elif index < len_src and index >= len_comp:
            d.append(_removed(path+'['+str(index)+']', src[index]))
        else:
            raise Exception('This should not happen')
    return d
    
def show(src):
    print(json.dumps(src, indent=4))
        

def diff(src, comp, **kw):
    path = kw.get('path', '')
    if src != None and comp == None:
        if path == '':
            return [_removed(path, src)]
        return [_updated(path, src, comp)]
    if src == None and comp != None:
        if path == '':
            return [_added(path, comp)]
        return [_updated(path, src, comp)]
    if src == None and comp == None:
        return []
    if isinstance(src, dict):
        if not isinstance(comp, dict):
            return [_updated(path, src, comp)]
        return _dict_diff(path, src, comp)   
    if isinstance(src, list): 
        if not isinstance(comp, list):
            return [_updated(path, src, comp)]
        return _list_diff(path, src, comp)
    if src != comp:
        return [_updated(path, src, comp)]
    return []

def apply(src, diff):
    pass
    
    
    
    
    
    