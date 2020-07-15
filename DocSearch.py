import math
import operator
import numpy as np

# Stores all Unique Words as Keys, Values are where word is in Document
# Therefore builds Dictionary and Inverted Index in One
indexSearch = {}
angleStorage = []
queries = []
relevantDocuments = []

def main():
    # Initial Assignment
    global indexSearch
    indexSearch = readFile("docs.txt",0)
    queries = readFile("queries.txt",1)
    print("Words in dictionary:  " + str(len(indexSearch)))
    # Query Loop
    for query in queries:
        print("Query:  " + query)
        print("Relevant documents: ", end = "")
        angleStorage = []
        # Finds Relevant Documents
        relevantDocuments = querySearch(query,indexSearch)
        for document in relevantDocuments:
            print(document, end = " ")
        print("")
        for document in relevantDocuments:
            # Add Results to Array
            angleStorage.append(str(document) + "," + " %.5f" % calculateAngle(createVectorArray(query,indexSearch,document)))
        # Sort in Order
        tempVal = []
        finalAngles = []
        upper = len(angleStorage)
        # Uses Selection Sort
        while len(finalAngles) != upper:
            pos = 0
            tempVal = angleStorage[0].split(",")
            tempVal = float(tempVal[1])
            lowestValue = tempVal
            for i in range(len(angleStorage)):
                #Find Lowest Value
                tempVal = angleStorage[i].split(",")
                tempVal = float(tempVal[1])
                if tempVal < lowestValue:
                    lowestValue = tempVal
                    pos = i
            finalAngles.append(angleStorage[pos])
            del angleStorage[pos]
        # Print Formatted
        for angles in finalAngles:
            tempVal = angles.split(",")
            print(tempVal[0] + " " + tempVal[1])

def chomp(line):
    return map(operator.methodcaller('rstrip', '\r\n'), line)

def readFile(filePath,option):
    temp = {}
    file = open(filePath,'r')
    idDoc = 0
    if option == 0:
        storage = {}
    else:
        storage = []
    # Read Each Line
    for line in chomp(file):
        start = True
        line = line.replace("\t"," ")
        idDoc += 1
        if option == 0:
            line = line.split()
            for word in line:
                # Create Index
                if storage.get(word):
                    # Existing Word
                    temp = storage.get(word)
                    if temp.get(idDoc):
                        storage[word][idDoc] += 1
                    else:
                    #New Word
                        temp[idDoc] = 1
                        storage[word] = temp
                else:
                    # New Word
                    storage[word] = {idDoc: 1}
        else:
            # Creates Query Array
            storage.append(line)
    file.close()
    return storage

def querySearch(query,index):
    foundDocuments = []
    keys = []
    multipleQuery = query.split(" ")
    counter = -1
    # Load any and all Documents into Array
    for query in multipleQuery:
        counter += 1
        foundDocuments.append([])
        if query in index:
            keys = index[query]
            for key in keys:
                foundDocuments[counter].append(key)
    # Perform Intersection if multiple word query
    for i in range(1, len(foundDocuments)):
        foundDocuments[0] = intersection(foundDocuments[0],foundDocuments[i])

    foundDocuments = foundDocuments[0]
    return foundDocuments

def intersection(A,B):
    intersect = []
    for elementA in A:
        for elementB in B:
            if elementB == elementA and (elementB not in (intersect) or elementA not in (intersect)):
                intersect.append(elementB)
                break
    return intersect

def calculateAngle(arr):
    a = arr[0]
    b = arr[1]
    normA = np.linalg.norm(a)
    normB = np.linalg.norm(b)
    cosTheta = np.dot (a,b) / (normA * normB)
    theta = math.degrees(math.acos(cosTheta))
    return theta

def createVectorArray(query,index,docID):
    # Split Query
    arr = []
    queries = query.split(" ")
    innerDict = {}
    counter = 0
    A = np.zeros((len(index),), dtype=int) #A is Query
    B = np.zeros((len(index),), dtype=int) #B is Document
    for key in index:
        innerDict = index[key]
        for query in queries:
            if key == query:
                A[counter] = 1
        if innerDict.get(docID):
            B[counter] = innerDict[docID]
        counter += 1
    arr.append(A)
    arr.append(B)
    return arr

main()
