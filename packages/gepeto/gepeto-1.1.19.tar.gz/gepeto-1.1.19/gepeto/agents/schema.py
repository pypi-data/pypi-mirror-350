from datetime import datetime
from typing import Union, Literal, Dict, Any, Tuple, Optional, Type, List, Callable
from gepeto.prompts.schema import Prompt
from gepeto.team.schema import AgentFunction
from pydantic import BaseModel, computed_field, create_model
from gepeto.team.schema import Agent
from gepeto.team.utils import debug_print
from gepeto.team.utils import func_to_json
## MAJOR TECH DEBT
class PromptAddSchema(BaseModel):
    name: str


class PromptSchema(PromptAddSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
# id=17 
# content='You are a dinosaur and you tell jokes about dinosaurs' 
# description='dino prompt' 
# prompt_id=13 
# created_at=datetime.datetime(2024, 12, 27, 9, 27, 55, 157509) 
# updated_at=datetime.datetime(2024, 12, 27, 9, 27, 55, 157509) 
# name='dino joker' 
# organization_id=3 






class PromptVersionSchema(BaseModel):
    id: int
    content: str
    description: str
    prompt_id: int
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]
    name: Union[str, None] = None
    prompt: Union[PromptSchema, None] = None
###

class AgentCreateSchema(BaseModel):
    name: str
    model: str
    prompt_version_id: int
    response_schema: Optional[dict] = None
    temperature: Union[float, None] = None
    max_tokens: Union[int, None] = None
    functions: Union[List[str], None] = None
    tool_choice: Union[str, None] = None
    parallel_tool_calls: Union[bool, None] = None


class AgentUpdateSchema(AgentCreateSchema):
    id: int

class AgentSchema(AgentUpdateSchema):
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    prompt_version: Union[PromptVersionSchema, None] = None

    @computed_field
    def functions_as_json(self) -> List[dict]:
        return [func_to_json(f) for f in self.functions]

    @computed_field
    def response_schema_as_pydantic(self) -> Union[BaseModel, None]:
        if not self.response_schema:
            return None

        type_mapping = {
            'string': str,
            'integer': int,
            'number': float,
            'boolean': bool,
            'array': list,
            'object': dict
        }

        defs = self.response_schema.get('$defs', {})
        models = {}

        def process_field(field_info: Dict[str, Any], required: bool) -> Tuple[Any, Any]:
            """
            Process individual field information and return a tuple suitable for Pydantic model creation.
            """
            if 'anyOf' in field_info:
                # Handle Union types, excluding 'null' for optional fields
                union_types = [
                    type_mapping.get(option['type'], str)
                    for option in field_info['anyOf']
                    if option['type'] != 'null'
                ]
                field_type = Union[tuple(union_types)]
                default = field_info.get('default')
                if required:
                    return (field_type, ...)
                else:
                    return (Optional[field_type], default)
            
            elif 'enum' in field_info:
                # Handle enums using Literal
                enum_values = tuple(field_info['enum'])
                enum_type = Literal[enum_values]
                if required:
                    return (enum_type, ...)
                else:
                    return (Optional[enum_type], None)
            
            elif '$ref' in field_info:
                # Handle references to other models
                ref_path = field_info['$ref']
                ref_name = ref_path.split('/')[-1]
                if ref_name not in models:
                    raise ValueError(f"Reference '{ref_name}' not found in $defs.")
                ref_model = models[ref_name]
                if required:
                    return (ref_model, ...)
                else:
                    return (Optional[ref_model], None)
            
            else:
                # Handle basic types
                python_type = type_mapping.get(field_info.get('type'), str)
                if required:
                    return (python_type, ...)
                else:
                    default = field_info.get('default')
                    return (Optional[python_type], default)

        def create_pydantic_model(model_name: str, schema: Dict[str, Any]) -> BaseModel:
            """
            Create a Pydantic model from a JSON schema definition.
            """
            properties = schema.get('properties', {})
            required_fields = set(schema.get('required', []))
            fields = {}

            for field_name, field_info in properties.items():
                required = field_name in required_fields
                fields[field_name] = process_field(field_info, required)

            model = create_model(model_name, **fields, __base__=BaseModel)
            return model

        # First: Create all models defined in $defs
        for def_name, def_schema in defs.items():
            models[def_name] = create_pydantic_model(def_name, def_schema)

        # Second: Create the main model
        main_model_name = self.response_schema.get('title', 'DynamicModel')
        main_properties = self.response_schema.get('properties', {})
        main_required = set(self.response_schema.get('required', []))
        main_fields = {}

        for field_name, field_info in main_properties.items():
            required = field_name in main_required
            main_fields[field_name] = process_field(field_info, required)

        main_model = create_model(main_model_name, **main_fields, __base__= BaseModel)
        return main_model
    
    def to_agent(self) -> Agent:
        return Agent(
            id=self.id,
            name=self.name,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            instructions=self.map_prompt_version(self.prompt_version),
            functions=self.str_to_callable(self.functions),
            tool_choice=self.tool_choice if type(self.tool_choice) == str else "",
            parallel_tool_calls=self.parallel_tool_calls,
            response_format=self.response_schema_as_pydantic if self.response_schema else None
        )


    def map_prompt_version(self, agent_prompt_version: dict) -> Prompt:
        mapped_prompt = Prompt(
            id=agent_prompt_version.id,
            created_at=datetime.fromisoformat(agent_prompt_version.created_at),
            updated_at=datetime.fromisoformat(agent_prompt_version.updated_at),
            name=agent_prompt_version.prompt.name,
            description=agent_prompt_version.description,
            content=agent_prompt_version.content,
            prompt_id=agent_prompt_version.prompt_id)
        return mapped_prompt


    def str_to_callable(self, func_names):
        """
        Given a list of function names (strings), return a list of
        the corresponding callable objects. Raises ValueError if
        a name is not found or is not callable.
        """
        if func_names is None:
            return None
            
        # Skip empty or malformed function names
        if not func_names or func_names == '{}':
            return []

        callables_list = []
        debug_print(True, 'func names ', func_names)
        for name in func_names:
            # Skip if name is empty or malformed
            if not name or name == '{}':
                continue
                
            candidate = globals().get(name)
            if candidate is None:
                raise ValueError(f"Function {name} not found in global scope.")
            if not callable(candidate):
                raise ValueError(f"'{name}' is not callable.")
            callables_list.append(candidate)
        return callables_list       

    class Config:
        from_attributes = True

# New request models for agent CRUD requests:
class AgentSearchRequest(BaseModel):
    name: str

class AgentRequest(AgentSearchRequest):
    description: Optional[str] = None
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent"
    # Add any other fields you want to allow when creating/updating an Agent





