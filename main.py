from opinionPlot import OpinionPlot
import nltk


###################################################
#                  Main Definition                #
###################################################
def main():
    """ Main """
    op = OpinionPlot("testData.txt")
    op.plotOpinions("Opinions")
    op.plotAvgOpinions("Average Opinions")
    op.plotClusters("Clusters", 3)
    op.showPlots()


##################################################
#                   Call Main                    #
##################################################
if __name__ == '__main__':
    main()