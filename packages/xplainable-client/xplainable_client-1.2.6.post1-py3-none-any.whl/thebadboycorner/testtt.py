from pydantic import create_model
from pp_funcs import *
from typing import get_type_hints, Union, get_origin, get_args
import typing
import types


def test(a: Union[int | str] = 2.5, b: str = "3", c: tuple[int, int, str] = 1, d: Union[int, str] = 1) -> str:
    pass


def full_sig(cal, accept_different_default=True):
    print(cal.__annotations__)
    sig = inspect.signature(cal)
    print()
    # sig.parameters.get(param_name)

    # field_types = {name: annotation for name, annotation in sig.items() if name != 'self'}
    field_types = {}
    for p in sig.parameters.values():
        arg_type = None

        if p.annotation is not inspect.Parameter.empty:  # There is an annotation
            arg_type = p.annotation  # base truth

        if p.default is not inspect.Parameter.empty:  # There is a default
            if arg_type is None:  # no annotation so type is the type of default
                arg_type = type(p.default)
            else:
                origin = get_origin(arg_type)
                if origin in (types.UnionType, typing.Union):  # the annotated type is a Union

                    if type(p.default) not in get_args(arg_type) and accept_different_default:
                        # add the default type to the detected type
                        arg_type = Union[*(type(p.default), *(get_args(arg_type)))]
                else:
                    if type(p.default) is not arg_type and accept_different_default:
                        # add the default type and the annotation type to a union
                        arg_type = Union[*(type(p.default), arg_type)]
                    # print('Union: ', get_args(arg_type), p.default, )
                # print(arg_type, isinstance(arg_type, types.UnionType) or get_origin(arg_type) is Union)
                # print(get_origin(arg_type))
                # print(get_args(arg_type))
                # arg_type = Union[arg_type, type(p.default)]

        field_types.update(
            {
                p.name: (
                    arg_type,
                    p.default if p.default is not inspect.Parameter.empty else None
                )
            }
        )
        print()
    print(field_types)

    model = create_model(
        'GeneratedModel',
        **field_types  # {f[0]: (f[1], f[2]) for f in sig}
    )
    print(model)
    schema = model.schema_json(indent=2)
    print(schema)
    exit()


    print(sig.__annotations__)
    type_hints = get_type_hints(cal)
    # print(sig)
    # print(type_hints)
    # exit()

    param_types = list()
    for param_name in sig.parameters.keys():
        annotation_types = set()
        annotation = sig.parameters.get(param_name).annotation
        if annotation is inspect.Parameter.empty:
            pass
        else:
            if isinstance(annotation, type):
                annotation_types.add(annotation)
            elif isinstance(annotation, types.UnionType):
                annotation_types.update(set(annotation.__args__))
            elif isinstance(annotation, tuple):
                annotation_types.update(tuple)
            else:
                annotation_types.add(Any)

        default = sig.parameters.get(param_name).default

        if default is inspect.Parameter.empty or default is None:
            pass
        else:
            annotation_types.add(type(default))
        {get_type(t) for t in annotation_types}
        param_types.append(
            (
                param_name,
                Union[*annotation_types] if len(annotation_types) > 1 else
                list(annotation_types)[0] if len(annotation_types) > 0 else
                Any,
                default if default is not inspect.Parameter.empty else None
            )
        )
        print(param_types)

    return param_types
    """
    exit()


    param_types = {
        name: type_hints.get(name, param.annotation)
        for name, param in sig.parameters.items()
    }
    print(
        param_types.keys()
    )
    print(
        param_types.values()
    )

    print(param_types['b'])
    print(type(param_types['b']))

    print(param_types['d'])
    print(type(param_types['d']))

    param_defaults = {
        name: param.default if param.default is not inspect.Parameter.empty else None
        for name, param in sig.parameters.items()
    }
    print()
    print(
        param_defaults.keys()
    )
    print(
        [type(v) for v in param_defaults.values()]
    )
    print()
    """


sig = full_sig(MinMaxScaler)
print()
print(sig)
model = create_model(
    'GeneratedModel',
    **{f[0]: (f[1], f[2]) for f in sig}
)
print(
    model
)
schema = model.schema_json(indent=2)
print(schema)

exit()
field_types = {name: annotation for name, annotation in sig.items() if name != 'self'}


def create_pydantic_model_from_dict(field_types, field_defaults=None):
    # Prepare the fields dictionary for create_model
    fields = {}
    for field_name, type_set in field_types.items():
        # Handle 'typing.Any' type
        if Any in type_set:
            field_type = Any
        else:
            # Remove NoneType if present and build the Union
            type_set.discard(type(None))
            if len(type_set) == 1:
                field_type = next(iter(type_set))
            else:
                field_type = Union[tuple(type_set)]

        # Get default value if available
        default_value = field_defaults.get(field_name, ...) if field_defaults else ...

        # Assign the field with its type and default value
        fields[field_name] = (field_type, default_value)

    # Create the Pydantic model dynamically
    model = create_model('GeneratedModel', **fields)
    return model

field_defaults = {
    'c': 'default_value_for_c',
    'd': 100
}

# Create the Pydantic model
GeneratedModel = create_pydantic_model_from_dict(field_types, field_defaults)

# Generate JSON schema
schema = GeneratedModel.schema_json(indent=2)
print(schema)


exit()


class XpBaseTransformer(BaseEstimator, TransformerMixin):
    pass


llm_model = "gpt-4o-mini"


data = pd.read_csv('telco_customer_churn.csv')
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
data = data.dropna()
print("Data Loaded")

