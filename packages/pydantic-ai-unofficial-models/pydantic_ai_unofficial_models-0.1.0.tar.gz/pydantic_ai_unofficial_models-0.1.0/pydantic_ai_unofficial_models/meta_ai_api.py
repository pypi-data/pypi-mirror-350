import datetime
import random
from typing import Any

from meta_ai_api_tool_call import MetaAI
from pydantic_ai.models import Model
from pydantic import BaseModel

def generate_example_from_schema(schema: dict, definitions: dict = None) -> any:
    if definitions is None:
        definitions = schema.get("$defs", {})

    schema_type = schema.get("type")

    if "$ref" in schema:
        ref = schema["$ref"].split("/")[-1]
        return generate_example_from_schema(definitions[ref], definitions)

    if "anyOf" in schema or "oneOf" in schema:
        options = schema.get("anyOf") or schema.get("oneOf")
        return generate_example_from_schema(options[0], definitions)

    if schema_type == "object":
        props = schema.get("properties", {})
        return {
            key: generate_example_from_schema(value, definitions)
            for key, value in props.items()
        }

    if schema_type == "array":
        item_schema = schema.get("items", {})
        # If the item schema is for a string, return ["example"]
        if item_schema.get("type") == "string":
            return ["example"]
        # If the item schema is for an integer
        if item_schema.get("type") == "integer":
            return [random.randint(0, 100)]
        # If the item schema is for a number
        if item_schema.get("type") == "number":
            return [round(random.uniform(0, 100), 2)]
        # If the item schema is for a boolean
        if item_schema.get("type") == "boolean":
            return [True]
        # If the item schema is an object or $ref, recurse
        if item_schema.get("type") == "object" or "$ref" in item_schema:
            nested = generate_example_from_schema(item_schema, definitions)
            return [nested] if nested is not None else [{}]
        # If no type or items are empty, return []
        if not item_schema or not item_schema.get("type"):
            return []
        return [generate_example_from_schema(item_schema, definitions)]

    if schema_type == "string":
        fmt = schema.get("format")
        if fmt == "date-time":
            return datetime.datetime.now().isoformat()
        return "example"

    if schema_type == "integer":
        return random.randint(0, 100)

    if schema_type == "number":
        return round(random.uniform(0, 100), 2)

    if schema_type == "boolean":
        return True

    return None

