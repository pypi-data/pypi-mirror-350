from ambientagi.providers.voice_provider import TwilioVoiceAgent


def create_voice_agent(
    self,
    agent_id: str,
    system_message: str,
    twilio_sid: str,
    twilio_token: str,
    caller_id: str,
    voice: str = "alloy",
    temperature: float = 0.8,
) -> TwilioVoiceAgent:
    """
    Creates a TwilioVoiceAgent for the specified agent, enabling real-time voice interactions,
    phone call automation, and voice response systems using Twilio and OpenAI.

    Parameters:
    - agent_id (str): The ID of the agent to attach to the voice service.
    - system_message (str): The initial system message or greeting for the voice agent.
    - twilio_sid (str): The Twilio account SID for authentication.
    - twilio_token (str): The Twilio authentication token.
    - caller_id (str): The phone number or caller ID to use for outgoing calls.
    - voice (str): The voice model to use for speech synthesis (default is 'alloy').
    - temperature (float): The response creativity level for OpenAI interactions (default is 0.8).

    Returns:
    - TwilioVoiceAgent: An instance of the TwilioVoiceAgent class, pre-configured with Twilio and OpenAI integration.

    Capabilities:
    - Make and Receive Phone Calls
    - Voice-Activated Conversations
    - Speech Synthesis and Real-Time Interaction
    - Personalized Greetings and Call Flows
    - Call Recording and Transcription
    - IVR (Interactive Voice Response) Systems
    - Voice Command Recognition
    - Multi-Language Support
    - Integration with Other Services (e.g., CRM, Support Systems)
    Notes:
    - Ensure the agent is configured with valid Twilio credentials and permissions.
    - For security reasons, avoid hardcoding sensitive credentials in your code.
    - For more information on Twilio's voice capabilities, refer to the official Twilio Voice API documentation.
    - https://www.twilio.com/docs/voice
    - https://www.twilio.com/docs/voice/twiml
    - https://www.twilio.com/docs/voice/twiml/voice

    """
    # _agent = self.get_agent_info(agent_id)

    return TwilioVoiceAgent(
        openai_api_key=self.openai_wrapper.api_key,
        twilio_account_sid=twilio_sid,
        twilio_auth_token=twilio_token,
        twilio_caller_id=caller_id,
        voice=voice,
        temperature=temperature,
    )
