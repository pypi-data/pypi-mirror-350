# -*- coding: utf-8 -*-
import json
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    Union,
    cast,
    get_args,
)

import jsonref
from asgiref.sync import async_to_sync
from pydantic import BaseModel, ValidationError

from agentdev.schemas.message_schemas import (
    ParametersSchema,
    PromptMessageTool,
)
from .__base import BaseComponent, ComponentArgsT, ComponentReturnT


class Component(BaseComponent, Generic[ComponentArgsT, ComponentReturnT]):
    """
    Base class for all components, supporting both async and streaming
     capabilities.
    """

    name: str
    description: str

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any,
    ):
        """
        Initialize the base component

        Args:
            name: The name of the component
            description: The description of the component
            **kwargs: other arguments if needed
        """
        self.name = name if name else self.__class__.name
        self.description = (
            description if description else self.__class__.description
        )
        if not self.name or not self.description:
            raise ValueError(
                "Component name and description must be provided.",
            )
        self.input_type = self._input_type()
        self.return_type = self._return_type()
        self.parameters = self._parameters_parser()
        self.function_schema = PromptMessageTool(
            name=self.name,
            description=self.description,
            parameters=self.parameters,
        )

    async def _arun(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        """
        Run the component with the given arguments asynchronously.
        """
        raise NotImplementedError

    async def arun(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        """
        Run the component with the given arguments asynchronously.

        Args:
            args: Input parameters adhering to the input schema.
            **kwargs: Other arguments if needed

        Returns:
            ReturnT: Output parameters adhering to the output schema.
        """
        if not isinstance(args, self.input_type):
            raise TypeError(
                f"The input must in the format of {self.input_type.__name__} "
                f"or its subclass",
            )
        result = await self._arun(args, **kwargs)
        if not isinstance(result, self.return_type):
            raise TypeError(
                f"The return must in the format of "
                f"{self.return_type.__name__} or its subclass",
            )
        return result

    def run(self, args: Any, **kwargs: Any) -> Any:
        # make sure the async method could be called from sync context with or
        # without asyncio loop running
        return async_to_sync(self.arun)(args, **kwargs)

    def _input_type(self) -> Type[ComponentArgsT]:
        """
        Extract the generic input types
        Returns:
            Type[ComponentArgsT]: The input schema type, used for validating
            input arguments.
        """
        return get_args(self.__orig_bases__[0])[0]

    def _return_type(self) -> Type[ComponentReturnT]:
        """
        Extract the generic return types
        Returns:
            Type[ReturnT]: The return schema type, used for validating return
            values.
        """
        return get_args(self.__orig_bases__[0])[1]

    def _parameters_parser(self) -> ParametersSchema:
        """
        Parse the input type to generate the parameters schema
        Returns:
        """
        try:
            model_schema: Dict[str, Any] = self.input_type.model_json_schema()
        except AttributeError:
            # make sure user can  use the component without valid input type
            return ParametersSchema(type="object", properties={}, required=[])

        if "$defs" in model_schema:
            model_schema = cast(
                Dict[str, Any],
                jsonref.replace_refs(obj=model_schema, proxies=False),
            )  # type: ignore
            del model_schema["$defs"]

        if "required" not in model_schema:
            model_schema["required"] = []

        parameters = ParametersSchema(
            type="object",
            properties=model_schema["properties"],
            required=model_schema["required"],
        )

        return parameters

    @classmethod
    def verify_list_args(
        cls,
        args_list: List[Union[str, Dict, BaseModel]],
    ) -> List[ComponentArgsT]:
        """
        Verify the list of stringify input arguments
        Args:
            args_list: List of stringify input arguments
        Returns:
            List[ComponentArgsT]: The input arguments
        """
        return_list = []
        for args in args_list:
            return_list.append(cls.verify_args(args))
        return return_list

    @classmethod
    def verify_args(cls, args: Union[str, Dict, BaseModel]) -> BaseModel:
        """
        Verify the stringify input arguments
        Args:
            args: Stringify input arguments
        Returns:
            ComponentArgsT: The input arguments
        """
        try:
            if isinstance(args, str):
                args_dict = json.loads(args)
            elif isinstance(args, BaseModel):
                args_dict = args.model_dump()
            else:
                args_dict = args
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

        # Get the ArgsT type from the current class
        args_type = get_args(cls.__orig_bases__[0])[0]

        # Validate the arguments using the Pydantic model
        try:
            validated_args = args_type(**args_dict)
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

        return validated_args

    @classmethod
    def return_value_as_string(cls, value: ComponentArgsT) -> str:
        if isinstance(value, BaseModel):
            dumped = value.model_dump()
            if isinstance(dumped, dict):
                return json.dumps(dumped)
            return str(dumped)

        return str(value)
