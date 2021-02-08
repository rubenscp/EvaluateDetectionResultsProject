"""
Project: Creates the the train, valid and test datasets to use in the Yolo neural network.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 24/01/2021
Version: 1.0.0
"""

# Importing needed libraries

import os
import pathlib
import shutil

from random import randrange
from datetime import datetime
from Entity.BoundingBox import BoundingBox
from Entity.ObjectClassEnum import ObjectClassEnum

# ###########################################
# Constants
# ###########################################
LINE_FEED = '\n'


# ###########################################
# Application Methods
# ###########################################


# ###########################################
# Methods of Level 1
# ###########################################


# evaluate detection results
def evaluateDetectionResults(inputImagesDetectionsFullPath, inputImagesAnnotationsPath, evaluationPathAndFile):
    # removing and creating the evaluation file
    if os.path.exists(evaluationPathAndFile):
        os.remove(evaluationPathAndFile)

    # creating the evaluatin results file
    evaluationDetectionResultsFile = open(evaluationPathAndFile, 'a+')

    # configuring header
    line = 'image name' \
           + ';annotated object class' \
           + ';detected object in the correct position and class' \
           + ';confidence' \
           + ';detected object in the correct position and diferent class' \
           + ';others objects' \
           + ';result' \
           + LINE_FEED

    # write line
    evaluationDetectionResultsFile.write(line)

    # close file
    evaluationDetectionResultsFile.close()

    for fileName in os.listdir(inputImagesDetectionsFullPath):
        # print(fileName)
        print('------------------------------------------------------')

        # check if file is an image or not
        if fileName.lower().find('jpg') == -1 and fileName.lower().find('jpeg') == -1:
            continue

        # get jpeg position
        jpegPosition = -1
        jpegPosition = fileName.find('jpg')
        if jpegPosition == -1: jpegPosition = fileName.find('jpeg')
        if jpegPosition == -1: jpegPosition = fileName.find('JPG')
        if jpegPosition == -1: jpegPosition = fileName.find('JPEG')

        # get only image name
        imageName = fileName[:jpegPosition - 1]

        print(imageName)

        # getting the list of detected objects
        detectionLogFileName = inputImagesDetectionsFullPath + imageName + '-detection-log.txt'
        detectedObjectsList = getDetectedObjectsList(detectionLogFileName, imageName)

        # getting the list of annotated objects
        annotatedObjectsList = getAnnotatedObjectsList(inputImagesAnnotationsPath, imageName)

        # evaluating the results
        evaluateResultsOfImage(imageName, detectedObjectsList, annotatedObjectsList, evaluationPathAndFile)

    # close file
    # evaluationDetectionResultsFile.close()


# # evaluate detection results
# def evaluateDetectionResults(logDectionPathAndFile, inputImagesAnnotationsPath, evaluationPathAndFile):
#     # removing and creating the evaluation file
#     if os.path.exists(evaluationPathAndFile):
#         os.remove(evaluationPathAndFile)
#
#     # creating the evaluatin results file
#     evaluationDetectionResultsFile = open(evaluationPathAndFile, 'a+')
#
#     # configuring header
#     line = 'image name' \
#            + ';annotated object class' \
#            + ';detected object in the correct position and class' \
#            + ';detected object in the correct position and diferent class' \
#            + ';others objects' \
#            + ';result' \
#            + LINE_FEED
#
#     # write line
#     evaluationDetectionResultsFile.write(line)
#
#     # close file
#     evaluationDetectionResultsFile.close()
#
#     # open log detection file
#     logDetectionFile = open(logDectionPathAndFile, "r")
#
#     # reading next line
#     line = logDetectionFile.readline()
#
#     # processing the file
#     while line != '':
#
#         # looking for image name (jpg)
#         if line.lower().find('jpg') == -1 and line.lower().find('jpeg') == -1:
#             line = logDetectionFile.readline()
#             continue
#
#         # get jpeg position
#         jpegPosition = -1
#         jpegPosition = line.find('jpg')
#         if jpegPosition == -1: jpegPosition = line.find('jpeg')
#         if jpegPosition == -1: jpegPosition = line.find('JPG')
#         if jpegPosition == -1: jpegPosition = line.find('JPEG')
#
#         # get only the image name
#         imageName = line[5:jpegPosition - 1]
#
#         print('')
#         print(imageName)
#
#         # getting the list of detected objects
#         detectedObjectsList = getDetectedObjectsList(logDetectionFile, imageName)
#
#         # getting the list of annotated objects
#         annotatedObjectsList = getAnnotatedObjectsList(inputImagesAnnotationsPath, imageName)
#
#         # evaluating the results
#         evaluateResultsOfImage(imageName, detectedObjectsList, annotatedObjectsList, evaluationPathAndFile)
#
#         # reading next line
#         line = logDetectionFile.readline()
#
#     # close file
#     logDetectionFile.close()
#     evaluationDetectionResultsFile.close()


