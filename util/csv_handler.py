import csv 

def csv_to_json(csvFilePath):
    json_list = []
        
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csv_reader = csv.DictReader(csvf) 
            
        for row in csv_reader:             
            json_list.append(row)
    
        return json_list
            