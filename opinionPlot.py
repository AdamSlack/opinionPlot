import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from cvProcessor import CVProcessor

##################################################
#               Opinion Plot Class               #
##################################################
class OpinionPlot:

    def __init__(self, filePath):
        self.people = self.readFile(filePath)
        self.avgPoints = self.compileAvgPoints()
        self.clusters = []
        self.cvp = CVProcessor(filePath) # CV Tests
        for i in range(0, len(self.people)):
            self.people[i].additionalLabel = "Word Count: " + str(self.cvp.CVs[i].wordCount)

    def readFile(self, filePath):
        """ Reads file at specified location, populating opinion plot with People """
        f = open(filePath)
        ppl = []
        for l in f:
            l = l.strip(('\n'))
            strCoords = l.split(' ')
            pName = strCoords[0]
            points = []
            for i in range(1, len(strCoords)):
                coords = strCoords[i].split(',')
                p = []
                p.append(float(coords[0]))
                p.append(float(coords[1]))
                points.append(p)
            ppl.append(Person(pName, points))
        return ppl

    def compileAvgPoints(self):
        """ Creates a list of each person's average point. """
        avg = []
        for p in self.people:
            avg.append(p.avgPoint)
        return avg

    def calcColour(self, pos, max, min):
        """ Calculates the colour that should be used based on the position provided."""
        r = 0
        g = 0

        x = pos[0]
        y = pos[1]

        t = x + y

        if t > 0:
            g = 1
            r = 1 - t / max
        elif t < 0:
            r = 1
            g = 1 + t / min

        b = 0.0
        return r, g, b

    def addOriginLines(self):
        """ Adds lines through Origin on specified plot"""
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')

    def plotOpinions(self, figNum):
        """ Plots Each person onto the specified figure """
        for p in self.people:
            self.plotPerson(p, figNum)
        self.addOriginLines()

    def plotPerson(self, person, figNum):
        """ Plots specified person on specified figure """
        plt.figure(figNum)
        points = person.coordinates
        name = person.name
        xs = []
        ys = []
        for p in points:
            xs.append(p[0])
            ys.append(p[1])

        xs.append(xs[0])
        ys.append(ys[0])

        avg = person.avgPoint

        col = self.calcColour(avg, 20, 20)

        plt.plot(xs, ys, c=col)
        plt.plot(avg[0], avg[1], 'o', c=col)
        plt.annotate(name + " " + person.additionalLabel, (avg[0], avg[1]))

    def plotAvgOpinions(self, figNum):
        """ Plot the average opinions for each entity """
        plt.figure(figNum)
        self.addOriginLines()
        for p in self.people:
            self.plotPersonAvg(p)

    def plotPersonAvg(self, person):
        """ Plots the average opinion of a specified person """
        avg = person.avgPoint
        name = person.name
        col = self.calcColour(avg, 20, 20)

        plt.plot(avg[0], avg[1], 'o', c=col)
        plt.annotate(name + " " + person.additionalLabel, (avg[0], avg[1]))

    def plotClusters(self, figNum, clusterNum):
        """ Performs K-Means Clustering on the average opinions of each entity"""
        # K Means clustering...
        if clusterNum > 6:
            clusterNum = 6

        # Converting to np array for scikit
        npPoints = self.avgPoints

        # Configuring K-Means Object
        kmeans = KMeans(n_clusters=clusterNum, n_init=1, init='random')

        # Performing the Clustering
        kmeans.fit(npPoints)

        # sorting out the centoids held by K-Means object
        cx = []
        cy = []
        for c in kmeans.cluster_centers_:
            cx.append(c[0])
            cy.append(c[1])

        # Plotting K-Means centoids
        plt.figure(figNum)
        self.addOriginLines()

        cols = [(1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (1, 1, 0),
                (1, 0, 1),
                (0, 1, 1)]

        # Linking Point on graph to it's cluster
        centoidID = kmeans.predict(npPoints)

        # Plotting Points and link to cluster.
        for i in range(0, len(npPoints)):
            col = cols[centoidID[i]]

            xs = []
            ys = []

            # Plotting and annotating Point
            xs.append(self.avgPoints[i][0])
            ys.append(self.avgPoints[i][1])
            plt.plot(xs, ys, 'o', c=col)
            plt.annotate(self.people[i].name, (xs[0], ys[0]))

            # plotting the link to the cluster.
            xs.append(cx[centoidID[i]])
            ys.append(cy[centoidID[i]])
            plt.plot(xs, ys, c=col)

        # Plotting the actual cluster point.
        plt.plot(cx, cy, 'x', c=(0, 0, 0))

    def showPlots(self):
        """ Displays all plots created"""
        plt.show()


##################################################
#                  Person Class                  #
##################################################
class Person:

    def __init__(self, name, points, label=""):
        self.name = name
        self.coordinates = points
        self.avgPoint = self.calcAvg()
        self.additionalLabel = str(label)

    def calcAvg(self):
        xs = []
        ys = []
        avg = []
        for c in self.coordinates:
            xs.append(c[0])
            ys.append(c[1])
        avg.append(np.mean(xs))
        avg.append(np.mean(ys))
        return avg





