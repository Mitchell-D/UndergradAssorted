"""
Assignment: CS 330 Programming Assignment 1
Professor:  Dr. Mikel Petty
Name:       Mitchell Dodson
Date:       February 18, 2021
"""
from dataclasses import dataclass
import math as m
import numpy as np
import os

@dataclass
class SteeringFrame:
    """Holds updated linear and angular acceleration values"""
    lin: tuple
    ang: float

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

    def setTarget(self, target:"Character"):
        """Sets the movement target to the provided character"""
        self.target = target

    def setBehavior(self, behavior:int):
        """
        @param behavior:  (int)  new behavior

        Acceptable values:
         | 1:Stop         4:Flee   |
         | 2:reserved     5:Arrive |
         | 3:Seek                  |
        """

        if 0<behavior<6:
            self.behavior = behavior
        else:
            raise ValueError("behavior must be an integer from 1 to 5")

    def getBehavior(self):
        """returns the current behavior of this Character"""
        return self.behavior

    def getKinematic(self):
        """returns a dictionary describing this character's kinematic"""
        kinematic = {
                "time": self.charTime,
                "label": self.label,
                "behavior": self.behavior,
                "xpos": self.pos[0],
                "zpos": self.pos[1],
                "xvel": self.vel[0],
                "zvel": self.vel[1],
                "xacc": self.acc[0],
                "zacc": self.acc[1],
                "ber":self.ber,
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
        if not self.target and self.behavior not in (1,2):
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

        if Character.getMagnitude(self.vel) > self.vmax:
            self.vel = Character.normalize(self.vel, self.vmax)

        return self.getKinematic()

    def seek(self, targetPos:tuple) -> SteeringFrame:
        """returns a SteeringFrame for seeking the target position"""
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

    Stopper = Character(label="161", pos=(0,0), vel=(0,0),
            rvel=0, ber=0, vmax=0, amax=0
            )

    Fleer = Character(label="162", pos=(-25,50), vel=(0,-8),
            rvel=0, ber=m.pi/4, vmax=10, amax=2
            )

    Seeker = Character(label="163", pos=(50,-25), vel=(0,-8),
            rvel=0, ber=3*m.pi/2, vmax=8, amax=2
            )

    Arriver = Character(label="164", pos=(-50,-75), vel=(-6,4),
            rvel=0, ber=m.pi, vmax=8, amax=2
            )

    Stopper.setBehavior(1)
    Fleer.setTarget(Stopper)
    Fleer.setBehavior(4)
    Seeker.setTarget(Stopper)
    Seeker.setBehavior(3)
    Arriver.setTarget(Stopper)
    Arriver.setBehavior(5)

    kinematics = {
            "161":[],
            "162":[],
            "163":[],
            "164":[],
            }

    for i in range(101):
        kinematics[Stopper.getLabel()].append(
            Stopper.update(.5)
            )
        kinematics[Fleer.getLabel()].append(
            Fleer.update(.5)
            )
        kinematics[Seeker.getLabel()].append(
            Seeker.update(.5)
            )
        kinematics[Arriver.getLabel()].append(
            Arriver.update(.5)
            )
    files = {
        "stopperfile": "stopper.csv",
        "fleerfile": "fleer.csv",
        "seekerfile": "seeker.csv",
        "arriverfile": "arriver.csv",
        }
    with open(files["stopperfile"], "w", newline="") as stopperfile:
        writer = csv.writer(stopperfile, delimiter=",")
        rows = kinematics["161"]
        for row in rows:
            writer.writerow(list(row.values()))
    with open(files["fleerfile"], "w", newline="") as stopperfile:
        writer = csv.writer(stopperfile, delimiter=",")
        rows = kinematics["162"]
        for row in rows:
            writer.writerow(list(row.values()))
    with open(files["seekerfile"], "w", newline="") as stopperfile:
        writer = csv.writer(stopperfile, delimiter=",")
        rows = kinematics["163"]
        for row in rows:
            writer.writerow(list(row.values()))
    with open(files["arriverfile"], "w", newline="") as stopperfile:
        writer = csv.writer(stopperfile, delimiter=",")
        rows = kinematics["164"]
        for row in rows:
            writer.writerow(list(row.values()))
