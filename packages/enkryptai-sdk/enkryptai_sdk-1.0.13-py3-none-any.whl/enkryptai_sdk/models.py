from .base import BaseClient
from urllib.parse import urlparse, urlsplit
from .dto import ModelConfig, ModelResponse, ModelCollection


class ModelClientError(Exception):
    """
    A custom exception for ModelClient errors.
    """

    pass


class ModelClient(BaseClient):
    def __init__(self, api_key: str, base_url: str = "https://api.enkryptai.com:443"):
        super().__init__(api_key, base_url)

    @staticmethod
    def prepare_model_payload(config: ModelConfig | dict, is_custom: bool = False) -> dict:
        """
        Prepare the payload for model operations from a config object.
        
        Args:
            config (Union[ModelConfig, dict]): Configuration object or dictionary containing model details
            
        Returns:
            dict: Processed payload ready for API submission
        """
        if isinstance(config, dict):
            config = ModelConfig.from_dict(config)
        
        # Parse endpoint_url into components
        parsed_url = urlparse(config.model_config.endpoint_url)
        path_parts = parsed_url.path.strip("/").split("/")

        # Extract base_path and endpoint path
        if len(path_parts) >= 1:
            base_path = path_parts[0]  # Usually 'v1'
            remaining_path = "/".join(path_parts[1:])  # The rest of the path
        else:
            base_path = ""
            remaining_path = ""

        if config.model_config.paths:
            paths = config.model_config.paths.to_dict()
        else:
            paths = {
                "completions": f"/{remaining_path.split('/')[-1]}" if remaining_path else "",
                "chat": f"/{remaining_path}" if remaining_path else "",
            }

        # Convert custom_headers to list of dictionaries
        custom_headers = [header.to_dict() for header in config.model_config.custom_headers]

        payload = {
            "testing_for": config.testing_for,
            "model_name": config.model_name,
            "certifications": config.certifications,
            "model_config": {
                "model_provider": config.model_config.model_provider,
                "hosting_type": config.model_config.hosting_type,
                "model_source": config.model_config.model_source,
                "system_prompt": config.model_config.system_prompt,
                "endpoint": {
                    "scheme": parsed_url.scheme,
                    "host": parsed_url.hostname,
                    "port": parsed_url.port or (443 if parsed_url.scheme == "https" else 80),
                    "base_path": f"/{base_path}",
                },
                "paths": paths,
                "auth_data": {
                    "header_name": config.model_config.auth_data.header_name,
                    "header_prefix": config.model_config.auth_data.header_prefix,
                    "space_after_prefix": config.model_config.auth_data.space_after_prefix,
                },
                "apikeys": [config.model_config.apikey] if config.model_config.apikey else [],
                "tools": config.model_config.tools,
                "input_modalities": [m.value if hasattr(m, 'value') else m for m in config.model_config.input_modalities],
                "output_modalities": [m.value if hasattr(m, 'value') else m for m in config.model_config.output_modalities],
                "custom_curl_command": config.model_config.custom_curl_command,
                "custom_headers": custom_headers,
                "custom_payload": config.model_config.custom_payload,
                "custom_response_content_type": config.model_config.custom_response_content_type,
                "custom_response_format": config.model_config.custom_response_format,
                "metadata": config.model_config.metadata,
                "default_request_options": config.model_config.default_request_options,
            },
        }

        if not is_custom:
            payload["model_saved_name"] = config.model_saved_name
            payload["model_version"] = config.model_version

        return payload

    def add_model(self, config: ModelConfig) -> ModelResponse:
        """
        Add a new model configuration to the system.

        Args:
            config (ModelConfig): Configuration object containing model details

        Returns:
            dict: Response from the API containing the added model details
        """
        headers = {"Content-Type": "application/json"}
        payload = self.prepare_model_payload(config)

        try:
            response = self._request(
                "POST", "/models/add-model", headers=headers, json=payload
            )
            if response.get("error"):
                raise ModelClientError(f"API Error: {str(response)}")
            return ModelResponse.from_dict(response)
        except Exception as e:
            raise ModelClientError(str(e))

    def get_model(self, model_saved_name: str, model_version: str) -> ModelConfig:
        """
        Get model configuration by model saved name.

        Args:
            model_saved_name (str): Saved name of the model to retrieve
            model_version (str): Version of the model to retrieve

        Returns:
            ModelConfig: Configuration object containing model details
        """
        headers = {"X-Enkrypt-Model": model_saved_name, "X-Enkrypt-Model-Version": model_version}
        response = self._request("GET", "/models/get-model", headers=headers)
        # print(response)
        if response.get("error"):
            raise ModelClientError(f"API Error: {str(response)}")
        return ModelConfig.from_dict(response)

    def get_model_list(self):
        """
        Get a list of all available models.

        Returns:
            dict: Response from the API containing the list of models
        """
        try:
            response = self._request("GET", "/models/list-models")
            if isinstance(response, dict) and response.get("error"):
                raise ModelClientError(f"API Error: {str(response)}")
            return ModelCollection.from_dict(response)
        except Exception as e:
            return {"error": str(e)}

    def modify_model(self, config: ModelConfig, old_model_saved_name=None, old_model_version=None) -> ModelResponse:
        """
        Modify an existing model in the system.

        Args:
            old_model_saved_name (str): The old saved name of the model to modify
            old_model_version (str): The old version of the model to modify
            config (ModelConfig): Configuration object containing model details

        Returns:
            dict: Response from the API containing the modified model details
        """
        if old_model_saved_name is None:
            old_model_saved_name = config["model_saved_name"]

        if old_model_version is None:
            old_model_version = config["model_version"]

        headers = {"Content-Type": "application/json", "X-Enkrypt-Model": old_model_saved_name, "X-Enkrypt-Model-Version": old_model_version}
        # print(config)
        config = ModelConfig.from_dict(config)
        # Parse endpoint_url into components
        parsed_url = urlparse(config.model_config.endpoint_url)
        path_parts = parsed_url.path.strip("/").split("/")

        # Extract base_path and endpoint path
        if len(path_parts) >= 1:
            base_path = path_parts[0]  # Usually 'v1'
            remaining_path = "/".join(path_parts[1:])  # The rest of the path
        else:
            base_path = ""
            remaining_path = ""

        if config.model_config.paths:
            paths = config.model_config.paths.to_dict()
        else:
            # Determine paths based on the endpoint
            paths = {
                "completions": (
                    f"/{remaining_path.split('/')[-1]}" if remaining_path else ""
                ),
                "chat": f"/{remaining_path}" if remaining_path else "",
            }

        # Convert custom_headers to list of dictionaries
        custom_headers = [header.to_dict() for header in config.model_config.custom_headers]

        payload = {
            "model_saved_name": config.model_saved_name,
            "model_version": config.model_version,
            "testing_for": config.testing_for,
            "model_name": config.model_name,
            "certifications": config.certifications,
            "model_config": {
                "model_provider": config.model_config.model_provider,
                "hosting_type": config.model_config.hosting_type,
                "model_source": config.model_config.model_source,
                "system_prompt": config.model_config.system_prompt,
                "endpoint": {
                    "scheme": parsed_url.scheme,
                    "host": parsed_url.hostname,
                    "port": parsed_url.port
                    or (443 if parsed_url.scheme == "https" else 80),
                    "base_path": f"/{base_path}",  # Just v1
                },
                "paths": paths,
                "auth_data": {
                    "header_name": config.model_config.auth_data.header_name,
                    "header_prefix": config.model_config.auth_data.header_prefix,
                    "space_after_prefix": config.model_config.auth_data.space_after_prefix,
                },
                "apikeys": (
                    [config.model_config.apikey] if config.model_config.apikey else []
                ),
                "tools": config.model_config.tools,
                "input_modalities": [m.value if hasattr(m, 'value') else m for m in config.model_config.input_modalities],
                "output_modalities": [m.value if hasattr(m, 'value') else m for m in config.model_config.output_modalities],
                "custom_curl_command": config.model_config.custom_curl_command,
                "custom_headers": custom_headers,
                "custom_payload": config.model_config.custom_payload,
                "custom_response_content_type": config.model_config.custom_response_content_type,
                "custom_response_format": config.model_config.custom_response_format,
                "metadata": config.model_config.metadata,
                "default_request_options": config.model_config.default_request_options,
            },
        }
        try:
            response = self._request(
                "PATCH", "/models/modify-model", headers=headers, json=payload
            )
            if response.get("error"):
                raise ModelClientError(f"API Error: {str(response)}")
            return ModelResponse.from_dict(response)
        except Exception as e:
            raise ModelClientError(str(e))

    def delete_model(self, model_saved_name: str, model_version: str) -> ModelResponse:
        """
        Delete a specific model from the system.

        Args:
            model_saved_name (str): The saved name of the model to delete
            model_version (str): The version of the model to delete

        Returns:
            dict: Response from the API containing the deletion status
        """
        headers = {"X-Enkrypt-Model": model_saved_name, "X-Enkrypt-Model-Version": model_version}

        try:
            response = self._request("DELETE", "/models/delete-model", headers=headers)
            if response.get("error"):
                raise ModelClientError(f"API Error: {str(response)}")
            return ModelResponse.from_dict(response)
        except Exception as e:
            raise ModelClientError(str(e))
