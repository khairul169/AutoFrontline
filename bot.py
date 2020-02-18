import pyautogui as ui
import time
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
LEADER = './img/leader.png'
BACK_BTN = './img/back.png'

TDOLL_FULL = './img/tdollfull.png'
RETIREMENT = './img/retirement.png'
SELECT_DOLL = './img/select_doll.png'
SMART_SELECT = './img/smart_select.png'
OK_RETIRE = './img/ok_retire.png'
DISMANTLE = './img/dismantle.png'
RETURN_BASE = './img/return_base.png'
COMBAT = './img/combat.png'

LOW_HP = './img/low_hp.png'
OK_REPAIR = './img/ok_repair.png'

LOGISTIC_RESULT = './img/logistic.png'
OK_LOGISTIC = './img/ok_logistic.png'
LOAD_SUPPLY = './img/load_supply.png'

# states
STATE_NONE = 0
STATE_START_BATTLE = 1
STATE_SPAWN_MAIN_ECHELON = 2
STATE_DEPLOY_MAIN_ECHELON = 3
STATE_SPAWN_SECOND_ECHELON = 4
STATE_DEPLOY_SECOND_ECHELON = 5
STATE_START_GAME = 6
STATE_VIEW_DPS = 7
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
STATE_RETIRE = 19
STATE_BEGIN_COMBAT = 20


def getImagePos(img, confidence=0.8):
    pos = ui.locateOnScreen(img, confidence=confidence)
    if (pos != None):
        return ui.center(pos)
    return None


def withRandPos(pos, pixels=10):
    return (pos[0] + randint(-pixels, pixels), pos[1] + randint(-pixels, pixels))


