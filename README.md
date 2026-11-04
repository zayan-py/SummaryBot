# SummaryBot

My friends love chatting on Discord, even though I think the app is best kept purely for gaming voice calls. Every day, I come back to a server packed with hundreds of missed messages - far too many for me to actually sit down and read through to catch up.

So, I did what any programmer would do: I built a Discord bot to summarise the conversations for me. The architecture is straightforward. It uses the Pycord library to interface with Discord, pulls recent message history, formats the chat logs for an LLM API, and posts a concise breakdown directly back into the channel.

You can install (Pycord)[https://pycord.dev/] here
```pip install py-cord```
