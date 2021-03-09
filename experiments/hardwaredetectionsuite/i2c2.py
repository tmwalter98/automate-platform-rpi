import sqlite3
import re


## Use AST-like model to 
splitter_1 = r',|or'
combiner_and = r'&|and'
combiner_range = r'\-'

def combine_codes(codes):
    print(codes)
    
    if(re.search(combiner_and, codes)):
        ns = re.split(combiner_and, codes)
        n0 = int(str.strip(ns[0]), 16)
        n1 = int(str.strip(ns[1]), 16)
        return_set = [n0, n1]
    elif(re.search(combiner_range, codes)):
        range_ = re.split(combiner_range, codes)
        r0 = int(str.strip(range_[0]), 16)
        r1 = int(str.strip(range_[1]), 16)
        return_set = range(r0, r1 + 1)
    else:
        try:
            return_set = [int(str.strip(codes), 16)]
        except ValueError:
            return None    
    return set(return_set)

def split_codes(codes):
    split = re.split(splitter_1, codes)
    return [combine_codes(codes) for codes in split]




model_pattern = r'\("([\w\s/\-]+)", "([!\w\s\-&/\+]+)", \[([\w\s\-&,]+)\]\)'
address_sets = []
with open('i2c.txt') as f:
    for line in f.readlines():
        match = re.findall(pattern=model_pattern, string=line)
        for g in match:
            model, description, codes = g
            for address_set in split_codes(codes):
                address_sets.append((model, description, address_set))


for set in address_sets:
    print(set)

conn = sqlite3.connect('i2c_directory.db')
curr = conn.cursor()


curr.executemany('INSERT INTO address_set_lookup(address, address_set, model, device_type) VALUES (?,?,?,?)', devices)




conn.commit()
            

            