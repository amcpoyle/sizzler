Sizzler is named so because it is cooking up... employment...

It is an LLM agent built with LangChain that can be provided queries in a specific format to find job/internship listings. Sizzler then uses the Gmail API to send an email to the user, and this process can be scheduled using launchd (MacOS) or a similar program for Windows/Linux.

# Prerequisites
* Python
* LangChain and a new langchain project to setup tracing
* An OpenAI developer account and some tokens
* Google developer account
* An email address to send the alerts from
* An email address (your personal email) to receive emails
# Setup 
Set the following six environment variables:
  *RECEIVER_EMAIL = "your personal email"
  * SENDER_EMAIL = "the designated email to send alerts from"
  * LANGSMITH_TRACING="true"
  * LANGSMITH_API_KEY="your api key"
  * LANGSMITH_PROJECT="your project name"
  * OPENAI_API_KEY="your openai api key"

