import json
import os
import threading
from typing import List

from maitai._config_listener import ConfigListener
from maitai._maitai_client import MaitaiClient
from maitai.models.application import Application
from maitai.models.config import Config as ActionConfig
from maitai.models.key import Key, KeyMap
from maitai_common.config import config_service


class Config(MaitaiClient):

    maitai_ws = "wss://09hidyy627.execute-api.us-west-2.amazonaws.com/production"
    config_dir = os.path.expanduser(os.environ.get("MAITAI_CONFIG_DIR", "~/.maitai"))
    refresh_timer = None

    def __init__(self):
        self._api_key = None
        self._company_id = None
        self.websocket_listener_thread = None
        self.config_listener = None
        self._application_action_configs: dict[str, dict[str, ActionConfig]] = {}
        self.initialized = False
        self.auth_keys: KeyMap = KeyMap(
            openai_api_key=Key(id=-1, key_value=os.environ.get("OPENAI_API_KEY")),
            groq_api_key=Key(id=-1, key_value=os.environ.get("GROQ_API_KEY")),
            anthropic_api_key=Key(id=-1, key_value=os.environ.get("ANTHROPIC_API_KEY")),
            cerebras_api_key=Key(id=-1, key_value=os.environ.get("CEREBRAS_API_KEY")),
            sambanova_api_key=Key(id=-1, key_value=os.environ.get("SAMBANOVA_API_KEY")),
            gemini_api_key=Key(id=-1, key_value=os.environ.get("GEMINI_API_KEY")),
            azure_api_key=Key(id=-1, key_value=os.environ.get("AZURE_API_KEY")),
            deepseek_api_key=Key(id=-1, key_value=os.environ.get("DEEPSEEK_API_KEY")),
        )
        self.refresh_interval = 30 * 60  # 30 minutes in seconds

    @property
    def api_key(self):
        if self._api_key is None:
            if self.initialized:
                raise ValueError(
                    "Maitai API Key has not been set. Either pass it directly into the client, or by setting the environment variable MAITAI_API_KEY."
                )
            else:
                api_key = os.environ.get("MAITAI_API_KEY")
                if not api_key:
                    raise ValueError(
                        "Maitai API Key has not been set. Either pass it directly into the client, or by setting the environment variable MAITAI_API_KEY."
                    )
                self.initialize(api_key=api_key)
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def refresh_applications(self):
        response_json = self.init_sdk(self.api_key, self.maitai_host)

        applications = [
            Application.model_validate(app_json)
            for app_json in response_json["applications"]
        ]
        self._company_id = response_json.get("company_id")
        if not self._company_id:
            raise Exception("Company ID not found in response")

        # Process API keys from the response
        if "api_keys" in response_json:
            api_keys = response_json["api_keys"]
            # Update Groq API key if provided
            for key_name, key_value in api_keys.items():
                if key_value and hasattr(self.auth_keys, f"{key_name}_api_key"):
                    setattr(
                        self.auth_keys,
                        f"{key_name}_api_key",
                        Key(id=-1, key_value=key_value),
                    )

        self.store_application_metadata(applications)

    def initialize(self, api_key, retry=0):
        if self.initialized and self.api_key == api_key:
            return

        # Clean up existing threads before creating new ones
        self.cleanup()

        self.api_key = api_key
        self.initialized = True
        try:
            # Call init_sdk and process the response
            self.refresh_applications()
            self._initialize_websocket()
            self._start_refresh_timer()
        except Exception as e:
            self.cleanup()  # Ensure cleanup on failure
            try:
                self._load_config_from_file()
            except Exception:
                raise e from None
            self.initialized = False
            if retry < 5:
                if self.refresh_timer:
                    self.refresh_timer.cancel()
                self.refresh_timer = threading.Timer(
                    interval=2**retry,
                    function=self.initialize,
                    args=(api_key, retry + 1),
                )
                self.refresh_timer.daemon = True
                self.refresh_timer.start()

    def _start_refresh_timer(self):
        if self.refresh_timer:
            self.refresh_timer.cancel()
        self.refresh_timer = threading.Timer(
            self.refresh_interval, self._refresh_and_reschedule
        )
        self.refresh_timer.daemon = True
        self.refresh_timer.start()

    def _refresh_and_reschedule(self):
        try:
            self.refresh_applications()
        except Exception as e:
            pass
        finally:
            self._start_refresh_timer()

    def get_application_action_config(
        self, application_ref_name: str, action_type: str
    ) -> ActionConfig:
        return self._application_action_configs.get(application_ref_name, {}).get(
            action_type, config_service.get_default_config()
        )

    def store_application_metadata(self, applications: List[Application]):
        for application in applications:
            for action_type in application.action_types:
                if (
                    application.application_ref_name
                    not in self._application_action_configs
                ):
                    self._application_action_configs[
                        application.application_ref_name
                    ] = {}
                self._application_action_configs[application.application_ref_name][
                    action_type.action_type
                ] = action_type.meta
        self._dump_application_metadata()

    def _dump_application_metadata(self):
        filename = os.path.join(self.config_dir, "config.json")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            config_object = {}
            for ref_name, intent_map in self._application_action_configs.items():
                config_object[ref_name] = {}
                for intent_name, intent_config in intent_map.items():
                    config_object[ref_name][intent_name] = intent_config.model_dump()
            f.write(json.dumps(config_object, indent=2))

    def _load_config_from_file(self):
        filename = os.path.join(self.config_dir, "config.json")
        with open(filename, "r") as f:
            config_object = json.load(f)
            for ref_name, intent_map in config_object.items():
                if ref_name not in self._application_action_configs:
                    self._application_action_configs[ref_name] = {}
                for intent_name, intent_config in intent_map.items():
                    self._application_action_configs[ref_name][intent_name] = (
                        ActionConfig.model_validate(intent_config)
                    )

    def _initialize_websocket(self):
        self.config_listener = ConfigListener(
            self, self.maitai_ws, "APPLICATION_CONFIG_CHANGE", self._company_id
        )
        self.config_listener.start()

    def cleanup(self):
        if self.config_listener:
            self.config_listener.stop()

        if self.refresh_timer:
            self.refresh_timer.cancel()
            self.refresh_timer = None
        self.initialized = False


config = Config()

import atexit

atexit.register(config.cleanup)
