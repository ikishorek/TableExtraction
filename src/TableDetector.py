'''
Created on Nov 20, 2012

@author: shriram
'''
from CRF import CRF
import PreProcessor
import PostProcessor
import Trainer
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    xmls = ["Test1","Test2","Test3","Test4", "Test5"] #
    preprocessor = PreProcessor.PreProcessor()
    postprocessor = PostProcessor.PostProcessor()
    trainer = Trainer.Trainer()
    CRF = CRF()

################### CREATE HTMLS TO ANNOTATE ####################
#        for xmlname in xmls:      
#            preprocessedxml = preprocessor.preprocessxml("../TrainingData/xmls/"+ xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
#            trainer.train(preprocessedxml, xmlname)
   

################### TRAIN USING ANNOTATE XMLS ####################
    annotatedxmllist = list()
    for xmlname in xmls:
        fontdict = preprocessor.getFontDictionary(ET.parse("../TrainingData/xmls/"+ xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
        annotatedxml = trainer.readAnnotatedXml('../TrainingData/annotated/' + xmlname +"_annotated")
        annotatedxmllist.append([annotatedxml, fontdict])
    CRF.domaintrain(annotatedxmllist)
    
################### TEST USING TRAINED MODEL ####################
#    predictxmlname = "Test1"
#    predictxmllist = list()
#    fontdict = preprocessor.getFontDictionary(ET.parse("../TrainingData/xmls/"+ predictxmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
#    annotatedxml = trainer.readAnnotatedXml('../TrainingData/annotated/' + predictxmlname +"_annotated")
#    predictxmllist.append([annotatedxml, fontdict])
#    for annotatedxml in predictxmllist:
#        for page in annotatedxml[0]:
#            for col in page:
#                if(len(col) < 2):
#                    continue
#                predicted = CRF.predict(col, annotatedxml[1])
#                for i in xrange(len(predicted)):
#                    if(predicted[i][1].text is not None and predicted[i][1].text.lower().startswith("table")):
#                        print ""
#                        print predicted[i][1].text
#                    elif(predicted[i][0] == SparseType.OTHERSPARSE):
#                        print predicted[i][1].text
                        
################### TEST FOR UNSEEN PDF ####################
    xmlname = '2'          
    fontdict = preprocessor.getFontDictionary(ET.parse("../TestData/"+ xmlname + ".xml"))                  
    preprocessedxml = preprocessor.preprocessxml("../TestData/"+ xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
    alltables = list()
    for page in preprocessedxml:
        for col in page:
            if(len(col) < 2):
                    continue
            predicted = CRF.predict(col, fontdict)
            tables = postprocessor.findTables(predicted)
            if(len(tables) == 0):
                continue
            for t in tables:
                alltables.append(t)
    
    for table in alltables:
        print "============================================="
        for row in table:
            print row
            
    
    
    
    
