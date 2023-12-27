# public interface IPlayerState
# {
#     IPlayerState DoState(Player player);
# }
from dataclasses import dataclass
from typing import Any


@dataclass
class PlayerState:
    do_state: Any