# ###########################################
# Methods of Level 2
# ###########################################


# get the bounding boxes of all detected objects of the image
def getDetectedObjectsList(detectionLogFileName, imageName):
    # defining the detected objects list
    detectedObjectsList = []

    # open log detection file
    detectionLogFile = open(detectionLogFileName, "r")

    # reading next line
    line = detectionLogFile.readline()

    # setting control
    foundBoundingBoxes = False

    # searching bounding boxes
    while line != '':

        # looking for image name (jpg)
        if not foundBoundingBoxes and (line.lower().find('jpg') == -1 and line.lower().find('jpeg') == -1):
            line = detectionLogFile.readline()
            continue

        # reading next line
        line = detectionLogFile.readline()

        # check if finished the search
        if line == '':
            break

        # setting found bounding boxes
        foundBoundingBoxes = True

        # adjusting string line
        line = line.replace('\t', ' ')
        line = line.replace('\t', ' ')
        line = line.replace('\t', ' ')
        line = line.replace('\t', ' ')
        line = line.replace('\n', ' ')
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')

        # getting the array of values
        values = line.split(' ')

        # get fields of bounding box
        className = values[0].replace(':', '')
        className = className[2:]
        confidence = int(values[1].replace('%', ''))
        linP1 = int(values[5])
        colP1 = int(values[3])
        linP2 = linP1 + int(values[9])
        colP2 = colP1 + int(values[7])

        print(line)
        print('detected fields', className, confidence, linP1, colP1, linP2, colP2)

        # creating a new bounding box instance
        detectedBoundingBox = BoundingBox(linP1, colP1, linP2, colP2, className, confidence)

        # adding new item to the list
        detectedObjectsList.append(detectedBoundingBox)

        # # reading next line
        # line = detectionLogFileName.readline()
        #
        # # check if finished the search
        # if line.find('net.optimized') != -1 or line == '':
        #     break

    # returning the detected objects list
    return detectedObjectsList


# getting the list of annotated objects
def getAnnotatedObjectsList(inputImagesAnnotationsPath, imageName):
    # defining the annotated objects list
    annotatedObjectsList = []

    # open annotation file
    imageAnnotationFileName = imageName + ".txt"
    imageAnnotationPathAndFileName = inputImagesAnnotationsPath + imageAnnotationFileName

    # open log detection file
    imageAnnotationFile = open(imageAnnotationPathAndFileName, "r")

    # reading next line
    line = imageAnnotationFile.readline()

    # processing the file
    while line != '':
        # getting the array of values
        values = line.split(' ')

        # get fields of bounding box
        idClass = int(values[0])
        className = ObjectClassEnum.getValueName(idClass)
        colOfCentrePoint = float(values[1])
        linOfCentrePoint = float(values[2])
        heightOfCentrePoint = float(values[3])
        widthOfCentrePoint = float(values[4])

        # calculating the new points of bounding box
        linP1 = colOfCentrePoint
        colP1 = linOfCentrePoint
        linP2 = heightOfCentrePoint
        colP2 = widthOfCentrePoint
        confidence = 0

        # creating a new bounding box instance
        annotatedBoundingBox = BoundingBox(0, 0, 0, 0, '')
        annotatedBoundingBox.setYoloAnnotation(416, 416,
                                               colOfCentrePoint, linOfCentrePoint,
                                               widthOfCentrePoint, heightOfCentrePoint,
                                               0,
                                               idClass)

        # adding new item to the list
        annotatedObjectsList.append(annotatedBoundingBox)

        # reading next line
        line = imageAnnotationFile.readline()

    # close file
    imageAnnotationFile.close()

    # returning the annotated objects list
    return annotatedObjectsList


