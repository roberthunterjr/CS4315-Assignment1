import math

class CSVReader:

    def __init__(self,fpath):
        self.fpath = fpath
        self.data = []
        self.attribute_list = []
        self.markedFields = []
    def read(self,markedFields):
        myfile = self.fpath
        with open(myfile, 'rb') as csvfile:
            # first pass to trim
            newData = []
            for line in csvfile:
                newline = []
                splitLine = line.split(',')
                for i in range(len(splitLine) - 1):
                    if i in markedFields:
                        newline.append(splitLine[i])
                # add classifier filed to new line
                newline.append(splitLine[-1])
                newData.append(newline)
            # Now lines
            self.attribute_list = list(newData[0])
            del newData[0]
            self.data = list(newData)

            # ## Old way
            # i = 0
            # for line in csvfile:
            #     if (i == 0):
            #         self.attribute_list = line.split(',')
            #     else:
            #         self.data.append(line.split(','))
            #     i = i + 1
        return {'attributes': self.attribute_list, 'data': self.data}


# #######################
# #### Output Tests #####
# #######################
# records = CSVReader('../Sources/Adult/adult.csv').read()
# adultTest = dataSet(records['data'], records['attributes'],"")
# newtest = adultTest.pluck([0,1,2,3,4,5,6,7,8,9,10,11,12])
# print(newtest.getAttributes())
# # print(newtest.getTuples())
# print(newtest.getClassName())
# # print(newtest.categorize(1))
# gain = newtest.gainExpected()
# print(gain)
# print(newtest.gainByAttr(1))
# print(newtest.getSplitAttributeByGain())
# print(newtest.splitDataOnAttribute(1))