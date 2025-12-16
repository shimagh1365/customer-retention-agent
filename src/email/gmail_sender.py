import os
import json
import base64
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from email.mime.text import MIMEText


class GmailDraftSender:
    """
    Uses Google Web OAuth with loopback redirect for authentication.
    Creates draft emails in Gmail.
    """

    SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

    def __init__(
        self,
        credentials_path="credentials/credentials.json",
        token_path="credentials/token.json",
        redirect_port=8899
    ):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.redirect_port = redirect_port

        self.service = self._authenticate()

    # --------------------------------------------------------------
    # OAuth Handler
    # --------------------------------------------------------------
    def _authenticate(self):
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(
                self.token_path,
                self.SCOPES
            )

        # Refresh or start OAuth
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = self._run_web_oauth_flow()

            # Save token
            with open(self.token_path, "w") as token_file:
                token_file.write(creds.to_json())

        # Build Gmail service
        return build("gmail", "v1", credentials=creds)

    # --------------------------------------------------------------
    # Web OAuth Redirect Handler
    # --------------------------------------------------------------
    def _run_web_oauth_flow(self):
        flow = Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=self.SCOPES,
            redirect_uri=f"http://localhost:{self.redirect_port}/oauth2callback"
        )

        auth_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent"
        )

        print("\n🌍 OPEN THIS URL IN YOUR BROWSER:\n")
        print(auth_url)
        print(f"\n⏳ Waiting for Google redirect to localhost:{self.redirect_port} ...")

        # Start temporary server to catch redirect
        code_holder = {"code": None, "state": state}

        class OAuthHandler(BaseHTTPRequestHandler):
            def do_GET(self_inner):
                if "/oauth2callback" in self_inner.path:
                    from urllib.parse import urlparse, parse_qs

                    query = parse_qs(urlparse(self_inner.path).query)
                    code_holder["code"] = query.get("code", [None])[0]

                    # Show browser success message
                    self_inner.send_response(200)
                    self_inner.send_header("Content-type", "text/html")
                    self_inner.end_headers()
                    self_inner.wfile.write(
                        b"<h1>Authentication complete. You may close this window.</h1>"
                    )

        server = HTTPServer(("localhost", self.redirect_port), OAuthHandler)
        thread = threading.Thread(target=server.handle_request)
        thread.start()
        thread.join()

        # Exchange code for token
        print("🔄 Exchanging auth code for token...")

        flow.fetch_token(code=code_holder["code"])

        print("✅ Gmail OAuth complete.")

        return flow.credentials

    # --------------------------------------------------------------
    # Create Gmail Draft
    # --------------------------------------------------------------
    def create_draft(self, sender_email, to_email, subject, body_text):
        message = MIMEText(body_text)
        message["to"] = to_email
        message["from"] = sender_email
        message["subject"] = subject

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode("utf-8")

        create_message = {"message": {"raw": encoded_message}}

        draft = self.service.users().drafts().create(
            userId="me",
            body=create_message
        ).execute()

        return draft
