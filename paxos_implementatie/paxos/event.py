from dataclasses import dataclass
from typing import List, Any, Optional
from paxos_implementatie.paxos.computer import Computer


@dataclass
class Event:
    tick: int
    fails: List[Computer]
    repairs: List[Computer]
    message_destination: Optional[Computer]
    message_value: Optional[Any]