# convert to dict of {column: type}
types = data.dtypes
dtype_dict = {
    col: 'numeric' if dtype in [int, float, 'int64', 'float64'] else 'categorical' if dtype in [str, 'O'] else str(dtype)
    for col, dtype in types.items()
}
del data
try:
    print(data)
except Exception as e:
    print(e)
# print(dtype_dict)
# exit()


apply = "minmax scale monthly charges"
# apply = "remove senior citizen column"
# apply = "swap the values of senior citizen"
# apply = "fly to the moon"
# apply = "change online security to lowercase"
# apply = "rename the online security column to Security"
# apply = "in online security remove the rows where the value is the values that has the most letters in it for the column"


print("\nTypes Loaded\n")
# print(TypeResponse.model_json_schema())
# print()
# exit()


def remove_column(column_name: list[str]):
    return lambda x: x.drop([column_name])


def modify_apply(apply, data) -> str:

    messages = [
        {"role": "system", "content": MODIFY_INSTRUCTIONS(data)},
        {"role": "user", "content": apply}
    ]

    result = litellm.completion(
        api_key="sk-proj-5Ay4ISQv4kBgYs7ijKreT3BlbkFJeTIi2OKaevKN2bGcu0sc",
        model=llm_model,
        messages=messages,
        request_timeout=120,
        temperature=0,
        num_retries=0
    )
    return result.choices[0].message["content"]


def column_step(apply, data, columns) -> StepIdentify:

    messages = [
        {"role": "system", "content": COLUMN_INSTRUCTIONS(data, columns)},
        {"role": "user", "content": apply}
    ]

    result = litellm.completion(
        api_key="sk-proj-5Ay4ISQv4kBgYs7ijKreT3BlbkFJeTIi2OKaevKN2bGcu0sc",
        model=llm_model,
        messages=messages,
        request_timeout=120,
        temperature=0,
        num_retries=0,
        response_format=StepIdentify
    )
    return StepIdentify(**json.loads(result.choices[0].message["content"]))


def check_apply(apply, data) -> TypeResponse:

    messages = [
        {"role": "system", "content": CHECK_SYSTEM_INSTRUCTIONS(data)},
        {"role": "user", "content": apply}
    ]

    result = litellm.completion(
        api_key="sk-proj-5Ay4ISQv4kBgYs7ijKreT3BlbkFJeTIi2OKaevKN2bGcu0sc",
        model=llm_model,
        messages=messages,
        request_timeout=120,
        temperature=0,
        num_retries=0,
        response_format=TypeResponse
    )
    return TypeResponse(**json.loads(result.choices[0].message["content"]))


def custom_class_apply(apply, data) -> CustomStepDefinition:

    messages = [
        {"role": "system", "content": CUSTOM_CLASS_INSTRUCTIONS(data)},
        {"role": "user", "content": apply}
    ]

    result = litellm.completion(
        api_key="sk-proj-5Ay4ISQv4kBgYs7ijKreT3BlbkFJeTIi2OKaevKN2bGcu0sc",
        model=llm_model,
        messages=messages,
        request_timeout=120,
        temperature=0,
        num_retries=0,
        response_format=CustomStepDefinition
    )
    return CustomStepDefinition(**json.loads(result.choices[0].message["content"]))


def builtin_step_apply(apply, data, suggestion: str = None) -> BuiltinStepDefinition:

    messages = [
        {"role": "system", "content": BUILTIN_CLASS_INSTRUCTIONS(data, suggestion)},
        {"role": "user", "content": apply}
    ]

    result = litellm.completion(
        api_key="sk-proj-5Ay4ISQv4kBgYs7ijKreT3BlbkFJeTIi2OKaevKN2bGcu0sc",
        model=llm_model,
        messages=messages,
        request_timeout=120,
        temperature=0,
        num_retries=0,
        response_format=BuiltinStepDefinition
    )
    return BuiltinStepDefinition(**json.loads(result.choices[0].message["content"]))


print("Running...")

# checked = modify_apply(apply, data)
# print(checked)
# exit()

pipline = Pipeline([])


checked = asyncio.run(check_columns(apply, dtype_dict))
print(checked.span_type)
print(checked.columns)

if checked.span_type == SpanTypes.COLUMN:
    checked = asyncio.run(get_step(apply, dtype_dict))
    print(checked.step_type)
    print(checked.proposed_step_class)
    clss = {b.__name__: b for b in builtin_classes}.get(checked.proposed_step_class, None)
    print(clss)
    print(inspect.signature(clss))
    print()
    asyncio.run(get_builtin(apply, dtype_dict, clss))

exit()

print()
checked = check_apply(apply, dtype_dict)
print(checked.step_type)
print(checked.action_type)
print(checked.message)
print()


if checked.step_type in [StepType.CLASS, StepType.FUNC, StepType.NONE]:
    result = custom_class_apply(apply, dtype_dict)
    print(result.step_class_definition)
    print()
    print(result.step_class_instantiation)
    print()
    print(result.step_name)
    print()
    print(result.columns)
    print()
elif checked.step_type == StepType.BUILTIN:
    result = builtin_step_apply(apply, dtype_dict, checked.message)
    print()
    print(result.step_class)
    print(result.step_class_instantiation)
    print(result.step_name)
    print(result.columns)
    pipline.steps.append((result.step_name, ))

"""
"StandardScaler",
"MinMaxScaler",
"MaxAbsScaler",
"RobustScaler",
"OneHotEncoder",
"LabelEncoder",
"OrdinalEncoder",
"Binarizer",
"PolynomialFeatures",
"KBinsDiscretizer",
"SimpleImputer",
"KNNImputer",
"MissingIndicator",
"Normalizer",
"PowerTransformer",
"QuantileTransformer",
"VarianceThreshold",
"FunctionTransformer",
"""