# evaluating the results
def evaluateResultsOfImage(imageName, detectedObjectsList, annotatedObjectsList, evaluationPathAndFile):
    # initializing line
    line = ''

    # writing the result of evaluation
    evaluationDetectionResultsFile = open(evaluationPathAndFile, 'a+')

    # processing objects annotated and detected
    for annotatedObject in annotatedObjectsList:

        # setting the image name
        line = imageName

        # setting the annotated class name
        line += ';' + annotatedObject.className

        # initializing fields of detected object
        detectedObjectInTheCorrectPositionAndClass = ''
        confidence = 0
        detectedObjectInTheCorrectPositionAndDiferentClass = ''
        othersDetectedObject = ''
        result = ''

        # checking if there is some detected object
        if len(detectedObjectsList) == 0:
            # setting fields
            detectedObjectInTheCorrectPositionAndClass = 'not detected'
            detectedObjectInTheCorrectPositionAndDiferentClass = ''
            othersDetectedObject = ''
            result = 'failure'

        else:

            # checking detected object list
            for detectedObject in detectedObjectsList:
                # print(imageName)

                # checking location of the object
                hasIntersection = checkLocationDectetedObject(annotatedObject, detectedObject)

                # checking if the annotated and detected objetcs has some intersection point
                if hasIntersection:
                    if annotatedObject.className == detectedObject.className:
                        detectedObjectInTheCorrectPositionAndClass = detectedObject.className
                        confidence = detectedObject.confidence
                        result = 'success'
                    else:
                        detectedObjectInTheCorrectPositionAndDiferentClass = detectedObject.className
                        result = 'failure'
                else:
                    othersDetectedObject += detectedObject.className + ' '
                    result = 'failure'

        # evaluating if has any object detected
        if detectedObjectInTheCorrectPositionAndClass == '':
            detectedObjectInTheCorrectPositionAndClass = 'not detected'

        # setting line
        line += ';' + detectedObjectInTheCorrectPositionAndClass \
                + ';' + str(confidence) \
                + ';' + detectedObjectInTheCorrectPositionAndDiferentClass \
                + ';' + othersDetectedObject \
                + ';' + result \
                + LINE_FEED

        # writing line
        evaluationDetectionResultsFile.write(line)

    # close file
    evaluationDetectionResultsFile.close()


# checks location of the object
def checkLocationDectetedObject(annotatedObject, detectedObject):
    # # initializing variable
    # hasIntersection = False

    print('anotada', annotatedObject.linPoint1, annotatedObject.colPoint1, annotatedObject.linPoint2,
          annotatedObject.colPoint2)
    print('detectada', detectedObject.linPoint1, detectedObject.colPoint1, detectedObject.linPoint2,
          detectedObject.colPoint2)

    # evaluating intersection
    for lin in range(detectedObject.linPoint1, detectedObject.linPoint2 + 1):
        for col in range(detectedObject.colPoint1, detectedObject.colPoint2 + 1):
            if (lin >= annotatedObject.linPoint1 and col >= annotatedObject.colPoint1
                    and lin <= annotatedObject.linPoint2 and col <= annotatedObject.colPoint2
            ):
                return True

    # # evaluating intersection when detected object is in the northwest of the annotated object
    # if (detectedObject.linPoint1 <= annotatedObject.linPoint1 and detectedObject.colPoint1 <= annotatedObject.colPoint1
    #         and detectedObject.linPoint2 >= annotatedObject.linPoint1 and detectedObject.colPoint2 >= annotatedObject.colPoint1
    #         and detectedObject.linPoint2 <= annotatedObject.linPoint2 and detectedObject.colPoint2 >= annotatedObject.colPoint2
    # ):
    #     hasIntersection = True
    #
    # # evaluating intersection when detected object is in the northeast of the annotated object
    # if (detectedObject.linPoint1 >= annotatedObject.linPoint1 and detectedObject.colPoint2 >= annotatedObject.colPoint2
    #         and detectedObject.linPoint2 <= annotatedObject.linPoint1 and detectedObject.colPoint1 <= annotatedObject.colPoint2
    #         and detectedObject.linPoint2 >= annotatedObject.linPoint2 and detectedObject.colPoint1 >= annotatedObject.colPoint1
    # ):
    #     hasIntersection = True

    # returning result
    return False


# ############################################################################


def getImageFileNameWithouExtension(fileName):
    # getting jpg position
    jpegPosition = -1
    jpegPosition = fileName.find('jpg')
    if jpegPosition == -1: jpegPosition = fileName.find('jpeg')
    if jpegPosition == -1: jpegPosition = fileName.find('JPG')
    if jpegPosition == -1: jpegPosition = fileName.find('JPEG')

    # getting only image name
    imageFileName = fileName[:jpegPosition - 1]

    # returning image file name
    return imageFileName


