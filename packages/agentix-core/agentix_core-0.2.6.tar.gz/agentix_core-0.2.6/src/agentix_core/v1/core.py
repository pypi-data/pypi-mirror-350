import os
import aiohttp
import logging
import math
import asyncio

logger = logging.getLogger("core.task")

#===================================================================================================
class Core:
    """Handles the calls to core APIs for task authentication, execution, and lifecycle management."""

    def __init__(
        self, 
        AGENT_NAME: str, 
        CORE_API: str, 
    ):
        """
        Initialize Core API handler with agent credentials and base API URL.

        Args:
            AGENT_NAME (str): The agent's username for authentication.
            CORE_API (str): Base URL of the Core API service.

        Raises:
            ValueError: If AGENT_NAME or CORE_API is missing or empty.
        """

        if not AGENT_NAME:
            raise ValueError("[INIT] AGENT_NAME is required and cannot be empty.")
        if not CORE_API:
            raise ValueError("[INIT] CORE_API is required and cannot be empty.")

        self.CORE_API = CORE_API.rstrip("/")
        self.AGENT_NAME = AGENT_NAME
        self.JWT_TOKEN = None

    #================================================================================================
    # login to Core and get JWT
    #================================================================================================
    async def login(self, PASSWORD: str = None) -> bool:
        """
        Authenticate the agent to Core using username/password and store JWT token.

        Args:
            PASSWORD (str): Password for the agent.

        Returns:
            bool: True if login is successful.

        Raises:
            ValueError: If password is not provided.
            RuntimeError: If authentication fails after retries.
        """

        logger.info(f"🔑 [LOGIN] Authenticating to Core API with user: {self.AGENT_NAME}")
        
        if not PASSWORD:
            raise ValueError("[LOGIN] PASSWORD must be provided to login.")

        logger.info("🔐 [LOGIN] Using username and password for logging to Core.")

        login_url = f"{self.CORE_API}/auth"
        headers = {"Referer": self.CORE_API}

        auth_payload = {
            "identifier": self.AGENT_NAME,
            "password": PASSWORD
        }

        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(login_url, json=auth_payload, headers=headers) as login_response:
                        login_json = await login_response.json()
                        if login_response.status == 200 and "jwt" in login_json:
                            self.JWT_TOKEN = login_json["jwt"]
                            logger.info(f"✅ [LOGIN] Login succeeded on attempt {attempt}")
                            break
                        else:
                            logger.warning(f"⚠️ [LOGIN] Login failed on attempt {attempt}: {login_response.status} - {login_json}")
            except Exception as e:
                logger.error(f"❌ [LOGIN] Login error on attempt {attempt}: {e}")

            if attempt < max_retries:
                logger.info("🔁 [LOGIN] Retrying in 2 seconds...")
                await asyncio.sleep(2)
            else:
                raise RuntimeError("[LOGIN] ❌ Authentication failed after maximum retry attempts.")

        return True
    #================================================================================================
    # Connect to Task in Core
    #================================================================================================
    async def connect_task(self, task_key: str) -> dict:
        """
        Establishes a session for the given task and returns job cookies.

        Args:
            task_key (str): Task key to identify the task session.

        Returns:
            dict: Dictionary of job cookies from the response.

        Raises:
            ValueError: If task_key is not provided or JWT is missing.
            RuntimeError: If the connection fails or cookies are missing.
        """
        logger.info(f"🔑 Authenticating to Core API with user: {self.AGENT_NAME}")

        if not self.JWT_TOKEN:
            logger.error("🔐 [CONNECT] Must login to Core before connecting to task.")
            raise ValueError("[CONNECT] Must login to Core before connecting to task.")
        
        if not task_key:
            logger.error("🔐 [CONNECT] Must provide task_key to connect.")
            raise ValueError("[CONNECT] task_key must be provided to connect.")
        
        connect_url = f"{self.CORE_API}/v1/tasks/{task_key}/connect"
    
        try:
            connect_headers = {
                "Authorization": f"Bearer {self.JWT_TOKEN}",
                "Referer": self.CORE_API
            }

            async with aiohttp.ClientSession() as connect_session:
                async with connect_session.post(connect_url, headers=connect_headers) as connect_response:
                    if connect_response.status != 200:
                        raise RuntimeError(f"❌ [CONNECT] Connect failed: {connect_response.status} - {await connect_response.text()}")

                    JOB_COOKIE = connect_session.cookie_jar.filter_cookies(self.CORE_API)
                    JOB_COOKIE = {k: morsel.value for k, morsel in JOB_COOKIE.items()}

                    if not JOB_COOKIE:
                        logger.error("❌ [CONNECT] No cookies found in the response.")
                        raise RuntimeError("❌ [CONNECT] No cookies found in the response.")
                    
                    logger.info("✅ JOB_COOKIE successfully returned from connect response")
                    return JOB_COOKIE

        except Exception as e:
            logger.error(f"[CONNECT] ❌ Error during connect request: {e}")
            raise RuntimeError(f"[CONNECT] ❌ Error during connect request: {e}")

    #================================================================================================
    # Start Task in Core
    #================================================================================================
    async def start_task(self, JOB_COOKIE: dict, task_key: str, reterive_agent_assignment: bool = False) -> dict:
        """
        Starts a task in Core by calling the `/start` endpoint.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task to start.
            reterive_agent_assignment (bool, optional): If True, Core will return agent assignment details.

        Returns:
            dict: JSON response returned by Core, typically containing updated task state or assignment data.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or response is invalid.
        """
        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [START-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [START-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
        
        if not task_key:
            logger.error("❌ [START-TASK] task_key is required and cannot be empty.")
            raise ValueError("❌ [START-TASK] task_key is required and cannot be empty.")

        try:
            logger.info(f">>> [START-TASK] Starting Task: {task_key}")

            start_task_url = f"{self.CORE_API}/v1/tasks/{task_key}/start"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Starting Task from {self.AGENT_NAME}",
                    "retrieveAgentAssignment": reterive_agent_assignment
                }
            }

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(start_task_url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None

                    if response.status == 200 and response_json is not None:
                        logger.info(f"<<<<< ✅ [START-TASK] Task Started!")
                        return response_json
                    else:
                        logger.error(f"❌ [START-TASK] Failed to start task. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [START-TASK] Failed to start task. HTTP Status: {response.status} - {response_json}")

        except Exception as e:
            logger.error(f"❌ [START-TASK] Error calling Start Task API: {e}")
            raise RuntimeError(f"❌ [START-TASK] Error calling Start Task API: {e}")

    #================================================================================================
    # Submit Task in Core
    #================================================================================================
    async def submit_task(self, JOB_COOKIE: dict, task_key: str) -> bool:
        """
        Submits a task in Core by calling the `/submit` endpoint.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task to submit.

        Returns:
            bool: True if task submission succeeds.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or submission is rejected.
        """

        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [SUBMIT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [SUBMIT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
        
        if not task_key:
            logger.error("❌ [SUBMIT-TASK] task_key is required and cannot be empty.")
            raise ValueError("❌ [SUBMIT-TASK] task_key is required and cannot be empty.")

        try:
            logger.info(f">>> [SUBMIT-TASK] Submit Task: {task_key}")

            url = f"{self.CORE_API}/v1/tasks/{task_key}/submit"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Submitting Task from {self.AGENT_NAME}"
                }
            }

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None
                    
                    if response.status != 200:
                        logger.error(f"❌ [SUBMIT-TASK]Failed to submit task. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [SUBMIT-TASK] Failed to submit task. HTTP Status: {response.status} - {response_json}")
                    
                    logger.info(f"<<<<< ✅ [SUBMIT-TASK] Task Submitted!")
                    return True

        except Exception as e:
            logger.error(f"❌ [SUBMIT-TASK] Error calling Submit Task API: {e}")
            raise RuntimeError(f"❌ [SUBMIT-TASK] Error calling Submit Task API: {e}")

    #================================================================================================
    # Reject Task in Core
    #================================================================================================
    async def reject_task(self, JOB_COOKIE: dict, task_key: str, rejection_reason: str = "No reason provided") -> bool:
        """
        Rejects a task in Core by calling the `/reject` endpoint.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task to reject.
            rejection_reason (str, optional): Reason for rejecting the task. Defaults to "No reason provided".

        Returns:
            bool: True if task rejection succeeds.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or rejection is unsuccessful.
        """

        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [REJECT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [REJECT-TASK] JOB_COOKIE is required and must be a non-empty dictionary.")

        if not task_key:
            logger.error("❌ [REJECT-TASK] task_key is required and cannot be empty.")
            raise ValueError("❌ [REJECT-TASK] task_key is required and cannot be empty.")
        
        try:
            logger.info(f">>> Reject Task: {task_key}")

            url = f"{self.CORE_API}/v1/tasks/{task_key}/reject"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {
                "data": {
                    "metadata": f"Rejecting Task from {self.AGENT_NAME}",
                    "reason": rejection_reason
                }
            }

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None
                    
                    if response.status != 200:
                        logger.error(f" ❌ [REJECT-TASK] Failed to reject task. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [REJECT-TASK] Failed to reject task. HTTP Status: {response.status} - {response_json}")
                    
                    logger.info(f"<<<<< ✅ Task Rejected!")
                    
                    return True

        except Exception as e:
            logger.error(f"❌ [REJECT-TASK] Error calling Reject Task API: {e}")
            raise RuntimeError(f"❌ [REJECT-TASK] Error calling Reject Task API: {e}")

    #================================================================================================
    # Update Task Usage in Core
    #================================================================================================
    async def update_usage(self, JOB_COOKIE: dict, task_key: str, duration_seconds: int):
        """
        Updates the usage time of a task in Core by calling the `/usage` endpoint.
        Duration is rounded up to the nearest full minute.

        Args:
            JOB_COOKIE (dict): Dictionary of cookies required for session authentication.
            task_key (str): Unique identifier of the task.
            duration_seconds (int): Number of seconds the task has been active.

        Returns:
            bool: True if the usage update is successful.

        Raises:
            ValueError: If JOB_COOKIE or task_key is missing or invalid.
            RuntimeError: If the HTTP request fails or the update is rejected.
        """

        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [USAGE] JOB_COOKIE is required and must be a non-empty dictionary.")
            raise ValueError("❌ [USAGE] JOB_COOKIE is required and must be a non-empty dictionary.")

        if not task_key:
            logger.error("❌ [USAGE] task_key is required and cannot be empty.")
            raise ValueError("❌ [USAGE] task_key is required and cannot be empty.")
        
        try:
            duration_minutes = math.ceil(duration_seconds / 60)
            logger.info(f">>> Update Usage for Task: {task_key}, Duration: {duration_seconds}s (~{duration_minutes} min)")

            url = f"{self.CORE_API}/v1/tasks/{task_key}/usage"
            headers = {"Referer": f"{self.CORE_API}"}
            request_body = {"amount": duration_minutes}

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.post(url, headers=headers, json=request_body, allow_redirects=False) as response:
                    response_json = await response.json() if "application/json" in response.headers.get("Content-Type", "") else None

                    if response.status not in [200, 201, 202, 203, 204]:
                        logger.error(f"❌ [USAGE] Failed to update usage. HTTP Status: {response.status} - {response_json}")
                        raise RuntimeError(f"❌ [USAGE] Failed to update usage. HTTP Status: {response.status} - {response_json}")
                    
                    logger.info("✅ [USAGE] Usage updated successfully!")
                    
                    return True

        except Exception as e:
            logger.error(f"❌ [USAGE] Error calling Update Usage API: {e}")
            raise RuntimeError(f"❌ [USAGE] Error calling Update Usage API: {e}")

    #================================================================================================
    # Download file from task API
    #================================================================================================
    async def download_file(self, JOB_COOKIE: dict, task_key: str, key: str, type: str, output_dir: str) -> str:
        """
        Downloads a file from the Core task API and saves it locally.

        Args:
            JOB_COOKIE (dict): Session cookies returned from `connect_task()`.
            task_key (str): The task key to identify the task.
            key (str): The file key (S3-style).
            file_type (str): The type/category of the file (e.g., "config", "media").
            output_dir (str): The local directory to save the file.

        Returns:
            str: Path to the saved local file.
        """
        logger.info(f"📥 Download request for task_key: {task_key} - file_key: {key} - type: {type} - into output folder: {output_dir}")
        
        if not JOB_COOKIE or not isinstance(JOB_COOKIE, dict):
            logger.error("❌ [DOWNLOAD] JOB_COOKIE must be a valid dictionary.")
            raise ValueError("❌ [DOWNLOAD] JOB_COOKIE must be a valid dictionary.")

        if not task_key or not key or not type or not output_dir:
            raise ValueError("❌ [DOWNLOAD] task_key, key, file_type, and output_dir are required.")

        download_url = f"{self.CORE_API}/v1/tasks/{task_key}/file?key={key}&type={type}"
        headers = {"Referer": self.CORE_API}

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Use base filename from key
        local_file_path = os.path.join(output_dir, os.path.basename(key))

        try:
            logger.info(f"📥 [DOWNLOAD] Downloading {key} from task API to {local_file_path} ...")

            async with aiohttp.ClientSession(cookies=JOB_COOKIE) as session:
                async with session.get(download_url, headers=headers) as response:
                    if response.status == 200:
                        file_data = await response.read()
                        with open(local_file_path, 'wb') as f:
                            f.write(file_data)

                        logger.info(f"✅ [DOWNLOAD] File saved to {local_file_path}")
                        return local_file_path

                    else:
                        logger.error(f"❌ [DOWNLOAD] Failed to fetch file. Status: {response.status}")
                        raise RuntimeError(f"❌ [DOWNLOAD] Failed to download file. HTTP Status: {response.status}")

        except Exception as e:
            logger.error(f"❌ [DOWNLOAD] Exception while downloading file: {e}")
            raise RuntimeError(f"❌ [DOWNLOAD] Error while downloading file: {e}")

    #================================================================================================
    # Create New Job in Core
    #================================================================================================
    async def new_job(self, workflow_id: int, customer: dict, language: str = "en", valid_until: int = 60) -> dict:
        """
        Creates a new job in the Core system using the specified workflow and customer info.

        Args:
            workflow_id (int): The ID of the workflow to trigger.
            customer (dict): Dictionary containing customer details.
            language (str, optional): Job language code. Defaults to "en".
            valid_until (int, optional): Job expiration in seconds. Defaults to 60.

        Returns:
            dict: The created job data returned by the API.

        Raises:
            ValueError: If required parameters are missing or invalid.
            RuntimeError: If job creation fails.
        """
        logger.info(f"🚀 Creating new job for workflow: {workflow_id}")

        if not self.JWT_TOKEN:
            raise ValueError("❌ [NEW-JOB] Must login to Core before creating a job.")

        if not isinstance(workflow_id, int):
            raise ValueError("❌ [NEW-JOB] workflow_id must be an integer.")

        if not isinstance(customer, dict):
            raise ValueError("❌ [NEW-JOB] customer must be a dictionary.")

        url = f"{self.CORE_API}/v1/jobs"
        headers = {
            "Authorization": f"Bearer {self.JWT_TOKEN}",
            "Referer": self.CORE_API,
            "Content-Type": "application/json"
        }

        payload = {
            "data": {
                "workflow": workflow_id,
                "validUntil": valid_until,
                "language": language,
                "customer": customer
            }
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    response_json = await response.json()

                    if response.status in [200, 201, 202, 203, 204]:
                        logger.info("✅ [NEW-JOB] Job created successfully.")
                        return response_json
                    else:
                        logger.error(f"❌ [NEW-JOB] Failed to create job. Status: {response.status}, Response: {response_json}")
                        raise RuntimeError(f"❌ [NEW-JOB] Failed to create job. Status: {response.status}, Response: {response_json}")

        except Exception as e:
            logger.error(f"❌ [NEW-JOB] Exception during job creation: {e}")
            raise RuntimeError(f"❌ [NEW-JOB] Exception during job creation: {e}")

    #================================================================================================
    # Start Job in Core
    #================================================================================================
    async def start_job(self, job_key: str, access_key: str, metadata: str) -> tuple:
        """
        Starts a job using jobKey and accessKey, returning job cookies and the response JSON.

        Args:
            job_key (str): The job key string.
            access_key (str): The access key string.
            metadata (str): Metadata string to be included in the request.

        Returns:
            tuple: (job_cookie_dict, response_json)
        """
        if not self.JWT_TOKEN:
            raise ValueError("[START-JOB] Must login to Core before starting job.")

        if not job_key or not access_key:
            raise ValueError("[START-JOB] job_key and access_key must be provided.")

        url = f"{self.CORE_API}/v1/jobs/{job_key}/{access_key}/start?noRedirect=true"
        headers = {
            "Authorization": f"Bearer {self.JWT_TOKEN}",
            "Referer": self.CORE_API
        }
        body = {
            "data": {
                "metadata": metadata
            }
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=body) as response:
                    response_json = await response.json()
                    if response.status not in [200]:
                        raise RuntimeError(f"❌ [START-JOB] Failed: {response.status} - {response_json}")

                    cookies = session.cookie_jar.filter_cookies(self.CORE_API)
                    job_cookie = {k: v.value for k, v in cookies.items()}

                    if not job_cookie:
                        raise RuntimeError("❌ [START-JOB] No job cookies returned.")

                    logger.info("✅ [START-JOB] Job started and cookies obtained.")
                    return job_cookie, response_json
        except Exception as e:
            logger.error(f"❌ [START-JOB] Error: {e}")
            raise RuntimeError(f"❌ [START-JOB] Error: {e}")
