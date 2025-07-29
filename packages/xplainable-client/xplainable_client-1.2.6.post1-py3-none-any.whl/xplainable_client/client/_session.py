from functools import cached_property
import xplainable
import json
from requests.adapters import HTTPAdapter
import ipywidgets
import sys
from IPython.display import display

from urllib3.util import Retry
import requests


class Session:
    """ A client for interfacing with the xplainable web api (xplainable cloud).

    Access models, preprocessors and user data from xplainable cloud. API keys
    can be generated at https://beta.xplainable.io.

    Args:
        api_key (str): A valid api key.
    """

    def __init__(self, api_key=None, hostname='https://api.xplainable.io', org_id=None, team_id=None):
        if not api_key:
            raise ValueError('A valid API Key is required. Generate one from the xplainable app.')

        self.api_key = api_key
        self.hostname = hostname
        self._setup_session()  # Set up the session and other initialization steps

        print("gefradghjk")
        print(f'{self.hostname}/client/connect')
        response = self._session.get(
            url=f'{self.hostname}/client/connect',
        )
        content = json.loads(response.content)
        print(content)
        self.username = content["username"]
        self.key = content["key"]
        self.expires = content["expires"]
        print(self.username, self.key, self.expires)

        version_info = sys.version_info
        self.python_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'
        self.xplainable_version = xplainable.__version__
        print(self.python_version)
        print(self.xplainable_version)
        return

        if org_id is None or team_id is None:
            self._ext = f"organisations/{self.user_data['organisation_id']}/teams/{self.user_data['team_id']}"

            # You can still use the _render_init_table here if you want to display it,
            # or you can return the data dict for a more script-friendly approach.
            # data = self._gather_initialization_data()
        else:
            self._ext = f"organisations/{org_id}/teams/{team_id}"

    @cached_property
    def user_data(self):
        """ Retrieves the user data for the active user.
        Returns:
            dict: User data
        """
        response = self._session.get(
            url=f'{self.hostname}/client/connect',
        )
        if response.status_code == 200:
            return self.get_response_content(response)

        else:
            raise Exception(
                f"{response.status_code} Unauthenticated. {response.json()['detail']}"
            )

    def _setup_session(self):
        """ Set up the session with retry strategy and session headers. """
        self._session = requests.Session()
        self._session.headers['api_key'] = self.api_key
        retry_strategy = Retry(total=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount(self.hostname, adapter)

    def get_response_content(self, response):
        print("get_response_content")
        print(response)
        if response.status_code == 200:
            return json.loads(response.content)
        elif response.status_code == 401:
            err_string = "401 Unauthorised"
            content = json.loads(response.content)
            if 'detail' in content:
                err_string = err_string + f" ({content['detail']})"

            raise Exception(err_string)
        else:
            raise Exception(response.status_code, json.loads(response.content))

    def _gather_initialization_data(self):
        """ Gather data to display or return upon initialization. """
        version_info = sys.version_info
        self.python_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'
        self.xplainable_version = xplainable.__version__

        return {
            "xplainable version": self.xplainable_version,
            "python version": self.python_version,
            "user": self.user_data['username'],
            "organisation": self.user_data['organisation_name'],
            "team": self.user_data['team_name'],
        }

    @staticmethod
    def _render_init_table(data):
        from xplainable.gui.components import KeyValueTable, Header
        table = KeyValueTable(
            data,
            transpose=False,
            padding="0px 45px 0px 5px",
            table_width='auto',
            header_color='#e8e8e8',
            border_color='#dddddd',
            header_font_color='#20252d',
            cell_font_color='#374151'
        )
        header = Header('Initialised', 30, 16, avatar=False)
        header.divider.layout.display = 'none'
        header.title = {'margin': '4px 0 0 8px'}
        output = ipywidgets.VBox([header.show(), table.html_widget])
        display(output)