# move images and annotations files
def moveImageAndAnnotationFiles(croppedImagesClassNamePath, trainValidTestDatasetsPath, numberOfImages,
                                specificDestinationFolder):
    # defining auxiliary variables
    imagesCounter = 0

    # process images
    while (imagesCounter < numberOfImages):
        # getting the files list
        filesList = os.listdir(croppedImagesClassNamePath)

        # getting the random position
        index = randrange(len(filesList))

        # getting the file name
        fileName = filesList[index]

        # check if file is an image or not
        if fileName.lower().find('jpg') == -1 and fileName.lower().find('jpeg') == -1:
            continue

        # move image file
        source = croppedImagesClassNamePath + fileName
        destination = trainValidTestDatasetsPath + specificDestinationFolder + fileName
        shutil.move(source, destination)

        # move annotation file
        source = croppedImagesClassNamePath + getImageFileNameWithouExtension(fileName) + '.txt'
        destination = trainValidTestDatasetsPath + specificDestinationFolder + getImageFileNameWithouExtension(
            fileName) + '.txt'
        shutil.move(source, destination)

        # saving processing results
        saveProcessingResults(trainValidTestDatasetsPath, fileName)

        # counting files moved
        imagesCounter += 1


# process images
def organizeImagesByClassName(croppedImagesPath, trainValidTestDatasetsPath,
                              percentageOfTrainImages, percentageOfValidImages, percentageOfTestImages, className):
    # setting the full path name
    croppedImagesClassNamePath = croppedImagesPath + className + '/'

    # get the total number of images by class
    numberOfTotalImages = len(list(pathlib.Path(croppedImagesClassNamePath).glob('*.jpg')))
    images = list(pathlib.Path(croppedImagesClassNamePath).glob('*.jpg'))

    # calculating the number of images used in train, valid and test datasets
    numberOfTrainImages = round(numberOfTotalImages * percentageOfTrainImages / 100.0)
    numberOfValidImages = round(numberOfTotalImages * percentageOfValidImages / 100.0)
    numberOfTestImages = numberOfTotalImages - numberOfTrainImages - numberOfValidImages

    # moving to specific folders
    moveImageAndAnnotationFiles(croppedImagesClassNamePath, trainValidTestDatasetsPath, numberOfTrainImages, 'train/')
    moveImageAndAnnotationFiles(croppedImagesClassNamePath, trainValidTestDatasetsPath, numberOfValidImages, 'valid/')
    moveImageAndAnnotationFiles(croppedImagesClassNamePath, trainValidTestDatasetsPath, numberOfTestImages, 'test/')


# save results of processing
def saveProcessingResults(trainValidTestDatasetsPath, fileName):
    # creating the processing results file
    processingResultsFile = open(trainValidTestDatasetsPath + 'processingResults.txt', 'a+')

    # replacing characters to split string
    fileName = fileName.replace('-', '.')

    # getting the array of names parts
    values = fileName.split('.')

    # setting line to write
    line = values[0] + ' ' \
           + values[1] + ' ' \
           + values[3] + ' ' \
           + values[4] + ' ' \
           + LINE_FEED

    # write line
    processingResultsFile.write(line)

    # closing file
    processingResultsFile.close()


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # INPUT_DETECTION_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/EvaluateDetectionResultsProject/inputOutputData/input/detectionLog/'
    INPUT_IMAGES_DETECTIONS_PATH = \
        'C:/Users/Rubens/Google Drive (rubens.castro@ufg.br)/DoctoralProjects/YOLOv4/Results/Detection/'
    INPUT_IMAGES_ANNOTATIONS_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/EvaluateDetectionResultsProject/inputOutputData/input/imagesAnnotations/'
    OUTPUT_EVALUATION_DETECTIONS_RESULTS_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/EvaluateDetectionResultsProject/inputOutputData/output/'

    IMAGES_DETECTIONS = 'Detection-19'
    INPUT_IMAGES_DETECTIONS_FULL_PATH = INPUT_IMAGES_DETECTIONS_PATH + IMAGES_DETECTIONS + '/'



    # datetime object containing current date and time
    # now = datetime.now()
    # nowDateTime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # evaluationFile = 'evaluationOfDetection-' + nowDateTime + '.txt'
    evaluationResult = 'resultsOf' + IMAGES_DETECTIONS + '.txt'
    evaluationPathAndFile = OUTPUT_EVALUATION_DETECTIONS_RESULTS_PATH + evaluationResult

    print('Evaluating Detection Results')
    print('----------------------------')
    print('')
    print('Input log detection path                 : ', INPUT_IMAGES_DETECTIONS_PATH)
    print('Input images annotations path            : ', INPUT_IMAGES_ANNOTATIONS_PATH)
    print('Output evaluation detection results path : ', OUTPUT_EVALUATION_DETECTIONS_RESULTS_PATH)
    print('')

    # processing the annotated images
    evaluateDetectionResults(INPUT_IMAGES_DETECTIONS_FULL_PATH,
                             INPUT_IMAGES_ANNOTATIONS_PATH,
                             evaluationPathAndFile)

    # end of processing
    print('End of processing')