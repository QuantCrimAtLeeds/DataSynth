import arcpy, os.path, random, math
from numpy import genfromtxt

path = r"C:\PythonWorkspace\PDProject"
arcpy.env.workspace = path

# Map variables
bufferSize = "300 Meters"
"""
str: The size of the buffer around the initial burglary.
"""
threshold = 80
"""
int: The threshold value out of 100, above which the burglar will move from a cluster.
"""
iterations = 10
"""
int: The number of clusters to be created.
"""
backgroundBurglaries = 100
"""
int: The number of background burglaries to be created.
"""
minBurglaries = 3
"""
int: The minimum number of burglaries in a cluster.
"""
maxBurglaries = 12
"""
int: The maximum number of burglaries in a cluster.
"""
prevPoint = (0,0)
"""
point: Previous location of initial burglary.
"""

# Monte Carlo variables
maxNum = 0
"""
int: The maximum value in the sample file.
"""
minNum = 0
"""
int: The minimum value in the sample file.
"""
interval = 0.0
"""
float: The interval for the sample file ((max - min) / numberOfBins).
"""
numberOfBins = 20
"""
int: The number of bins to separate the sample file into.
"""
bins = [[0.0 for x in range(numberOfBins)] for y in range(2)]
"""
list: Create the bins list, initialised as 0.0.
"""

def setNumbers(filename):
    """

    Function to set the frequency distribution of numbers returned by the sampler.
    For use with Monte Carlo Sampling.

    Adapted from the work of Sim Reaney and Andy Evans at
    http://www.geog.leeds.ac.uk/courses/other/programming/info/code/modelling/calibration/MonteCarlo.java

    Args:
        filename (str): The location of the file containing the sample data.
        
    """
    data = fileAsArray(filename)
    
    i = 0
    while (i < numberOfBins):
        bins[0][i] = interval + (interval * (i) + minNum)

        j = 0
        while (j < len(data)):
            if data[j] < bins[0][i]:
                bins[1][i] = bins[1][i] + 1
                
            j = j + 1
            
        bins[1][i] = bins[1][i] / len(data)
        i = i + 1

def getNumber(random):
    """

    Function to return a number at a rate determined by a preset distribution.
    For use with Monte Carlo Sampling.

    Adapted from the work of Sim Reaney and Andy Evans at
    http://www.geog.leeds.ac.uk/courses/other/programming/info/code/modelling/calibration/MonteCarlo.java

    Args:
        random (int): A random number between 0 and 1 to be used in selecting a bin.

    Returns:
        value (float): The result of the Monte Carlo sampling using the random input.
        
    """
    value = 0.0
    i = 0
    
    while (i < numberOfBins):
        if random < bins[1][i]:
            value = bins[0][i]
            break
        
        i = i + 1

    return value

def fileAsArray(filename):
    """

    Function to return a file as a one-dimensional array.
    For use with Monte Carlo Sampling.

    Adapted from the work of Sim Reaney and Andy Evans at
    http://www.geog.leeds.ac.uk/courses/other/programming/info/code/modelling/calibration/MonteCarlo.java

    Args:
        filename (str): The location of the file containing the sample data.

    Returns:
        data (int[]): The data in the file as a one-dimensional array. 
        
    """
    data2d = genfromtxt(filename, delimiter=',')
    
    position = 0
    data = []
    global minNum
    global maxNum
    
    for line in data2d:
        for value in line:
            data.append(value)
            if position == 0:
                maxNum = value
                minNum = value
                
            if value > maxNum:
                maxNum = value
                
            if value < minNum:
                minNum = value
                
            position = position + 1

    global interval
    interval = float(maxNum - minNum)/numberOfBins

    return data


