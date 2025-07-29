import litellm
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Optional, Union, Any, Literal
import pandas as pd
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
import json
from openai import OpenAI
from enum import Enum

from system_instructions import *
from prep_models import *


data_str = lambda d: f"\n\nData:\nThe dataset fields are as follows: {d}"
response_format_str = lambda f: f"\n\nRespond in this JSON schema format:\n{f.model_json_schema()}"


async def check_columns(apply, data_dict: dict, model="gpt-4o-mini"):
    assert isinstance(data_dict, dict), f"data_dict must be a dict, not: {type(data_dict)}"

    class ColumnsIdentify(BaseModel):
        """
        span_type: column if the action is only done on a select number of specified columns or dataset if the step should be applied across the dataset
        columns: an optional list of the columns the step should be applied to.
        """
        span_type: SpanTypes
        columns: list[Literal[*list(data_dict.keys())]]

    messages = [
        {"role": "system", "content": CHECK_SPAN_INSTRUCTIONS + data_str(data_dict) + response_format_str(ColumnsIdentify)},
        {"role": "user", "content": apply}
    ]

    result = litellm.completion(
        api_key="sk-proj-5Ay4ISQv4kBgYs7ijKreT3BlbkFJeTIi2OKaevKN2bGcu0sc",
        model=model,
        messages=messages,
        request_timeout=120,
        temperature=0,
        num_retries=0,
        response_format=ColumnsIdentify
    )
    return ColumnsIdentify(**json.loads(result.choices[0].message["content"]))


async def get_step(apply, data_dict: dict, model="gpt-4o-mini"):

    messages = [
        {"role": "system", "content": COLUMN_INSTRUCTIONS + data_str(data_dict) + response_format_str(StepIdentify)},
        {"role": "user", "content": apply}
    ]

    result = litellm.completion(
        api_key="sk-proj-5Ay4ISQv4kBgYs7ijKreT3BlbkFJeTIi2OKaevKN2bGcu0sc",
        model=model,
        messages=messages,
        request_timeout=120,
        temperature=0,
        num_retries=0,
        response_format=StepIdentify
    )
    return StepIdentify(**json.loads(result.choices[0].message["content"]))


async def get_builtin(apply, data_dict: dict, builtin_class, model="gpt-4o-mini"):
    assert builtin_class in builtin_classes, f"Class not one of the chosen ones"
    sig = inspect.signature(builtin_class.__init__)


    fields = {name: param.annotation for name, param in sig.parameters.items() if name != 'self'}
    fields = {**fields, '__module__': builtin_class.__module__}
    print(fields)
    exit()
    pydantic_model = type(f"{builtin_class.__name__}Model", (BaseModel,), fields)
    print(pydantic_model)


