import inspect
import json
import re
import random
import time
import urllib
import uuid
from typing import Dict, List, Generator, Iterator, Optional, Any, Callable

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup


class FacebookInvalidCredentialsException(Exception):
    pass


class FacebookRegionBlocked(Exception):
    pass


def function_to_tool_schema(fn: Callable) -> Dict[str, Any]:
    """
    Converts a Python function into an Anthropic tool schema dict, using JSON Schema for input_schema.
    Args:
        fn (Callable): The function to convert.
    Returns:
        dict: Tool schema with name, description, input_schema.
    """
    sig = inspect.signature(fn)
    params = sig.parameters
    description = inspect.getdoc(fn) or ""

    def pytype_to_jsonschema(ann):
        if ann == int:
            return "integer"
        elif ann == float:
            return "number"
        elif ann == bool:
            return "boolean"
        elif ann == str:
            return "string"
        elif ann == list:
            return "array"
        elif ann == dict:
            return "object"
        return "string"  # fallback

    input_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
        "required": [],
    }
    for name, param in params.items():
        ann = param.annotation if param.annotation != inspect.Parameter.empty else str
        param_type = pytype_to_jsonschema(ann)
        param_desc = ""
        if param.default == inspect.Parameter.empty:
            input_schema["required"].append(name)
        input_schema["properties"][name] = {
            "type": param_type,
            "description": param_desc,
        }
    if not input_schema["required"]:
        del input_schema["required"]
    return {
        "name": fn.__name__,
        "description": description,
        "input_schema": input_schema,
    }


def generate_offline_threading_id() -> str:
    """
    Generates an offline threading ID.

    Returns:
        str: The generated offline threading ID.
    """
    # Maximum value for a 64-bit integer in Python
    max_int = (1 << 64) - 1
    mask22_bits = (1 << 22) - 1

    # Function to get the current timestamp in milliseconds
    def get_current_timestamp():
        return int(time.time() * 1000)

    # Function to generate a random 64-bit integer
    def get_random_64bit_int():
        return random.getrandbits(64)

    # Combine timestamp and random value
    def combine_and_mask(timestamp, random_value):
        shifted_timestamp = timestamp << 22
        masked_random = random_value & mask22_bits
        return (shifted_timestamp | masked_random) & max_int

    timestamp = get_current_timestamp()
    random_value = get_random_64bit_int()
    threading_id = combine_and_mask(timestamp, random_value)

    return str(threading_id)


def extract_value(text: str, start_str: str, end_str: str) -> str:
    """
    Helper function to extract a specific value from the given text using a key.

    Args:
        text (str): The text from which to extract the value.
        start_str (str): The starting key.
        end_str (str): The ending key.

    Returns:
        str: The extracted value.
    """
    start = text.find(start_str) + len(start_str)
    end = text.find(end_str, start)
    return text[start:end]


def format_response(response: dict) -> str:
    """
    Formats the response from Meta AI to remove unnecessary characters.

    Args:
        response (dict): The dictionnary containing the response to format.

    Returns:
        str: The formatted response.
    """
    text = ""
    for content in (
        response.get("data", {})
        .get("node", {})
        .get("bot_response_message", {})
        .get("composed_text", {})
        .get("content", [])
    ):
        text += content["text"] + "\n"
    return text


