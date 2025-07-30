import inspect
import json
import logging
from dataclasses import fields, is_dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Dict,
    List,
    Optional,
    ParamSpec,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

logger = logging.getLogger(__name__)

# Define a TypeVar for dataclass types
T = TypeVar("T")
# Define a ParamSpec for user llm function signatures
P = ParamSpec("P")


def _map_py_type_to_json_type(py_type: Any) -> str:
    """Maps Python type hints to JSON schema type strings."""
    if py_type is str:
        return "string"
    if py_type is int:
        return "integer"
    if py_type is float:
        return "number"
    if py_type is bool:
        return "boolean"
    if py_type is list or get_origin(py_type) is list:
        return "array"
    if py_type is dict or get_origin(py_type) is dict:
        return "object"
    if get_origin(py_type) is Union:
        # For Union[X, NoneType] (Optional[X]), return type of X
        args = get_args(py_type)
        if len(args) == 2 and type(None) in args:
            non_none_arg = args[0] if args[1] is type(None) else args[1]
            return _map_py_type_to_json_type(non_none_arg)
    return "string"  # Default or for complex types not easily mapped


def _generate_tool_schema(tool_func: Callable[..., Awaitable[str]]) -> Dict[str, Any]:
    """Generates a JSON schema-like description for a tool function's parameters."""
    sig = inspect.signature(tool_func)
    parameters_schema: Dict[str, Any] = {"type": "object", "properties": {}}
    required_params: List[str] = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):  # Skip self/cls for methods
            continue

        param_type = param.annotation
        if param_type is inspect.Parameter.empty:
            param_type = str  # Default to string if no type hint

        json_type = _map_py_type_to_json_type(param_type)
        param_schema: Dict[str, Any] = {"type": json_type}

        # If the parameter has a default value, add it to the schema
        if param.default is not inspect.Parameter.empty:
            param_schema["default"] = param.default

        parameters_schema["properties"][name] = param_schema

        if param.default is inspect.Parameter.empty:
            required_params.append(name)

    if required_params:
        parameters_schema["required"] = required_params

    return parameters_schema


