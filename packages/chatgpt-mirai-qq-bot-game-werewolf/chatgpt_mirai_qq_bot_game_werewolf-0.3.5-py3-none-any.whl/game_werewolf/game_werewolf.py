from typing import Dict, Any, List
from bs4 import BeautifulSoup
from kirara_ai.logger import get_logger
from kirara_ai.llm.adapter import LLMBackendAdapter
from collections import Counter
import random
import time
from enum import Enum
from kirara_ai.llm.format.request import LLMChatRequest
from kirara_ai.llm.format.message import LLMChatMessage,LLMChatTextContent
import re
class Role(Enum):
    WEREWOLF = ("狼人", "夜晚可以选择一名玩家进行袭击,并和你的狼队友一起投票,可以通过袭击自己来骗解药。不要暴露自己和狼队友的身份。")
    VILLAGER = ("村民", "白天参与讨论和投票，试图找出狼人。")
    WITCH = ("女巫", "夜晚可以选择使用解药拯救一名玩家或使用毒药杀死一名玩家,一般都在第一天使用解药（无法救自己）,注意同守同救则被拯救玩家直接死亡，但是偶尔也要小心对方是狼人自刀骗解药。")
    SEER = ("预言家", "夜晚可以查验一名玩家的身份,没发现狼人前不会轻易透露身份。")
    GUARD = ("守卫", "夜晚可以选择一名玩家进行保护，第一天一般选择不守护,优先保护神职,注意同守同救则被守护玩家直接死亡。")

    def __init__(self, name: str, description: str):
        self._value_ = name
        self.description = description

class GameState(Enum):
    NIGHT = "Night"
    DAY = "Day"

logger = get_logger("GameWerewolf")

class Player:
    def __init__(self, role: Role, llm: LLMBackendAdapter,model_name:str):
        self.role = role
        self.number = 0
        self.alive = True
        self.protected = False
        self.chatLog = []  # 每个玩家独有的聊天记录
        self.hasSavePotion = False  # 女巫的解药
        self.hasKillPotion = False  # 女巫的毒药
        self.llm = llm  # LLM 实例
        self.model_name = model_name

    def updateSystem(self, message: str):
        # 记录系统消息到玩家的聊天记录
        self.chatLog.append(message)
    def extract_first_number(self,s: str) -> int:
        match = re.search(r'\d+', s)  # 查找第一个数字
        return int(match.group()) if match else None  # 返回数字或 None
    def requestVote(self, prompt: str, valid_targets: List[int]) -> int:
        # 使用 LLM 模拟玩家的投票
        message = f"已知信息{self.chatLog}\n本次任务:{prompt}，要求回复玩家编号，不用任何说明\n有效目标: {valid_targets}\n请投票（输入玩家编号,-1为弃票）:"
        logger.debug(message)

        for attempt in range(3):  # Retry up to 3 times
            try:
                response = self.llm.chat(LLMChatRequest(messages = [LLMChatMessage(role="system", content=[LLMChatTextContent(text="你是一个资深的狼人杀游戏玩家，请根据以下背景和要求进行投票")]),LLMChatMessage(role="user", content=[LLMChatTextContent(text=message)])],model=self.model_name))
                logger.debug(response)
                content = response.message.content[0].text.replace("\n","")
                vote = self.extract_first_number(content)
                return vote if vote in valid_targets else valid_targets[0]
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # If it's the last attempt, raise the error
                    raise

    def requestSpeech(self, prompt: str) -> str:
        # 使用 LLM 模拟玩家的发言
        message = f"已知信息{self.chatLog}\n{prompt}\n本次任务:请开始你的发言:"
        logger.debug(message)

        for attempt in range(3):  # Retry up to 3 times
            try:
                response = self.llm.chat(LLMChatRequest(messages = [LLMChatMessage(role="system", content=[LLMChatTextContent(text="你是一个资深的狼人杀游戏玩家(女巫属于神职阵营)，请在没把握把所有对手淘汰的情况下透露自己身份，请根据以下背景和要求直接进行简要发言，不要输出分析过程")]),LLMChatMessage(role="user", content=[LLMChatTextContent(text=message)])],model=self.model_name))
                return response.message.content[0].text.replace("\n","")  # 返回 LLM 的发言内容
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # If it's the last attempt, raise the error
                    raise

