import csv
import math

class csvReader:

    def __init__(self,fpath):
        self.fpath = fpath
        self.data = []
        self.attribute_list = []
    def read(self):
        myfile = self.fpath
        with open(myfile, 'rb') as csvfile:
            i = 0
            for line in csvfile:
                if (i == 0):
                    self.attribute_list = line.split(',')
                else:
                    self.data.append(line.split(','))
                i = i + 1
        return {'attributes': self.attribute_list, 'data': self.data}

class dataSet:
    def __init__(self, data, attributes, label):
        self.data = data
        self.attributes = attributes
        self.label = label
    def getNumRows(self):
        return len(self.data)
    def getAttributes(self):
        return self.attributes

    def getClassName(self):
        return self.attributes[-1]
    def getClassIndex(self):
        return len(self.attributes) - 1

    def getTuples(self):
        return self.data

    # Returns a new dataset with the given indicies removed
    def pluck(self,indicies):
        newData = []
        newAttributes = []
        for row in self.data:
            newRow = []
            for i in range(len(row)):
                if i not in indicies:
                    newRow.append(row[i])
            newData.append(newRow)
        for i in range(len(self.attributes)):
            if i not in indicies:
                newAttributes.append(self.attributes[i])

        return dataSet(newData,newAttributes,"")

    def pluckName(self, attribute):
        aIndex = self.attributes.index(attribute)
        if aIndex >= 0:
            return self.pluck(aIndex)

    # returns categorizing item

    # categorizes the given index
    def categorize(self, tIndex):
        attr = {}
        cIndex = self.getClassIndex()
        for row in self.data:
            classification = row[cIndex]
            attribute = row[tIndex]
            if attr.get(attribute) == None:
                emptyBranch = {}
                emptyBranch[classification] = 1
                attr[attribute] = {'count': 1, 'classes': emptyBranch}
            else:
                attr[attribute]['count'] += 1
                # print('attr: ',attr[attribute]['classes'])
                if attr[attribute]['classes'].get(classification) == None:
                    attr[attribute]['classes'][classification] = 1
                else:
                    attr[attribute]['classes'][classification] += 1
        return attr

    # The information needed to classify a Tuple
    def gainExpected(self):
        cIndex = self.getClassIndex()
        classes = {}
        totalCount = len(self.getTuples()) + 0.0
        gain = 0.0
        for row in self.data:
            # totalCount += 1
            if row[cIndex] in classes:
                classes[row[cIndex]] += 1
            else:
                classes[row[cIndex]] = 1
        for cName in classes:
            # print('totalCount',totalCount)
            cRatio = (classes[cName]/totalCount)
            # print('cRatio',cRatio)
            coeff = cRatio * (math.log(cRatio,2))
            gain = gain - coeff
            # print('coeff:',coeff)
        return gain
    
    # The gain from an individual attr
    def gainByAttr(self,aIndex):
        aDict = self.categorize(aIndex)
        attrTotal = len(self.getTuples()) + 0.0
        gain = 0
        # print(aDict)
        # print('Total number unique attr',attrTotal)
        for attribute in aDict:
            attrCount = aDict[attribute]['count'] + 0.0
            attrClasses = aDict[attribute]['classes']
            attrRatio = attrCount/attrTotal
            attrCoeff = 0.0
            # print('attr is :',attribute,'count is ',attrCount,' ratio is ', attrRatio)
            # print('the classess are ',attrClasses)
            for cbranch in attrClasses:
                classRatio = attrClasses[cbranch]/attrCount
                classCoeff = classRatio * math.log(classRatio,2)
                attrCoeff = attrCoeff - classCoeff
        return attrCoeff
    
    # main function to determine the attribute that provides the most gain
    def getSplitAttributeByGain(self):
        #Will probably need to check term conditions
        splitting_attrbute_index = -1
        eGain = self.gainExpected()
        gBits = eGain
        # Ignore the classification index
        for i in range(len(self.attributes) - 1):
            aGainBits = self.gainByAttr(i)
            if aGainBits < gBits :
                gBits = aGainBits
                splitting_attrbute_index = i
        return {'expected_gain':eGain,'attribute_gain':gBits,'attribute_index':splitting_attrbute_index}

    # function splits dataset and returns dictionary of datasetObjects based on splitting attribute
    def splitDataOnAttribute(self, aIndex):
        array_collection = {}
        dset_collection = []
        newAttributes = list(self.attributes)
        del newAttributes[aIndex]
        for row in self.data:
            attribute_key = row[aIndex]
            newRow = list(row)
            del newRow[aIndex]
            if attribute_key not in array_collection:
                array_collection[attribute_key] = []
            array_collection[attribute_key].append(newRow)
        for sortedAttribute in array_collection:
            # print(array_collection[sortedAttribute])
            dSet = dataSet(array_collection[sortedAttribute],newAttributes, sortedAttribute)
            # print(dSet.getTuples())
            dset_collection.append(dSet)
        return dset_collection



#######################
#### Output Tests #####
#######################
records = csvReader('../Sources/Adult/adult.csv').read()
adultTest = dataSet(records['data'], records['attributes'],"")
newtest = adultTest.pluck([0,1,2,3,4,5,6,7,8,9,10,11,12])
print(newtest.getAttributes())
# print(newtest.getTuples())
print(newtest.getClassName())
# print(newtest.categorize(1))
gain = newtest.gainExpected()
print(gain)
print(newtest.gainByAttr(1))
print(newtest.getSplitAttributeByGain())
print(newtest.splitDataOnAttribute(1))