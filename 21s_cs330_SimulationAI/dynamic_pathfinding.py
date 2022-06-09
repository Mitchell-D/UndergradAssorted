"""
Assignment: CS 330 Programming Assignment 2
Professor:  Dr. Mikel Petty
Name:       Mitchell Dodson
Date:       March 15, 2021
"""
from dataclasses import dataclass
import math as m
import numpy as np
import os
from pprint import pprint as ppt

@dataclass
class SteeringFrame:
    """Holds updated linear and angular acceleration values"""
    lin: tuple
    ang: float

@dataclass
class Waypoint:
    """Holds parameter and endpoint information about a path waypoint"""
    x: float
    y: float
    param: float=None
    unitDist: float=None
    def  tuplePos(self) -> tuple:
        return (self.x, self.y)

class Path:
    def __init__(self):
        self.unitLength = 0
        self.waypoints = []

    def pythagoras(self, p1:tuple, p2:tuple):
        """Calculates the linear distance between 2 points"""
        return m.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

    def addWaypoint(self, waypoint:tuple):
        """Adds a waypoint to the end of the path"""
        newWP = Waypoint(waypoint[0], waypoint[1])
        self.waypoints.append(newWP)

        if len(self.waypoints) != 1:
            newSegment = self.pythagoras(
                self.waypoints[len(self.waypoints)-2].tuplePos(),
                newWP.tuplePos()
                )
            self.unitLength += newSegment

        self.waypoints[-1].unitDist = self.unitLength
        self.refreshParams()

    def dotProduct(self, v1:tuple, v2:tuple):
        """returns scalar product of the 2 provided vectors"""
        return v1[0]*v2[0] + v1[1]*v2[1]

    def getDifference(self, v1:tuple, v2:tuple):
        """returns vector difference of v1 and v2"""
        return ( v1[0]-v2[0], v1[1]-v2[1])

    def scaleVector(self, v:tuple, a:float):
        """scale provided vector by given value 'a'"""
        return (v[0]*a, v[1]*a)

    def getLambda(self, pos:tuple, p1:tuple, p2:tuple):
        """returns lambda value as defined on ch7p2 presentation slide 24"""
        qp = self.getDifference(p2, p1)
        xp = self.getDifference(pos, p1)
        return self.dotProduct(xp, qp)/self.dotProduct(qp, qp)

    def getRelSegmentGeometry(self, pos:tuple, p1:tuple, p2:tuple):
        """returns the closest point and minimum distance to segment p1-p2"""
        l = self.getLambda(pos, p1, p2)
        if l <= 0:
            s = p1
        elif l >= 1:
            s = p2
        else:
            #  v1 and v2 are inverted in second difference method since we
            #  actually want to add p1 with the scaled vector in the first
            s = self.getDifference(
                    p1, self.scaleVector(self.getDifference(p1,p2), l ))
        dist = self.pythagoras(pos, s)
        return (s, dist)

    def getClosestPoint(self, pos:tuple):
        """
        returns the closest point, and indeces of waypoint segment
        closest to the provided coordinate location.
        """
        d_min = None
        s_min = None
        i_min = None
        for i in range(len(self.waypoints)-1):
            s, d = self.getRelSegmentGeometry(
                    pos,
                    self.waypoints[i].tuplePos(),
                    self.waypoints[i+1].tuplePos(),
                    )
            if d_min:
                if d<d_min:
                    d_min = d
                    s_min = s
                    i_min = i
            else:
                d_min = d
                s_min = s
                i_min = i

        return (s_min, (i_min, i_min+1))

    def getParam(self, pos:tuple):
        """returns the path parameter closest to the provided coord position"""
        s, segment = self.getClosestPoint(pos)
        #print("closest point:",s)
        a = self.waypoints[segment[0]]
        b = self.waypoints[segment[1]]
        t = self.pythagoras(self.getDifference(s,a.tuplePos()),(0,0)) / \
                self.pythagoras(
                    self.getDifference(
                        b.tuplePos(),
                        a.tuplePos()
                        ),
                    (0,0))
        closeParam = a.param + t*(b.param-a.param)
        return closeParam

    def getPosition(self, pathParam: float):
        """returns the unit position of point at pathParam"""
        assert (0 <= pathParam <= 1)
        #print("looking :",pathParam)

        for i in range(len(self.waypoints)):
            if self.waypoints[i].param >= pathParam:
                break
        #print(self.waypoints[i].param)
        a = self.waypoints[i-1]
        b = self.waypoints[i]
        t =  (pathParam-a.param) / (b.param-a.param)
        xpos = a.x + t*(b.x-a.x)
        ypos = a.y + t*(b.y-a.y)
        return (xpos, ypos)

    def getUnitLength(self):
        """returns the full length of the path in units"""
        return self.unitLength

    def refreshParams(self):
        """recalculates the length of the path from waypoint 1"""
        if len(self.waypoints) != 1:
            for wp in self.waypoints:
                wp.param = wp.unitDist/self.unitLength

    def printWaypoints(self):
        """represents waypoints in this path"""
        for wp in self.waypoints:
            print(wp)

