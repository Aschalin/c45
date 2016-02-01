from string import split
import math
import operator


def majorityCnt(classlist):
    classcount = {}
    for vote in classlist:
        if vote not in classcount.keys():
            classcount[vote] = 0
        classcount[vote] += 1
    sortedClassCount = sorted(classcount.iteritems(), key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]


def entropy(dataset):
    n = len(dataset)
    labels = {}
    for record in dataset:
        label = record[-1]
        if label not in labels.keys():
            labels[label] = 0
        labels[label] += 1
    ent = 0.0
    for key in labels.keys():
        prob = float(labels[key]) / n
        ent = -prob * math.log(prob, 2)
    return ent


def splitDataset(dataset, nclom, value):
    retDataSet = []
    for record in dataset:
        if record[nclom] == value:
            reducedRecord = record[:nclom]
            reducedRecord.extend(record[nclom + 1:])
            retDataSet.append(reducedRecord)
    return retDataSet


def chooseBestFeatureToSplit(dataset):
    numberFeature = len(dataset[0]) - 1
    baseEntropy = entropy(dataset)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numberFeature):
        featureList = [x[i] for x in dataset]
        uniqueValues = set(featureList)
        newEntropy = 0.0
        for value in uniqueValues:
            subDataset = splitDataset(dataset, i, value)
            prob = len(subDataset) / float(len(dataset))
            newEntropy += prob * entropy(subDataset)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def buildTree(dataset, labels):
    classlist = [x[-1] for x in dataset]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(classlist) == 1:
        return majorityCnt(classlist)
    bestFeature = chooseBestFeatureToSplit(dataset)
    bestFeatureLabel = labels[bestFeature]
    tree = {bestFeatureLabel: {}}
    del (labels[bestFeature])
    featValues = [x[bestFeature] for x in dataset]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        tree[bestFeatureLabel][value] = buildTree(splitDataset(dataset, bestFeature, value), subLabels)
    return tree


def classify(tree, labels, testvec):
    firstStr = tree.keys()[0]
    secondDict = tree[firstStr]
    featIndex = labels.index(firstStr)
    for key in secondDict.keys():
        if testvec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], labels, testvec)
            else:
                classLabel = secondDict[key]
    try:
        return classLabel
    except:
        return 1


def printTree(tree, tabs):
    if type(tree) is dict:
        for key, value in tree.iteritems():
            for i in range(0, tabs):
                print "\t",
            print key, ":"
            printTree(value, tabs + 1)
    else:
        for i in range(0, tabs):
            print "\t",
        print tree


fs = open("dtree.data")
dataset = []
for line in fs:
    lineSplit = split(line[:-1], "\t")
    #print lineSplit
    dataset.append([float(value) for value in lineSplit])
fs.close()

nfeature = len(dataset[0])
labels = ["att" + str(i) for i in range(1, nfeature)]
labels2 = [x for x in labels]
tree = buildTree(dataset, labels)
printTree(tree, 0)
print "test data"
try:
    fs = open("dtreeTest.data")
    datasetTest = []
    for line in fs:
        lineSplit = split(line[:-1], "\t")
        #print lineSplit
        datasetTest.append([float(value) for value in lineSplit])
    fs.close()

    nPos = 0
    for r in datasetTest:
        ret = classify(tree, labels2, r)
        if ret == r[-1]:
            nPos += 1
    ntest = len(datasetTest)
    print "The pass rate is " + str(nPos / float(ntest))
except:
    pass