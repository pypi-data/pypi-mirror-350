from ._client_cog_base import *
import pandas as pd
import json
from xplainable_client.client.utils import get_df_delta
from xplainable.preprocessing.pipeline import XPipeline
from xplainable.preprocessing import transformers as xtf
from xplainable.preprocessing.transformers import XBaseTransformer


class Preprocessing(Client_Cog):

    def create_preprocessor(
        self, preprocessor_name: str, preprocessor_description: str,
        pipeline: XPipeline, df: pd.DataFrame = None
    ) -> str:
        payload = {
            "preprocessor_name": preprocessor_name,
            "preprocessor_description": preprocessor_description
        }

        payload.update(self.prepare_pipeline(pipeline, df))

        url = f'{self.session.hostname}/client/models/create'
        response = self.session._session.post(url=url, json=payload)
        content = self.session.get_response_content(response)
        return content

    def prepare_pipeline(self, pipeline, df) -> dict:
        # Structure the stages and deltas
        stages = []
        deltas = []
        if df is not None:
            before = df.copy()
            deltas.append({"start": json.loads(before.head(10).to_json(orient='records'))})
            delta_gen = pipeline.transform_generator(before)
        for stage in pipeline.stages:
            step = {
                'feature': stage['feature'],
                'name': stage['name'],
                'params': stage['transformer'].__dict__
            }
            if "code_def" in stage.keys():
                step["code_def"] = stage["code_def"]
            stages.append(step)
            if df is not None:
                after = delta_gen.__next__()
                delta = get_df_delta(before.copy(), after.copy())
                deltas.append(delta)
                before = after.copy()
        # Get current versions
        versions = {
            "xplainable_version": self.session.xplainable_version,
            "python_version": self.session.python_version
        }
        # Create payload
        payload = {
            "stages": stages,
            "deltas": deltas,
            "versions": versions
        }
        return payload

    def create_preprocessor_id(self, preprocessor_name: str, preprocessor_description: str) -> str:
        """ Creates a new preprocessor and returns the preprocessor id.
        Args:
            preprocessor_name (str): The name of the preprocessor
            preprocessor_description (str): The description of the preprocessor
        Returns:
            int: The preprocessor id
        """
        payoad = {
            "preprocessor_name": preprocessor_name,
            "preprocessor_description": preprocessor_description
        }
        response = self.session._session.post(
            url=f'{self.session.hostname}/v1/{self.session._ext}/create-preprocessor',
            json=payoad
        )

        preprocessor_id = self.session.get_response_content(response)

        return preprocessor_id

    def create_preprocessor_version(
        self, preprocessor_id: str, pipeline: XPipeline, df: pd.DataFrame = None
    ) -> str:
        """ Creates a new preprocessor version and returns the version id.
        Args:
            preprocessor_id (int): The preprocessor id
            pipeline (xplainable.preprocessing.pipeline.Pipeline): pipeline
        Returns:
            int: The preprocessor version id
        """
        payload = self.prepare_pipeline(pipeline, df)

        # Create a new version and fetch id
        url = (
            f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/'
            f'{preprocessor_id}/add-version'
            )

        response = self.session._session.post(url=url, json=payload)
        version_id = self.session.get_response_content(response)["version_id"]
        return version_id

    def update_preprocessor_version(
        self, preprocessor_id: str, version_id: str, pipeline: XPipeline, df: pd.DataFrame = None
    ) -> str:
        """ Updates version.
        Args:
            preprocessor_id (int): The preprocessor id
            version_id (int): The preprocessor version id
            pipeline (xplainable.preprocessing.pipeline.Pipeline): pipeline
        Returns:
            int: The preprocessor version id
        """
        payload = self.prepare_pipeline(pipeline, df)

        # Create a new version and fetch id
        url = (
            f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/'
            f'{preprocessor_id}/update-version/{version_id}'
            )

        response = self.session._session.post(url=url, json=payload)
        version_id = self.session.get_response_content(response)
        return version_id

    def list_preprocessors(self) -> list:
        """ Lists all preprocessors of the active user's team.
        Returns:
            dict: Dictionary of preprocessors.
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors'
            )
        data = self.session.get_response_content(response)
        [i.pop('user') for i in data]
        return data

    # get_preprocessor

    def list_preprocessor_versions(self, preprocessor_id: int) -> list:
        """ Lists all versions of a preprocessor.
        Args:
            preprocessor_id (int): The preprocessor id
        Returns:
            dict: Dictionary of preprocessor versions.
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}/versions'
            )

        data = self.session.get_response_content(response)
        [i.pop('user') for i in data]
        return data

    def load_preprocessor(
            self, preprocessor_id: int, version_id: int,
            gui_object: bool = False, response_only: bool = False):
        """ Loads a preprocessor by preprocessor_id and version_id.
        Args:
            preprocessor_id (int): The preprocessor id
            version_id (int): The version id
            response_only (bool, optional): Returns the preprocessor metadata.
        Returns:
            xplainable.preprocessing.pipeline.Pipeline: The loaded pipeline
        """
        def build_transformer(stage):
            """Build transformer from metadata"""
            if not hasattr(xtf, stage["name"]):
                if "code_def" in dict(stage).keys():
                    exec(stage["code_def"], globals())
                    return globals()[stage["name"]](**stage['params'])
                else:
                    raise ValueError(f"{stage['name']} does not exist in the transformers module")
            # Get transformer function
            func = getattr(xtf, stage["name"])
            return func(**stage['params'])

        try:
            preprocessor_response = self.session._session.get(
                url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}/versions/{version_id}'
                )
            response = self.session.get_response_content(preprocessor_response)
            if response_only:
                return response
        except Exception as e:
            raise ValueError(
            f'Preprocessor with ID {preprocessor_id}:{version_id} does not exist')

        stages = response['stages']
        deltas = response['deltas']

        pipeline = XPipeline()
        for stage in stages:
            p_stage = {
                    'feature': stage['feature'],
                    'name': stage['name'],
                    'transformer': build_transformer(stage)
                }
            if "code_def" in stage.keys():
                p_stage["code_def"] = stage["code_def"]
            pipeline.add_stages(
                [p_stage]
            )

        if not gui_object:
            return pipeline
        else:
            return pipeline
            """
            from ..gui.screens.preprocessor import Preprocessor
            pp = Preprocessor()
            pp.pipeline = pipeline
            pp.df_delta = deltas
            pp.state = len(pipeline.stages)
            return pp
            """


    def get_preprocessor_version_pipeline(self, preprocessor_id: str, version_id: str):
        """ Returns the pipeline of a preprocessor version.
        Args:
            preprocessor_id (int): The preprocessor id
            version_id (int): The version id
        Returns:
            xplainable.preprocessing.pipeline.Pipeline: The pipeline
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}/versions/{version_id}/pipeline'
            )
        data = self.session.get_response_content(response)
        return data

    def delete_preprocessor_version(self, preprocessor_id: str, version_id: str):
        """ Deletes a preprocessor version.
        Args:
            preprocessor_id (int): The preprocessor id
            version_id (int): The version id
        Return:
            json: A json response
        """
        response = self.session._session.delete(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}/versions/{version_id}'
            )
        return response

    def restore_preprocessor_version(self, preprocessor_id: str, version_id: str):
        """ Restores a preprocessor version.
        Args:
            preprocessor_id (int): The preprocessor id
            version_id (int): The version id
        Return:
            json: A json response.
        """
        response = self.session._session.put(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}/versions/{version_id}/restore'
            )
        return response

    def delete_preprocessor(self, preprocessor_id: str):
        """ Deletes a preprocessor.
        Args:
            preprocessor_id (int): The preprocessor id
        Return:
            json: A json response
        """
        response = self.session._session.delete(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}'
            )
        return response

    def restore_preprocessor(self, preprocessor_id: str):
        """ Restores a preprocessor.
        Args:
            preprocessor_id (int): The preprocessor id
        Return:
            json: A json response
        """
        response = self.session._session.post(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}/restore'
            )
        return response

    def check_signature(self, preprocessor_id: str, preprocessor_version_id: str, model_id: str, model_version_id: str):
        """ Checks the signature of a preprocessor version.
        Args:
            preprocessor_id (int): The preprocessor id
            preprocessor_version_id (int): The preprocessor version id
            model_id (int): The model id
            model_version_id (int): The model version id
        Return:
            dict: A json response of signatures_match, pipeline_columns, model_columns.
        """

        payload = {
            'model_id': model_id,
            'version_id': model_version_id
        }
        response = self.session._session.post(
            url=f'{self.session.hostname}/v1/{self.session._ext}/preprocessors/{preprocessor_id}/versions/{preprocessor_version_id}/check-signature',
            json=payload
        )
        output = self.session.get_response_content(response)
        return output



