import typing
from typing import TypeAlias, Optional, Tuple, Dict, Any

from lattica_common.app_api import HttpClient, generate_random_token_name

ModelId: TypeAlias = str
Token: TypeAlias = str
WorkerStatus: TypeAlias = Dict[str, str]


class LatticaManagement:
    # license_key is a JWT account token
    def __init__(self, license_key: str):
        """Initialize LatticaManagement with a license key"""
        self.account_token = license_key
        # self.agent_app = LatticaAppAPI(license_key)
        self.http_client = HttpClient(license_key, module_name='lattica_management')

    def get_account_credits(self) -> str:
        """Query the remaining credit quota."""
        return typing.cast(str, self.http_client.send_http_request('api/finance/get_account_credits'))

    def generate_query_token(self, model_id: str, token_name: Optional[str] = None) -> Token:
        if token_name is None:
            token_name = generate_random_token_name(10)
        response = self.http_client.send_http_request(
            "api/token/generate_token",
            req_params={
                'modelId': model_id,
                'tokenName': token_name
            })
        token = response.get('token')

        if token is None:
            raise ValueError("The response does not contain a 'token' field.")

        return typing.cast(Token, token)

    def get_worker_status(self, model_id: ModelId, worker_session_id: str) -> WorkerStatus:
        """Get the status of a specific worker."""
        try:
            return typing.cast(
                WorkerStatus,
                self.http_client.send_http_request(
                    'api/worker/poll_worker_status',
                    req_params={
                        'modelId': model_id,
                        'workerSessionId': worker_session_id
                    }
                )
            )
        except Exception as e:
            raise Exception(f"Failed to get worker status: {e}")

    def get_active_workers(self, model_id: str):
        """Get a list of active workers for a given model."""
        try:
            data = typing.cast(
                Dict[str, Any],
                self.http_client.send_http_request(
                    'api/worker/get_active_workers',
                    req_params={
                        'modelId': model_id
                    }
                )
            )
            return data["activeWorkers"]
        except Exception as e:
            raise Exception(f"Failed to get active workers: {e}")

    def update_account_info(self, company_name: Optional[str] = None, 
                            contact_name: Optional[str] = None,
                            email: Optional[str] = None, 
                            phone_number: Optional[str] = None):
        """Update account information."""
        try:
            req_body = {}
            if company_name is not None:
                req_body["companyName"] = company_name
            if contact_name is not None:
                req_body["contactName"] = contact_name
            if email is not None:
                req_body["email"] = email
            if phone_number is not None:
                req_body["phoneNumber"] = phone_number

            response = typing.cast(
                Dict[str, Any],
                self.http_client.send_http_request(
                    'api/account/update_account_info',
                    req_params=req_body
                )
            )
            return response["message"]
        except Exception as e:
            raise Exception(f"Failed to update account info: {e}")

    def get_account_info(self):
        """Retrieve details about the current account."""
        try:
            response = typing.cast(
                Dict[str, Any],
                self.http_client.send_http_request(
                    'api/account/get_account_info'
                )
            )
            # Return the entire account info object
            return {
                "accountId": response.get("accountId"),
                "createdAt": response.get("createdAt"),
                "email": response.get("email"),
                "companyName": response.get("companyName"),      # Can be None
                "contactName": response.get("contactName"),      # Can be None
                "phoneNumber": response.get("phoneNumber"),      # Can be None
                "credits": response.get("credits"),
                "authExpDate": response.get("authExpDate")       # Can be None
            }
        except Exception as e:
            raise Exception(f"Failed to get account info: {e}")

    def retrieve_payment_transaction(self):
        """Retrieve payment transaction history."""
        try:
            response = typing.cast(
                Dict[str, Any],
                self.http_client.send_http_request(
                    'api/account/retrieve_payment_transaction'
                )
            )
            return response["payments"]
        except Exception as e:
            raise Exception(f"Failed to retrieve payment transaction: {e}")

    def unassign_token_from_model(self, token_id: str, model_id: str):
        """Unassign a token from a model."""
        try:
            resp = typing.cast(
                Dict[str, Any],
                self.http_client.send_http_request(
                    'api/token/unassign_token_from_model',
                    req_params={
                        'tokenId': token_id,
                        'modelId': model_id
                    }
                )
            )
            return {
                "message": resp["message"],
                "warning": resp["warning"],
            }
        except Exception as e:
            raise Exception(f"Failed to unassign token from model: {e}")

    def assign_token_to_model(self, token_id: str, model_id: str):
        """Assign a token to a model."""
        try:
            resp = typing.cast(
                Dict[str, Any],
                self.http_client.send_http_request(
                    'api/token/assign_token_to_model',
                    req_params={
                        'tokenId': token_id,
                        'modelIdToAssign': model_id
                    }
                )
            )
            return {
                "message": resp["message"],
                "warning": resp.get("warning"),  # This field is optional
            }
        except Exception as e:
            raise Exception(f"Failed to assign token to model: {e}")
        
    def create_model(
        self, 
        model_name: str, 
    ) -> str:
        print("Register new model...")
        model_id = typing.cast(ModelId, self.http_client.send_http_request(
            'api/model/create_model',
            req_params={
                'modelName': model_name
            }))
        print(f'Model ID: {model_id}')

        return model_id
    
    # ---------------------- #
    # ---------------------- #
    # ---------------------- #
    # ---------------------- #

    def delete_token(self, token_id: str):
        """Delete a specific token."""
        try:
            resp = self.http_client.send_http_request(
                'api/token/delete_token',
                req_params={'tokenId': token_id}
            )
            return resp["message"]
        except Exception as e:
            raise Exception(f"Failed to delete token: {e}")

    def update_token_info(
        self,
        token_id: str,
        token_name: Optional[str] = None,
        token_note: Optional[str] = None,
        status: Optional[str] = None
    ):
        """Update token information."""
        try:
            req_body = {'tokenId': token_id}
            if token_name is not None:
                req_body['tokenName'] = token_name
            if token_note is not None:
                req_body['tokenNote'] = token_note
            if status is not None:
                req_body['status'] = status

            resp = self.http_client.send_http_request(
                'api/token/update_token_info',
                req_params=req_body
            )
            return resp["message"]
        except Exception as e:
            raise Exception(f"Failed to update token info: {e}")

    def get_token_info(self, token_jwt: str):
        """Get details about a token."""
        try:
            resp = self.http_client.send_http_request(
                'api/token/get_token_info',
                req_params={'token': token_jwt}
            )
            return {
                "tokenStatus": resp["token"]["status"],
                "tokenName": resp["token"]["tokenName"],
                "tokenExpiration": resp["token"]["expirationDate"],
                "modelName": resp["model"].get("modelName"),
                "modelStatus": resp["model"].get("status"),
                "workerStatus": resp["worker"].get("status"),
                "evalKeyCreatedAt": resp["evaluationKey"].get("createdAt")
            }
        except Exception as e:
            raise Exception(f"Failed to get token info: {e}")

    def list_tokens(
        self,
        status: Optional[str] = None,
        model_id: Optional[str] = None,
        issue_date: Optional[str] = None
    ):
        """List tokens based on optional filters."""
        try:
            req_body = {}
            if status is not None:
                req_body["status"] = status
            if model_id is not None:
                req_body["modelId"] = model_id
            if issue_date is not None:
                req_body["issueDate"] = issue_date

            resp = self.http_client.send_http_request(
                'api/token/list_tokens',
                req_params=req_body
            )
            return {
                "message": resp.get("message"),
                "tokens": resp.get("tokens", [])
            }
        except Exception as e:
            raise Exception(f"Failed to list tokens: {e}")

    def stop_worker(self, model_id: str, worker_session_id: str) -> WorkerStatus:
        """Stop a running worker."""
        try:
            return typing.cast(WorkerStatus, self.http_client.send_http_request(
                'api/worker/stop_worker',
                req_params={
                    'modelId': model_id,
                    'workerSessionId': worker_session_id
                }
            ))
        except Exception as e:
            raise Exception(f"Failed to stop worker: {e}")

    def start_worker(self, model_id: str) -> WorkerStatus:
        """Start a new worker."""
        try:
            return typing.cast(WorkerStatus, self.http_client.send_http_request(
                'api/worker/start_worker',
                req_params={
                    'modelId': model_id,
                }))
        except Exception as e:
            raise Exception(f"Failed to start worker: {e}")

    def update_model(
        self,
        model_id: str,
        model_name: Optional[str] = None,
        description: Optional[str] = None,
        visibility: Optional[str] = None,
        auto_restart: Optional[bool] = None,
        input_type: Optional[str] = None,
        output_type: Optional[str] = None,
        status: Optional[str] = None
    ):
        """Update model configuration."""
        try:
            req_body = {'modelId': model_id}
            if model_name is not None:
                req_body['modelName'] = model_name
            if description is not None:
                req_body['description'] = description
            if visibility is not None:
                req_body['visibility'] = visibility
            if auto_restart is not None:
                req_body['autoRestart'] = auto_restart
            if input_type is not None:
                req_body['inputType'] = input_type
            if output_type is not None:
                req_body['outputType'] = output_type
            if status is not None:
                req_body['status'] = status

            resp = self.http_client.send_http_request(
                'api/model/update',
                req_params=req_body
            )
            return {
                "message": resp.get("message"),
                "modelId": resp.get("modelId"),
                "warning": resp.get("warning")
            }
        except Exception as e:
            raise Exception(f"Failed to update model: {e}")

    def activate_model(self, model_id: str):
        """Activate a model."""
        try:
            resp = self.http_client.send_http_request(
                'api/model/activate_model',
                req_params={'modelId': model_id}
            )
            return resp["message"]
        except Exception as e:
            raise Exception(f"Failed to activate model: {e}")

    def deactivate_model(self, model_id: str):
        """Deactivate a model."""
        try:
            resp = self.http_client.send_http_request(
                'api/model/deactivate_model',
                req_params={'modelId': model_id}
            )
            return resp["message"]
        except Exception as e:
            raise Exception(f"Failed to deactivate model: {e}")

    def update_model_visibility(self, model_id: str, visibility: str):
        """Update a model's visibility."""
        try:
            resp = self.http_client.send_http_request(
                'api/model/update_model_visibility',
                req_params={
                    'modelId': model_id,
                    'visibility': visibility
                }
            )
            return {
                "message": resp["message"],
                "modelId": resp["modelId"],
                "newVisibility": resp["newVisibility"]
            }
        except Exception as e:
            raise Exception(f"Failed to update model visibility: {e}")

    def get_model_info(self, model_id: str):
        """Retrieve information about a model."""
        try:
            resp = self.http_client.send_http_request(
                'api/model/get_model_info',
                req_params={'modelId': model_id}
            )
            model_data = resp.get("model", {})
            return {
                "modelId": model_data.get("modelId"),
                "modelName": model_data.get("modelName"),
                "description": model_data.get("description", ""),
                "visibility": model_data.get("visibility"),
                "createdAt": model_data.get("createdAt"),
                "updatedAt": model_data.get("updatedAt", ""),
                "version": model_data.get("version", "1.0"),
                "status": model_data.get("status"),
                "uploadStatus": model_data.get("uploadStatus", ""),
                "inputType": model_data.get("inputType", ""),
                "outputType": model_data.get("outputType", ""),
                "autoRestart": model_data.get("autoRestart", "")
            }
        except Exception as e:
            raise Exception(f"Failed to get model info: {e}")

    def list_models(self, visibility: Optional[str] = None):
        """List models, optionally filtered by visibility."""
        try:
            req_body = {}
            if visibility is not None:
                req_body["visibility"] = visibility

            resp = self.http_client.send_http_request(
                'api/model/list_models',
                req_params=req_body
            )
            return resp.get("models", [])
        except Exception as e:
            raise Exception(f"Failed to list models: {e}")

    def list_worker_sessions(
        self,
        model_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ):
        """List worker sessions, optionally filtered by modelId, fromDate, and toDate."""
        try:
            req_body = {}
            if model_id is not None:
                req_body["modelId"] = model_id
            if from_date is not None:
                req_body["fromDate"] = from_date
            if to_date is not None:
                req_body["toDate"] = to_date

            resp = self.http_client.send_http_request(
                'api/worker/list_worker_sessions',
                req_params=req_body
            )
            return {
                "workerSessions": resp.get("workerSessions", []),
                "message": resp.get("message", "")
            }
        except Exception as e:
            raise Exception(f"Failed to list worker sessions: {e}")

    def upload_plain_model(self, model_file_path, model_id):
        self.http_client.send_http_file_request(
            'api/files/upload_non_homomorphic_model',
            req_params={'modelId': model_id},
            model_file_path=model_file_path
        )
