import getpass
import time
import json
import requests

from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from mst.core.usage_logger import LogAPIUsage
from mst.authsrv import AuthSRV


class TDX:
    """Interface for TDX API"""

    def __init__(
        self,
        user: str = getpass.getuser(),
        proxy: bool = False,
        password: str = None,
        sandbox: bool = False,
    ):
        """Create instance of TDX

        Args:
            sandbox (bool, optional): whether to connect to sandbox instance
            user (str, optional): username for tdx api connections
            proxy (bool, optional): True to enable IT bulkproxy usage
            password (str, optional): password for tdx api connections
                will retrieve from 'tdx' instance in authsrv if not specified
        """
        LogAPIUsage()

        self.user = user
        if password:
            self.password = password
        else:
            self.password = AuthSRV().fetch(instance="tdx", user=self.user)

        # Session state
        self.session_obj = None
        self.session_ctime = 0
        self.session_token = None
        self.sandbox = sandbox
        self.proxy = proxy

        # Hardwired, they should never change during normal usage
        self.app_id = 57
        self.portal_app_id = 48

    def url(self, path: str):
        """returns a url with a particular sub path based on sandbox status

        Args:
            path (str): relative API path

        Returns:
            str: the full URL
        """
        url = ""
        if self.sandbox:
            url = "https://tdx.umsystem.edu/SBTDWebApi"
        else:
            url = "https://tdx.umsystem.edu/TDWebApi"

        if path and path.startswith("/"):
            url = url + path
        else:
            url = url + "/" + path

        return url

    def session(self):
        """returns a requests session object preauthenticated and configured with appropriate proxies for tdx API usage

        Args:
            None

        Returns:
            requests.Session() object

        """
        session_cutoff = time.time() - 3600
        if self.session_obj and self.session_ctime > session_cutoff:
            return self.session_obj

        # Yes, these should be http urls, it's being used as a 'CONNECT' proxy for https URLs
        session = requests.Session()
        if self.proxy:
            session.proxies.update(
                {
                    "http": "http://app-bulkproxy-vip.srv.mst.edu:3128",
                    "https": "http://app-bulkproxy-vip.srv.mst.edu:3128",
                }
            )

        # Establish a default retry handler - delay = backoff * 2^attempts
        retry_strategy = Retry(
            backoff_factor=5,
            total=7,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        # Update global object
        self.session_obj = session
        self.session_ctime = time.time()

        # get a login session cookie/etc.
        body = {"UserName": self.user, "Password": self.password}

        response = session.post(
            url=self.url("/api/auth/login"),
            data=json.dumps(body),
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            self.session_token = response.text
        else:
            raise RuntimeError("failed to obtain session token")

        # Establish default session auth
        session.headers.update({"Authorization": f"Bearer {self.session_token}"})

        return session
