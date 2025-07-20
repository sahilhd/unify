"""
Email service using Resend for UniLLM
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Try to import resend, but don't fail if not installed
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logger.warning("Resend not installed. Email sending will be logged only.")

class EmailService:
    """Email service for sending verification emails"""
    
    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY")
        self.from_email = os.getenv("RESEND_FROM_EMAIL", "noreply@unillm.com")
        self.enabled = RESEND_AVAILABLE and self.api_key is not None
        
        if self.enabled:
            resend.api_key = self.api_key
            logger.info("Email service initialized with Resend")
        else:
            logger.warning("Email service disabled - RESEND_API_KEY not set or Resend not installed")
    
    def send_verification_email(self, email: str, verification_url: str) -> bool:
        """Send email verification email"""
        try:
            if not self.enabled:
                logger.info(f"EMAIL VERIFICATION (disabled): {email} -> {verification_url}")
                return True
            
            subject = "Verify your UniLLM account"
            html_content = self._get_verification_email_template(verification_url, email)
            
            response = resend.emails.send({
                "from": self.from_email,
                "to": email,
                "subject": subject,
                "html": html_content
            })
            
            logger.info(f"Verification email sent to {email}: {response.get('id', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {str(e)}")
            return False
    
    def send_welcome_email(self, email: str) -> bool:
        """Send welcome email after successful verification"""
        try:
            if not self.enabled:
                logger.info(f"WELCOME EMAIL (disabled): {email}")
                return True
            
            subject = "Welcome to UniLLM! Your account is now active"
            html_content = self._get_welcome_email_template()
            
            response = resend.emails.send({
                "from": self.from_email,
                "to": email,
                "subject": subject,
                "html": html_content
            })
            
            logger.info(f"Welcome email sent to {email}: {response.get('id', 'unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {email}: {str(e)}")
            return False
    
    def _get_verification_email_template(self, verification_url: str, email: str) -> str:
        """Get HTML template for verification email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify your UniLLM account</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Welcome to UniLLM!</h1>
                <p>Verify your email address to get started</p>
            </div>
            
            <div class="content">
                <h2>Hi there!</h2>
                <p>Thanks for signing up for UniLLM! To complete your registration and start using our unified LLM platform, please verify your email address.</p>
                
                <div style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </div>
                
                <p><strong>What happens next?</strong></p>
                <ul>
                    <li>Click the button above to verify your email</li>
                    <li>Your account will be activated immediately</li>
                    <li>You'll be redirected to your dashboard</li>
                    <li>Start using UniLLM with OpenAI, Anthropic, and Google models!</li>
                </ul>
                
                <p><strong>Can't click the button?</strong></p>
                <p>Copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #667eea;">{verification_url}</p>
                
                <p><strong>Link expires in 24 hours</strong></p>
                <p>If you didn't create an account with UniLLM, you can safely ignore this email.</p>
            </div>
            
            <div class="footer">
                <p>© 2024 UniLLM. All rights reserved.</p>
                <p>This email was sent to {email}</p>
            </div>
        </body>
        </html>
        """
    
    def _get_welcome_email_template(self) -> str:
        """Get HTML template for welcome email"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to UniLLM!</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }
                .content {
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }
                .button {
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 20px 0;
                }
                .footer {
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 Welcome to UniLLM!</h1>
                <p>Your account is now active</p>
            </div>
            
            <div class="content">
                <h2>You're all set!</h2>
                <p>Your email has been verified and your UniLLM account is now active. You can start using our unified LLM platform right away!</p>
                
                <div style="text-align: center;">
                    <a href="https://unillm-frontend.railway.app/dashboard" class="button">Go to Dashboard</a>
                </div>
                
                <h3>What you can do now:</h3>
                <ul>
                    <li><strong>Chat with AI models</strong> - Use OpenAI GPT-4, Anthropic Claude, and Google Gemini</li>
                    <li><strong>Unified API</strong> - Same code works with any provider</li>
                    <li><strong>Manage your usage</strong> - Track credits and billing</li>
                    <li><strong>API access</strong> - Use your API key for integrations</li>
                </ul>
                
                <h3>Getting Started:</h3>
                <ol>
                    <li>Visit your dashboard to see your account overview</li>
                    <li>Check out the chat interface to test different models</li>
                    <li>Review your API key in the settings</li>
                    <li>Start building with our unified API!</li>
                </ol>
                
                <p><strong>Need help?</strong></p>
                <p>Check out our documentation or reach out to our support team.</p>
            </div>
            
            <div class="footer">
                <p>© 2024 UniLLM. All rights reserved.</p>
                <p>Thanks for choosing UniLLM!</p>
            </div>
        </body>
        </html>
        """

# Global email service instance
email_service = EmailService() 