# Email Validator Usage Examples

This document provides examples of how to use the Email Validator API in various programming languages.

## Python Example

### Single Email Validation
```python
import aiohttp
import asyncio

async def validate_email(email: str, api_key: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        async with session.post(
            "https://api.emailvalidator.com/v1/validate",
            json={"email": email},
            headers=headers
        ) as response:
            return await response.json()

# Usage
async def main():
    api_key = "your-api-key-here"
    result = await validate_email("test@example.com", api_key)
    print(f"Validation result: {result}")

asyncio.run(main())
```

### Batch Validation with Rate Limiting
```python
import asyncio
from typing import List, Dict
import aiohttp
from aiohttp import ClientResponseError

class EmailValidator:
    def __init__(self, api_key: str, batch_size: int = 10):
        self.api_key = api_key
        self.batch_size = batch_size
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def validate_batch(self, emails: List[str]) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    "https://api.emailvalidator.com/v1/validate/batch",
                    json={"emails": emails},
                    headers=self.headers
                ) as response:
                    if response.status == 429:  # Rate limited
                        retry_after = int(response.headers.get("Retry-After", "5"))
                        await asyncio.sleep(retry_after)
                        return await self.validate_batch(emails)
                    
                    return (await response.json())["results"]
            except ClientResponseError as e:
                print(f"Error validating batch: {e}")
                return []
    
    async def validate_all(self, emails: List[str]) -> List[Dict]:
        results = []
        for i in range(0, len(emails), self.batch_size):
            batch = emails[i:i + self.batch_size]
            batch_results = await self.validate_batch(batch)
            results.extend(batch_results)
            await asyncio.sleep(1)  # Rate limiting precaution
        return results

# Usage
async def main():
    validator = EmailValidator("your-api-key-here")
    emails = [
        "test1@example.com",
        "test2@example.com",
        "test3@example.com"
    ]
    results = await validator.validate_all(emails)
    for result in results:
        print(f"{result['email']}: {'Valid' if result['is_valid'] else 'Invalid'}")

asyncio.run(main())
```

## Node.js Example

### Single Email Validation
```javascript
const axios = require('axios');

async function validateEmail(email, apiKey) {
    try {
        const response = await axios.post(
            'https://api.emailvalidator.com/v1/validate',
            { email },
            {
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('Validation error:', error.response?.data || error.message);
        throw error;
    }
}

// Usage
async function main() {
    try {
        const result = await validateEmail('test@example.com', 'your-api-key-here');
        console.log('Validation result:', result);
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

### Batch Validation with Rate Limiting
```javascript
const axios = require('axios');

class EmailValidator {
    constructor(apiKey, batchSize = 10) {
        this.apiKey = apiKey;
        this.batchSize = batchSize;
        this.client = axios.create({
            baseURL: 'https://api.emailvalidator.com/v1',
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });
    }

    async validateBatch(emails) {
        try {
            const response = await this.client.post('/validate/batch', { emails });
            return response.data.results;
        } catch (error) {
            if (error.response?.status === 429) {
                const retryAfter = parseInt(error.response.headers['retry-after'] || '5');
                await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
                return this.validateBatch(emails);
            }
            throw error;
        }
    }

    async validateAll(emails) {
        const results = [];
        for (let i = 0; i < emails.length; i += this.batchSize) {
            const batch = emails.slice(i, i + this.batchSize);
            const batchResults = await this.validateBatch(batch);
            results.push(...batchResults);
            await new Promise(resolve => setTimeout(resolve, 1000)); // Rate limiting
        }
        return results;
    }
}

// Usage
async function main() {
    const validator = new EmailValidator('your-api-key-here');
    const emails = [
        'test1@example.com',
        'test2@example.com',
        'test3@example.com'
    ];

    try {
        const results = await validator.validateAll(emails);
        results.forEach(result => {
            console.log(`${result.email}: ${result.is_valid ? 'Valid' : 'Invalid'}`);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
```

## Error Handling Best Practices

```python
# Python error handling example
async def validate_with_retry(email: str, max_retries: int = 3) -> dict:
    retry_count = 0
    while retry_count < max_retries:
        try:
            result = await validate_email(email)
            return result
        except aiohttp.ClientResponseError as e:
            if e.status == 429:  # Rate limited
                retry_after = int(e.headers.get("Retry-After", "5"))
                await asyncio.sleep(retry_after)
                retry_count += 1
                continue
            elif e.status >= 500:  # Server error
                await asyncio.sleep(2 ** retry_count)
                retry_count += 1
                continue
            else:
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
    
    raise Exception("Max retries exceeded")
```

## Configuration Best Practices

```python
# Python configuration example
class EmailValidatorConfig:
    def __init__(self):
        self.api_key = os.getenv("EMAIL_VALIDATOR_API_KEY")
        self.base_url = os.getenv("EMAIL_VALIDATOR_URL", "https://api.emailvalidator.com/v1")
        self.batch_size = int(os.getenv("EMAIL_VALIDATOR_BATCH_SIZE", "10"))
        self.max_retries = int(os.getenv("EMAIL_VALIDATOR_MAX_RETRIES", "3"))
        self.timeout = int(os.getenv("EMAIL_VALIDATOR_TIMEOUT", "30"))

    def validate(self):
        if not self.api_key:
            raise ValueError("API key not configured")
```

Remember to:
1. Always implement proper error handling
2. Use environment variables for configuration
3. Implement retry logic with exponential backoff
4. Handle rate limits appropriately
5. Use batch validation when possible
6. Include proper timeout handling
7. Log validation results and errors