# Function to perform the login
def get_fb_session(email, password, proxies=None):
    login_url = "https://www.facebook.com/login/?next"
    headers = {
        "authority": "mbasic.facebook.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    # Send the GET request
    response = requests.get(login_url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")

    # Parse necessary parameters from the login form
    lsd = soup.find("input", {"name": "lsd"})["value"]
    jazoest = soup.find("input", {"name": "jazoest"})["value"]

    # Define the URL and body for the POST request to submit the login form
    post_url = "https://www.facebook.com/login/?next"
    data = {
        "lsd": lsd,
        "jazoest": jazoest,
        "login_source": "comet_headerless_login",
        "email": email,
        "pass": password,
        "login": "1",
        "next": None,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": None,
        "Referer": "https://www.facebook.com/",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.facebook.com",
        "DNT": "1",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "cookie": f"datr={response.cookies.get('datr')};",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
    }

    from requests import cookies

    # Send the POST request
    session = requests.session()
    jar = cookies.RequestsCookieJar()
    session.proxies = proxies
    session.cookies = jar

    result = session.post(post_url, headers=headers, data=data)
    if "sb" not in jar or "xs" not in jar:
        raise FacebookInvalidCredentialsException(
            "Was not able to login to Facebook. Please check your credentials. "
            "You may also have been rate limited. Try to connect to Facebook manually."
        )

    cookies = {
        **result.cookies.get_dict(),
        "sb": jar["sb"],
        "xs": jar["xs"],
        "fr": jar["fr"],
        "c_user": jar["c_user"],
    }

    response_login = {
        "cookies": cookies,
        "headers": result.headers,
        "response": response.text,
    }
    meta_ai_cookies = get_cookies()

    url = "https://www.meta.ai/state/"

    payload = f'__a=1&lsd={meta_ai_cookies["lsd"]}'
    headers = {
        "authority": "www.meta.ai",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": f'ps_n=1; ps_l=1; dpr=2; _js_datr={meta_ai_cookies["_js_datr"]}; abra_csrf={meta_ai_cookies["abra_csrf"]}; datr={meta_ai_cookies["datr"]};; ps_l=1; ps_n=1',
        "origin": "https://www.meta.ai",
        "pragma": "no-cache",
        "referer": "https://www.meta.ai/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, proxies=proxies
    )

    state = extract_value(response.text, start_str='"state":"', end_str='"')

    url = f"https://www.facebook.com/oidc/?app_id=1358015658191005&scope=openid%20linking&response_type=code&redirect_uri=https%3A%2F%2Fwww.meta.ai%2Fauth%2F&no_universal_links=1&deoia=1&state={state}"
    payload = {}
    headers = {
        "authority": "www.facebook.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": f"datr={response_login['cookies']['datr']}; sb={response_login['cookies']['sb']}; c_user={response_login['cookies']['c_user']}; xs={response_login['cookies']['xs']}; fr={response_login['cookies']['fr']}; abra_csrf={meta_ai_cookies['abra_csrf']};",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }
    session = requests.session()
    session.proxies = proxies
    response = session.get(url, headers=headers, data=payload, allow_redirects=False)

    next_url = response.headers["Location"]

    url = next_url

    payload = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.meta.ai/",
        "Connection": "keep-alive",
        "Cookie": f'dpr=2; abra_csrf={meta_ai_cookies["abra_csrf"]}; datr={meta_ai_cookies["_js_datr"]}',
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
    }
    session.get(url, headers=headers, data=payload)
    cookies = session.cookies.get_dict()
    if "abra_sess" not in cookies:
        raise FacebookInvalidCredentialsException(
            "Was not able to login to Facebook. Please check your credentials. "
            "You may also have been rate limited. Try to connect to Facebook manually."
        )

    return cookies


def get_cookies() -> dict:
    """
    Extracts necessary cookies from the Meta AI main page.

    Returns:
        dict: A dictionary containing essential cookies.
    """
    session = HTMLSession()
    response = session.get("https://www.meta.ai/")
    return {
        "_js_datr": extract_value(
            response.text, start_str='_js_datr":{"value":"', end_str='",'
        ),
        "abra_csrf": extract_value(
            response.text, start_str='abra_csrf":{"value":"', end_str='",'
        ),
        "datr": extract_value(
            response.text, start_str='datr":{"value":"', end_str='",'
        ),
        "lsd": extract_value(
            response.text, start_str='"LSD",[],{"token":"', end_str='"}'
        ),
    }


def get_session(
    proxy: Optional[Dict] = None, test_url: str = "https://api.ipify.org/?format=json"
) -> requests.Session:
    """
    Get a session with the proxy set.

    Args:
        proxy (Dict): The proxy to use
        test_url (str): A test site from which we check that the proxy is installed correctly.

    Returns:
        requests.Session: A session with the proxy set.
    """
    session = requests.Session()
    if not proxy:
        return session
    response = session.get(test_url, proxies=proxy, timeout=10)
    if response.status_code == 200:
        session.proxies = proxy
        return session
    else:
        raise Exception("Proxy is not working.")


MAX_RETRIES = 3


class MetaAI:
    """
    A class to interact with the Meta AI API to obtain and use access tokens for sending
    and receiving messages from the Meta AI Chat API.
    """

    def __init__(
        self, fb_email: str = None, fb_password: str = None, proxy: dict = None
    ):
        self.session = get_session()
        self.session.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            }
        )
        self.access_token = None
        self.fb_email = fb_email
        self.fb_password = fb_password
        self.proxy = proxy

        self.is_authed = fb_password is not None and fb_email is not None
        self.cookies = self.get_cookies()
        self.external_conversation_id = None
        self.offline_threading_id = None

    def get_access_token(self) -> str:
        """
        Retrieves an access token using Meta's authentication API.

        Returns:
            str: A valid access token.
        """

        if self.access_token:
            return self.access_token

        url = "https://www.meta.ai/api/graphql/"
        payload = {
            "lsd": self.cookies["lsd"],
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAbraAcceptTOSForTempUserMutation",
            "variables": {
                "dob": "1999-01-01",
                "icebreaker_type": "TEXT",
                "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
            },
            "doc_id": "7604648749596940",
        }
        payload = urllib.parse.urlencode(payload)  # noqa
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f'_js_datr={self.cookies["_js_datr"]}; '
            f'abra_csrf={self.cookies["abra_csrf"]}; datr={self.cookies["datr"]};',
            "sec-fetch-site": "same-origin",
            "x-fb-friendly-name": "useAbraAcceptTOSForTempUserMutation",
        }

        response = self.session.post(url, headers=headers, data=payload)

        try:
            auth_json = response.json()
        except json.JSONDecodeError:
            raise FacebookRegionBlocked(
                "Unable to receive a valid response from Meta AI. This is likely due to your region being blocked. "
                "Try manually accessing https://www.meta.ai/ to confirm."
            )

        access_token = auth_json["data"]["xab_abra_accept_terms_of_service"][
            "new_temp_user_auth"
        ]["access_token"]

        # Need to sleep for a bit, for some reason the API doesn't like it when we send request too quickly
        # (maybe Meta needs to register Cookies on their side?)
        time.sleep(1)

        return access_token

    def prompt(
        self,
        message: str,
        stream: bool = False,
        attempts: int = 0,
        new_conversation: bool = False,
        tools: list = None,
    ) -> Dict or Generator[Dict, None, None]:
        """
        Sends a message to the Meta AI and returns the response. Optionally supports tool selection and calling.

        Args:
            message (str): The message to send.
            stream (bool): Whether to stream the response or not. Defaults to False.
            attempts (int): The number of attempts to retry if an error occurs. Defaults to 0.
            new_conversation (bool): Whether to start a new conversation or not. Defaults to False.
            tools (list): Optional list of tool definitions (dicts with 'name', 'description', 'parameters').

        Returns:
            dict: A dictionary containing the response message and sources, or tool call output.

        Raises:
            Exception: If unable to obtain a valid response after several attempts.
        """
        if tools:
            tool_blocks = []
            for tool in tools:
                if callable(tool):
                    tool_callable = tool
                    tool = function_to_tool_schema(tool_callable)
                schema_props = tool.get("input_schema", {}).get("properties", {})
                schema_required = tool.get("input_schema", {}).get("required", [])
                schema_lines = []
                for pname, pinfo in schema_props.items():
                    desc = pinfo.get("description", "")
                    typ = pinfo.get("type", "string")
                    req = " (required)" if pname in schema_required else ""
                    schema_lines.append(f"    - {pname} ({typ}){req}: {desc}")
                tool_block = (
                    f"Tool name: {tool['name']}\nDescription: {tool['description']}\nInput schema:\n"
                    + (
                        "\n".join(schema_lines)
                        if schema_lines
                        else "    (no parameters)"
                    )
                )
                tool_blocks.append(tool_block)
            tools_section = "\n\n".join(tool_blocks)
            json_struct = {
                "type": "tool_use",
                "id": "tooluse_<unique_id>",
                "name": "<function_name>",
                "input": {},
            }
            tool_instruction = (
                "IMPORTANT:\n"
                "- If you need to use a tool, strictly return ONLY a JSON object in the format below (strictly no extra text, no commentary, no explanation, just one json object).\n"
                "- If you have enough information to answer the user's query, return ONLY a user-friendly text answer (not JSON, not a tool call).\n"
                "- NEVER mix JSON and text in the same response.\n"
                "- Do NOT execute or simulate the tool, and do NOT provide an answer unless you have all the information needed.\n"
                "----\n"
                "You are given a list of available tools/functions.\n"
                "Give only one tool call per response. Select the most relevant tool for getting the most immediate step on the basis of the current information and query.\n"
                "Here are the available tools:\n"
                f"{tools_section}\n\n"
                "Take the latest message and decide what needs to be done next based on the available data and tools.\n"
                f"**RETURN ONLY A JSON OBJECT IN THE FOLLOWING FORMAT (for tool calls):\n{json.dumps(json_struct, indent=4)}\n**\n"
                "User Query: " + message
            )
            message = tool_instruction

        if not self.is_authed:
            self.access_token = self.get_access_token()
            auth_payload = {"access_token": self.access_token}
            url = "https://graph.meta.ai/graphql?locale=user"

        else:
            auth_payload = {"fb_dtsg": self.cookies["fb_dtsg"]}
            url = "https://www.meta.ai/api/graphql/"

        if not self.external_conversation_id or new_conversation:
            external_id = str(uuid.uuid4())
            self.external_conversation_id = external_id
        payload = {
            **auth_payload,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "useAbraSendMessageMutation",
            "variables": json.dumps(
                {
                    "message": {"sensitive_string_value": message},
                    "externalConversationId": self.external_conversation_id,
                    "offlineThreadingId": generate_offline_threading_id(),
                    "suggestedPromptIndex": None,
                    "flashVideoRecapInput": {"images": []},
                    "flashPreviewInput": None,
                    "promptPrefix": None,
                    "entrypoint": "ABRA__CHAT__TEXT",
                    "icebreaker_type": "TEXT",
                    "__relay_internal__pv__AbraDebugDevOnlyrelayprovider": False,
                    "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
                }
            ),
            "server_timestamps": "true",
            "doc_id": "7783822248314888",
        }
        payload = urllib.parse.urlencode(payload)  # noqa
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "x-fb-friendly-name": "useAbraSendMessageMutation",
        }
        if self.is_authed:
            headers["cookie"] = f'abra_sess={self.cookies["abra_sess"]}'
            # Recreate the session to avoid cookie leakage when user is authenticated
            self.session = requests.Session()
            self.session.proxies = self.proxy

        response = self.session.post(url, headers=headers, data=payload, stream=stream)
        if not stream:
            raw_response = response.text
            last_streamed_response = self.extract_last_response(raw_response)
            if not last_streamed_response:
                return self.retry(message, stream=stream, attempts=attempts)

            extracted_data = self.extract_data(last_streamed_response)
            if tools:
                # Try to extract JSON from the message text
                def extract_json_from_text(s):
                    # Find the first {...} block in the string
                    match = re.search(r"(\{[\s\S]+\})", s)
                    if match:
                        try:
                            obj = json.loads(match.group(1))
                            return obj
                        except Exception:
                            return None
                    return None

                message_text = extracted_data.get("message", "")
                tool_json = extract_json_from_text(message_text)
                if tool_json:
                    return {**extracted_data, "message": tool_json}
            return extracted_data

        else:
            lines = response.iter_lines()
            is_error = json.loads(next(lines))
            if len(is_error.get("errors", [])) > 0:
                return self.retry(message, stream=stream, attempts=attempts)
            return self.stream_response(lines)

    def retry(self, message: str, stream: bool = False, attempts: int = 0):
        """
        Retries the prompt function if an error occurs.
        """
        if attempts <= MAX_RETRIES:
            time.sleep(3)
            return self.prompt(message, stream=stream, attempts=attempts + 1)
        else:
            raise Exception(
                "Unable to obtain a valid response from Meta AI. Try again later."
            )

    def extract_last_response(self, response: str) -> Dict:
        """
        Extracts the last response from the Meta AI API.

        Args:
            response (str): The response to extract the last response from.

        Returns:
            dict: A dictionary containing the last response.
        """
        last_streamed_response = None
        for line in response.split("\n"):
            try:
                json_line = json.loads(line)
            except json.JSONDecodeError:
                continue

            bot_response_message = (
                json_line.get("data", {})
                .get("node", {})
                .get("bot_response_message", {})
            )
            chat_id = bot_response_message.get("id")
            if chat_id:
                external_conversation_id, offline_threading_id, _ = chat_id.split("_")
                self.external_conversation_id = external_conversation_id
                self.offline_threading_id = offline_threading_id

            streaming_state = bot_response_message.get("streaming_state")
            if streaming_state == "OVERALL_DONE":
                last_streamed_response = json_line

        return last_streamed_response

    def stream_response(self, lines: Iterator[str]):
        """
        Streams the response from the Meta AI API.

        Args:
            lines (Iterator[str]): The lines to stream.

        Yields:
            dict: A dictionary containing the response message and sources.
        """
        for line in lines:
            if line:
                json_line = json.loads(line)
                extracted_data = self.extract_data(json_line)
                if not extracted_data.get("message"):
                    continue
                yield extracted_data

    def extract_data(self, json_line: dict):
        """
        Extract data and sources from a parsed JSON line.

        Args:
            json_line (dict): Parsed JSON line.

        Returns:
            Tuple (str, list): Response message and list of sources.
        """
        bot_response_message = (
            json_line.get("data", {}).get("node", {}).get("bot_response_message", {})
        )
        response = format_response(response=json_line)
        fetch_id = bot_response_message.get("fetch_id")
        sources = self.fetch_sources(fetch_id) if fetch_id else []
        medias = self.extract_media(bot_response_message)
        return {"message": response, "sources": sources, "media": medias}

    @staticmethod
    def extract_media(json_line: dict) -> List[Dict]:
        """
        Extract media from a parsed JSON line.

        Args:
            json_line (dict): Parsed JSON line.

        Returns:
            list: A list of dictionaries containing the extracted media.
        """
        medias = []
        imagine_card = json_line.get("imagine_card", {})
        session = imagine_card.get("session", {}) if imagine_card else {}
        media_sets = (
            (json_line.get("imagine_card", {}).get("session", {}).get("media_sets", []))
            if imagine_card and session
            else []
        )
        for media_set in media_sets:
            imagine_media = media_set.get("imagine_media", [])
            for media in imagine_media:
                medias.append(
                    {
                        "url": media.get("uri"),
                        "type": media.get("media_type"),
                        "prompt": media.get("prompt"),
                    }
                )
        return medias

    def get_cookies(self) -> dict:
        """
        Extracts necessary cookies from the Meta AI main page.

        Returns:
            dict: A dictionary containing essential cookies.
        """
        session = HTMLSession()
        headers = {}
        if self.fb_email is not None and self.fb_password is not None:
            fb_session = get_fb_session(self.fb_email, self.fb_password)
            headers = {"cookie": f"abra_sess={fb_session['abra_sess']}"}
        response = session.get(
            "https://www.meta.ai/",
            headers=headers,
        )
        cookies = {
            "_js_datr": extract_value(
                response.text, start_str='_js_datr":{"value":"', end_str='",'
            ),
            "datr": extract_value(
                response.text, start_str='datr":{"value":"', end_str='",'
            ),
            "lsd": extract_value(
                response.text, start_str='"LSD",[],{"token":"', end_str='"}'
            ),
            "fb_dtsg": extract_value(
                response.text, start_str='DTSGInitData",[],{"token":"', end_str='"'
            ),
        }

        if len(headers) > 0:
            cookies["abra_sess"] = fb_session["abra_sess"]
        else:
            cookies["abra_csrf"] = extract_value(
                response.text, start_str='abra_csrf":{"value":"', end_str='",'
            )
        return cookies

    def fetch_sources(self, fetch_id: str) -> List[Dict]:
        """
        Fetches sources from the Meta AI API based on the given query.

        Args:
            fetch_id (str): The fetch ID to use for the query.

        Returns:
            list: A list of dictionaries containing the fetched sources.
        """

        url = "https://graph.meta.ai/graphql?locale=user"
        payload = {
            "access_token": self.access_token,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "AbraSearchPluginDialogQuery",
            "variables": json.dumps({"abraMessageFetchID": fetch_id}),
            "server_timestamps": "true",
            "doc_id": "6946734308765963",
        }

        payload = urllib.parse.urlencode(payload)  # noqa

        headers = {
            "authority": "graph.meta.ai",
            "accept-language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f'dpr=2; abra_csrf={self.cookies.get("abra_csrf")}; datr={self.cookies.get("datr")}; ps_n=1; ps_l=1',
            "x-fb-friendly-name": "AbraSearchPluginDialogQuery",
        }

        response = self.session.post(url, headers=headers, data=payload)
        response_json = response.json()
        message = response_json.get("data", {}).get("message", {})
        search_results = (
            (response_json.get("data", {}).get("message", {}).get("searchResults"))
            if message
            else None
        )
        if search_results is None:
            return []

        references = search_results["references"]
        return references

    def get_cookies(self) -> dict:
        """
        Extracts necessary cookies from the Meta AI main page.

        Returns:
            dict: A dictionary containing essential cookies.
        """
        session = HTMLSession()
        headers = {}
        if self.fb_email is not None and self.fb_password is not None:
            fb_session = get_fb_session(self.fb_email, self.fb_password)
            headers = {"cookie": f"abra_sess={fb_session['abra_sess']}"}
        response = session.get(
            "https://www.meta.ai/",
            headers=headers,
        )
        cookies = {
            "_js_datr": extract_value(
                response.text, start_str='_js_datr":{"value":"', end_str='",'
            ),
            "datr": extract_value(
                response.text, start_str='datr":{"value":"', end_str='",'
            ),
            "lsd": extract_value(
                response.text, start_str='"LSD",[],{"token":"', end_str='"}'
            ),
            "fb_dtsg": extract_value(
                response.text, start_str='DTSGInitData",[],{"token":"', end_str='"'
            ),
        }

        if len(headers) > 0:
            cookies["abra_sess"] = fb_session["abra_sess"]
        else:
            cookies["abra_csrf"] = extract_value(
                response.text, start_str='abra_csrf":{"value":"', end_str='",'
            )
        return cookies

    def fetch_sources(self, fetch_id: str) -> List[Dict]:
        """
        Fetches sources from the Meta AI API based on the given query.

        Args:
            fetch_id (str): The fetch ID to use for the query.

        Returns:
            list: A list of dictionaries containing the fetched sources.
        """

        url = "https://graph.meta.ai/graphql?locale=user"
        payload = {
            "access_token": self.access_token,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "AbraSearchPluginDialogQuery",
            "variables": json.dumps({"abraMessageFetchID": fetch_id}),
            "server_timestamps": "true",
            "doc_id": "6946734308765963",
        }

        payload = urllib.parse.urlencode(payload)  # noqa

        headers = {
            "authority": "graph.meta.ai",
            "accept-language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f'dpr=2; abra_csrf={self.cookies.get("abra_csrf")}; datr={self.cookies.get("datr")}; ps_n=1; ps_l=1',
            "x-fb-friendly-name": "AbraSearchPluginDialogQuery",
        }

        response = self.session.post(url, headers=headers, data=payload)
        response_json = response.json()
        message = response_json.get("data", {}).get("message", {})
        search_results = (
            (response_json.get("data", {}).get("message", {}).get("searchResults"))
            if message
            else None
        )
        if search_results is None:
            return []

        references = search_results["references"]
        return references
