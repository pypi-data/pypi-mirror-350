from prep_models import *

OVERALL_INSTRUCTIONS = """
You want to create an interactive Scikit-learn preprocessing pipeline where the steps are determined by asking the end-user how they would like to manipulate their provided data, and then persist these steps for future use.

You are a part of a system that takes a user's instruction on how to manipulate a dataset and turns it into a pipeline step.

"""


MODIFY_INSTRUCTIONS = lambda data: f"""
You are an assisting program to a developer creating pipelines to manipulate and preprocess data in a manor that the end user specifies.
You are given the user's desired action and then you must return a brief but comprehensive explanation of what the user intends to be done.
Don't include any code.

Data:
The dataset fields are as follows: {data}

Return the response as an instruction to a larger language model
"""

CHECK_SPAN_INSTRUCTIONS = f"""
You are a part of a system that takes a user's instruction on how to manipulate a dataset and turns it into a pipeline step.

In this step, you simply respond with what type of step this is, either a whole-dataset step or one that only applies to specific columns.
If the step will only be applied to specific columns, also return a list of columns names from the dataset that the step should be applied to
This will be used to decide if the step will be added to the pipeline as-is or as a step in ColumnTransformer step that will be added to the pipeline.
"""

COLUMN_INSTRUCTIONS = f"""
You are a part of a system that takes a user's instruction on how to manipulate a dataset and turns it into a pipeline step.

Previously it has been determined that the pipeline step will be a ColumnTransformer.

In this step, you simply respond with what class the step inside the ColumnTransformer should be, one of the following options:
the action can be performed by one of the built in classes of sklearn preprocessing, or the action requires a FunctionTransformer or the action requires a custom class 
"""

CHECK_SYSTEM_INSTRUCTIONS = lambda data: f"""
In Python
You are to help users create a sklearn ColumnTransformer preprocessor step to accomplish the task that the user specifies.
Ignore any other methods of accomplishing the task like pandas methods, etc. the action must become a step in a ColumnTransformer 

Data:
The dataset fields are as follows: {data}

Respond in this JSON schema:
{TypeResponse.model_json_schema()}
"""
"""
the preprocessor st
The preprocessor step must only use either sklearn components or a custom class inheriting from sklearn.
The preprocessor step may use custom step class like {'{'}class CustomTransformer(BaseEstimator, TransformerMixin):{'}'}.
the preprocessor step can not be FunctionTransformer or a ColumnTransformer at all,
if something is required that cannot be done with sklearn components, it should be a custom class
Return weather a custom class is needed, or if the step can be constructed by existing sklearn components; or finally if this preprocessing step is likely not feasible
the final pipeline will the .fit() on the data and then .transform() on the data.
Assume all import have been done
"""

CUSTOM_CLASS_INSTRUCTIONS = lambda data: f"""
In Python
You will help the user create a preprocessing step.
Provide code for a custom class that will be used as a step in a sklearn / scikit-learn Pipeline.
the class should inherit from the following class:

class XpBaseTransformer(BaseEstimator, TransformerMixin):
    pass


Data:
The dataset fields are as follows: {data}

Respond in this JSON schema:
{CustomStepDefinition.model_json_schema()}
"""


def BUILTIN_CLASS_INSTRUCTIONS(data, suggestion: str = None):
    suggest_text = ""
    if suggestion:
        suggest_text = f"Here is a suggestions how it could be done: suggestion"

    return f"""
    In Python
    return which built-in sklearn class will perform the action defined by the user.
    This object will be a part of a ColumnTransformer.
    The class will be used to perform a preprocessing step defined by the user message.ies to
    Provide both the class name and the instantiation code with relevant args and columns the step appl
    {suggest_text}
    
    Data:
    The dataset fields are as follows: {data}

    Respond in this JSON schema:
    {BuiltinStepDefinition.model_json_schema()}
    """


SYSTEM_INSTRUCTIONS = lambda data: f"""
In Python
Provide code to create a preprocessing step for a sklearn / scikit-learn ColumnTransformer that will be added to a Pipeline.

The response should adhere to the following constraints:
Use either: existing sklearn preprocessor steps or a FunctionTransformer
If a FunctionTransformer is used, the response must include the definition of the function i.e. "def func(..." but don't add any comments

There is the following function that can be used to create column drop steps with FunctionTransformer:
def remove_column(column_name: list[str]):
    return lambda x: x.drop([column_name])
This function has been defined and does not need to be defined again.


Data:
The dataset fields are as follows: {data}, make sure to use the correct column names in the instantiation code.


You are to generate this preprocessor for the input provided by the user.
"""

"""
Here are examples of inputs and the expected output to help with understanding and formatting:

Apply: Combine 'First Name' and 'Last Name' columns
Output: {{
             "definition": "class CombineColumns(XBaseTransformer):\n\tsupported_types = ['categorical']\n\tdef __init__(self, columns: list[str], new_column_name: str):\n\t\tsuper().__init__()\n\t\tself.columns = columns\n\t\tself.new_column_name = new_column_name\n\tdef transform(self, x: pd.DataFrame) -> pd.DataFrame:\n\t\tx[self.new_column_name] = x[self.columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)\n\t\treturn x.drop(self.columns, axis=1)"
                           "instantiation": "CombineColumns(columns=['First Name', 'Last Name'])"
         }}
"""


