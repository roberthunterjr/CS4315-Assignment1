from dataset import dataSet
from anytree import Node, RenderTree
from reader import CSVReader

class decisionTree:

    # initialize the tree with the dataSet as the root
    def __init__(self, rootSet):
        self.rootNode = Node(rootSet.getLabel())
        self.rootSet = rootSet
    
    def printTree(self):
        for pre, fill, node in RenderTree(self.rootNode):
            print('%s%s' % (pre, node.name))
    
    def generateBranches(self, currentDataSet, parentNode):
        if currentDataSet.isLeaf():
            # print('Is leaf')
            Node(currentDataSet.getLabel() + 'Leaf', parent=parentNode)
        # Start splitting tree and recursing
        else:
            splitting_attribute_index = currentDataSet.getSplitAttributeByGain()['attribute_index']
            split_data = currentDataSet.splitDataOnAttribute(splitting_attribute_index)
            for branch in split_data:
                nodeLabel = branch.getLabel()
                # nodeLabel = 'hey'
                newNode = Node(nodeLabel, parent=parentNode)
                self.generateBranches(branch, newNode)
    def runTree(self):
        self.generateBranches(self.rootSet, self.rootNode)
        self.printTree()
records = CSVReader('../Sources/Adult/adult.csv').read([1,3,4,5,6,7,8])
print(records)
recordSet = dataSet(records['data'], records['attributes'], 'root')
testTree = decisionTree(recordSet)
testTree.runTree()