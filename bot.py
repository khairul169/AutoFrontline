import pyautogui as ui
import time
import numpy as np
from random import randint

# images
CMD_POST = './img/cmdpost.png'
HELIPORT = './img/heliport.png'
OK_BTN = './img/ok.png'
START = './img/start.png'
RESUPPLY = './img/resupply.png'
PLANNING = './img/planning.png'
PLANNING_ACT = './img/planning_active.png'
EXECUTE = './img/execute.png'
POINT1 = './img/point1.png'
POINT2 = './img/point2.png'
RETURN_BTN = './img/return.png'
ZERO_TWO = './img/zerotwo.png'
BATTLE = './img/battle.png'
BATTLE_RESULT = './img/battle_result.png'
FORMATION = './img/formation.png'
COMBAT_EFFECTIVENESS = './img/ce.png'
REMOVE = './img/remove.png'
LEADER = './img/leader.png'
BACK_BTN = './img/back.png'

# states
STATE_NONE = 0
STATE_START_BATTLE = 1
STATE_SPAWN_MAIN_ECHELON = 2
STATE_DEPLOY_MAIN_ECHELON = 3
STATE_SPAWN_SECOND_ECHELON = 4
STATE_DEPLOY_SECOND_ECHELON = 5
STATE_START_GAME = 6
STATE_VIEW_MAIN_ECHELON = 7
STATE_RESUPPLY = 8
STATE_PLANNING = 9
STATE_SELECT_POINT1 = 10
STATE_SELECT_POINT2 = 11
STATE_EXECUTE = 12
STATE_WAIT = 13
STATE_PREPARE_FORMATION = 14
STATE_SET_FORMATION = 15
STATE_SWAP_DPS = 16
STATE_SELECT_DPS = 17
STATE_BACK_TO_GAME = 18

def getImagePos(img):
    pos = ui.locateOnScreen(img, confidence=0.8)
    if (pos != None):
        return ui.freeArea(pos)
    return None


def withRandPos(pos, pixels=10):
    return (pos[0] + randint(-pixels, pixels), pos[1] + randint(-pixels, pixels))


def clickAt(img, doubleClick=False, offset=None):
    pos = getImagePos(img)
    if (pos):
        if (offset):
            pos = (pos[0] + offset[0], pos[1] + offset[1])

        # add random offset
        pos = withRandPos(pos)

        if (doubleClick):
            ui.doubleClick(pos, interval=0.4)
        else:
            ui.click(pos)
        return True
    return False


def doTask(img, result, doubleClick=False):
    resPos = getImagePos(result)
    if (resPos):
        return True

    clickAt(img, doubleClick)
    return False


