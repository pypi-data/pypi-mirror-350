from typing import Any, Dict,List
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration
import httpx
import logging

logger = logging.getLogger(__name__)

class GoogleGeminiApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='google-gemini', integration=integration, **kwargs)
        self.base_url = "https://generativelanguage.googleapis.com"

    def _get_headers(self) -> Dict[str, str]:
      """
      Override the base method to return empty headers.
      The Gemini API key is passed as a query parameter ('key'),
      not in an Authorization header for these endpoints.
      """
      logger.debug(f"Overriding _get_headers for {self.name}. Returning empty dict to prevent default auth header.")
      return {}

    def _add_api_key_param(self, params: Dict[str, Any] | None) -> Dict[str, Any]:
        """Helper to add the API key as a 'key' query parameter."""
        actual_params = params.copy() if params else {}
        if 'key' not in actual_params and self.integration:
            try:
                credentials = self.integration.get_credentials()
                api_key = credentials.get("api_key") or credentials.get("API_KEY") or credentials.get("apiKey")
                if api_key:
                    actual_params['key'] = api_key
                    logger.debug("Added API key as query parameter.")
                else:
                      # This might happen if the store returned credentials without an api_key field
                    logger.warning("API key retrieved from integration credentials is None or empty.")
            except Exception as e:
                logger.error(f"Error retrieving API key from integration: {e}")
        return actual_params

    def _get(self, url: str, params: Dict[str, Any] | None = None) -> httpx.Response:
        """
        Make a GET request, ensuring the API key is added as a query parameter.
        """
        actual_params = self._add_api_key_param(params)
        logger.debug(f"Making GET request to {url} with params: {actual_params}")
        return super()._get(url, params=actual_params)

    def _post(
        self, url: str, data: Dict[str, Any], params: Dict[str, Any] | None = None
    ) -> httpx.Response:
        """
        Make a POST request, ensuring the API key is added as a query parameter.
        """
        actual_params = self._add_api_key_param(params)
        logger.debug(
            f"Making POST request to {url} with params: {actual_params} and data: {data}"
        )
        # Note: The parent _post in application.py still uses httpx.post directly
        # and calls self._get_headers() again, which is fine because our override returns {}.
        return super()._post(url, data=data, params=actual_params)

    def _delete(self, url: str, params: Dict[str, Any] | None = None) -> httpx.Response:
        """
        Make a DELETE request, ensuring the API key is added as a query parameter.
        """
        actual_params = self._add_api_key_param(params)
        logger.debug(f"Making DELETE request to {url} with params: {actual_params}")
        return super()._delete(url, params=actual_params)


    def text_only_input(
        self,
        contents: List[Dict[str, Any]], # Removed key=None
        generationConfig: Dict[str, Any] | None = None,
        safetySettings: List[Dict[str, Any]] | None = None
    ) -> Dict[str, Any]:
        """
        Generates content using the Gemini 1.5 Flash model via POST request.

        The API key is automatically added as a query parameter by the overridden _post method.

        Args:
            contents (list[dict[str, Any]]): contents Example: "[{'parts': [{'text': 'Write a story about a magic backpack.'}]}]".
            generationConfig (dict[str, Any], optional): generationConfig
            safetySettings (list[dict[str, Any]], optional): safetySettings
                Example:
                ```json
                {
                  "contents": [
                    {
                      "parts": [
                        {
                          "text": "List 5 popular cookie recipes"
                        }
                      ]
                    }
                  ],
                  "generationConfig": {
                    "response_mime_type": "application/json",
                    "response_schema": {
                      "items": {
                        "properties": {
                          "recipe_name": {
                            "type": "STRING"
                          }
                        },
                        "type": "OBJECT"
                      },
                      "type": "ARRAY"
                    }
                  }
                }
                ```

        Returns:
            dict[str, Any]: text-only input / text-and-image input / interractive chat / generate content from uploaded file / generate content from uploaded file / video[2]: generate content from uploaded file / video[3]: generate content from uploaded file / generate content from uploaded file / single-turn function calling / multi turn function call / JSON mode / random / generation config example

        Tags:
            Function Calling, important
        """
        # Ensure contents is not None, as it's a required parameter based on the OpenAPI spec
        if contents is None:
            raise ValueError("Missing required parameter 'contents'")
        if not isinstance(contents, list):
            # Add type checking for robustness based on expected input
            raise TypeError("'contents' must be a list")

        request_body = {
            'contents': contents,
        }
        if generationConfig is not None:
            request_body['generationConfig'] = generationConfig
        if safetySettings is not None:
            request_body['safetySettings'] = safetySettings

        url = f"{self.base_url}/v1beta/models/gemini-1.5-flash-8b-exp-0827:generateContent"
        # No explicit 'key' parameter needed here; _post handles it from integration
        query_params = {}

        logger.debug(f"Calling _post for generateContent with body: {request_body} and params: {query_params}")

        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status() # This will raise HTTPError for 400 status
        return response.json()

    # --- Rest of the tool methods (same as previous correction) ---
    def fetch_model(self) -> Dict[str, Any]:
        """
        Retrieves the configuration details for the Gemini 1.5 Flash-8B model via a GET request.

        Returns:
            dict[str, Any]: model

        Tags:
            Models, important
        """
        url = f"{self.base_url}/v1beta/models/gemini-1.5-flash-8b-exp-0827"
        query_params = {}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def fetch_models(self, pageSize=None, pageToken=None) -> Dict[str, Any]:
        """
        Retrieves a paginated list of available models, supporting page size and token parameters for result navigation.

        Args:
            pageSize (string): The `pageSize` parameter specifies the maximum number of items to include in each page of the response for the GET operation at the `/v1beta/models` path. Example: '5'.
            pageToken (string): Used in GET requests to specify the page token for fetching the next page of results. Example: 'Chxtb2RlbHMvZ2VtaW5pLTEuNS1wcm8tbGF0ZXN0'.

        Returns:
            dict[str, Any]: models

        Tags:
            Models, important
        """
        url = f"{self.base_url}/v1beta/models"
        query_params = {k: v for k, v in [('pageSize', pageSize), ('pageToken', pageToken)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def generate_atext_stream(self, alt=None, contents=None) -> Any:
        """
        Generates a streaming response from the Gemini 1.5 Flash model for multimodal input content.

        Args:
            alt (string): Specifies the alternative format for the response, commonly set to "sse" for server-sent events, allowing for streaming of the generated content. Example: 'sse'.
            contents (array): contents
                Example:
                ```json
                {
                  "contents": [
                    {
                      "parts": [
                        {
                          "text": "Tell me about this instrument"
                        },
                        {
                          "inline_data": {
                            "mime_type": "image/jpeg"
                          }
                        }
                      ]
                    }
                  ]
                }
                ```

        Returns:
            Any: generate a text stream

        Tags:
            Text Generation
        """
        request_body = {
            'contents': contents,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1beta/models/gemini-1.5-flash-8b-exp-0827:streamGenerateContent"
        query_params = {k: v for k, v in [('alt', alt)] if v is not None}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def resumable_upload_request(self, file=None) -> Any:
        """
        Uploads a file to storage using the POST method, with headers specifying upload protocol, command, content length, and content type.

        Args:
            file (object): file
                Example:
                ```json
                {
                  "file": {
                    "display_name": "state_of_the_union_address.mp3"
                  }
                }
                ```

        Returns:
            Any: resumable upload request / resumable upload request / resumable upload request / upload request

        Tags:
            Document Processing
        """
        request_body = {
            'file': file,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/upload/v1beta/files"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def prompt_document(self, contents=None) -> Dict[str, Any]:
        """
        Generates content using the Gemini model, accepting input prompts and returning a streamed response across various media types, such as text, images, and audio.

        Args:
            contents (array): contents
                Example:
                ```json
                {
                  "contents": [
                    {
                      "parts": [
                        {
                          "text": "Summarize the uploaded document."
                        },
                        {
                          "file_data": {
                            "file_uri": "{{FILE_URI}}",
                            "mime_type": "application/pdf"
                          }
                        }
                      ]
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: prompt document

        Tags:
            Document Processing
        """
        request_body = {
            'contents': contents,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1beta/models/gemini-1.5-pro-latest:generateContent"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def text_tokens(self, contents=None) -> Dict[str, Any]:
        """
        Calculates the number of tokens and billable characters for input content when using the Gemini 1.5 Flash 8B model.

        Args:
            contents (array): contents
                Example:
                ```json
                {
                  "contents": [
                    {
                      "parts": [
                        {
                          "text": "Hi, my name is Bob."
                        }
                      ],
                      "role": "user"
                    },
                    {
                      "parts": [
                        {
                          "text": "Hi Bob"
                        }
                      ],
                      "role": "model"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: text tokens / chat tokens / media tokens

        Tags:
            Count Tokens
        """
        request_body = {
            'contents': contents,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1beta/models/gemini-1.5-flash-8b-exp-0827:countTokens"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def fetch_tuned_models(self, page_size=None) -> Dict[str, Any]:
        """
        Retrieves a list of tuned models at the specified page size using the GET method.

        Args:
            page_size (string): Specifies the maximum number of items to return in a single response page. Example: '10'.

        Returns:
            dict[str, Any]: fetch models Copy

        Tags:
            Fine Tunning
        """
        url = f"{self.base_url}/v1beta/tunedModels"
        query_params = {k: v for k, v in [('page_size', page_size)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def create_atuned_model(self, base_model=None, display_name=None, tuning_task=None) -> Dict[str, Any]:
        """
        Creates a tuned model using the "POST" method at the "/v1beta/tunedModels" endpoint and returns a response upon successful creation.

        Args:
            base_model (string): base_model Example: 'models/gemini-1.5-flash-001-tuning'.
            display_name (string): display_name Example: 'number generator model'.
            tuning_task (object): tuning_task
                Example:
                ```json
                {
                  "base_model": "models/gemini-1.5-flash-001-tuning",
                  "display_name": "number generator model",
                  "tuning_task": {
                    "hyperparameters": {
                      "batch_size": 2,
                      "epoch_count": 5,
                      "learning_rate": 0.001
                    },
                    "training_data": {
                      "examples": {
                        "examples": [
                          {
                            "output": "2",
                            "text_input": "1"
                          },
                          {
                            "output": "4",
                            "text_input": "3"
                          },
                          {
                            "output": "-2",
                            "text_input": "-3"
                          },
                          {
                            "output": "twenty three",
                            "text_input": "twenty two"
                          },
                          {
                            "output": "two hundred one",
                            "text_input": "two hundred"
                          },
                          {
                            "output": "one hundred",
                            "text_input": "ninety nine"
                          },
                          {
                            "output": "9",
                            "text_input": "8"
                          },
                          {
                            "output": "-97",
                            "text_input": "-98"
                          },
                          {
                            "output": "1,001",
                            "text_input": "1,000"
                          },
                          {
                            "output": "10,100,001",
                            "text_input": "10,100,000"
                          },
                          {
                            "output": "fourteen",
                            "text_input": "thirteen"
                          },
                          {
                            "output": "eighty one",
                            "text_input": "eighty"
                          },
                          {
                            "output": "two",
                            "text_input": "one"
                          },
                          {
                            "output": "four",
                            "text_input": "three"
                          },
                          {
                            "output": "eight",
                            "text_input": "seven"
                          }
                        ]
                      }
                    }
                  }
                }
                ```

        Returns:
            dict[str, Any]: create a tuned model

        Tags:
            Fine Tunning
        """
        request_body = {
            'base_model': base_model,
            'display_name': display_name,
            'tuning_task': tuning_task,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1beta/tunedModels"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def prompt_the_tuned_model(self, tunedModel, contents=None) -> Dict[str, Any]:
        """
        Generates content using a specified tuned model defined at path "/v1beta/{tunedModel}:generateContent" by sending a POST request.

        Args:
            tunedModel (string): tunedModel
            contents (array): contents
                Example:
                ```json
                {
                  "contents": [
                    {
                      "parts": [
                        {
                          "text": "LXIII"
                        }
                      ]
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: prompt the tuned model

        Tags:
            Fine Tunning
        """
        if tunedModel is None:
            raise ValueError("Missing required parameter 'tunedModel'")
        request_body = {
            'contents': contents,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1beta/{tunedModel}:generateContent"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def delete_tuned_model(self, tunedModel) -> Dict[str, Any]:
        """
        Deletes a specified tuned model and returns a success status upon removal.

        Args:
            tunedModel (string): tunedModel

        Returns:
            dict[str, Any]: delete tuned model

        Tags:
            Fine Tunning
        """
        if tunedModel is None:
            raise ValueError("Missing required parameter 'tunedModel'")
        url = f"{self.base_url}/v1beta/{tunedModel}"
        query_params = {}
        response = self._delete(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def generate_embeddings(self, content=None, model=None) -> Dict[str, Any]:
        """
        Generates a text embedding vector from input text using the specified Gemini Embedding model, allowing for semantic analysis and comparison of textual content.

        Args:
            content (object): content
            model (string): model
                Example:
                ```json
                {
                  "content": {
                    "parts": [
                      {
                        "text": "Hello world"
                      }
                    ]
                  },
                  "model": "models/text-embedding-004"
                }
                ```

        Returns:
            dict[str, Any]: generate embeddings

        Tags:
            Embeddings
        """
        request_body = {
            'content': content,
            'model': model,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1beta/models/text-embedding-004:embedContent"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def batch_embeddings(self, requests=None) -> Dict[str, Any]:
        """
        Generates batch embeddings for a list of text inputs using the "text-embedding-004" model via a POST request to the "/v1beta/models/text-embedding-004:batchEmbedContents" endpoint.

        Args:
            requests (array): requests
                Example:
                ```json
                {
                  "requests": [
                    {
                      "content": {
                        "parts": [
                          {
                            "text": "What is the meaning of life?"
                          }
                        ]
                      },
                      "model": "models/text-embedding-004"
                    },
                    {
                      "content": {
                        "parts": [
                          {
                            "text": "How much wood would a woodchuck chuck?"
                          }
                        ]
                      },
                      "model": "models/text-embedding-004"
                    },
                    {
                      "content": {
                        "parts": [
                          {
                            "text": "How does the brain work?"
                          }
                        ]
                      },
                      "model": "models/text-embedding-004"
                    }
                  ]
                }
                ```

        Returns:
            dict[str, Any]: batch embeddings

        Tags:
            Embeddings
        """
        request_body = {
            'requests': requests,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        url = f"{self.base_url}/v1beta/models/text-embedding-004:batchEmbedContents"
        query_params = {}
        response = self._post(url, data=request_body, params=query_params)
        response.raise_for_status()
        return response.json()

    def discovery_document(self, version=None) -> Dict[str, Any]:
        """
        Retrieves discovery metadata for REST APIs, including available endpoints and parameters, based on the specified version.

        Args:
            version (string): Specifies the API version to use for the request, allowing clients to target a specific release without modifying the URI structure. Example: 'v1beta'.

        Returns:
            dict[str, Any]: Get Discovery Document
        """
        url = f"{self.base_url}/$discovery/rest"
        query_params = {k: v for k, v in [('version', version)] if v is not None}
        response = self._get(url, params=query_params)
        response.raise_for_status()
        return response.json()

    def list_tools(self):
        # ... (keep the implementation as before) ...
        return [
            self.fetch_model,
            self.fetch_models,
            self.text_only_input,
            self.generate_atext_stream,
            self.resumable_upload_request,
            self.prompt_document,
            self.text_tokens,
            self.fetch_tuned_models,
            self.create_atuned_model,
            self.prompt_the_tuned_model,
            self.delete_tuned_model,
            self.generate_embeddings,
            self.batch_embeddings,
            self.discovery_document
        ]