class Character:
    def __init__(self, label:str, pos:tuple, vel:tuple, rvel:float,
            ber:float, vmax:float, amax:float):
        """
        Creates a new character with provided values

        @param label:     (str)            character's label (should be unique)
        @param pos:       (2-member tuple) initial posiiton
        @param vel:       (2-member tuple) initial velocity
        @param rvel:      (float)          initial rotational velocity
        @param ber:       (float)          initial bearing in rad
        @param vmax:      (float)          maximum velocity
        @param amax:      (float)          maximum acceleration
        """
        self.behavior = 1
        self.target = None
        self.charTime = 0
        self.acc = (0,0)
        self.pos = pos
        self.vel = vel
        self.rvel = rvel
        self.ber = ber
        self.vmax = vmax
        self.amax = amax
        self.label = label
        self.path = None
        self.align = False

    def setPath(self, path:Path):
        """Update character with a path to follow when Follow behavior used"""
        self.path = path

    def setTarget(self, target:"Character"):
        """Sets the movement target to the provided character"""
        self.target = target

    def setAlign(self, align:bool):
        """determine whether the character aligns with movement direction"""
        self.align = align

    def setBehavior(self, behavior:int):
        """
        @param behavior:  (int)  new behavior

        Acceptable values:
         | 1:Stop         4:Flee   |
         | 2:reserved     5:Arrive |
         | 3:Seek         6:Follow |
        """

        if 0<behavior<7:
            self.behavior = behavior
        else:
            raise ValueError("behavior must be an integer from 1 to 5")

    def getBehavior(self):
        """returns the current behavior of this Character"""
        if self.behavior == 6:
            return 3
        else:
            return self.behavior

    def getKinematic(self):
        """returns a dictionary describing this character's kinematic"""
        kinematic = {
                "time": self.charTime-.5,
                "label": self.label,
                "xpos": self.pos[0],
                "zpos": self.pos[1],
                "xvel": self.vel[0],
                "zvel": self.vel[1],
                "xacc": self.acc[0],
                "zacc": self.acc[1],
                "ber":self.ber,
                "behavior": self.behavior,
                }
        return kinematic
    def getLabel(self):
        """returns the label of this Character"""
        return self.label

    def update(self, timestep):
        """
        Actually updates the character's position based on current behavior
        """
        self.charTime += timestep
        if not self.target and self.behavior not in (1,2,6):
            raise ValueError("A target must be provided for this action!")

        if self.behavior == 1:
            newSteering = SteeringFrame((0,0),0)
        elif self.behavior == 2:
            newSteering = SteeringFrame((0,0),0)
        elif self.behavior == 3:
            newSteering = self.seek(self.target.pos)
        elif self.behavior == 4:
            newSteering = self.flee(self.target.pos)
        elif self.behavior == 5:
            newSteering = self.arrive(self.target.pos)
        elif self.behavior == 6:
            newSteering = self.follow()

        self.pos = Character.getDifference(
                self.pos,
                Character.scale(self.vel,-1*timestep)
                )
        self.ber += self.rvel*timestep

        self.acc = newSteering.lin
        self.vel = Character.getDifference(
                self.vel,
                Character.scale(self.acc, -1*timestep)
                )
        self.rvel += newSteering.ang * timestep

        if self.align:
            self.ber = m.atan2(self.vel[1], self.vel[0])

        if Character.getMagnitude(self.vel) > self.vmax:
            self.vel = Character.normalize(self.vel, self.vmax)

        return self.getKinematic()

    def seek(self, targetPos:tuple) -> SteeringFrame:
        """returns a SteeringFrame for seeking the target position"""
        #print(f"seeking {targetPos} from {self.pos}")
        lin = Character.getDifference(targetPos, self.pos)
        lin = Character.normalize(lin, self.amax)
        return SteeringFrame(lin, 0)

    def flee(self, targetPos:tuple) -> SteeringFrame:
        """returns a SteeringFrame for fleeing from the target position"""
        lin = Character.getDifference(self.pos,targetPos)
        lin = Character.normalize(lin, self.amax)
        return SteeringFrame(lin, 0)

    def arrive(self, targetPos:tuple, arriveRad:float=20.0, slowRad:float=40.0,
            timeToTarget:float=0.1) -> SteeringFrame:
        """returns a SteeringFrame for arriving near the target position"""
        direction = Character.getDifference(targetPos, self.pos)
        distance = Character.getMagnitude(direction)
        if distance < arriveRad:
            return SteeringFrame((0,0),0)
        elif distance > slowRad:
            targetSpeed = self.vmax
        else:
            targetSpeed = self.vmax * distance / slowRad

        targetVel = Character.normalize(direction, self.amax)
        lin = Character.getDifference(targetVel, self.vel)
        lin = Character.normalize(lin, 1/timeToTarget)

        if Character.getMagnitude(lin) > self.amax:
            Character.normalize(lin, self.amax)

        return SteeringFrame(lin, 0)

    def follow(self, pathOffset:float=.02):
        """follows a Path object, provided with setPath() method"""
        curParam = self.path.getParam(self.pos)
        targetParam = curParam + pathOffset
        targetPos = self.path.getPosition(targetParam)
        #print("seeking param:",targetParam)
        return self.seek(targetPos)

    @staticmethod
    def getDifference(v1:tuple, v2:tuple) -> tuple:
        """returns the difference of 2 provided 2-member tuples"""
        return (v1[0]-v2[0], v1[1]-v2[1])

    @staticmethod
    def getMagnitude(vector:tuple) -> float:
        """returns the magnitude of a 2-member tuple"""
        return m.sqrt(vector[0]**2 + vector[1]**2)

    @staticmethod
    def normalize(vector:tuple, fmag:float=1) -> tuple:
        """
        normalizes a tuple to a magnitude of 1 if no magnitude is provided,
        otherwise normalizes the tuple to the provided magnitude.
        """
        imag = Character.getMagnitude(vector)
        return (fmag*vector[0]/imag, fmag*vector[1]/imag)

    @staticmethod
    def scale(vector:tuple, mag:float) -> tuple:
        """scales the provided 2-member vector by provided magnitude"""
        return (vector[0]*mag, vector[1]*mag)

if __name__=="__main__":
    import csv

    myPath = Path()
    path_waypoints = ((75,-20),(45,20),(15,-40),(-15,40),(-45,-60),(-75,60))
    for wp in path_waypoints:
        myPath.addWaypoint(wp)
        print(myPath.getUnitLength())
    myPath.printWaypoints()
    #print(a.getParam((-20, -20)))

    follower = Character(label="171", pos=(70,-40), vel=(0,0),
            rvel=0, ber=0, vmax=4, amax=2)
    follower.setPath(myPath)
    follower.setBehavior(6)
    follower.setAlign(True)

    kinematics = []
    for i in range(101):
        kinematics.append(follower.update(.5))

    with open("follower.csv", "w", newline="") as fp:
        writer = csv.writer(fp, delimiter=",")
        rows = kinematics
        for row in rows:
            #print(row.values())
            writer.writerow(list(row.values()))