class Bot:
    def __init__(self):
        self.state = STATE_NONE
        self.center = (700, 400)
        self.freeArea = (1161, 449)

    def loop(self):
        nextThink = 1.0

        if (self.state == STATE_START_BATTLE):
            # Spawn main echelon
            if (doTask(ZERO_TWO, BATTLE)):
                time.sleep(0.5)
                clickAt(BATTLE)
                nextThink = 0.5
                self.state = STATE_PREPARE_FORMATION
            else:
                nextThink = 0.1

        elif (self.state == STATE_PREPARE_FORMATION):
            if (doTask(CMD_POST, FORMATION)):
                nextThink = 0.8
                self.state = STATE_SET_FORMATION
            else:
                nextThink = 0.1

        elif (self.state == STATE_SET_FORMATION):
            if (doTask(FORMATION, COMBAT_EFFECTIVENESS)):
                nextThink = 0.4
                self.state = STATE_SWAP_DPS
            else:
                nextThink = 0.1

        elif (self.state == STATE_SWAP_DPS):
            if (clickAt(COMBAT_EFFECTIVENESS, offset=(-200, 100))):
                nextThink = 0.4
                self.state = STATE_SELECT_DPS
            else:
                nextThink = 0.1

        elif (self.state == STATE_SELECT_DPS):
            if (clickAt(LEADER, offset=(100, -100))):
                nextThink = 0.4
                self.state = STATE_BACK_TO_GAME
            else:
                ui.moveTo(withRandPos(self.center, 40))
                ui.scroll(-50)
                nextThink = 0.1

        elif (self.state == STATE_BACK_TO_GAME):
            if (clickAt(BACK_BTN)):
                nextThink = 0.4
                self.state = STATE_SPAWN_MAIN_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_SPAWN_MAIN_ECHELON):
            # Spawn main echelon
            if (doTask(CMD_POST, OK_BTN)):
                nextThink = 0.4
                self.state = STATE_DEPLOY_MAIN_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_SPAWN_MAIN_ECHELON):
            # Spawn main echelon
            if (doTask(CMD_POST, OK_BTN)):
                nextThink = 0.4
                self.state = STATE_DEPLOY_MAIN_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_DEPLOY_MAIN_ECHELON):
            # Deploy echelon
            if (doTask(OK_BTN, START)):
                nextThink = 0.4
                self.state = STATE_START_GAME
            else:
                nextThink = 0.1

        elif (self.state == STATE_START_GAME):
            # Start game
            if (clickAt(START)):
                nextThink = 0.5
                self.state = STATE_SPAWN_SECOND_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_SPAWN_SECOND_ECHELON):
            # Spawn second echelon
            if (doTask(HELIPORT, OK_BTN)):
                nextThink = 0.5
                self.state = STATE_SET_FORMATION
            else:
                nextThink = 0.1

        elif (self.state == STATE_DEPLOY_SECOND_ECHELON):
            # Deploy echelon
            if (doTask(OK_BTN, CMD_POST)):
                nextThink = 0.5
                self.state = STATE_VIEW_MAIN_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_VIEW_MAIN_ECHELON):
            # View main echelon
            #if (doTask(CMD_POST, RESUPPLY, doubleClick=True)):
            if (clickAt(CMD_POST)):
                nextThink = 0.5
                self.state = STATE_PLANNING
            else:
                nextThink = 0.1

        """
        elif (self.state == STATE_RESUPPLY):
            # Resupply main echelon
            if (clickAt(RESUPPLY)):
                nextThink = 0.5
                self.state = STATE_PLANNING
            else:
                nextThink = 0.1
        """

        elif (self.state == STATE_PLANNING):
            # Resupply main echelon
            if (doTask(PLANNING, PLANNING_ACT)):
                nextThink = 0.5
                self.state = STATE_SELECT_POINT1
            else:
                nextThink = 0.1

        elif (self.state == STATE_SELECT_POINT1):
            # Resupply main echelon
            if (clickAt(POINT1, offset=(-40, 0))):
                nextThink = 0.5
                self.state = STATE_SELECT_POINT2
            else:
                nextThink = 0.5
                ui.moveTo(withRandPos(self.freeArea, 40))
                ui.scroll(50)

        elif (self.state == STATE_SELECT_POINT2):
            # Resupply main echelon
            if (clickAt(POINT2, offset=(-20, -20))):
                nextThink = 0.5
                self.state = STATE_EXECUTE
            else:
                nextThink = 0.5
                ui.moveTo(withRandPos(self.freeArea, 30))
                ui.scroll(50)

        elif (self.state == STATE_EXECUTE):
            # Resupply main echelon
            if (clickAt(EXECUTE)):
                nextThink = 0.5
                self.state = STATE_WAIT
            else:
                nextThink = 0.1

        elif (self.state == STATE_WAIT):
            returnPos = getImagePos(RETURN_BTN)
            battleRes = getImagePos(BATTLE_RESULT)

            if (returnPos):
                time.sleep(3.0)
                for i in range(6):
                    ui.click(withRandPos(self.freeArea, 40))
                    time.sleep(0.6)

                nextThink = 1.0
                self.state = STATE_START_BATTLE

            elif (battleRes):
                for i in range(6):
                    ui.click(withRandPos(self.freeArea, 40))
                    time.sleep(0.5)

            else:
                nextThink = 0.1

        time.sleep(nextThink)

    def main(self):
        time.sleep(3.0)

        self.state = STATE_START_BATTLE

        while (True):
            self.loop()


bot = Bot()
bot.main()
