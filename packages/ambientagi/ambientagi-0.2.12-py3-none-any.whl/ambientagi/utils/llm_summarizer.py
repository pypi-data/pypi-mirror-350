import logging

from openai import OpenAI  # type: ignore

logger = logging.getLogger(__name__)


client = OpenAI(api_key="your")


def summarize_for_email(user_text: str) -> str:
    """
    Given raw text (e.g., top AI headlines or user notes),
    produce a concise summary optimized for emailing.
    """
    # For demonstration, we format a prompt that instructs the LLM
    # to find key points and condense them into a short paragraph.
    prompt = f"""
    You are a concise summarizer. The user has provided the following content:
    \"\"\"{user_text}\"\"\"

    Please produce a short, friendly email body. It should:

    1. Begin with a greeting (like "Hello,").
    2. Offer a very brief (one or two sentences) general summary of all the news items.
    3. Then list each headline with:
    - A short description
    - The article link

    Do not include an email subject line or placeholders such as "[Your Name]" or "Subject:".
    Keep it short, relevant, and suitable for an email body also add emojis where need  .
    """

    try:
        # A hypothetical call to your LLM (e.g., GPT-4 or GPT-3.5, etc.)
        # This example uses the "gpt-4o" model name (adjust if needed).
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You summarize text for brief email updates.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,  # Slight creativity but minimal drift
            max_tokens=200,  # Enough room for a short paragraph
        )

        # Extract the summary text from the LLM's response
        summary_text = response.choices[0].message.content
        if summary_text is not None:
            summary_text = summary_text.strip()
        else:
            summary_text = "No response received."

        # Return the summary as a string
        return summary_text

    except Exception as e:
        logger.info(f"Error during summarization: {e}")
        # If there's an error, fall back to returning the original or a notice
        return "Summary not available due to an error."