class Agent:
    def __init__(
        self,
        llm_interaction_func: Callable[
            Concatenate[List[Dict[str, str]], P], Awaitable[str]
        ],
        initial_prompt: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Callable[..., Awaitable[str]]]] = None,  # MODIFIED
        default_temperature: Optional[float] = None,
        default_max_tokens: Optional[int] = None,
        max_iterations: int = 5,
        max_log_length: int = 700,
    ):
        """
        Initialize an Agent object.

        Parameters:
            llm_interaction_func: Async function for LLM interaction. Takes a list of messages following OpenAI format and returns LLM's response string
            initial_prompt: Initial prompt list following OpenAI message format
            tools: List of tool functions. Each tool is an async function that takes a string parameter and returns a string result.
                  The tool's __name__ attribute is used as the tool name, and __doc__ as the tool description
            temperature: Optional temperature parameter for LLM (implementation depends on llm_interaction_func)
            max_tokens: Optional maximum number of tokens for LLM (implementation depends on llm_interaction_func)
            max_iterations: Maximum number of iterations for tool interactions or internal reasoning in one query call
            max_log_length: Maximum length of log messages to print (in debug mode)
        """
        self.llm_interaction_func = llm_interaction_func
        self.initial_prompt = initial_prompt.copy() if initial_prompt else []
        self.memory: List[Dict[str, str]] = self.initial_prompt.copy()
        self.tools = tools if tools else []
        self.tool_map: Dict[str, Callable[..., Awaitable[str]]] = {  # MODIFIED
            tool.__name__: tool for tool in self.tools
        }
        self.tool_schemas: Dict[str, Dict[str, Any]] = {
            tool.__name__: _generate_tool_schema(tool) for tool in self.tools
        }
        self.temperature = default_temperature
        self.max_tokens = default_max_tokens
        self.max_iterations = max_iterations

        self._system_prompt_parts: List[str] = []
        self._log_length = max_log_length
        self._build_system_prompt()

    def _build_system_prompt(self, structured_output_type: Optional[Type[T]] = None):
        """
        Build system prompt including tool descriptions and structured output instructions.

        Parameters:
            structured_output_type: Optional structured output type
        """
        self._system_prompt_parts = []

        if self.tools:
            tool_descriptions_for_prompt = []
            for tool in self.tools:
                tool_name = tool.__name__
                tool_doc = (
                    inspect.getdoc(tool) or "No description available for this tool."
                )
                tool_schema = self.tool_schemas[tool_name]
                schema_for_prompt = {
                    "tool_name": tool_name,
                    "description": tool_doc,
                    "parameters": tool_schema,
                }
                tool_descriptions_for_prompt.append(
                    json.dumps(schema_for_prompt, ensure_ascii=False)
                )

            self._system_prompt_parts.append(
                "You have access to the following tools. "
                "If you decide to use a tool, respond ONLY with a JSON object in the following format, "
                "containing 'tool_name' (string) and 'arguments' (an object containing the arguments for the tool). "
                "Do not include any other text or explanation before or after the JSON.\n"
                "Available tool schemas:\n[\n"
                + ",\n".join(tool_descriptions_for_prompt)
                + "\n]\n"
                "If you don't need to use a tool, respond to the user directly."
            )

        if structured_output_type:
            if not is_dataclass(structured_output_type):
                raise ValueError("structured_output_type must be a dataclass.")
            field_details = []
            example_json_parts = []
            for f in fields(structured_output_type):
                field_type_name = (
                    f.type.__name__ if hasattr(f.type, "__name__") else str(f.type)  # type: ignore
                )
                field_details.append(f'  "{f.name}": "{field_type_name}"')
                if field_type_name == "str":
                    example_value = f"example {f.name}"
                elif field_type_name == "int":
                    example_value = 0
                elif field_type_name == "float":
                    example_value = 0.0
                elif field_type_name == "bool":
                    example_value = False
                elif field_type_name.startswith("List") or field_type_name.startswith(
                    "list"
                ):
                    example_value = []
                elif field_type_name.startswith("Dict") or field_type_name.startswith(
                    "dict"
                ):
                    example_value = {}
                else:
                    example_value = "..."
                example_json_parts.append(
                    f'    "{f.name}": {json.dumps(example_value, ensure_ascii=False)}'
                )

            json_schema_desc = "{\n" + ",\n".join(field_details) + "\n}"
            example_json = "{\n" + ",\n".join(example_json_parts) + "\n  }"
            self._system_prompt_parts.append(
                f"\nWhen you provide your final answer, and you are not using a tool, "
                f"you MUST format your response as a single JSON object conforming to the following structure. "
                f"Do not include any other text, explanations, or markdown formatting before or after the JSON object. "
                f"Ensure all specified fields are present.\n"
                f"Structure:\n{json_schema_desc}\n"
                f"Example:\n{example_json}"
            )

    def _get_current_messages_with_system_prompt(self) -> List[Dict[str, str]]:
        """
        Combine system prompt with current memory for sending to LLM.
        """
        # 确保系统提示在最前面，并且只有一个
        # 如果内存中已经有系统提示，我们可能会选择替换它或附加到它
        # 这里采用简单策略：如果内存为空或第一个不是系统提示，则添加新的系统提示
        current_messages = self.memory.copy()
        system_prompt_str = "\n\n".join(self._system_prompt_parts)
        if not system_prompt_str:
            return current_messages
        if not current_messages or current_messages[0].get("role") != "system":
            current_messages.insert(0, {"role": "system", "content": system_prompt_str})
        else:
            current_messages[0]["content"] = system_prompt_str
        return current_messages

    async def query(
        self,
        user_input: str,
        structured_output_type: Optional[Type[T]] = None,
        **kwargs: Any,
    ) -> Union[str, T, Dict[str, Any]]:
        """
        Run an Agent query.

        Parameters:
            user_input: User's input string
            structured_output_type: Optional structured output type
            **kwargs: Additional keyword arguments to pass to llm_interaction_func.
                     These will override any matching parameters set during initialization.

        Returns:
            Response in the appropriate type based on structured_output_type
        """
        # Rebuild system prompt to include new structured output type
        self._build_system_prompt(structured_output_type)
        self.memory.append({"role": "user", "content": user_input})

        llm_kwargs = {}
        if self.temperature is not None:
            llm_kwargs["temperature"] = self.temperature
        if self.max_tokens is not None:
            llm_kwargs["max_tokens"] = self.max_tokens
        llm_kwargs.update(kwargs)

        for iteration in range(self.max_iterations):
            messages_for_llm = self._get_current_messages_with_system_prompt()
            logger.debug(f"--- Iteration {iteration + 1} ---")
            logger.debug("--- Sending to LLM ---")
            for msg in messages_for_llm:
                logger.debug(
                    f"{msg['role']}: {msg['content'][: self._log_length]}{'...' if len(msg['content']) > self._log_length else ''}"
                )

            try:
                llm_response_text = await self.llm_interaction_func(
                    messages_for_llm, **llm_kwargs
                )  # type: ignore
            except TypeError:
                llm_response_text = await self.llm_interaction_func(messages_for_llm)  # type: ignore

            logger.debug(f"--- LLM Response --- \n{llm_response_text}")

            if self.tools:
                try:
                    # Attempt to strip markdown code block fences if present
                    cleaned_response_text = llm_response_text.strip()
                    if cleaned_response_text.startswith("```json"):
                        cleaned_response_text = cleaned_response_text[
                            len("```json") :
                        ].strip()
                    if cleaned_response_text.startswith("```"):
                        cleaned_response_text = cleaned_response_text[
                            len("```") :
                        ].strip()
                    if cleaned_response_text.endswith("```"):
                        cleaned_response_text = cleaned_response_text[
                            : -len("```")
                        ].strip()

                    potential_tool_call = json.loads(cleaned_response_text)
                    tool_name = None
                    tool_arguments = None

                    if (
                        isinstance(potential_tool_call, dict)
                        and "tool_name" in potential_tool_call
                    ):
                        tool_name = potential_tool_call["tool_name"]

                        if "arguments" in potential_tool_call:
                            if isinstance(potential_tool_call["arguments"], dict):
                                tool_arguments = potential_tool_call["arguments"]
                            else:
                                logger.warning(
                                    f"Tool arguments for '{tool_name}' is not a dict: {potential_tool_call['arguments']}"
                                )

                    if (
                        tool_name
                        and tool_name in self.tool_map
                        and tool_arguments is not None
                    ):
                        self.memory.append(
                            {
                                "role": "assistant",
                                "content": llm_response_text,
                            }  # Store original LLM response
                        )
                        tool_function = self.tool_map[tool_name]
                        logger.info(
                            f"Calling tool: {tool_name} with args: {tool_arguments}"
                        )
                        try:
                            # Ensure tool_arguments is a dict for **kwargs
                            if not isinstance(tool_arguments, dict):
                                raise ValueError(
                                    f"Tool arguments for {tool_name} must be a dictionary, got {type(tool_arguments)}"
                                )
                            tool_result = await tool_function(**tool_arguments)
                        except Exception as e:
                            tool_result = f"Error executing tool {tool_name}: {e}"
                            logger.error(f"Error during tool execution: {tool_result}")

                        self.memory.append(
                            {"role": "tool", "name": tool_name, "content": tool_result}
                        )
                        continue  # Go to next iteration with tool result

                except json.JSONDecodeError:
                    logger.debug(
                        f"LLM response is not a valid JSON tool call: {llm_response_text[:200]}"
                    )
                    pass  # Not a tool call, proceed as normal response
                except Exception as e:
                    logger.error(
                        f"Error processing potential tool call: {e}. Response: {llm_response_text[:200]}"
                    )
                    pass

            self.memory.append({"role": "assistant", "content": llm_response_text})

            if structured_output_type:
                try:
                    # Attempt to strip markdown code block fences if present for structured output too
                    cleaned_response_text = llm_response_text.strip()
                    if cleaned_response_text.startswith("```json"):
                        cleaned_response_text = cleaned_response_text[
                            len("```json") :
                        ].strip()
                    if cleaned_response_text.startswith("```"):
                        cleaned_response_text = cleaned_response_text[
                            len("```") :
                        ].strip()
                    if cleaned_response_text.endswith("```"):
                        cleaned_response_text = cleaned_response_text[
                            : -len("```")
                        ].strip()

                    parsed_json = json.loads(cleaned_response_text)
                    structured_object = structured_output_type(**parsed_json)
                    return structured_object
                except (json.JSONDecodeError, TypeError, ValueError) as e:
                    logger.warning(
                        f"Failed to parse LLM response into structured_output_type ({type(e).__name__}). Response: {llm_response_text[:200]}"
                    )
                    if iteration == self.max_iterations - 1:
                        return llm_response_text  # Return raw string on last attempt
            else:
                return llm_response_text  # Return raw string if no structured output expected

        final_response = (
            self.memory[-1]["content"]
            if self.memory and self.memory[-1]["role"] == "assistant"
            else "Max iterations reached without a final response."
        )
        logger.debug(
            f"Max iterations reached. Returning last assistant message or fallback: {final_response}"
        )
        return final_response

    def clear_memory(self):
        """
        Clear Agent's memory and reset it to initial prompt state.
        """
        self.memory = self.initial_prompt.copy()
        logger.debug("Memory cleared.")
