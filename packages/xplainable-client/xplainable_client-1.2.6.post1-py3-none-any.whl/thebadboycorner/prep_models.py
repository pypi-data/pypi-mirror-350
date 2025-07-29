from enum import Enum
from pydantic import BaseModel
from typing import Optional, Literal
from sklearn.preprocessing import *
from sklearn.impute import *
import inspect


class SpanTypes(str, Enum):
    COLUMN = "column"
    DATASET = "dataset"


class ColumnsIdentify(BaseModel):
    """
    span_type: column if the action is only done on a select number of specified columns or dataset if the step should be applied across the dataset
    columns: an optional list of the columns the step should be applied to.
    """
    span_type: SpanTypes
    columns: Optional[list[str]]


class StepTypes(str, Enum):
    BUILTIN = "builtin"
    FUNCTION = "function"
    CUSTOM = "custom"

builtin_classes = [
    StandardScaler,
    MinMaxScaler,
    MaxAbsScaler,
    RobustScaler,
    OneHotEncoder,
    LabelEncoder,
    OrdinalEncoder,
    Binarizer,
    PolynomialFeatures,
    KBinsDiscretizer,
    SimpleImputer,
    KNNImputer,
    MissingIndicator,
    Normalizer,
    PowerTransformer,
    QuantileTransformer,
]


class StepIdentify(BaseModel):
    """
    step_type:
        'builtin' if the action can be done by any of the built-in sklearn preprocessing classes,
        'function' if the action required a FunctionTransformer,
        'custom' if a new custom class inheriting is needed to perform the action
    proposed_step_class: The sklearn step class to be used
    """
    step_type: StepTypes
    proposed_step_class: Optional[Literal[*[b.__name__ for b in builtin_classes]]]


class ActionType(str, Enum):
    DROP = "drop"
    MODIFY = "modify"
    CREATE = "create"


class StepType(str, Enum):
    BUILTIN = "built_in"
    FUNC = "func_transformer"
    COlUMN = "column_transformer"
    CLASS = "custom_class"
    NONE = "none"


class TypeResponse(BaseModel):
    """
    step_type: StepType - the type of the step required to perform the transformation, one of:
        built_in: the action can be performed by existing sklearn preprocessing class
        func_transformer: the action can be performed with a FunctionTransformer with a defined function or a lambda function
        column_transformer: the action can be performed with a ColumnTransformer with a defined function or a lambda function
        custom_class: the actions requires a fit on the data and thus must be a custom class
        none: the specifed action is likely not achievable given the data or other constraints
    action_type: ActionType - the type of the general / rough type of action the user wants to perform:
        drop: drop one or many columns
        modify: modify the values of one or many columns
        create: create a new column
    message: Optional[str] - a supplementing message with a suggestion on how to implement the action using the bulit-ins an explanation of why the step is not feasible if NONE is chosen for step_type
    """
    step_type: StepType
    action_type: ActionType
    message: Optional[str]


class CustomStepDefinition(BaseModel):
    """
    step_class_definition: str - just python class codeblock, should start with class, no comments included, no imports
    step_class_instantiation: str - python object instantiation code to instantiate the class defined in definition
    step_name: str - name of the step in the pipeline
    columns: list of column names the step should be applied to
    """
    step_class_definition: str
    step_class_instantiation: str
    step_name: str
    columns: list[str]


class BuiltinStepDefinition(BaseModel):
    """
    step_class: the sklearn class to be used, such as MinMaxScaler, etc.
    step_class_instantiation: python object instantiation code for the step: MinMaxScaler()
    step_name: simple name of the step
    columns: list of column names the step should be applied to
    """
    step_class: str
    step_class_instantiation: str
    step_name: str
    columns: list[str]

