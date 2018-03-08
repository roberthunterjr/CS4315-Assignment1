from dataset import dataSet
from anytree import Node, RenderTree
from reader import csvReader

class decisionTree:

    # initialize the tree with the dataSet as the root
    def __init__(self, rootSet):
        self.rootNode = Node(rootSet.getLabel())
        
    
    def printTree(self):
        for pre, fill, node in RenderTree(self.rootNode):
            print('%s%s' % (pre, node.name))
    

records = csvReader('../Sources/Adult/adult.csv').read()
recordSet = dataSet(records['data'], records['attributes'], 'root')
testTree = decisionTree(recordSet)
testTree.printTree()