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
    def runTree(self):
        self.generateBranches(self.rootSet, self.rootNode)
        self.printTree()
records = CSVReader('../Sources/Adult/adult.csv').read()
recordSet = dataSet(records['data'], records['attributes'], 'root')
testTree = decisionTree(recordSet)
testTree.runTree()