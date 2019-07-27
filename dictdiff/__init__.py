import logging
import json
from pip._internal.cli.cmdoptions import src

logger = logging.getLogger(__name__)


def _added(path, new_value):
    return {
        'path': path,
        'new_value': new_value
    }
    
def add(path, new_value):
    return _added(path, new_value)

def _is_add(d):
    return 'new_value' in d and 'old_value' not in d
        
def _removed(path, old_value):
    return {
        'path': path,
        'old_value': old_value
    }
    
def remove(path, old_value):
    return _removed(path, old_value)  

def _is_remove(d):
    return 'old_value' in d and 'new_value' not in d
        
        
def _updated(path, old_value, new_value):
    return {
        'path': path,
        'new_value': new_value,
        'old_value': old_value
    }
    
def update(path, old_value, new_value):
    return _updated(path, old_value, new_value)

def _is_update(d):
    return 'new_value' in d and 'old_value' in d

def _new_value(d):
    return d.get('new_value', None)
        
def _old_value(d):
    return d.get('old_value', None)
        
    
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

def _split_path(path):
    if path == None:
        return path
    if path == '':
        return ['']
    if '.' not in path and '[' not in path:
        return [path]
    paths = []
    item = ''
    for c in path:
        if c == '.':
            if item != '':
                paths.append(item)
            item = ''
            continue
        if c == '[':
            if item != '':
                paths.append(item)
            item = '['
            continue
        item = item+c
    if item != '':
        paths.append(item)
    return paths
        

def _apply_d(src, d):
    path = d['path']
    if path == '':
        return _new_value(d)
    hold = src
    paths = _split_path(path)
    if len(paths) > 1:
        for item in paths[:-1]:
            if item[0] == '[':
                hold = hold[int(item[1:-1])]
            else:
                hold = hold[item]
    item = paths[-1]
    if _is_add(d):
        if item[0] == '[':
            hold.insert(int(item[1:-1]), _new_value(d))
        else:
            hold[item] = _new_value(d)
    elif _is_remove(d):
        if item[0] == '[':
            hold.pop(int(item[1:-1]))
        else:
            del hold[item]
    elif _is_update(d):
        if item[0] == '[':
            hold[int(item[1:-1])] = _new_value(d)
        else:
            hold[item] = _new_value(d)
    else:
        raise Exception('This should not happen!')
    return src         

def apply(src, diff):
    resp = src.copy()
    for d in diff:
        resp = _apply_d(resp, d)
    return resp
        
    
    
    
    
    
    