class Witch(Player):
    def __init__(self, llm: LLMBackendAdapter):
        super().__init__(Role.WITCH, llm)
        self.hasSavePotion = True  # 初始时女巫有解药
        self.hasKillPotion = True  # 初始时女巫有毒药

class GameWerewolf:

    def __init__(self, werewolf_count:int = 2,willager_count:int =2, llm: LLMBackendAdapter = None,model_name:str=""):
        self.werewolf_count = werewolf_count
        self.willager_count = willager_count
        self.llm = llm
        self.model_name= model_name
        self.players = []
        self.state = GameState.NIGHT
        self.day = 1
        self.night_deaths = []
        self.current_player_index = 0  # 当前轮到的玩家索引
        self.human_player_index = None  # 存储人类玩家的索引
        self.speech = None  # 存储人类玩家的操作
        self.game_progress = {}  # 存储当前游戏进程和信息
        self.votes = {}
        self.execute_player_num = None  # 存储人类玩家的操作
        self.process = 1
        self.firstKill = True
        self.killNum = None
        self.chatAllLog = []



    def play(self, speech, llm: LLMBackendAdapter = None,model_name: str=""):
        logger.debug(speech)
        if speech == "开始":
            self.start_game()
            self.human_player_index = random.randint(0, len(self.players) - 1)
            self.chatAllLog.append(f"人类玩家的编号是{self.human_player_index+1},身份是{self.players[self.human_player_index].role._value_}")
            speech = None
        # 继续游戏进程
        for player in self.players:
            player.llm = llm
            player.model_name = model_name
        self.speech = speech
        try :
            while not self.check_win():
                logger.debug("update_day")
                update_day =  self.update_day()
                if self.check_win():
                    info = "\n".join(self.chatAllLog)
                    self.players[self.human_player_index].chatLog = []
                    self.chatAllLog = []
                    return self.check_win()+"\n\n游戏总记录:\n"+info
                if update_day and isinstance(update_day,str):
                    info = "\n#".join(self.players[self.human_player_index].chatLog)
                    self.players[self.human_player_index].chatLog = []
                    return f"当前游戏信息:\n{info}\n"+update_day

        except Exception as e:
            logger.error(f"Error play werewolf: {e}")
            self.speech=0
        return self.check_win()

    def start_game(self):
        self.players = [Player(role=None, llm=self.llm,model_name = self.model_name) for _ in range(3+self.werewolf_count+self.willager_count)]  # Create players based on player_count
        self.assign_roles()
        self.process=1
        self.day=1
        self.votes = {}
        logger.debug(self.players)

    def assign_roles(self):
        total_players = len(self.players)
        if total_players < 5:
            raise ValueError("游戏需要至少5名玩家")

        special_roles = [Role.SEER, Role.WITCH]
        if total_players >= 5:
            special_roles.append(Role.GUARD)

        werewolf_count = self.werewolf_count
        villager_count = self.willager_count

        if villager_count < 1:
            raise ValueError("角色分配失败：村民数量不足")

        roles = (
                [Role.WEREWOLF] * werewolf_count +
                special_roles +
                [Role.VILLAGER] * villager_count
        )
        random.shuffle(roles)
        roleNames = [f"{werewolf_count}{Role.WEREWOLF._value_}",f"{villager_count}{Role.VILLAGER._value_}"
            ,f"1{Role.SEER._value_}",f"1{Role.WITCH._value_}",f"1{Role.GUARD._value_}"]

        werewolves = []  # 用于存储狼的编号
        for i, player in enumerate(self.players):
            player.number = i + 1
            player.role = roles[i]
            player.alive = True
            if player.role == Role.WEREWOLF:
                werewolves.append(player.number)  # 记录狼的编号
            if player.role == Role.WITCH:
                player.hasSavePotion = True
                player.hasKillPotion = True
            player.updateSystem(f"你的身份是{roles[i]._value_}，你的编号是{player.number}，你的身份描述：{roles[i].description}, 当前玩家身份有{roleNames}")
            self.chatAllLog.append(f"{player.number}号玩家的身份是{roles[i]._value_}")

        # 公告狼队友的信息
        for wolf in werewolves:
            self.get_player(wolf).updateSystem(f"你的队友是: {', '.join(map(str, werewolves))}（狼队友）")

    def update_day(self):

        self.state = GameState.NIGHT
        self.night_deaths = []
        night_actions = self.night_actions()
        if night_actions:
            return night_actions
        target_player = self.get_player(self.killNum)
        logger.debug(f"{self.killNum}状态:{target_player.alive},第{self.day}天,是否首杀:{self.firstKill}")
        if not target_player.alive and self.day == 1  and self.firstKill:
            if target_player.number == self.human_player_index + 1 and not self.speech:
                return f"首晚被杀，请发表遗言";
            last_words = target_player.requestSpeech("你在第一晚被刀了,请发表遗言")  if target_player.number != self.human_player_index+1 else self.speech
            self.speech = None
            self.broadcast(f"玩家 {self.killNum} 的遗言：{last_words}")
        self.firstKill = False
        self.state = GameState.DAY
        day_actions = self.day_actions()
        if day_actions:
            return day_actions
        self.day += 1
        return False

    def night_actions(self):
        # Guard action
        logger.debug(f"guard_action,{self.process},{self.current_player_index+1}, {self.human_player_index+1} ,{self.speech}")
        guard = self.guard_action()
        if not guard:
            return "请选择要守护的玩家（输入玩家编号）"
        # Werewolf action
        logger.debug(f"werewolf_action,{self.process},{self.current_player_index+1}, {self.human_player_index+1} ,{self.speech}")
        attack_target = self.werewolf_action()
        if not attack_target:
            return "请选择要袭击的玩家（输入玩家编号）"
        # Witch action
        logger.debug(f"witch_action,{self.process},{self.current_player_index+1}, {self.human_player_index+1} ,{self.speech}")
        witch_action = self.witch_action(attack_target)
        if witch_action:
            return witch_action

        if self.check_win():
            return True
        # Seer action
        logger.debug(f"seer_action,{self.process},{self.current_player_index+1}, {self.human_player_index+1} ,{self.speech}")
        seer_action = self.seer_action()
        if not seer_action:
            return "请选择要查验的玩家（输入玩家编号）"
        return False

    def day_actions(self):
        logger.debug(f"daytime_discussion,{self.process},{self.current_player_index+1}, {self.human_player_index+1} ,{self.speech}")
        daytime_discussion = self.daytime_discussion()
        candidates = [p.number for p in self.players if p.alive ]
        no_alive = [p.number for p in self.players if not p.alive ]
        if not daytime_discussion:
            return f"当前存活玩家：{candidates},死亡玩家：{no_alive},请发表你的看法"
        logger.debug(f"daytime_voting,{self.process},{self.current_player_index+1}, {self.human_player_index+1} ,{self.speech}")
        eliminated = self.daytime_voting()
        if not eliminated:
            return "请选择要放逐的玩家（输入玩家编号，-1 为弃票）"
        if eliminated and isinstance(eliminated,int):
            logger.debug(f"execute_player,{self.process},{self.current_player_index+1}, {self.human_player_index+1} ,{self.speech}")
            execute_player = self.execute_player(eliminated)
            if not execute_player:
                return "请发表遗言"
            self.votes={}
            self.execute_player_num = None

        return False

    def guard_action(self):
        if self.process == 1:
            for guard in [p for p in self.players if p.role == Role.GUARD and p.alive and p.number >= self.current_player_index+1]:
                if guard.number == self.human_player_index+1 and not self.speech:
                    self.current_player_index = guard.number - 1
                    return False
                candidates = [p.number for p in self.players if p.alive]
                vote = guard.requestVote("请选择要守护的玩家（输入玩家编号）", valid_targets=candidates+[-1]) if guard.number != self.human_player_index+1 else self.speech
                self.speech = None
                target_player = self.get_player(int(vote))
                if target_player:
                    target_player.protected = True
                    logger.debug(f"{guard.number}选择守护玩家{vote}")
                    guard.updateSystem(f"你选择守护玩家 {vote}")
                    self.chatAllLog.append(f"{guard.number}选择守护玩家{vote}")
            self.current_player_index = 0
            self.process= 2
        return True

    def werewolf_action(self):
        if self.process == 2:
            candidates = [p.number for p in self.players if p.alive ]
            for wolf in [p for p in self.players if p.role == Role.WEREWOLF and p.alive  and p.number >= self.current_player_index+1]:
                if wolf.number == self.human_player_index+1 and not self.speech:
                    self.current_player_index = wolf.number - 1
                    return False
                vote = wolf.requestVote(f"当前第{self.day}天,请选择袭击目标（存活玩家：{candidates}）", valid_targets=candidates) if wolf.number != self.human_player_index+1 else self.speech
                if self.speech:
                    self.killNum = int(self.speech)
                    self.current_player_index = 0
                    self.process = 3
                    break
                self.killNum = int(vote)
                self.speech = None
                logger.debug(f"{wolf.number}选择袭击玩家{vote}")

            self.current_player_index = 0
            self.process = 3
            for wolf in [p for p in self.players if p.role == Role.WEREWOLF and p.alive ]:
                wolf.updateSystem(f"您选择袭击玩家{self.killNum}")
            self.chatAllLog.append(f"狼人共同选择袭击玩家{self.killNum}")
        return self.killNum

    def witch_action(self, attack_target):
        target_player = self.get_player(attack_target)

        if self.process == 3:
            if target_player and target_player.alive and not target_player.protected:
                target_player.alive = False
                self.night_deaths.append(target_player.number)
            if target_player and target_player.protected and not self.speech:
                logger.debug(f"玩家 {attack_target} 被守卫保护，未受袭击")
                self.chatAllLog.append(f"玩家 {attack_target} 被守卫保护，未受袭击")
            witch = next((p for p in self.players if p.role == Role.WITCH and p.alive), None)
            if not witch:
                self.current_player_index = 0
                self.process = 5
                return False


            if witch.hasSavePotion and witch.number != target_player.number:
                if witch.number == self.human_player_index+1 and not self.speech:
                    self.current_player_index = witch.number - 1
                    return f"{attack_target}被杀， 是否使用解药？（1: 是，0: 否）"
                use_potion = witch.requestVote(f"当前第{self.day}天,{attack_target}被杀， 是否使用解药？（1: 是，0: 否）", valid_targets=[0, 1]) if witch.number != self.human_player_index+1 else self.speech
                self.speech = None

                if int(use_potion) == 1:
                    target_player.alive = True
                    witch.hasSavePotion = False
                    logger.debug(f"{witch.number}使用了解药拯救玩家 {attack_target}")
                    witch.updateSystem(f"你使用了解药拯救玩家 {attack_target}")
                    self.chatAllLog.append(f"{witch.number}使用了解药拯救玩家 {attack_target}")
                    self.process = 5
                    if target_player.protected:
                        target_player.alive = False
                        self.chatAllLog.append(f"触发同守同救，玩家 {attack_target}立即死亡")
                else:
                    self.process = 4
            self.current_player_index = 0
            if self.check_win():
                return self.check_win()

        if self.process == 3 or self.process == 4:
            witch = next((p for p in self.players if p.role == Role.WITCH and p.alive), None)
            if not witch:
                self.current_player_index = 0
                self.process = 5
                return False

            if witch.hasKillPotion:
                if witch.number == self.human_player_index+1 and not self.speech:
                    self.current_player_index = witch.number - 1
                    return f"请选择要毒杀的玩家（-1 表示不使用）"
                target = witch.requestVote(f"当前第{self.day}天,请选择要毒杀的玩家（-1 表示不使用，第一天一般不使用）", valid_targets=[p.number for p in self.players if p.alive and p.number != witch.number] + [-1]) if witch.number != self.human_player_index+1 else self.speech
                self.speech = None
                if int(target) != -1:
                    self.get_player(int(target)).alive = False
                    witch.hasKillPotion = False
                    self.night_deaths.append(int(target))
                    logger.debug(f"{witch.number}使用了毒药毒杀玩家 {target}")
                    witch.updateSystem(f"你毒杀了玩家 {int(target)}")
                    self.chatAllLog.append(f"{witch.number}使用了毒药毒杀玩家 {target}")

                    if self.check_win():
                        return self.check_win()
            self.process = 5
            self.current_player_index = 0
        return False
    def seer_action(self):
        if self.process == 5:
            for seer in [p for p in self.players if p.role == Role.SEER and (p.alive or self.killNum == p.number) and p.number >= self.current_player_index+1]:
                if seer.number == self.human_player_index+1 and not self.speech:
                    self.current_player_index = seer.number - 1
                    return False
                target = seer.requestVote(f"当前第{self.day}天,请选择要查验的玩家", valid_targets=[p.number for p in self.players if p.alive and p.number != seer.number]) if seer.number != self.human_player_index+1 else self.speech
                self.speech = None
                if target:
                    role_info = self.get_player(int(target)).role
                    seer.updateSystem(f"你查验了玩家 {target} 的身份是：{role_info._value_}")
                    logger.debug(f"{seer.number}查验了玩家{target} 的身份是：{role_info._value_}")
                    self.chatAllLog.append(f"{seer.number}查验了玩家{target} 的身份是：{role_info._value_}")
            self.process = 6
            self.current_player_index = 0
            self.broadcast(f"---第{self.day}天晚上已结束---")
        return True

    def daytime_discussion(self):
        if self.process == 6:
            candidates = [p.number for p in self.players if p.alive ]
            no_alive = [p.number for p in self.players if not p.alive ]
            for player in self.players:
                logger.debug(f"{player.number}号玩家开始发言,当前顺序:{self.current_player_index + 1},人类发言顺序{self.human_player_index+1},人类输入:{self.speech}")
                if player.alive and player.number >= self.current_player_index + 1:
                    if player.number == self.human_player_index+1 and not self.speech:
                        self.current_player_index = player.number - 1
                        return False
                    speech = player.requestSpeech(f"当前第{self.day}天,请发表你的看法,还存活的玩家有{candidates},死亡玩家有{no_alive}") if player.number != self.human_player_index+1 else self.speech
                    self.speech = None
                    self.broadcast(f"玩家 {player.number} 说：{speech}")
            self.process = 7
            self.current_player_index = 0
        return True
    def daytime_voting(self):
        if self.process == 7:
            candidates = [p.number for p in self.players if p.alive ]

            for voter in self.players:
                if voter.alive and voter.number == self.human_player_index+1 and not self.speech:
                    logger.debug(f"{voter.number}请选择要放逐的玩家:{self.speech}")
                    self.current_player_index = voter.number - 1
                    return False
                if voter.alive:
                    vote = voter.requestVote(f"请选择要放逐的玩家（存活玩家：{candidates+[-1]}）", valid_targets=candidates + [-1]) if voter.number != self.human_player_index+1 else self.speech
                    self.votes[voter.number] = int(vote)
            self.process = 8
            self.speech = None
            self.current_player_index = 0
        logger.debug(self.votes)
        return self.resolve_votes(self.votes, "放逐", is_public=True)

    def resolve_votes(self, votes, action_name, is_public=False):
        valid_votes = [v for v in votes.values() if v != -1]
        if not valid_votes:
            self.broadcast(f"本次{action_name}未达成共识")
            return True
        counter = Counter(valid_votes)
        max_count = counter.most_common(1)[0][1]
        candidates = [num for num, cnt in counter.items() if cnt == max_count]
        if len(candidates) > 1:
            result = random.choice(candidates)
            msg = f"平票！随机选择玩家 {result}"
        else:
            result = candidates[0]
            msg = f"达成共识选择玩家 {result}"
        if is_public:
            self.broadcast(msg)
        logger.debug(msg)
        return result

    def check_win(self) -> bool:
        logger.debug("check_win")
        alive_players = [p for p in self.players if p.alive]
        werewolves = [p for p in alive_players if p.role == Role.WEREWOLF]
        villagers = [p for p in alive_players if p.role != Role.WEREWOLF]
        if not werewolves:
            return "好人阵营胜利"  # Villagers win
        if len(werewolves) >= len(villagers):
            return "狼人阵营胜利"  # Werewolves win
        return False

    def get_player(self, number: int):
        for player in self.players:
            if player.number == number:
                return player
        return None

    def broadcast(self, message: str):
        for player in self.players:
            player.updateSystem(message)
        self.chatAllLog.append(message)

    def execute_player(self, number):
        if self.process == 8:
            player = self.get_player(number)
            if player:
                player.alive = False
                votes = []
                for index, vote in self.votes.items():
                    votes.append(f"{index}投{vote}")
                votesStr = ",".join(votes)
                self.broadcast(f"玩家 {number} 被放逐,票型:{votesStr}")
                if self.check_win():
                    return True

                if player.number == self.human_player_index + 1 and not self.speech:
                    self.execute_player_num = number
                    return False
                last_words = player.requestSpeech("当前第{self.day}天,请发表遗言(不要透露狼队友身份)") if player.number != self.human_player_index + 1 else self.speech
                self.speech = None
                self.broadcast(f"玩家 {number} 的遗言：{last_words}")
            self.process = 1
            self.current_player_index = 0
            self.broadcast(f"---第{self.day+1}天白天已结束---")
        return True

