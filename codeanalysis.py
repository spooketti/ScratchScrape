import json

with open("projects/1072618409.json","r") as file:
    data = json.load(file)
    
numOfSprites = len(data['targets']) #includes the stage as well
blocks_with_no_parent = list()

logicComplexity = {"repeat":0, #
                   "variables":0,
                   "functions":0,
                   "conditionals":0,
                   "arithmetic":0,
                   "comparison":0, # < > =
                   "complexMath":0, #anything in the menu that lets you do cos sin atan etc
                   "scriptCount":0} #defined by how many blocks have no parents (start of a script)

for i in range(numOfSprites):
    
    def followCodeChain(blockData):
        if(blockData["opcode"] in ["control_repeat","control_repeat_until"] ):
            logicComplexity["repeat"] += 1
        #i dont know how to find functions so u can have fun james
        
        if(blockData["opcode"] in ["control_if", "control_if_else"]):
            logicComplexity["conditionals"] += 1
            
        if(blockData["opcode"] in ["operator_add", "operator_subtract", "operator_multiply", "operator_divide"]):
            logicComplexity["arithmetic"] += 1
        
        if(blockData["opcode"] in ["operator_equals", "operator_lt", "operator_gt"]):
            logicComplexity["comparison"] += 1
            
        if(blockData["opcode"] in ["operator_mathop"]):
            logicComplexity['complexMath'] += 1
        
        # followCodeChain(data["targets"][i]["blocks"][blockData["next"]])
        
    logicComplexity["variables"] += len(data["targets"][i]["variables"])

    blocks = data['targets'][i]['blocks']
    print(data["targets"][i]["name"])
    
    blocks_with_no_parent = list(filter(lambda item: item[1].get("parent") is None, blocks.items()))
    logicComplexity["scriptCount"] += len(blocks_with_no_parent)
    
    for i in blocks:
        followCodeChain(blocks[i])
print(logicComplexity)

import matplotlib.pyplot as plt

plt.bar(range(len(logicComplexity)), list(logicComplexity.values()), align='center')
plt.xticks(range(len(logicComplexity)), list(logicComplexity.keys()))
plt.title("Scratch User Project Complexity")
plt.show()
