#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import threading
import time


########################################################################
class Soldier(threading.Thread):
    """The class of a soldier."""

    def __init__(self, name):
        """Constructor"""
        threading.Thread.__init__(self, name=name)
        self.name = name  # the name of this soldier
        self.setDaemon(True)  # this is a daemon thread.

        # the time of this soldier need to finish the job
        self.playTime = random.randint(1, 10)

        # is the soldier stop shotting, if timeout or the target has been killed,
        # he may stop.
        self.isStopped = False
        self.isSuccess = False  # did he kill the target?

    def assassinate(self):
        """The task, to kill the target."""

        for i in range(self.playTime):
            print('%s play(%d)' % (self.name, i + 1))
            time.sleep(1)

        # ----------------------------------------------------------------------

    def run(self):
        """Start to move ..."""
        print('%s has moved out, need time: %d ...' % (self.name, self.playTime))
        self.assassinate()
        print('%s stopped ...' % self.name)
        self.isStopped = True  # the target has been killed, then he stopped.
        self.isSuccess = True


class Commander(threading.Thread):
    """The class of commander, a commander will command only one soldier."""

    # ----------------------------------------------------------------------
    def __init__(self, soldier):
        """Constructor"""
        threading.Thread.__init__(self, name='Commander')
        self.soldier = soldier

    # ----------------------------------------------------------------------
    def run(self):
        """Authorize the soldier to start killing."""

        self.soldier.start()
        try:
            # Boss said: give the soldier 5 seconds to finish his job
            self.soldier.join(5)
        except:
            pass

        # Use the class's own attribute to judge whether it is timeout.
        # if self.soldier.isAlive():
        if not self.soldier.isStopped:
            print('%s is timeout!' % self.soldier.name)

            # the soldier run out his time, then he stopped.
            self.soldier.isStopped = True


def killing():
    """Let's pull the trigger, start killing !"""
    t1 = time.time()

    # Get ready for the commanders
    l_commander = []
    for i in range(10):  # 10 soldiers

        # get ready for the soldier
        soldier = Soldier('soldier-%d' % (i + 1))
        if i == 5 or i == 9:
            soldier.playTime = 10000

        l_commander.append(Commander(soldier))
        # Soldiers move out one by one.
        for cmd in l_commander:
            cmd.start()
        isBreak = False
        while not isBreak:
            isBreak = True
            for cmd in l_commander:
                if cmd.soldier.isStopped == False:
                    isBreak = False
                    # Check the results of the battle at the schedule time.
                    for cmd in l_commander:
                        print('%s, is success: %s' % (cmd.soldier.name, cmd.soldier.isSuccess))
                        # Go back to base.
                        time.sleep(20)
                        # Check the results at the final time.
                    for cmd in l_commander:
                        print('%s, is success: %s' % (cmd.soldier.name, cmd.soldier.isSuccess))

                    t2 = time.time()
                    print('Total time: %.2f' % (float(t2 - t1)))


killing()
