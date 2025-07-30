# ambientagi/providers/email_provider.py
import logging
import os
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional

from ambientagi.utils.llm_summarizer import summarize_for_email

logger = logging.getLogger(__name__)


class EmailProvider:
    def __init__(
        self,
        agent_info: Dict[str, Any],
        smtp_server: str = "smtp.gmail.com",  # Default to Gmail
        smtp_port: int = 587,  # TLS port
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
    ):
        """
        Initialize the provider with agent_info and optional SMTP configs.
        By default, we configure the provider for Gmail's SMTP server using TLS on port 587.

        If you have 2FA enabled on your account, you must use an 'App Password' instead of
        your normal Gmail password. (See: https://myaccount.google.com/security -> App Passwords)
        """
        self.agent_info = agent_info
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(
        self,
        to_address: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        from_address: Optional[str] = None,
        auto_summarize: bool = True,
    ) -> Dict[str, str]:
        """
        Send an email, optionally summarizing the 'body' via LLM before sending.

        :param to_address: Main recipient address
        :param subject: Email subject
        :param body: Raw text content (will be auto-summarized if auto_summarize is True)
        :param cc: List of addresses for CC
        :param bcc: List of addresses for BCC
        :param from_address: If None, defaults to self.username
        :param auto_summarize: If True, run 'summarize_for_email' on 'body' first
        :return: A dictionary with status + message (success or error)
        """
        if not from_address:
            from_address = self.username or "noreply@example.com"

        # Build the recipient list
        recipients = [to_address]
        if cc:
            recipients.extend(cc)
        if bcc:
            recipients.extend(bcc)

        try:
            # 1) If auto_summarize is True, call the LLM-based summarizer on the raw body
            final_body = body
            if auto_summarize:
                logger.info("Summarizing email body via LLM before sending...")
                final_body = summarize_for_email(body)

            # 2) Construct the MIME message with UTF-8
            msg = MIMEMultipart()
            msg["From"] = from_address
            msg["To"] = to_address
            if cc:
                msg["Cc"] = ", ".join(cc)
            msg["Subject"] = str(Header(subject, "utf-8"))

            body_part = MIMEText(final_body, "plain", "utf-8")
            msg.attach(body_part)

            # 3) Connect to SMTP and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                if self.use_tls:
                    server.starttls()
                    server.ehlo()

                if self.username and self.password:
                    server.login(self.username, self.password)

                server.sendmail(from_address, recipients, msg.as_string())

            return {"status": "success", "message": "Email sent successfully"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def send_email_with_footer(
        self,
        to_address: str,
        subject: str,
        body: str,
        footer_image_path: str = "footer.png",  # Path to the local image
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        from_address: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Send an email with an image footer from the local machine.
        """
        if not from_address:
            from_address = self.username or "noreply@example.com"

        recipients = [to_address] + (cc if cc else []) + (bcc if bcc else [])

        # Create the email container
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address
        msg["Subject"] = subject
        if cc:
            msg["CC"] = ", ".join(cc)

        # Email body in HTML format
        html_body = f"""
        <html>
        <head>
            <style>
                white-space: pre-wrap;
                .footer-image {{
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    max-width: 200px;
                }}
            </style>
        </head>
        <body>
            <p style="white-space: pre-wrap;">{body}</p>
            <br>
            <img src="cid:footer_image" class="footer-image">
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        # Attach the image
        if os.path.exists(footer_image_path):
            with open(footer_image_path, "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header("Content-ID", "<footer_image>")
                img.add_header("Content-Disposition", "inline", filename="footer.jpg")
                # Set a small image size
                img.add_header("Content-Size", "width=100,height=100")
                msg.attach(img)
        else:
            return {"status": "error", "message": "Footer image not found"}

        try:
            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                if self.use_tls:
                    server.starttls()
                    server.ehlo()

                if self.username and self.password:
                    server.login(self.username, self.password)

                # Send email
                server.sendmail(from_address, recipients, msg.as_string())

            return {"status": "success", "message": "Email sent"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
