from typing import Any, Dict, List, Optional, Annotated
from kirara_ai.workflow.core.block import Block, Input, Output, ParamMeta
from kirara_ai.im.message import IMMessage, TextMessage, VoiceMessage
from kirara_ai.im.sender import ChatSender
from .game_werewolf import GameWerewolf
import asyncio
from kirara_ai.logger import get_logger
from kirara_ai.ioc.container import DependencyContainer
from kirara_ai.llm.llm_manager import LLMManager
from kirara_ai.llm.llm_registry import LLMAbility
import threading
import json
import os
import pickle

logger = get_logger("GameWerewolf")

def model_name_options_provider(container: DependencyContainer, block: Block) -> List[str]:
    llm_manager: LLMManager = container.resolve(LLMManager)
    return llm_manager.get_supported_models(LLMAbility.TextChat)

class GameWerewolfBlock(Block):
    """音乐搜索Block"""
    name = "game_werewolf"

    inputs = {
        "speech": Input(name="speech", label="发言", data_type=str, description="发言"),
        "sender": Input("sender", "聊天对象", ChatSender, "聊天对象")
    }


    outputs = {
        "message": Output(name="message", label="IM消息", data_type=IMMessage, description="IM消息"),
    }
    container: DependencyContainer
    game_instances: Dict[str, GameWerewolf]  # 新增字典来存储实例

    def __init__(self, werewolf_count: Annotated[Optional[int],ParamMeta(label="狼人数量", description="狼人数量"),] = 1, willager_count: Annotated[Optional[int],ParamMeta(label="平民数量", description="平民数量"),] = 1,
      model_name: Annotated[
          Optional[str],
          ParamMeta(label="模型 ID", description="要使用的模型 ID", options_provider=model_name_options_provider),
      ] = None,
      segment_messages: Annotated[
          Optional[bool],
          ParamMeta(label="分段发送", description="是否按换行分段发送消息"),
      ] = False):
        super().__init__()
        self.game_instances = {}  # 初始化字典
        self.werewolf_count = werewolf_count
        self.willager_count = willager_count
        self.model_name = model_name
        self.segment_messages = segment_messages
        self.logger = logger
        # 修改存储路径到当前文件所在目录
        self.storage_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game_saves')
        os.makedirs(self.storage_dir, exist_ok=True)
        self.load_games()

    def get_storage_path(self, group_id):
        """获取特定游戏实例的存储路径"""
        return os.path.join(self.storage_dir, f'game_{group_id}.pkl')

    def save_game(self, group_id, game):
        """保存游戏实例到文件"""
        try:
            storage_path = self.get_storage_path(group_id)
            # 临时移除不可序列化的属性
            temp_llm = game.llm
            temp_locks = game.lock
            game.llm = None
            game.lock = None
            
            # 保存游戏状态
            with open(storage_path, 'wb') as f:
                pickle.dump(game, f)
            
            # 恢复属性
            game.llm = temp_llm
            game.lock = temp_locks
        except Exception as e:
            self.logger.error(f"Error saving game state: {e}")

    def load_games(self):
        """加载所有保存的游戏实例"""
        try:
            for filename in os.listdir(self.storage_dir):
                if filename.startswith('game_') and filename.endswith('.pkl'):
                    group_id = filename[5:-4]  # 提取group_id
                    storage_path = os.path.join(self.storage_dir, filename)
                    try:
                        with open(storage_path, 'rb') as f:
                            game = pickle.load(f)
                            game.lock = threading.Lock()  # 重新创建锁
                            self.game_instances[group_id] = game
                    except Exception as e:
                        self.logger.error(f"Error loading game {filename}: {e}")
                        # 如果加载失败，删除损坏的存档
                        os.remove(storage_path)
        except Exception as e:
            self.logger.error(f"Error loading games: {e}")

    def execute(self, **kwargs) -> Dict[str, Any]:
        speech = kwargs.get("speech", "").lstrip().strip()
        sender = kwargs.get("sender")
        group_id = sender.group_id if sender.group_id else sender.user_id  # 获取 group_id 或 user_id
        llm_manager = self.container.resolve(LLMManager)
        model_id = self.model_name or llm_manager.get_llm_id_by_ability(LLMAbility.TextChat)
        if not model_id:
            raise ValueError("No available LLM models found")
        
        llm = llm_manager.get_llm(model_id)
        # 获取或创建 GameWerewolf 实例
        if group_id not in self.game_instances:
            game = GameWerewolf(self.werewolf_count, self.willager_count, llm, model_id)
            game.lock = threading.Lock()
            self.game_instances[group_id] = game

        game = self.game_instances[group_id]
        game.llm = llm  # 确保每次都更新 llm 实例

        message_elements = []
        try:
            if not game.lock.acquire(blocking=False):
                result = "游戏正在进行中"
            else:
                try:
                    result = game.play(speech, llm, self.model_name)
                    # 保存游戏状态
                    self.save_game(group_id, game)
                finally:
                    game.lock.release()

            if self.segment_messages and isinstance(result, str):
                for segment in result.split('\n#'):
                    if segment.strip():
                        message_elements.append(TextMessage(segment.strip()))
            else:
                message_elements.append(TextMessage(result))

            # 如果游戏结束，删除存档
            if isinstance(result, str) and ("胜利" in result):
                storage_path = self.get_storage_path(group_id)
                if os.path.exists(storage_path):
                    os.remove(storage_path)
                del self.game_instances[group_id]

            return {"message": IMMessage(sender=ChatSender.get_bot_sender(), message_elements=message_elements)}
        except Exception as e:
            self.logger.error(str(e))
            message_elements.append(TextMessage(str(e)))
            return {"message": IMMessage(sender=ChatSender.get_bot_sender(), message_elements=message_elements)}