def setup():
    """

    Function to be called when creating a new model.
    Creates required initial shape files and empties them if they already exist.
    Sets up the Monte Carlo sampling distribution for later use.
        
    """
    # Creates the feature class for the boundary
    if arcpy.Exists("boundary.shp"):
        print "Boundary file exists"
    else:
        arcpy.CreateFeatureclass_management(path, "boundary.shp", "POLYGON")

        # Create polygon of size 10km x 10km
        array = arcpy.Array([arcpy.Point(0, 0),
                             arcpy.Point(0, 10000),
                             arcpy.Point(10000, 10000),
                             arcpy.Point(10000, 0)
                             ])
        polygon = arcpy.Polygon(array)

        # Open an InsertCursor and insert polygon
        cursor = arcpy.da.InsertCursor("boundary.shp", ["SHAPE@"])
        cursor.insertRow([polygon])
        del cursor
        print "Boundary file created"

    # Creates the feature class for the burglaries
    if arcpy.Exists("burglaries.shp"):
        # Clears the burglary file
        arcpy.DeleteFeatures_management("burglaries.shp")
        print "Burglaries file exists"
    else:
        # Creates the burglary file
        arcpy.CreateFeatureclass_management(path, "burglaries.shp", "POINT")
        arcpy.AddField_management("burglaries.shp", "ITER", "SHORT")
        arcpy.AddField_management("burglaries.shp", "TYPE", "TEXT")
        print "Burglaries file created"

    # Creates the feature class for the buffers
    if arcpy.Exists("buffers.shp"):
        # Clears the buffers file
        arcpy.DeleteFeatures_management("buffers.shp")
        print "Buffers file exists"
    else:
        # Creates the buffers file
        arcpy.CreateFeatureclass_management(path, "buffers.shp", "POLYGON")
        arcpy.AddField_management("buffers.shp", "ITER", "SHORT")
        print "Buffers file created"

    # Creates the frequency distribution for the Monte Carlo sampling
    setNumbers(path + r'\testData.txt')
        
def randomPoints(interimName, boundary, numPoints, iterVal, pointType):
    """

    Function to add random points within a boundary and append to the burglaries shape file.
    Note the interim file must be separately deleted before it can be reused.
    This is because it may be required again in a later step.

    Args:
        interimName (str): The name of the interim shapefile to be created to hold the random points.
        boundary (str): The name of the boundary shapefile to create the points within.
        numPoints (int): The number of points to be created.
        iterVal (int): The number of the current iteration to be added to the attribute table for the points created.
        pointType (str): The type of point being created (INITIAL, SECONDARY, BACKGROUND) to be added to the attribute table for the points created.
        
    """

    global prevPoint
    
    # Creates the random points
    arcpy.CreateRandomPoints_management(path, interimName, boundary, "", numPoints)
    arcpy.AddField_management(interimName, "ITER", "SHORT")
    arcpy.AddField_management(interimName, "TYPE", "TEXT")

    # Updates the fields in the table
    with arcpy.da.UpdateCursor(interimName, ["ITER", "TYPE", "SHAPE@XY"]) as cursor:
        for row in cursor:
            row[0] = iterVal
            row[1] = pointType
            if pointType == "INITIAL":
                prevPoint = (row[2][0], row[2][1])
            cursor.updateRow(row)

    # Adds the subsequent points into the burglaries.shp class that will contain all burglaries        
    arcpy.Append_management(interimName, "burglaries.shp", "NO_TEST")


