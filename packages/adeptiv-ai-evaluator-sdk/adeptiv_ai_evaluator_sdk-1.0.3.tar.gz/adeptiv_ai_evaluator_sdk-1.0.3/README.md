# Adeptiv-AI Universal GenAI Evaluation SDK

A lightweight, flexible, and production-ready SDK for evaluating and benchmarking **any** generative AI model outputs. Built with async support and AWS integration for scalable production deployments.

**Zero Formatting Requirements**: Send whatever your model produces exactly as-is - raw text, JSON, binary data, proprietary formats, or any other output.

## Why Use Adeptiv-AI SDK?

- **Universal**: Works with any generative AI model (text, image, code, audio, etc.)
- **Production-Ready**: Built-in AWS SQS integration for scalable processing
- **Async-First**: Fully asynchronous with high-performance capabilities
- **Flexible**: Accepts any output format (JSON, text, structured data)
- **Simple**: Clean, consistent API with intelligent environment detection
- **Lightweight**: Minimal dependencies with optional AWS extras
- **Reliable**: Built-in retry logic, error handling, and fallback mechanisms
- **Secure**: Enterprise-grade security with API keys and custom headers

## Installation

### Python SDK (Async)

```bash
pip install adeptiv-ai-evaluator-sdk

```

## Quick Start

### Basic Usage (Development)

```python
import asyncio
from adeptiv_ai_evaluator import AsyncEvaluatorClient

async def main():
    client = AsyncEvaluatorClient(
        api_key="your_adeptiv_ai_api_key",
        source="my-adeptiv-ai-app",
        environment="development"
    )
    
    # Connect to Adeptiv-AI service
    if await client.connect():
        # Send ANY model output exactly as your model produces it
        result = await client.send_output(
            your_model_raw_output,  # Use the exact output from your model
            model="your-model-name",
            metadata={"any": "relevant info"}
        )
        print(result)
    
    await client.close()

```

## Example Use Cases

- **Model Quality Assessment**: Evaluate GenAI model quality, accuracy and safety
- **Benchmark Comparisons**: Compare different models against each other
- **Performance Monitoring**: Monitor model drift and performance over time
- **Human Review Pipeline**: Log outputs for human evaluation and review
- **A/B Testing**: Create shareable evaluations for model comparison
- **Production Monitoring**: Real-time evaluation of production AI systems
- **Compliance Tracking**: Maintain audit trails for AI model outputs

## API Reference

### AsyncEvaluatorClient

#### Methods

- `connect()` - Establish connection to Adeptiv-AI service
- `send_output(data, metadata=None, model=None)` - Send individual output
- `batch_add(data, metadata=None, model=None)` - Add to batch queue
- `batch_send()` - Send entire batch
- `health_check()` - Check service and AWS connectivity
- `close()` - Clean up resources

#### Parameters

- `api_key`: Your Adeptiv-AI API key
- `source`: Application identifier
- `environment`: "development" or "production"
- `max_retries`: Number of retry attempts (default: 3)
- `retry_delay`: Base delay between retries (default: 1.0s)
- `aws_region`: AWS region for SQS/Lambda (default: us-east-1)

## Support

- **Documentation**: [https://docs.adeptiv-ai.com/sdk](https://docs.adeptiv-ai.com/sdk)
- **GitHub Issues**: [https://github.com/adeptiv-ai/evaluator-sdk/issues](https://github.com/adeptiv-ai/evaluator-sdk/issues)
- **Email Support**: [sdk@adeptiv-ai.com](mailto:sdk@adeptiv-ai.com)
- **Enterprise Support**: [enterprise@adeptiv-ai.com](mailto:enterprise@adeptiv-ai.com)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Adeptiv-AI** - Advancing AI evaluation and safety through intelligent automation.