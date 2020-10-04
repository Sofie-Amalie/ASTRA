# name:                     ASTRA - Astronaut Scheduling Tool for Rest & Activity
# author:                   Aleksander Fiuk
# date created:             04/10/2020
# info:                     software created for NASA Space Apps Challenge

from datetime import date as date

### WIP ###
# calculate need levels based on previous experiences
def getNeedLevels(cycleHistory):
    comfortLevel = 0
    return comfortLevel

class State():

    def __init__(self, currentNeedLevels, currentActivity, currentMode):
        self._needs = currentNeedLevels
        self._mode = currentMode
        self._activity = currentActivity
        self._thresholds = {
            "hunger": [0.5, 0.75, 0.9],
            "sleep": [0.5, 0.75, 0.9],
            "comfort": [0.5, 0.75, 0.9]
        }

    def triggerUrge(self):
        if (self._needs["hunger"] >= self._thresholds["hunger"][0] or
            self._needs["sleep"] >= self._thresholds["sleep"][0] or
            self._needs["comfort"] >= self._thresholds["comfort"][0]):
            return True
        else: return False

    def triggerDiscomfort(self):
        if (self._needs["hunger"] >= self._thresholds["hunger"][1] or
            self._needs["sleep"] >= self._thresholds["sleep"][1] or
            self._needs["comfort"] >= self._thresholds["comfort"][1]):
            return True
        else: return False

    def triggerNonproductive(self):
        if (self._needs["hunger"] >= self._thresholds["hunger"][2] or
                self._needs["sleep"] >= self._thresholds["sleep"][2] or
                self._needs["comfort"] >= self._thresholds["comfort"][2]):
            return True
        else:
            return False

class Cycle():

    def __init__(self, sleepTimeTuple, chronotype, hoursOfExercise, dinnerShift, utc):
        sleepTimeTuple = (sleepTimeTuple[0]+utc,sleepTimeTuple[1]+utc)
        self.sleepSch = []
        self.exerciseSch = []
        self.nutritionSch = []

        firstBigSleep = sleepTimeTuple[0] > sleepTimeTuple[1]

        for i in range(24):
            if firstBigSleep:
                self.sleepSch.append( (int(i < sleepTimeTuple[1]) + int(i >= sleepTimeTuple[0])) )
            else:

                self.sleepSch.append( int(i>=sleepTimeTuple[0]) * int(i<sleepTimeTuple[1]) )

        exerciseCounter = 0

        for i in range(24):

            if firstBigSleep == False:
                self.nutritionSch.append(int(i==sleepTimeTuple[1] or i==sleepTimeTuple[0]-dinnerShift+24 or i==sleepTimeTuple[0]-dinnerShift or
                                         i==int((sleepTimeTuple[1]+sleepTimeTuple[0]-dinnerShift+24)/2)))

            else:
                self.nutritionSch.append(int(
                    i == sleepTimeTuple[1] or i == sleepTimeTuple[0] - dinnerShift + 24 or i == sleepTimeTuple[
                        0] - dinnerShift or
                    i == int((sleepTimeTuple[1] + sleepTimeTuple[0] - dinnerShift) / 2)))

        for i in range(24):
            if chronotype == "NO":
                if exerciseCounter == hoursOfExercise: self.exerciseSch.append(0)
                else:
                    if exerciseCounter is not 0: self.exerciseSch.append(1)
                    else:
                        self.exerciseSch.append(int(i==sleepTimeTuple[1]+1 or i==sleepTimeTuple[1]-23))
                    if self.exerciseSch[i] == 1: exerciseCounter+=1

            if chronotype == "EB":
                if exerciseCounter == hoursOfExercise: self.exerciseSch.append(0)
                else:
                    if exerciseCounter is not 0: self.exerciseSch.append(1)
                    else:
                        if self.nutritionSch[i] == 1: self.exerciseSch.append(0)
                        else:
                            self.exerciseSch.append(int(i==sleepTimeTuple[0]-6 or i==sleepTimeTuple[1]+18))
                    if self.exerciseSch[i] == 1: exerciseCounter+=1

        # self.resolveConflicts()

    ### WIP ###
    def resolveConflicts(self):
        flag = []
        earliestEx = None
        for i in range(24):
            if earliestEx is not None and self.exerciseSch[i] == 1:
                earliestEx=1
            flag.append(int(self.nutritionSch[i]==1 and self.exerciseSch[i]==1))
            if self.exerciseSch[i+1] == 0:
                self.nutritionSch[i] = 0
                self.nutritionSch[i+1] = 1
            else:
                for j in range(int(i>earliestEx)*(i-earliestEx)+int(i<earliestEx)*(earliestEx+i-22)):
                    self.exerciseSch[i-j-1] = 1
                self.exerciseSch[i] = 0
        self.resolveConflicts()

    def disp(self,utc):
        print("#########################################")
        print("#\t\t\tASTRA Cycle Display\t\t\t#")
        print('# Hour\t|\tActivity\t|\tMode\t\t#')
        for i in range(24):
            print('#',i,'\t|\t',i,'\t|\tMode\t\t#')

class CycleHistory():

    def __init__(self,stateHistory,activityHistory,sleepHistory):
        self.states = stateHistory
        self.activities = activityHistory
        self.sleepLog = sleepHistory

class Task():

    def __init__(self,durationTuple,date,utc):
        durationTuple = (durationTuple[0]+utc,durationTuple[1]+utc)
        self.duration = durationTuple
        self.date = date
        self.activitySch = []

        firstBigTask = durationTuple[0] > durationTuple[1]

        for i in range(24):
            if firstBigTask:
                self.activitySch.append((int(i < durationTuple[1]) + int(i >= durationTuple[0])))
            else:

                self.activitySch.append(int(i >= durationTuple[0]) * int(i < durationTuple[1]))

def checkForTasksConflicts(taskList):
    for i in range(len(taskList)):
        for j in range(len(taskList)):
            if i==j or i>j: continue
            for k in range(24):
                if taskList[i].activitySch[k] == 1 and taskList[j].activitySch[k] == 1:
                    if taskList[i].date == taskList[j].date:
                        raise NameError("Tasks are colliding:",j," and ",i)

class Schedule():

    def __init__(self,cycleHistory,targetCycle,taskList):
        self.taskTimes = 
        self.start = 0,0
        self._internalClock = self.start
        self.stop = 0,0
        self.plan = []

        for

    def tiktok(self):
        for i in range(24*(self.stop[1]-self.start[1])+(self.stop[0]-self.start[0])):
            # assess state
            # execute schedule
            # change mode
            # reschedule

    def changeMode(self,mode):
        self.mode = mode
        if mode == "Emergency": self.rescheduleEmergency()
        elif mode == "Restore": self.rescheduleRestore()
        elif mode == "Alert": self.rescheduleAlert()
        else: self.enterRegular()




cyc = Cycle((23,7),"EB",3,5,0)
print(cyc.sleepSch)
print(cyc.nutritionSch)
print(cyc.exerciseSch)
# cyc.disp(0)