def specificPoint(distance, bearing, interimName, boundary, iterVal):
    """

    Function to add a specific point at a distance from the previous initil burglary point to the burglaries shape file.
    Note the interim file must be separately deleted before it can be reused.
    This is because it may be required again in a later step.

    Args:
        distance (float): The distance from the previous point to create the new point in meters.
        bearing (int): The bearing from the last point to create the new point (0-360)
        interimName (str): The name of the interim shapefile to be created to hold the random points.
        boundary (str): The name of the boundary shapefile to create the points within.
        iterVal (int): The number of the current iteration to be added to the attribute table for the points created.
        
    """

    global prevPoint

    # Calculate the angle and bearing from the previous point
    angle = 90 - bearing
    bearing = math.radians(bearing)
    angle =   math.radians(angle)

    # Use trigonometry to calculate new point location
    cosa = math.cos(angle)
    cosb = math.cos(bearing)
    xNew, yNew = \
        (prevPoint[0] +(distance * cosa), prevPoint[1]+(distance * cosb))
    point = arcpy.Point(xNew, yNew)

    # Search in boundary file
    cursor = arcpy.SearchCursor(boundary)
    for rowid in cursor:
        # Get boundary polygon
        polygon = rowid.Shape

        #If new point is inside boundary
        if polygon.contains(point):
            # Create the row to be added to the initPoint shapefile
            row = ((xNew, yNew), iterVal, "INITIAL")

            # Creates the feature class
            arcpy.CreateFeatureclass_management(path, interimName, "POINT")
            arcpy.AddField_management(interimName, "ITER", "SHORT")
            arcpy.AddField_management(interimName, "TYPE", "TEXT")

            # Uses an update cursor to add to the interim file
            cursor = arcpy.da.InsertCursor(interimName, ["SHAPE@XY", "ITER", "TYPE"])
            cursor.insertRow(row)
            del cursor

            # Adds the subsequent point into the burglaries.shp class that will contain all burglaries        
            arcpy.Append_management(interimName, "burglaries.shp", "NO_TEST")

            # Updates the prebvious point location
            prevPoint = (xNew, yNew)
        else:
            # Try again using the same function parameters but a new random bearing value
            specificPoint(distance, random.randint(0, 360), interimName, boundary, iterVal)
   
def newZone(distance):
    """

    Funtion to add a new burglary cluster within the boundary.
    Distance can be set to 0 if the point being added is to be the first in the area.

    Args:
        distance (float): The distance from the previous point to create the new point in meters.
        
    """
    if distance == 0:
        # Creates the first random burglary point
        randomPoints("initPoint.shp", "boundary.shp", 1, iteration, "INITIAL")
    else:
        # Creates subsequent burglary point at specific position
        specificPoint(distance, random.randint(0, 360), "initPoint.shp", "boundary.shp", iteration)
    
    # Creates the buffer around the initial point in a  cluster
    arcpy.Buffer_analysis("initPoint.shp", "initBuff.shp", bufferSize)

    # Adds the buffer into the buffers.shp class that will contain all buffers
    arcpy.Append_management("initBuff.shp", "buffers.shp", "NO_TEST")
    
    # Delete the initial point so the class can be reused
    arcpy.Delete_management("initPoint.shp")

    # Calculate number of further burglaries
    # Bounds for number of burglaries set from parameters. 1 is subtracted to compensate for the original burglary point
    subsequent = (minBurglaries - 1)
    while random.randint(0, 100) < threshold and subsequent < (maxBurglaries - 1):
        subsequent += 1

    print "Iteration " + str(iteration) + " has " + str(subsequent + 1) + " burglaries."

    if subsequent != 0:
        # Generate further burglaries in area
        randomPoints("subsPoint.shp", "initBuff.shp", subsequent, iteration, "SECONDARY")
        
        # Delete the subsequent points so the class can be reused
        arcpy.Delete_management("subsPoint.shp")

    # Delete the initial buffer so the class can be reused
    arcpy.Delete_management("initBuff.shp")

def randomNoise():
    """

    Function to generate random burglaries inside the boundary not related to a cluster.
    
    """
    # Creates the background burglaries (i.e. random noise)
    randomPoints("randomNoise.shp", "boundary.shp", backgroundBurglaries, 0, "BACKGROUND")

    # Delete the random noise points so the class can be reused
    arcpy.Delete_management("randomNoise.shp")



# Main part of the program
setup()

iteration = 1
newZone(0)
iteration += 1

while iteration <= iterations:
    newZone(getNumber(random.uniform(0,1)))
    iteration += 1

randomNoise()
