from typing import Optional, Union
import os
import json
import warnings
import requests
import time
try:
    from rebrowser_playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    try:
        from playwright.sync_api import sync_playwright
        PLAYWRIGHT_AVAILABLE = True
        warnings.warn(
            "Using standard playwright instead of rebrowser-patches. Some anti-bot systems may detect automation. "
            "To improve stealth, install with 'pip install rebrowser-playwright'",
            ImportWarning
        )
    except ImportError:
        PLAYWRIGHT_AVAILABLE = False
        warnings.warn(
            "Playwright is not available. Some features will be disabled. "
            "To enable all features, install with 'pip install simplex[playwright]'",
            ImportWarning
        )

# BASE_URL = "https://simplex-dev-shreya--api-server-and-container-service-fas-bba69e.modal.run"
# BASE_URL = "https://simplex-dev--api-server-and-container-service-fastapi-app.modal.run"
BASE_URL = "https://api.simplex.sh"

class Playwright:
    def __init__(self, simplex_instance):
        self.simplex = simplex_instance
        
    def click(self, locator: str, locator_type: str, exact: Optional[bool] = False, 
              element_index: Optional[str] = None, nth_index: Optional[int] = None, 
              locator_options: Optional[dict] = None):
        
        if element_index and element_index not in ["first", "last", "nth"]:
            raise ValueError("element_index must be 'first', 'last', or 'nth'")
        
        if element_index=="nth" and not nth_index:
            raise ValueError("nth_index is required when element_index is 'nth'")
        
        data = {
            'session_id': self.simplex.session_id,
            'locator': locator,
            'locator_type': locator_type,
        }     
        
        if element_index:
            data['element_index'] = element_index
            data['nth_index'] = nth_index

        if exact:
            data['exact'] = exact
            
        if locator_options:
            data['locator_options'] = json.dumps(locator_options)

        response = requests.post(
            f"{BASE_URL}/playwright/click",
            headers={
                'x-api-key': self.simplex.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the click action with playwright failed to return a response. Did you set your api_key when creating the Simplex class?")
        
        if "succeeded" in response.json():
            return
        else:
            raise ValueError(f"Failed to click element: {response.json()['error']}")

class Simplex:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session_id = None
        if PLAYWRIGHT_AVAILABLE:
            self.pw_browser = None
            self.pw = None
        else:
            self.pw_browser = None
            self.pw = None
        
    def close_session(self):
        if PLAYWRIGHT_AVAILABLE and self.pw_browser:
            try:
                self.pw_browser.close()
                self.pw_browser = None
            except Exception as e:
                print(f"Failed to close pw_browser: {e}")
        if PLAYWRIGHT_AVAILABLE and self.pw:
            try:
                self.pw.stop()
                self.pw = None
            except Exception as e:
                print(f"Failed to stop pw: {e}")
        if not self.session_id:
            return
        response = requests.post(
            f"{BASE_URL}/close_session",
            headers={
                'x-api-key': self.api_key
            },
            data={'session_id': self.session_id}
        )
        self.session_id = None
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the close_session action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to close session: {response.json()['error']}")

    def create_session(self, show_in_console: Optional[bool] = True, proxies: Optional[bool] = True, workflow_name: Optional[str] = None, session_data: Optional[dict | str] = None):
        if self.session_id:
            raise ValueError("A session is already active. Please close the current session before creating a new one.")
        
        if session_data:
            if isinstance(session_data, dict):
                session_data_dict = session_data
            else:
                try:
                    # Try to parse as JSON string first
                    session_data_dict = json.loads(session_data)
                except json.JSONDecodeError:
                    # If parsing fails, treat as file path
                    try:
                        with open(session_data, 'r') as f:
                            session_data_dict = json.load(f)
                    except Exception as e:
                        raise ValueError(f"Failed to load session data. Input must be valid JSON string, dictionary, or path to JSON file. Error: {str(e)}")
            response = requests.post(
                f"{BASE_URL}/create_session",
                headers={
                    'x-api-key': self.api_key
                },
                data={'proxies': proxies, 'session_data': json.dumps(session_data_dict), 'workflow_name': workflow_name}
            )
        else:
            response = requests.post(
                f"{BASE_URL}/create_session",
                headers={
                    'x-api-key': self.api_key
                },
                data={'proxies': proxies, "workflow_name": workflow_name}
            )
        # Check for non-200 status code
        if response.status_code != 200:
            raise ValueError(f"Create session request failed with status code {response.status_code}: {response.text}")

        response_json = response.json()
        if 'session_id' not in response_json:
            raise ValueError(f"It looks like the session wasn't created successfully. Did you set your api_key when creating the Simplex class?")
        self.session_id = response_json['session_id']
        livestream_url = response_json['livestream_url']
        
        # Start Playwright without using context manager
        if PLAYWRIGHT_AVAILABLE:
            self.pw = sync_playwright().start()
        self.connect_url = response_json['connect_url']
        # self.pw_browser = self.pw.chromium.connect_over_cdp(response_json['connect_url'])
        if not "api.simplex.sh" in BASE_URL:
            livestream_url = f"http://localhost:3000/session/{self.session_id}"
        
        if show_in_console:
            print(f"Livestream URL: {livestream_url}")

        return self.session_id, livestream_url

    def goto(self, url: str, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action goto with url='{url}'")
        
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        data = {
            'url': url,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/goto",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the goto action failed to return a response. Did you set your api_key when creating the Simplex class?")
    
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to goto url: {response.json()['error']}")
        
    def enqueue_actions(self, actions: list):
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action enqueue_actions with actions={actions}")
        
        data = {
            'actions': json.dumps(actions),
            'session_id': self.session_id,
        }

        response = requests.post(
            f"{BASE_URL}/enqueue_actions",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the enqueue_actions action failed to return a response. Did you set your api_key when creating the Simplex class?")
    
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to enqueue actions: {response.json()['error']}")

    def captcha_exists(self):
        data = {
            'session_id': self.session_id,
        }

        response = requests.post(
            f"{BASE_URL}/captcha_exists",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the captcha_exists action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return response.json()['captcha_detected']
        else:
            raise ValueError(f"Failed to check if captcha is present: {response.json()['error']}")

    def wait_for_captcha(self):
        data = {
            'session_id': self.session_id,
        }
        
        response = requests.post(
            f"{BASE_URL}/wait_for_captcha",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the wait_for_captcha action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return response.json()['captcha_solved']
        else:
            raise ValueError(f"Failed to wait for captcha: {response.json()['error']}")

    def agentic(self, task: str, max_steps: Optional[int] = 10):
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action agentic with task='{task}'")
        
        data = {
            'task': task,
            'session_id': self.session_id,
            'max_steps': max_steps
        }

        response = requests.post(
            f"{BASE_URL}/agentic",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the agentic action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to complete agentic task: {response.json()['error']}")

    def click(self, element_description: str, dropdown_option: bool = False, override_fail_state: bool = False):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action click with element_description='{element_description}'")

        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state,
            'dropdown_option': dropdown_option
        }

        response = requests.post(
            f"{BASE_URL}/click",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the click action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["element_clicked"]
        else:
            raise ValueError(f"Failed to click element: {response.json()['error']}")

    def get_dropdown_options(self, element_description: str, override_fail_state: bool = False):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action get_dropdown_options with element_description='{element_description}'")
        
        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/get_dropdown_options",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the get_dropdown_options action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return response.json()['dropdown_options']
        else:
            raise ValueError(f"Failed to get dropdown options: {response.json()['error']}")
            
        
    def select_dropdown_option(self, element_description: str, override_fail_state: bool = False):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action select_from_dropdown with element_description='{element_description}'")
        
        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }
        
        response = requests.post(
            f"{BASE_URL}/select_dropdown_option",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the select_dropdown_option action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return response.json()["element_clicked"]
        else:
            raise ValueError(f"Failed to select dropdown option: {response.json()['error']}")

    def scroll_to_element(self, element_description: str, override_fail_state: bool = False):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action scroll_to_element with element_description='{element_description}'")  
        
        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/scroll_to_element",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the scroll_to_element action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to scroll element into view: {response.json()['error']}")
        
    def hover(self, element_description: str, override_fail_state: bool = False):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action hover with element_description='{element_description}'")
        
        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/hover",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():  
            raise ValueError(f"It looks like the hover action failed to return a response. Did you set your api_key when creating the Simplex class?")
            
        if response.json()["succeeded"]:
            return
        else:
            raise ValueError(f"Failed to hover: {response.json()['error']}")

    def type(self, text: str, override_fail_state: bool = False):
        if not text or not text.strip():
            raise ValueError("text cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action type with text='{text}'")

        data = {
            'text': text,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/type",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to type text: {response.json()['error']}")    

    def reload(self, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError("Must call create_session before calling action reload")

        data = {
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/reload",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the reload action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to reload: {response.json()['error']}")
        
    def press_enter(self, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError("Must call create_session before calling action press_enter")

        data = {
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/press_enter",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the press_enter action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to press enter: {response.json()['error']}")
        
    def press_tab(self, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError("Must call create_session before calling action press_tab")

        data = {
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/press_tab",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the press_tab action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to press tab: {response.json()['error']}")
        
    def delete_text(self, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError("Must call create_session before calling action delete_text")

        data = {
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/delete_text",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the delete_text action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to delete text: {response.json()['error']}")

    def bot_tests(self, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError("Must call create_session before calling action bot_tests")

        data = {
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/bot_tests",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the bot_tests action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to run bot tests: {response.json()['error']}")

    def extract_text(self, element_description: str, override_fail_state: bool = False):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action extract_text with element_description='{element_description}'")

        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/extract-text",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        response_json = response.json()
        if 'succeeded' not in response_json:
            raise ValueError(f"It looks like the extract_text action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response_json["succeeded"]:
            return response_json["text"]
        else:
            raise ValueError(f"Failed to extract text: {response_json['error']}")

    def scroll(self, pixels: float, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action scroll with pixels={pixels}")

        data = {
            'pixels': pixels,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/scroll",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the scroll action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to scroll: {response.json()['error']}")

    def wait(self, milliseconds: int, override_fail_state: bool = False):
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action wait with milliseconds={milliseconds}")

        data = {
            'milliseconds': milliseconds,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }
        response = requests.post(
            f"{BASE_URL}/wait",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the wait action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to wait: {response.json()['error']}")
        
    def set_dialog_settings(self, accept: bool = True):
        if not self.session_id:
            raise ValueError("Must call create_session before calling action set_dialog_settings")
        
        data = {
            'session_id': self.session_id,
            'accept': accept
        }

        response = requests.post(
            f"{BASE_URL}/set_dialog_settings",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the set_dialog_settings action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to set dialog settings: {response.json()['error']}")
        
    def get_dialog_message(self):
        if not self.session_id:
            raise ValueError("Must call create_session before calling action get_dialog_message")
        
        data = {
            'session_id': self.session_id
        }

        response = requests.post(
            f"{BASE_URL}/get_dialog_message",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the get_dialog_message action failed to return a response. Did you set your api_key when creating the Simplex class?")
        
        res = response.json()
        if res['succeeded']:
            if 'message' in res:
                return res['message']
            else:
                return None
        else:
            raise ValueError(f"Failed to get dialog message: {response.json()['error']}")
        
        
        
    def create_login_session(self, url: str, save_directory: Optional[str] = None):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("This feature requires playwright. Install simplex[playwright] to use it.")
        
        def get_website_name(url: str) -> str:
            """Extract website name from URL"""
            from urllib.parse import urlparse
            netloc = urlparse(url).netloc
            # Remove www. if present
            if netloc.startswith('www.'):
                netloc = netloc[4:]
            return netloc.replace(".", "_")

        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",  
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-automation',
                ],
                ignore_default_args=['--enable-automation']
            )
            # Create context and pages
            context = browser.new_context(viewport=None)
            main_page = context.new_page()
            main_page.goto(url)
            
            # Create control page in same context
            control_page = context.new_page()
            # Use a simple HTML file instead of set_content
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Capture Session</title>
            </head>
            <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f5f5f5;">
                <button id="capture-btn" style="
                    padding: 20px 40px;
                    font-size: 18px;
                    cursor: pointer;
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                ">Click here when logged in to capture session</button>
            </body>
            </html>
            """
            import tempfile
            # Write to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w') as f:
                f.write(html_content)
                temp_path = f.name
            
            try:
                # Load from file instead of set_content
                control_page.goto(f"file://{temp_path}")
                control_page.wait_for_selector('#capture-btn', timeout=30000)
                
                # Wait for button click
                control_page.evaluate("""
                    () => {
                        return new Promise((resolve) => {
                            document.getElementById('capture-btn').onclick = () => {
                                resolve(true);
                            }
                        });
                    }
                """)
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass
            
            # Use context.storage_state() instead of browser.storage_state()
            storage = context.storage_state()
            if save_directory:
                filename = os.path.join(save_directory, get_website_name(url) + "_session_data.json")
            else:
                filename = get_website_name(url) + "_session_data.json"
            
            with open(filename, 'w') as f:
                json.dump(storage, f, indent=2)
                
            print(f"Session data saved to '{filename}'")
            
            browser.close()

        return filename

    def get_network_response(self, url: str):
        print(f"Getting network response for {url}")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action get_network_response with url='{url}'")
        
        data = {
            'url': url,
            'session_id': self.session_id
        }
        
        response = requests.post(
            f"{BASE_URL}/get_network_response",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )

        if 'status' not in response.json():
            raise ValueError(f"It looks like the get_network_response action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['status'] == 'success':
            return response.json()['response']
        else:
            raise ValueError(f"Failed to get network response: {response.json()['error']}")

    def restore_login_session(self, session_data: str):
        """
        Restore a login session from either a file path or a JSON string.
        
        Args:
            session_data: Either a file path to JSON file or a JSON string
        """
        try:
            # Try to parse as JSON string first
            session_data_dict = json.loads(session_data)
        except json.JSONDecodeError:
            # If parsing fails, treat as file path
            try:
                with open(session_data, 'r') as f:
                    session_data_dict = json.load(f)
            except Exception as e:
                raise ValueError(f"Failed to load session data. Input must be valid JSON string or path to JSON file. Error: {str(e)}")
        
        data = {
            'session_data': json.dumps(session_data_dict),
            'session_id': self.session_id
        }
        
        response = requests.post(
            f"{BASE_URL}/restore_login_session",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the restore_login_session action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to restore login session: {response.json()['error']}")

    def click_and_upload(self, element_description: str, file_path_or_callable: Union[str, callable], override_fail_state: bool = False):
        """
        Args:
            element_description: Description of the element to click and upload to
            file_path_or_callable: Either a path to the file to be uploaded or a callable that returns a file-like object in 'rb' mode
            override_fail_state: Boolean to override fail state, default is False
        """
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action click_and_upload with element_description='{element_description}'")
        
        if not isinstance(file_path_or_callable, str) and not callable(file_path_or_callable):
            raise TypeError("file_path_or_callable must be either a string or a callable, not a " + type(file_path_or_callable).__name__)

        if isinstance(file_path_or_callable, str):
            files = {
                'file': open(file_path_or_callable, 'rb')
            }
        elif callable(file_path_or_callable):
            files = {
                'file': file_path_or_callable()
            }
        else:
            raise ValueError("You must provide either a valid file path or a callable that returns a file-like object.")
        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/click_and_upload",
            headers={
                'x-api-key': self.api_key
            },
            files=files,
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the click_and_upload action failed to return a response. Did you set your api_key when creating the Simplex class?")
        if response.json()['succeeded']:
            return
        else:
            raise ValueError(f"Failed to click and upload: {response.json()['error']}")

    def click_and_download(self, element_description: str, override_fail_state: bool = False):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action click_and_download with element_description='{element_description}'")
        
        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/click_and_download",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
                
        # Get filename from Content-Disposition header
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            try:
                filename = content_disposition.split('filename=')[1].strip('"')
            except:
                try: 
                    filename_star = content_disposition.split('filename*=')[1].split(';')[0]
                    # Parse the RFC 5987 encoded filename
                    encoding, _, fname = filename_star.split("'", 2)
                    # URL decode the filename
                    from urllib.parse import unquote
                    filename = unquote(fname)
                except Exception:
                    raise ValueError("File failed to be parsed from Content-Disposition header.")
        else:
            try:
                raise ValueError(response.json()["error"])
            except:
                raise ValueError("No Content-Disposition header found. File was not downloaded.")
        
        
        # Check if response content is empty
        if len(response.content) == 0:
            raise ValueError("Downloaded file is empty (0 bytes)")
        
        return filename, response.content
    
    def exists(self, element_description: str, override_fail_state: bool = False, max_steps: Optional[int] = None):
        if not element_description or not element_description.strip():
            raise ValueError("element_description cannot be empty")
        if not self.session_id:
            raise ValueError(f"Must call create_session before calling action exists with element_description='{element_description}'")

        data = {
            'element_description': element_description,
            'session_id': self.session_id,
            'override_fail_state': override_fail_state,
            'max_steps': max_steps
        }

        response = requests.post(
            f"{BASE_URL}/exists",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the exists action failed to return a response. Did you set your api_key when creating the Simplex class?")
        response_json = response.json()
        
        if response_json['succeeded']:
            return response_json['exists'], response_json['reasoning']
        else:
            raise ValueError(f"Failed to check if element exists: {response_json['error']}")
        
    def capture_login_session(self, override_fail_state: bool = False):
        data = {
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }
        response = requests.post(
            f"{BASE_URL}/capture_login_session",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the capture_login_session action failed to return a response. Did you set your api_key when creating the Simplex class?")
        response_json = response.json()
        if response_json['succeeded']:
            return response_json['storage_state']
        else:
            raise ValueError(f"Failed to capture login session: {response_json['error']}")
    
            
    def get_page_url(self, override_fail_state: bool = False):
        data = {
            'session_id': self.session_id,
            'override_fail_state': override_fail_state
        }

        response = requests.post(
            f"{BASE_URL}/get_page_url",
            headers={
                'x-api-key': self.api_key
            },
            data=data
        )
        if 'succeeded' not in response.json():
            raise ValueError(f"It looks like the get_page_url action failed to return a response. Did you set your api_key when creating the Simplex class?")
        response_json = response.json()
        # print(response_json)
        if response_json['succeeded']:
            return response_json['url']
        else:
            raise ValueError(f"Failed to get page url: {response_json['error']}")