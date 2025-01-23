import json

with open("projects/1072618382.json","r") as file:
    data = json.load(file)
    
numOfSprites = len(data['targets']) #includes the stage as well
blocks_with_no_parent = list()


for i in range(numOfSprites):
    
    def followCodeChain(blockData):
        print(blockData["opcode"])
        if(blockData["next"] == None):
            return
        followCodeChain(data["targets"][i]["blocks"][blockData["next"]])


    blocks = data['targets'][i]['blocks']
    blocks_with_no_parent = list(filter(lambda item: item[1].get("parent") is None, blocks.items()))
    for blockid, blockData in blocks_with_no_parent:
        followCodeChain(blockData)

