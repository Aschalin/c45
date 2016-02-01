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


def entropy(data):
    n = len(data)
    labels = {}
    for record in data:
        label = record[-1]
        if label not in labels.keys():
            labels[label] = 0
        labels[label] += 1
    ent = 0.0
    for key in labels.keys():
        prob = float(labels[key]) / n
        ent = -prob * math.log(prob, 2)
    return ent


def splitDataset(data, nclom, value):
    retDataSet = []
    for record in data:
        if record[nclom] == value:
            reducedRecord = record[:nclom]
            reducedRecord.extend(record[nclom + 1:])
            retDataSet.append(reducedRecord)
    return retDataSet


def chooseBestFeatureToSplit(data):
    numberFeature = len(data[0]) - 1
    baseEntropy = entropy(data)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numberFeature):
        featureList = [x[i] for x in data]
        uniqueValues = set(featureList)
        newEntropy = 0.0
        for value in uniqueValues:
            subDataset = splitDataset(data, i, value)
            prob = len(subDataset) / float(len(data))
            newEntropy += prob * entropy(subDataset)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def buildTree(data, labels):
    classlist = [x[-1] for x in data]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(classlist) == 1:
        return majorityCnt(classlist)
    bestFeature = chooseBestFeatureToSplit(data)
    bestFeatureLabel = labels[bestFeature]
    tree = {"Label": bestFeatureLabel}
    del (labels[bestFeature])
    featValues = [x[bestFeature] for x in data]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        tree[value] = buildTree(splitDataset(data, bestFeature, value), subLabels)
    return tree


def classify(tree, labels, record):
    label = tree['Label']
    currentNode = {}
    for key, value in tree.iteritems():
        if not key == 'Label':
            currentNode[key] = value
    currColumn = labels.index(label)
    for key, value in currentNode.iteritems():
        if record[currColumn] == key:
            if type(value) is dict:
                result = classify(value, labels, record)
            else:
                result = value
    try:
        return result
    except:
        return 'error'


def printTree(tree, tabs, tabsDone = True, str = ''):
    if type(tree) is dict:
        for key, value in tree.iteritems():
            if not key == "Label":
                if tabsDone == False:
                    str = "\t\t\t" * tabs
                    str += "\t  "
                    tabsDone = True
                else:
                    str += "-%4s-" % (tree["Label"])
                str += "+-%2s->" % (key)
                printTree(value, tabs + 1, tabsDone, str)
                tabsDone = False

    else:
        print "%s%2s" % (str, tree)


fs = open("dtree.data")
data = []
for line in fs:
    lineSplit = split(line[:-1], "\t")
    data.append([value for value in lineSplit])
fs.close()

nfeature = len(data[0])
labels = ["att" + str(i) for i in range(1, nfeature)]
labels2 = [x for x in labels]
tree = buildTree(data, labels)
printTree(tree, 0)

try:
    fs = open("dtreeTest.data")
    testData = []
    for line in fs:
        lineSplit = split(line[:-1], "\t")
        testData.append([value for value in lineSplit])
    fs.close()

    nPos = 0
    for r in testData:
        ret = classify(tree, labels2, r)
        if ret == r[-1]:
            nPos += 1
    ntest = len(testData)
    print "The pass rate is " + str(nPos / float(ntest))
except:
    pass