import json
import os
import time
import uuid
import asyncio
from typing import Dict, List, Optional, Union, Any
import aiohttp
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncEvaluatorClient:
    """Asynchronous client for sending model outputs to evaluation service via AWS."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        client_secret: Optional[str] = None,
        source: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        custom_headers: Optional[Dict[str, str]] = None,
        session_id: Optional[str] = None,
        aws_region: Optional[str] = None,
        lambda_function_name: Optional[str] = None,
        sqs_queue_url: Optional[str] = None,
        api_gateway_url: Optional[str] = None,
        environment: str = "development",
    ):
        # API authentication - Updated with adeptiv-ai prefix
        self.api_key = api_key or os.environ.get("ADEPTIV_AI_EVALUATOR_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as ADEPTIV_AI_EVALUATOR_API_KEY environment variable")

        self.client_secret = client_secret or os.environ.get("ADEPTIV_AI_EVALUATOR_CLIENT_SECRET")
        self.source = source or os.environ.get("ADEPTIV_AI_EVALUATOR_SOURCE", "adeptiv-ai-default")
        self.base_url = base_url or os.environ.get("ADEPTIV_AI_EVALUATOR_BASE_URL", "http://127.0.0.1:8001")

        # Retry configuration
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Headers and session
        self.custom_headers = custom_headers or {}
        self.session_id = session_id or str(uuid.uuid4())

        # Environment configuration
        self.environment = environment or os.environ.get("ADEPTIV_AI_ENVIRONMENT", "development")

        # Connection status
        self.is_connected = False

        # AWS configuration - Updated with adeptiv-ai prefix
        self.aws_region = aws_region or os.environ.get("ADEPTIV_AI_AWS_REGION", "us-east-1")
        self.lambda_function_name = lambda_function_name or os.environ.get("ADEPTIV_AI_EVALUATOR_LAMBDA_FUNCTION")
        self.sqs_queue_url = sqs_queue_url or os.environ.get("ADEPTIV_AI_EVALUATOR_SQS_QUEUE_URL")
        self.api_gateway_url = api_gateway_url or os.environ.get("ADEPTIV_AI_EVALUATOR_API_GATEWAY_URL")

        # AWS clients
        self.sqs_client = None
        self.lambda_client = None

        # Batch processing queue
        self._batch_queue = []

        # Initialize AWS clients if in production
        if self.environment.lower() == "production":
            self._initialize_aws_clients()

    def _initialize_aws_clients(self):
        """Initialize AWS clients for production use."""
        try:
            self.sqs_client = boto3.client('sqs', region_name=self.aws_region)
            self.lambda_client = boto3.client('lambda', region_name=self.aws_region)
            logger.info("✅ AWS clients initialized successfully")
        except NoCredentialsError:
            logger.error("❌ AWS credentials not configured")
            raise ValueError("AWS credentials must be configured for production environment")
        except Exception as e:
            logger.error(f"❌ Error initializing AWS clients: {e}")
            raise

    async def connect(self) -> bool:
        """
        Verifies API key and client secret by calling authentication endpoint.
        Returns:
            True if verification successful, False otherwise.
        """
        verify_url = f"{self.base_url}/api/auth/sdk/connect/"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "X-SECRET-Key": self.client_secret,  # Fixed typo from X-SECRECT-Key
            "X-Adeptiv-AI-Source": self.source,
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(verify_url, headers=headers) as response:
                    if response.status == 200:
                        self.is_connected = True
                        logger.info("✅ Adeptiv-AI SDK successfully connected and verified.")
                        return True
                    else:
                        logger.error(f"❌ Verification failed: {response.status} - {await response.text()}")
                        return False
            except Exception as e:
                logger.error(f"❌ Error during connection: {e}")
                return False

    def _prepare_payload(self, data: Any, metadata: Optional[Dict] = None, model: Optional[str] = None) -> Dict:
        """
        Prepare the payload for sending to the API.
        """
        payload = {
            "raw_output": data,
            "session_id": self.session_id,
            "timestamp": time.time(),
            "source": self.source,
            "environment": self.environment,
            "adeptiv_ai_version": "1.0.0"
        }

        if metadata:
            payload["metadata"] = metadata

        if model:
            payload["model"] = model

        return payload

    async def send_output(self,
                          data: Any,
                          metadata: Optional[Dict] = None,
                          model: Optional[str] = None,
                          process_via_aws: Optional[bool] = None) -> Dict[str, Any]:
        """
        Asynchronously send model output for evaluation.
        In production, defaults to AWS processing.
        """
        if not self.is_connected:
            raise RuntimeError("❗ Not connected. Call `await connect()` first.")

        payload = self._prepare_payload(data, metadata, model)
        
        # Default to AWS processing in production
        if process_via_aws is None:
            process_via_aws = self.environment.lower() == "production"

        if process_via_aws:
            return await self._process_via_aws(payload)
        else:
            return await self._send_request_async(payload)

    async def batch_add(self, data: Any, metadata: Optional[Dict] = None, model: Optional[str] = None):
        """
        Add an item to the batch processing queue asynchronously.
        """
        payload = self._prepare_payload(data, metadata, model)
        self._batch_queue.append(payload)

    async def batch_send(self, process_via_aws: Optional[bool] = None) -> List[Dict[str, Any]]:
        """
        Send all items in the batch queue asynchronously.
        In production, defaults to AWS processing.
        """
        if not self.is_connected:
            raise RuntimeError("❗ Not connected. Call `await connect()` first.")

        if not self._batch_queue:
            return []

        batch_payload = {
            "api_key": self.api_key,
            "source": self.source,
            "batch": self._batch_queue,
            "environment": self.environment,
            "adeptiv_ai_session_id": self.session_id
        }

        # Default to AWS processing in production
        if process_via_aws is None:
            process_via_aws = self.environment.lower() == "production"

        if process_via_aws:
            result = await self._process_via_aws(batch_payload)
        else:
            result = await self._send_request_async(batch_payload, endpoint="/api/sdk/evaluate/batch")

        self._batch_queue = []
        return result

    async def _send_request_async(self, payload: Dict, endpoint: str = "/api/evaluate/chatbot/") -> Dict[str, Any]:
        """
        Send the request to the API asynchronously with retry logic.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "X-Adeptiv-AI-Source": self.source,
            **self.custom_headers
        }

        if self.client_secret:
            headers["X-SECRET-Key"] = self.client_secret

        for attempt in range(self.max_retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=headers) as response:
                        if response.status == 200:
                            result = await response.json()
                            logger.info(f"✅ Successfully sent output to Adeptiv-AI service")
                            return result
                        else:
                            error_text = await response.text()
                            logger.error(f"❌ API request failed: {response.status} - {error_text}")
                            
                            if attempt < self.max_retries:
                                wait_time = self.retry_delay * (2 ** attempt)
                                logger.info(f"⏳ Retrying in {wait_time} seconds... (attempt {attempt + 1}/{self.max_retries})")
                                await asyncio.sleep(wait_time)
                            else:
                                raise Exception(f"API request failed after {self.max_retries} retries: {response.status}")
            
            except Exception as e:
                if attempt < self.max_retries:
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.warning(f"⚠️ Request failed: {e}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"❌ Request failed after {self.max_retries} retries: {e}")
                    raise

    async def _process_via_aws(self, payload: Dict) -> Dict[str, Any]:
        """
        Process payload via AWS SQS for production use.
        """
        if not self.sqs_client or not self.sqs_queue_url:
            logger.warning("⚠️ AWS SQS not configured. Using direct API fallback.")
            return await self._send_request_async(payload, endpoint="/api/sdk/evaluate/batch")

        try:
            # Prepare SQS message
            sqs_message = {
                "payload": payload,
                "timestamp": time.time(),
                "source": "adeptiv-ai-sdk",
                "session_id": self.session_id,
                "environment": self.environment
            }

            # Send message to SQS
            response = self.sqs_client.send_message(
                QueueUrl=self.sqs_queue_url,
                MessageBody=json.dumps(sqs_message),
                MessageAttributes={
                    'AdeptivAISource': {
                        'StringValue': self.source,
                        'DataType': 'String'
                    },
                    'Environment': {
                        'StringValue': self.environment,
                        'DataType': 'String'
                    },
                    'SessionId': {
                        'StringValue': self.session_id,
                        'DataType': 'String'
                    }
                }
            )

            logger.info(f"✅ Successfully sent message to Adeptiv-AI SQS queue. MessageId: {response['MessageId']}")
            
            return {
                "status": "success",
                "message": "Payload sent to SQS for processing",
                "sqs_message_id": response['MessageId'],
                "timestamp": time.time()
            }

        except ClientError as e:
            logger.error(f"❌ AWS SQS error: {e}")
            # Fallback to direct API call
            logger.info("🔄 Falling back to direct API call")
            return await self._send_request_async(payload, endpoint="/api/sdk/evaluate/batch")
        
        except Exception as e:
            logger.error(f"❌ Unexpected error in AWS processing: {e}")
            # Fallback to direct API call
            logger.info("🔄 Falling back to direct API call")
            return await self._send_request_async(payload, endpoint="/api/sdk/evaluate/batch")

    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the service and AWS connections.
        """
        health_status = {
            "sdk_connected": self.is_connected,
            "environment": self.environment,
            "aws_configured": bool(self.sqs_client and self.sqs_queue_url),
            "session_id": self.session_id,
            "source": self.source
        }

        if self.environment.lower() == "production" and self.sqs_client:
            try:
                # Test SQS connection
                self.sqs_client.get_queue_attributes(
                    QueueUrl=self.sqs_queue_url,
                    AttributeNames=['QueueArn']
                )
                health_status["sqs_accessible"] = True
            except Exception as e:
                health_status["sqs_accessible"] = False
                health_status["sqs_error"] = str(e)

        return health_status

    async def close(self):
        """
        Clean up resources.
        """
        self.is_connected = False
        self._batch_queue.clear()
        logger.info("🔒 Adeptiv-AI SDK connection closed")


# Example usage
async def main():
    """
    Example usage of the AsyncEvaluatorClient
    """
    # Initialize client
    client = AsyncEvaluatorClient(
        environment="production",  # or "development"
        source="adeptiv-ai-chatbot-v1"
    )

    try:
        # Connect to the service
        if await client.connect():
            # Send individual output
            result = await client.send_output(
                data={"user_input": "Hello", "bot_response": "Hi there!"},
                metadata={"model": "gpt-4", "temperature": 0.7},
                model="gpt-4"
            )
            print(f"Single output result: {result}")

            # Batch processing
            await client.batch_add(
                data={"user_input": "How are you?", "bot_response": "I'm doing well!"},
                metadata={"model": "gpt-4", "temperature": 0.7}
            )
            await client.batch_add(
                data={"user_input": "What's the weather?", "bot_response": "I don't have access to weather data."},
                metadata={"model": "gpt-4", "temperature": 0.7}
            )
            
            batch_results = await client.batch_send()
            print(f"Batch results: {batch_results}")

            # Health check
            health = await client.health_check()
            print(f"Health status: {health}")

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())