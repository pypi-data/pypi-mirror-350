from dataclasses import dataclass, field, asdict
from Osdental.Shared.Code import Code
from Osdental.Shared.Message import Message

@dataclass
class Response:
    status: str = field(default=Code.PROCESS_SUCCESS_CODE)
    message: str = field(default=Message.PROCESS_SUCCESS_MSG)
    data: str = field(default=None)

    def send(self):
        return asdict(self)
