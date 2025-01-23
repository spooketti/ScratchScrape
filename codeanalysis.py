import json

with open("projects/1072618382.json","r") as file:
    data = json.load(file)
    
somedataidk = len(data['targets'])
blocks_with_no_parent = list()

for i in range(somedataidk):
    blocks = data['targets'][i]['blocks']
    blocks_with_no_parent += list(filter(lambda item: item[1].get("parent") is None, blocks.items()))

for blockid, blockData in blocks_with_no_parent:
    print(blockData)
