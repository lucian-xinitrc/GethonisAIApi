# Gethonis API

## Tutorial how to use the test script

### Run the script
The name of the script is `test.py`
```bash
python3 test.py
```

### Set the Values
**First Prompt**
In the first prompt you will set what AI model you will use.
```
Please type what AI client do you want:
```
Here you have three options:
`gethonis`
`openai`
`deepseek`

**Second Prompt**
In the second prompt you will need to type the token.
```
Please insert the token:
```
The token for testing is: `TEST`

**Third Prompt**
Here you will need to tell the program if you want with streaming or not.
```
Streaming? yes or no: 
```
The options as presented above are:
`yes`
`no`

### API Prompt
***Note: If the screen displays the text <Positive> than you have been authorised, if it says <Negative> contact the admin.***
**Insert Prompts**
As it is presented now you can insert any prompt that you want.
```
[ Write the prompt: ] 
```

### Settings
You can change the AI model or the streaming option while you are using the test program.
**Change the AI model**
Just simply time on write the prompt, `change_model`
```
[ Write the prompt: ] change_model
```
**Change the Streaming status**
Just simply time on write the prompt, `change_stream`
```
[ Write the prompt: ] change_stream
```