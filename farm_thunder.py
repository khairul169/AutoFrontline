import pyautogui as ui
import time
from random import randint

# images
CMD_POST = './farm_thunder/cp.png'
HELIPORT = './img/heliport.png'
OK_BTN = './img/ok.png'
START = './img/start.png'
RESUPPLY = './img/resupply.png'
PLANNING = './img/planning.png'
PLANNING_ACT = './img/planning_active.png'
EXECUTE = './img/execute.png'
POINT1 = './farm_thunder/point1.png'
POINT2 = './farm_thunder/point2.png'
POINT3 = './farm_thunder/point3.png'
POINT4 = './farm_thunder/point4.png'
POINT5 = './farm_thunder/point5.png'
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

TURN3 = './farm_thunder/turn3.png'
TERMINATE = './farm_thunder/terminate.png'
RESTART = './farm_thunder/restart.png'

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

    def loop(self):
        # Variables
        nextThink = 1.0

        # States
        if (self.state == STATE_SPAWN_MAIN_ECHELON):
            # Spawn main echelon
            if (doTask(CMD_POST, OK_BTN)):
                nextThink = 0.0
                self.state = STATE_DEPLOY_MAIN_ECHELON
            else:
                nextThink = 0.1

        elif (self.state == STATE_DEPLOY_MAIN_ECHELON):
            # Deploy echelon
            if (doTask(OK_BTN, START)):
                nextThink = 0.0
                self.state = STATE_START_GAME
            else:
                nextThink = 0.1

        elif (self.state == STATE_START_GAME):
            # Start game
            if (clickAt(START)):
                nextThink = 0.2
                self.state = STATE_VIEW_DPS
            else:
                nextThink = 0.1

        elif (self.state == STATE_VIEW_DPS):
            # View dps echelon
            if (doTask(CMD_POST, RESUPPLY, doubleClick=True)):
                nextThink = 0.0
                self.state = STATE_RESUPPLY
            else:
                nextThink = 0.1

        elif (self.state == STATE_RESUPPLY):
            # View dps echelon
            if (doTask(RESUPPLY, PLANNING)):
                nextThink = 0.1
                self.state = STATE_PLANNING
            else:
                nextThink = 0.1

        elif (self.state == STATE_PLANNING):
            # Resupply main echelon
            if (doTask(PLANNING, PLANNING_ACT)):
                nextThink = 0.1
                self.state = STATE_SELECT_POINT1
            else:
                nextThink = 0.1

        elif (self.state == STATE_SELECT_POINT1):
            # Resupply main echelon
            if (clickAt(POINT1, offset=(-40, -40))):
                time.sleep(0.1)
                #clickAt(POINT2)
                #time.sleep(0.1)

                for i in range(3):
                    ui.moveTo(withRandPos(self.center, 5))
                    ui.scroll(-200)
                    time.sleep(0.5)

                time.sleep(0.1)

                clickAt(POINT3)
                time.sleep(0.1)
                clickAt(POINT4)
                time.sleep(0.1)
                clickAt(POINT5, offset=(-40, -40))

                nextThink = 0.5
                self.state = STATE_EXECUTE
            else:
                nextThink = 0.2

        elif (self.state == STATE_EXECUTE):
            # Resupply main echelon
            if (clickAt(EXECUTE)):
                nextThink = 0.5
                self.state = STATE_WAIT
            else:
                nextThink = 0.1

        elif (self.state == STATE_WAIT):
            battleRes = getImagePos(BATTLE_RESULT)
            turn3Pos = getImagePos(TURN3)

            if (battleRes):
                for i in range(5):
                    ui.click(withRandPos(self.freeArea, 40))
                    time.sleep(0.3)

            elif (turn3Pos):
                time.sleep(5.5)
                clickAt(TERMINATE)
                time.sleep(0.8)
                clickAt(RESTART)

                nextThink = 2.0
                self.state = STATE_SPAWN_MAIN_ECHELON

            else:
                nextThink = 0.5

        if (nextThink > 0.0):
            time.sleep(nextThink)

    def main(self):
        self.state = STATE_SPAWN_MAIN_ECHELON
        ui.PAUSE = 0.0

        try:
            time.sleep(3.0)
            while (True):
                self.loop()
        except KeyboardInterrupt:
            print("Exiting..")


bot = Bot()
bot.main()
