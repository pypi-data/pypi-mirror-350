from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall, Function 
from gepeto.prompts import Prompt
from typing import List, Callable, Union, Optional, Type, Any
from pydantic import BaseModel

AgentFunction = Callable[[], Union[str, "Agent", dict]]


class Agent(BaseModel):
    id: int
    name: str = "Agent"
    model: str = "gpt-4o"
    instructions: Union[str, Callable[[], str], Prompt] = "You are a helpful agent"
    functions: List[AgentFunction] = []
    tool_choice: str = 'auto'
    parallel_tool_calls: bool = True
    max_tokens: int = 4096
    temperature: float = 0.0
    response_format: Optional[Type[BaseModel]] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Agent":
        return cls(**data)

    def equip(self, funcs: Union[AgentFunction, List[AgentFunction], object, List[object]]) -> None:
        """Add one or more functions to this agent's available functions.
        
        Args:
            funcs: A single function, list of functions, object (to add all its methods), 
                  or list of objects (to add all methods from each object)
        """
        # Convert single item to list for uniform handling
        funcs_list = funcs if isinstance(funcs, list) else [funcs]
        
        for func in funcs_list:
            if isinstance(func, object) and not callable(func):
                # Get all callable, non-private methods from object
                methods = [
                    getattr(func, name) 
                    for name in dir(func)
                    if callable(getattr(func, name)) and not name.startswith('_')
                ]
                self.functions.extend(methods)
            else:
                self.functions.append(func)


class Response(BaseModel):
    messages: List = []
    # agent: Optional[Agent] = None
    agent: Optional[Agent] = None
    context: dict = {}
    #populated only if the agent has a response_format
    response_object: Optional[BaseModel] = None
    completion: Optional[dict] = None


class Result(BaseModel):
    '''possible return values of agent function'''
    value: str = ""
    agent: Optional[Agent] = None
    context: dict = {}