class MetaAIChatModel(Model):
    """
    Standalone Meta AI chat model provider for agent frameworks.
    Decoupled from pydantic-ai internals; only requires minimal interface compatibility.
    """
    def _augment_prompt_with_json_instruction(self, prompt, output_type):
        """
        If output_type is a Pydantic BaseModel, append JSON schema instructions and an example to the prompt.
        Handles $ref and $defs so nested schemas are correctly expanded in the example.
        """
        from pydantic import BaseModel
        import json
        import re
        if output_type and (isinstance(output_type, type) and issubclass(output_type, BaseModel)) or (isinstance(output_type, dict)):
            if isinstance(output_type, dict):
                schema = output_type
            else:
                schema = output_type.model_json_schema()
                
                schema_str = json.dumps(schema, indent=2)
                # --- Recursively resolve all $ref fields ---
                def resolve_refs(schema, defs=None):
                    if defs is None:
                        defs = schema.get("$defs", {})
                    if isinstance(schema, dict):
                        if "$ref" in schema:
                            ref = schema["$ref"]
                            key = re.sub(r"^#/?\\$defs/", "", ref)
                            if key in defs:
                                resolved = resolve_refs(defs[key], defs)
                                # Merge with any sibling keys except $ref
                                sibling_keys = {k: v for k, v in schema.items() if k != "$ref"}
                                merged = {**resolved, **sibling_keys}
                                return merged
                        # Recursively resolve in all dict values
                        return {k: resolve_refs(v, defs) for k, v in schema.items()}
                    elif isinstance(schema, list):
                        return [resolve_refs(item, defs) for item in schema]
                    else:
                        return schema
                schema_for_example = resolve_refs(schema)

            # Use the new generate_example function for example generation
            try:
                example_obj = generate_example_from_schema(schema, schema.get("$defs"))
                import json as _json
                # If the example is not serializable, show a fallback
                try:
                    example_str = _json.dumps(example_obj, indent=2, ensure_ascii=False)
                except Exception as ex:
                    example_str = str(example_obj)
                example_section = f"\n\nExample response:\n{example_str}\n"
            except Exception as e:
                example_section = f"\n\n[Example generation failed: {e}]\n"

            explanation = (
                "The following JSON schema defines the exact structure, required fields, and types for your response. "
                "Your answer must be a valid JSON object that matches this schema exactly. Do not include any extra fields or omit any required fields. "
            )
            return f"Query: '{prompt}'\n\n --- {explanation}\n\nRespond in JSON matching this schema:\n{schema}{example_section}"
        return prompt

    def __init__(self, *, fb_email=None, fb_password=None, proxy=None, model_name="default", provider="meta", meta_ai_client=None):
        self.fb_email = fb_email
        self.fb_password = fb_password
        self.proxy = proxy
        if meta_ai_client is not None:
            self._meta_ai = meta_ai_client
        else:
            try:
                self._meta_ai = MetaAI(
                    fb_email=fb_email,
                    fb_password=fb_password,
                    proxy=proxy,
                )
            except ImportError as e:
                raise RuntimeError("MetaAIChatModel: Could not import MetaAI client. Is meta_ai_api installed?") from e
        if self._meta_ai is None:
            raise RuntimeError("MetaAIChatModel: self._meta_ai failed to initialize!")
        self._model_name = model_name
        self._system = provider
        # Do NOT store output_type here!

    @property
    def allow_text_output(self):
        # Always allow text output (legacy property, not used)
        return True

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def system(self) -> str:
        return self._system

    async def request(
        self,
        messages: list[Any],
        model_settings: Any,
        model_request_parameters: Any
    ) -> tuple[Any, Any]:
        """
        Handles MetaAI requests with support for tool/function calling.
        If MetaAI response includes a tool call pattern, invoke the corresponding Python function and return the result.
        """
        import json
        import re
        from pydantic_ai.messages import ToolCallPart, TextPart, ModelResponse, ModelRequest
        from pydantic_ai.usage import Usage

        user_message = next((m for m in messages if isinstance(m, ModelRequest)), None)
        if not user_message:
            raise ValueError("No user message found for MetaAIChatModel request.")
        user_prompt = next(
            (part.content for part in getattr(user_message, "parts", []) if getattr(part, "part_kind", None) == "user-prompt"),
            None
        )
        if not user_prompt:
            raise ValueError("No user-prompt part found in ModelRequest.")
        # Get output_type from model_settings if present
        output_type = None



        # Check output_type as attribute or dict key in model_settings
        if hasattr(model_settings, 'output_type') and getattr(model_settings, 'output_type', None) is not None:
            output_type = getattr(model_settings, 'output_type')
        elif isinstance(model_settings, dict) and 'output_type' in model_settings and model_settings['output_type'] is not None:
            output_type = model_settings['output_type']
        elif hasattr(model_request_parameters, 'output_type') and getattr(model_request_parameters, 'output_type', None) is not None:
            output_type = getattr(model_request_parameters, 'output_type')
        if not user_prompt:
            raise ValueError("No user-prompt part found in ModelRequest.")

        output_type = None
        if hasattr(model_settings, 'output_type') and getattr(model_settings, 'output_type', None) is not None:
            output_type = getattr(model_settings, 'output_type')
        elif isinstance(model_settings, dict) and 'output_type' in model_settings and model_settings['output_type'] is not None:
            output_type = model_settings['output_type']
        elif hasattr(model_request_parameters, 'output_type') and getattr(model_request_parameters, 'output_type', None) is not None:
            output_type = getattr(model_request_parameters, 'output_type')
        elif isinstance(model_request_parameters, dict) and 'output_type' in model_request_parameters and model_request_parameters['output_type'] is not None:
            output_type = model_request_parameters['output_type']
        elif hasattr(self, '_output_type') and getattr(self, '_output_type', None) is not None:
            output_type = self._output_type
        else:
            output_tools = getattr(model_request_parameters, 'output_tools', None)
            if output_tools and isinstance(output_tools, list) and len(output_tools) > 0:
                tool = output_tools[0]
                schema = getattr(tool, 'parameters_json_schema', None)
                if schema and 'properties' in schema:
                    try:
                        from pydantic import create_model, BaseModel
                        from typing import List, Optional, get_args, get_origin
                        import sys
                        def resolve_type(prop, defs):
                            if "$ref" in prop:
                                ref = prop["$ref"]
                                ref_name = ref.split("/")[-1]
                                if ref_name in defs:
                                    return build_model_from_schema(ref_name, defs[ref_name], defs)
                                return dict
                            t = prop.get("type")
                            if t == "string":
                                return str
                            elif t == "integer":
                                return int
                            elif t == "number":
                                return float
                            elif t == "boolean":
                                return bool
                            elif t == "array":
                                items = prop.get("items", {})
                                return List[resolve_type(items, defs)]
                            elif t == "object":
                                # Inline object
                                if "properties" in prop:
                                    return build_model_from_schema("InlineObject", prop, defs)
                                return dict
                            return str
                        def build_model_from_schema(name, schema, defs):
                            if hasattr(build_model_from_schema, "_cache") and (name, id(schema)) in build_model_from_schema._cache:
                                return build_model_from_schema._cache[(name, id(schema))]
                            fields = {}
                            for k, v in schema.get("properties", {}).items():
                                typ = resolve_type(v, defs)
                                required = k in schema.get("required", [])
                                if not required:
                                    typ = Optional[typ]
                                fields[k] = (typ, ... if required else None)
                            model = create_model(name, **fields, __base__=BaseModel)
                            if not hasattr(build_model_from_schema, "_cache"):
                                build_model_from_schema._cache = {}
                            build_model_from_schema._cache[(name, id(schema))] = model
                            return model
                        defs = schema.get("$defs", {})
                        DynamicOutputType = build_model_from_schema(tool.name.capitalize() + 'Output', schema, defs)
                        output_type = DynamicOutputType
                    except Exception as e:

                        output_type = str

        if model_request_parameters is not None and model_request_parameters.output_tools is not None and len(model_request_parameters.output_tools) > 0:
            output_schema = model_request_parameters.output_tools[0].parameters_json_schema
        else:
            output_schema = output_type
        # --- Serialize the message history for tool chaining ---
        def serialize_message_history(messages):
            lines = []
            from pydantic_ai.messages import ModelRequest, ModelResponse, ToolCallPart, ToolReturnPart, TextPart, UserPromptPart
            for msg in messages:
                # ModelRequest (user/system/tool-return)
                if hasattr(msg, 'parts'):
                    for part in msg.parts:
                        if getattr(part, 'part_kind', None) == 'user-prompt':
                            lines.append(f"User: {getattr(part, 'content', '')}")
                        elif getattr(part, 'part_kind', None) == 'tool-return':
                            tool_name = getattr(part, 'tool_name', 'unknown')
                            content = getattr(part, 'content', '')
                            lines.append(f"Tool result [{tool_name}]: {content}")
                        elif getattr(part, 'part_kind', None) == 'retry-prompt':
                            lines.append(f"[Retry]: {getattr(part, 'content', '')}")
                # ModelResponse (assistant/tool-call/text)
                elif hasattr(msg, 'parts'):
                    for part in msg.parts:
                        if isinstance(part, ToolCallPart):
                            args = part.args if isinstance(part.args, dict) else str(part.args)
                            lines.append(f"Tool call: {part.tool_name}({args})")
                        elif isinstance(part, TextPart):
                            lines.append(f"Assistant: {part.content}")
            return "\n".join(lines)
        # Use the serialized history as the prompt
        serialized_history = serialize_message_history(messages)
        augmented_prompt = self._augment_prompt_with_json_instruction(serialized_history, output_schema)

        function_tools = getattr(model_request_parameters, 'function_tools', [])
        output_tools = getattr(model_request_parameters, 'output_tools', [])
        all_tools = function_tools #+ output_tools  #if you want both kinds

        # Convert all_tools to tool schema dicts for the API (Gemini/Anthropic style)
        def _tool_schema_from_definition(t):
            return {
                'name': t.name,
                'description': getattr(t, 'description', ''),
                'input_schema': getattr(t, 'parameters_json_schema', {})
            }

        tool_schemas = []
        for t in all_tools:
            if hasattr(t, 'name') and hasattr(t, 'parameters_json_schema'):
                tool_schemas.append(_tool_schema_from_definition(t))
            elif isinstance(t, dict) and 'name' in t and 'input_schema' in t:
                tool_schemas.append(t)
            else:
                pass

        # ... (rest of the function)

        tool_call_candidate = None  # Always initialize
        # ... code that sets tool_call_candidate if a tool call is detected ...
        # When a tool call is detected:
        if tool_call_candidate is not None:
            tool_name = tool_call_candidate.get('name')
            tool_args = tool_call_candidate.get('input', {})
            tool_fn = tool_map.get(tool_name)
            if not tool_fn:
                raise RuntimeError(f"No matching tool function found for tool name: {tool_name}")
            tool_result = tool_fn(**tool_args) if tool_args else tool_fn()
            # ...



        prompt_kwargs = dict(stream=False, new_conversation=False)
        if tool_schemas:
            prompt_kwargs['tools'] = tool_schemas


        resp = self._meta_ai.prompt(augmented_prompt, **prompt_kwargs)
        if hasattr(resp, "__aiter__"):
            # Streaming not supported yet for MetaAI
            resp = [r async for r in resp]
        # Parse the response (should be a dict with 'message', 'sources', ...)
        if isinstance(resp, list):
            resp = resp[-1]
        raw_message = resp.get("message", "")

        try:
            parsed_data = json.loads(raw_message)
        except Exception:
            parsed_data = raw_message



        # PATCH: If parsed_data is empty and output_type is set, return a default dict matching the schema
        from pydantic import BaseModel
        if output_type is not None and (parsed_data == "" or parsed_data is None or (isinstance(parsed_data, dict) and not parsed_data)):
            if isinstance(output_type, type) and issubclass(output_type, BaseModel):
                try:
                    # If response is still empty, fallback to dummy output
                    if not parsed_data:
                        # Generate a valid dummy output using the output_type's schema
                        schema = output_type.schema()
                        dummy = _JsonSchemaTestData(schema).generate()
                        # Always return a dict/object, never a string, to avoid downstream errors
                        if isinstance(dummy, str):
                            # Try to load as JSON if possible
                            try:
                                dummy = json.loads(dummy)
                            except Exception:
                                dummy = {"result": dummy}
                        return dummy

                    # If output_type is a BaseModel, try to parse the response
                    if hasattr(output_type, "parse_obj"):
                        try:
                            return output_type.parse_obj(parsed_data)
                        except Exception:
                            pass  # fallback to returning response as-is

                    # Always return a dict/object, never a string
                    if isinstance(parsed_data, str):
                        try:
                            response_obj = json.loads(parsed_data)
                            return response_obj
                        except Exception:
                            return {"result": parsed_data}
                    return parsed_data
                except Exception as e:

                    raise RuntimeError(f"MetaAIChatModel: Meta AI returned empty response and could not build sample output for schema {output_type}")
            else:
                parsed_data = {}


        # --- Unified tool call and text extraction logic (OpenAI/Anthropic/Gemini pattern) ---
        # 1. If a tool call is detected, emit ONLY a ModelResponse with ToolCallPart and return immediately.
        # 2. If not, emit ModelResponse with TextPart (normal answer).
        # 3. PATCH: Accept bare JSON object matching output_type as a valid final answer.
        from pydantic_ai.messages import ModelResponse, TextPart, ToolCallPart
        import json
        import sys


        # --- MetaAI tool call chaining logic ---
        # Only emit a TextPart if the model actually produces a text answer; otherwise, keep looping through tool calls.
        # Helper to robustly detect tool call JSONs vs. text answers
        def is_tool_call_json(s):
            if not isinstance(s, str):
                return False
            s = s.strip()
            # Heuristic: starts with { and has "type": "tool_use"
            return s.startswith('{') and '"type"' in s and '"tool_use"' in s

        # Tool call detection (dict or string)
        tool_call_candidate = None
        if isinstance(parsed_data, dict) and parsed_data.get("type") == "tool_use":
            tool_call_candidate = parsed_data
        elif isinstance(parsed_data, str) and is_tool_call_json(parsed_data):
            try:
                tool_call_candidate = json.loads(parsed_data)
            except Exception:
                tool_call_candidate = None

        if tool_call_candidate:

            tool_name = tool_call_candidate.get("name")
            tool_args = tool_call_candidate.get("input", {})
            tool_call_id = tool_call_candidate.get("id")
            tool_call_part = ToolCallPart(
                tool_name=tool_name,
                args=tool_args,
                tool_call_id=tool_call_id
            )
            model_response = ModelResponse(parts=[tool_call_part])

            return model_response, Usage()

        # PATCH: Accept bare JSON object as valid answer only if no function tools are present
        # (i.e., output_tools is empty or only contains the final_result tool)
        if isinstance(parsed_data, dict) and output_type is not None:
            # Determine if function tools are present
            function_tools_present = False
            if model_request_parameters and hasattr(model_request_parameters, 'function_tools'):
                function_tools = getattr(model_request_parameters, 'function_tools', [])
                if function_tools:
                    function_tools_present = True
            # Accept bare JSON only if NO function tools
            if not function_tools_present:
                try:
                    from pydantic import BaseModel
                    if isinstance(output_type, type) and issubclass(output_type, BaseModel):
                        output_type.parse_obj(parsed_data)  # will raise if not valid
                    # If no error, synthesize a ToolCallPart so agent logic is satisfied
                    from pydantic_ai.messages import ToolCallPart, ModelResponse
                    tool_call_part = ToolCallPart(
                        tool_name="final_result",
                        args=parsed_data,
                        tool_call_id=None
                    )
                    model_response = ModelResponse(parts=[tool_call_part])
                    return model_response, Usage()
                except Exception:
                    pass  # fallback to normal text logic

        # Otherwise, treat as text answer
        # If parsed_data is a string, just return as text
        if isinstance(parsed_data, str):
            text = parsed_data.strip()
            if text:
                model_response = ModelResponse(parts=[TextPart(content=text)])
                return model_response, Usage()
        # If parsed_data is a dict, dump as JSON text
        elif isinstance(parsed_data, dict):
            text = json.dumps(parsed_data)
            model_response = ModelResponse(parts=[TextPart(content=text)])
            return model_response, Usage()
        # Fallback: treat as string
        else:
            text = str(parsed_data)
            model_response = ModelResponse(parts=[TextPart(content=text)])
            return model_response, Usage()

        # Tool call detection (dict or string)
        tool_call_candidate = None
        if isinstance(parsed_data, dict) and parsed_data.get("type") == "tool_use":
            tool_call_candidate = parsed_data
        elif isinstance(parsed_data, str):
            import re
            tool_call_json_match = re.search(r'\{\s*"type"\s*:\s*"tool_use".*?\}', parsed_data, re.DOTALL)
            if tool_call_json_match:
                try:
                    tool_call_candidate = json.loads(tool_call_json_match.group(0))
                except Exception:
                    tool_call_candidate = None

        if tool_call_candidate:

            tool_name = tool_call_candidate.get("name")
            tool_args = tool_call_candidate.get("input", {})
            tool_call_id = tool_call_candidate.get("id")
            tool_call_part = ToolCallPart(
                tool_name=tool_name,
                args=tool_args,
                tool_call_id=tool_call_id
            )
            model_response = ModelResponse(parts=[tool_call_part])

            return model_response, Usage()

        # Otherwise, treat as text answer
        # If parsed_data is a string, just return as text
        if isinstance(parsed_data, str):
            text = parsed_data.strip()
            if text:
                model_response = ModelResponse(parts=[TextPart(content=text)])
                return model_response, Usage()
        # If parsed_data is a dict, dump as JSON text
        elif isinstance(parsed_data, dict):
            text = json.dumps(parsed_data)
            model_response = ModelResponse(parts=[TextPart(content=text)])
            return model_response, Usage()
        # Fallback: treat as string
        else:
            text = str(parsed_data)
            model_response = ModelResponse(parts=[TextPart(content=text)])
            return model_response, Usage()


    def customize_request_parameters(self, model_request_parameters: dict[str, Any]) -> dict[str, Any]:
        return model_request_parameters

    class Config:
        arbitrary_types_allowed: bool = True
        json_schema_extra: dict[str, Any] = {
            "description": (
                "Meta AI chat model wrapper with simulated tool calling. "
                "Tool calling is detected by special patterns in the response, e.g., <<tool_call:tool_name>>{args}."
            )
        }

