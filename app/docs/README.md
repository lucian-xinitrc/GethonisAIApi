 # Gethonis API

## About

A lightweight Python library to interact with the Gethonis API. Gethonis combines the best of OpenAI's ChatGPT responses with DeepSeek's capabilities for an enhanced conversational experience.


## Gethonis Class Arguments

### Basic Example

```python
pip install gethonis
```

```python
import gethonis as geth

bot = geth.Gethonis("some token", "gethonis", False, "http://ip:port")
message = "Test Meessage"
print(bot.get_message(message))
```

**Models:**
* `gethonis`
* `openai`
* `deepseek`


### Class Example

```python
class Gethonis:
    """
    The python client for API interaction 
    Args:
        token (str): The token for authentication
        model (str): The AI model wanted
        stream (bool): If the user wants streaming response or not
        base_url (str): The url that the API runs operates on.
    """
    def get_message(self, message):
        """
        The user sends a message and the API responds.
            
        Args:
            message (str): The message that is sent by the user
                
        Returns:
            dictionary or requests.Response: As response from the API.
        """
```