def clickAt(img, doubleClick=False, offset=None, confidence=0.8):
    pos = getImagePos(img, confidence)
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
        self.center = (700, 400)
        self.freeArea = (1161, 449)

        # State
        self.state = STATE_NONE
        self.attempt = 0
        self.repair = False
        self.chapterFound = False

    def loop(self):
        # Variables
        nextThink = 1.0

        # States
        if (self.state == STATE_BEGIN_COMBAT):
            if (clickAt(LOGISTIC_RESULT)):
                time.sleep(1.0)
                clickAt(OK_LOGISTIC)
                nextThink = 1.0
            elif (doTask(COMBAT, ZERO_TWO)):
                nextThink = 0.5
                self.state = STATE_START_BATTLE
            else:
                nextThink = 0.1

        elif (self.state == STATE_START_BATTLE):
            chapterBtn = getImagePos(ZERO_TWO)
            
            
            # Spawn main echelon
            if (not self.chapterFound):
                if (chapterBtn):
                    self.chapterFound = True
                nextThink = 0.2
            
            elif (doTask(ZERO_TWO, BATTLE)):
                time.sleep(0.4)
                clickAt(BATTLE)
                time.sleep(0.4)

                if (clickAt(TDOLL_FULL)):
                    nextThink = 1.0
                    self.state = STATE_RETIRE
                    #self.state = STATE_BEGIN_COMBAT
                    print("Retiring..")

                else:
                    nextThink = 0.5
                    self.state = STATE_PREPARE_FORMATION
                
                self.chapterFound = False
            else:
                nextThink = 0.2

        elif (self.state == STATE_PREPARE_FORMATION):
            if (doTask(CMD_POST, FORMATION)):
                nextThink = 0.0
                self.state = STATE_SET_FORMATION
            else:
                nextThink = 0.1

        elif (self.state == STATE_SET_FORMATION):
            lowHp = getImagePos(LOW_HP)
            
            if (lowHp and not self.repair):
                print("Repairing...")
                clickAt(LOW_HP)
                time.sleep(1.5)
                clickAt(OK_REPAIR, confidence=0.9)
                nextThink = 1.5
                self.repair = True
            
            elif (clickAt(FORMATION)):
                nextThink = 1.8
                self.state = STATE_SWAP_DPS
                self.repair = False
            else:
                nextThink = 0.5

        elif (self.state == STATE_SWAP_DPS):
            if (clickAt(COMBAT_EFFECTIVENESS, offset=(-100, 100))):
                nextThink = 2.5
                self.state = STATE_SELECT_DPS
            else:
                nextThink = 0.1

        elif (self.state == STATE_SELECT_DPS):
            if (clickAt(LEADER, offset=(50, -100))):
                nextThink = 0.1
                self.state = STATE_BACK_TO_GAME
            else:
                ui.moveTo(withRandPos(self.center, 40))
                ui.scroll(-150)
                nextThink = 0.3

        elif (self.state == STATE_BACK_TO_GAME):
            if (doTask(BACK_BTN, CMD_POST)):
                nextThink = 0.0
                self.state = STATE_SPAWN_MAIN_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_SPAWN_MAIN_ECHELON):
            # Spawn main echelon
            if (doTask(CMD_POST, OK_BTN)):
                nextThink = 0.1
                self.state = STATE_DEPLOY_MAIN_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_DEPLOY_MAIN_ECHELON):
            # Deploy echelon
            if (doTask(OK_BTN, START)):
                nextThink = 0.0
                self.state = STATE_START_GAME
            else:
                nextThink = 0.05

        elif (self.state == STATE_START_GAME):
            # Start game
            if (clickAt(START)):
                nextThink = 0.8
                self.state = STATE_SPAWN_SECOND_ECHELON
                
                self.attempt += 1
                print("Attempt", self.attempt)
            else:
                nextThink = 0.1

        elif (self.state == STATE_SPAWN_SECOND_ECHELON):
            # Spawn second echelon
            if (doTask(HELIPORT, OK_BTN)):
                nextThink = 0.1
                self.state = STATE_DEPLOY_SECOND_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_DEPLOY_SECOND_ECHELON):
            # Deploy echelon
            if (doTask(OK_BTN, HELIPORT)):
                nextThink = 0.1
                self.state = STATE_VIEW_DPS
            else:
                nextThink = 0.1

        elif (self.state == STATE_VIEW_DPS):
            # View dps echelon
            if (doTask(HELIPORT, RESUPPLY, doubleClick=True)):
                nextThink = 0.0
                self.state = STATE_RESUPPLY
            else:
                nextThink = 0.1

        elif (self.state == STATE_RESUPPLY):
            # View dps echelon
            if (doTask(RESUPPLY, PLANNING)):
                isLoading = True

                while (isLoading):
                    ui.sleep(1.5)
                    clickAt(CMD_POST)
                    isLoading = getImagePos(LOAD_SUPPLY)
                
                nextThink = 0.1
                self.state = STATE_PLANNING
            else:
                nextThink = 0.1

        elif (self.state == STATE_PLANNING):
            # Resupply main echelon
            if (doTask(PLANNING, PLANNING_ACT)):
                nextThink = 0.2
                self.state = STATE_SELECT_POINT1
            else:
                nextThink = 0.1

        elif (self.state == STATE_SELECT_POINT1):
            # Resupply main echelon
            if (clickAt(POINT1, offset=(-20, 0))):
                nextThink = 0.1
                self.state = STATE_SELECT_POINT2
            else:
                nextThink = 0.4
                ui.moveTo(withRandPos(self.freeArea, 40))
                ui.scroll(200)

        elif (self.state == STATE_SELECT_POINT2):
            # Resupply main echelon
            if (clickAt(POINT2, offset=(-20, -20))):
                nextThink = 0.2
                self.state = STATE_EXECUTE
            else:
                nextThink = 0.4
                ui.moveTo(withRandPos(self.freeArea, 30))
                ui.scroll(150)

        elif (self.state == STATE_EXECUTE):
            # Resupply main echelon
            if (clickAt(EXECUTE)):
                nextThink = 0.1
                self.state = STATE_WAIT
            else:
                nextThink = 0.1

        elif (self.state == STATE_WAIT):
            returnPos = getImagePos(RETURN_BTN)
            battleRes = getImagePos(BATTLE_RESULT)

            if (returnPos):
                time.sleep(1.5)
                for i in range(6):
                    ui.click(withRandPos(self.freeArea, 40))
                    time.sleep(0.5)

                nextThink = 1.0
                self.state = STATE_START_BATTLE

            elif (battleRes):
                for i in range(6):
                    ui.click(withRandPos(self.freeArea, 40))
                    time.sleep(0.3)

            else:
                nextThink = 0.1

        elif (self.state == STATE_RETIRE):
            time.sleep(3.0)

            #print("RETIREMENT")

            clickAt(RETIREMENT)
            time.sleep(0.5)

            #print("SELECT_DOLL")

            clickAt(SELECT_DOLL)
            time.sleep(1.0)

            #print("SMART_SELECT")

            clickAt(SMART_SELECT)
            time.sleep(0.5)

            #print("OK_RETIRE")

            clickAt(OK_RETIRE)
            time.sleep(0.5)

            #print("DISMANTLE")

            clickAt(DISMANTLE)
            time.sleep(3.5)

            #print("RETURN_BASE")
            #clickAt(RETURN_BASE)
            
            combatBtn = False
            logisticRes = False

            while (not combatBtn and not logisticRes):
                clickAt(RETURN_BASE)
                time.sleep(0.2)
                combatBtn = getImagePos(COMBAT)
                logisticRes = getImagePos(LOGISTIC_RESULT)

            self.state = STATE_BEGIN_COMBAT
            nextThink = 0.1

        if (nextThink > 0.0):
            time.sleep(nextThink)

    def main(self):
        self.state = STATE_BEGIN_COMBAT
        ui.PAUSE = 0.0

        try:
            time.sleep(3.0)
            while (True):
                self.loop()
        except KeyboardInterrupt:
            print("Exiting..")


bot = Bot()
bot.main()
