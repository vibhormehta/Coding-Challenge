#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 22:32:03 2020

@author: vib
"""
import csv
import time
import collections

class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    def index_document(self, document, school_name, location):
        terms = document['text'].split(' ')
        term_to_docs_dict = dict()
        for term in terms:
            doc_ids = term_to_docs_dict.get(term, [])
            doc_ids.append(document['id'])
            term_to_docs_dict[term] = doc_ids

        # Update the inverted index
        update_dict = {
            key: doc_ids if key not in self.index
            else self.index[key] + doc_ids for (key, doc_ids) in term_to_docs_dict.items()}

        self.index.update(update_dict)
        # Add the document into the database
        self.db.update({document['id']: '{}\n{}'.format(school_name, location)})
        return document

    def lookup(self, query):
        return {term: self.index[term] for term in query.split(' ') if term in self.index}


def load(index):
    start_ts = time.time()
    input_file = 'school_data.csv'
    i = 0

    with open(input_file, 'rt', encoding='cp1252') as f:
        reader = csv.reader(f)
        for row in reader:

            doc = {
                'id': i,
                'text': " ".join([row[3], row[4], STATES.get(row[5], '')]).lower()
            }
            index.index_document(doc, row[3], "{}, {}".format(row[4], row[5]))
            i += 1

    print("Took {} s".format(time.time() - start_ts))
    return index

def search_schools(word):
    start_ts = time.time()    
    word = word.lower()
    start_ts = time.time()
    result = index.lookup(word)

    ll = []
    for ids in result.values():
        ll.extend(ids)

    counter = collections.Counter(ll)
    most_common = counter.most_common(3)
    #print(most_common)
    print("\nResults for {} (search took: {} s)".format(word, time.time() - start_ts))
    for i, c in enumerate(most_common, 1):
        document = db.get(c[0], None)
        print('{}.{}'.format(i, document))
    print("Took {} s".format(time.time() - start_ts))        
    
class load_csv:    
    input_file_location = 'school_data.csv'        
    def load(input=input_file_location):        
        with open(input,'rt',encoding='cp1252') as f:
            reader = csv.reader(f)    
            line_count = 0
            lookup = {}
            try:
                for row in reader:
                    if line_count == 0:
                        print(f'File loaded. Column names are {", ".join(row)}')
                        variables = row
                        line_count+=1
                    else:                                                
                        lookup[line_count] = {variable:value for variable, value in zip(variables,row)}
                        line_count += 1                
            except UnicodeDecodeError as e:
                print('error during decoding: ',e.reason, e.object)         
            print('Total lines loaded: ',line_count)
            return lookup
            

class counts:
    def print_counts(lookup=load_csv.load()):
        schools_set = set(lookup[i]['NCESSCH']for i in range(1,len(lookup)))
        cities_set = set(lookup[i]['LCITY05']for i in range(1,len(lookup)))
        mlocale_set = set(lookup[i]['MLOCALE']for i in range(1,len(lookup)))
        states_set = set(lookup[i]['LSTATE05']for i in range(1,len(lookup)))
        
        print('How many total schools are in this data set? \n Unique schools count is ',len(schools_set),'\n')    
        
        print('How many schools are in each state?')
        for state in states_set:
            unique_schools = set()
            for i in range(1,len(lookup)):
                if lookup[i]['LSTATE05']==state:
                    unique_schools.add(lookup[i]['NCESSCH'])
            print(STATES[state],':', len(unique_schools))

        print('How many schools are in each Metro-centric locale?\n')                            
        for locale in sorted(mlocale_set):
            unique_schools = set()
            for i in range(1,len(lookup)):
                if lookup[i]['MLOCALE']==locale:
                    unique_schools.add(lookup[i]['NCESSCH'])                
            print(locale,':', len(unique_schools))
        
        print('What city has the most schools in it? How many schools does it have in it?')
        max_schools = 0
        number_of_schools = 0
        for city in sorted(cities_set):
            unique_schools = set()
            for i in range(1,len(lookup)):
                if lookup[i]['LCITY05']==city:
                    unique_schools.add(lookup[i]['NCESSCH'])
                    number_of_schools = len(unique_schools)
                    if number_of_schools > max_schools:
                        max_schools = number_of_schools
                        max_schools_city = city
        print('city with most schools in it is ',max_schools_city,'with ',max_schools,'schools')
        
        print('How many unique cities have at least one school in it?')
        ncities_at_least_1_schl = 0    
        for city in sorted(cities_set):
            unique_schools = set()
            for i in range(1,len(lookup)):
                if lookup[i]['LCITY05']==city:
                    unique_schools.add(lookup[i]['NCESSCH'])
            if len(unique_schools)>1:
                ncities_at_least_1_schl +=1   
        print('Unique Cities with at least one school:', ncities_at_least_1_schl)
        

STATES = {
     'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California',
     'CO': 'Colorado','CT': 'Connecticut','C': 'District of Columbia','DC': 'District of Columbia',
     'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa',
     'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'MD': 'Maryland', 'NV': 'Nevada',
     'OH': 'Ohio', 'OR': 'Oregon'
 }


if __name__ == '__main__':
    # Counts:
    count_schools = counts()
    counts.print_counts()    
    # Search Test Cases:
    db = dict()
    index = InvertedIndex(db)
    rows = load(index)
    print('Test Cases: \n')    
    search_schools("elementary school highland park")
    search_schools("jefferson belleville")
    search_schools("riverside school 44")
    search_schools("granada charter school")
    search_schools("foley high alabama")
    search_schools("KUSKOKWIM")  