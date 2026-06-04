"""
Password Reset Module for iLEARN
=================================
Handles secure password reset tokens, email sending, and password updates.
Uses Resend for email delivery.
"""

import secrets
import sqlite3
from datetime import datetime, timedelta
import os

try:
    from resend import Resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False


class PasswordResetManager:
    """Manages password reset tokens and email sending."""
    
    # Token expiration: 1 hour
    TOKEN_EXPIRY_MINUTES = 60
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.resend_api_key = os.getenv('RESEND_API_KEY')
        self.resend_from_email = os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev')
        
        if self.resend_api_key and RESEND_AVAILABLE:
            self.resend_client = Resend(api_key=self.resend_api_key)
        else:
            self.resend_client = None
    
    def generate_reset_token(self) -> str:
        """Generate a secure random reset token."""
        return secrets.token_urlsafe(32)
    
    def get_user_by_email(self, email: str):
        """Fetch user by email from database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", 
            (email,)
        ).fetchone()
        conn.close()
        return user
    
    def create_reset_token(self, user_id: int, email: str) -> str:
        """
        Create a password reset token for a user.
        Returns the token string.
        """
        token = self.generate_reset_token()
        
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute(
                "INSERT INTO password_resets (user_id, token, created_at) VALUES (?, ?, ?)",
                (user_id, token, datetime.utcnow().isoformat())
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # Token already exists (extremely unlikely), generate new one
            conn.close()
            return self.create_reset_token(user_id, email)
        finally:
            conn.close()
        
        return token
    
    def verify_reset_token(self, token: str) -> dict:
        """
        Verify that a reset token is valid and not expired.
        Returns: {valid: bool, user_id: int, email: str, error: str}
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Find the reset token
        reset_record = conn.execute(
            "SELECT * FROM password_resets WHERE token = ?",
            (token,)
        ).fetchone()
        
        if not reset_record:
            conn.close()
            return {"valid": False, "error": "Invalid reset token"}
        
        # Check if token has expired (1 hour)
        created_at = datetime.fromisoformat(reset_record['created_at'])
        expiry_time = created_at + timedelta(minutes=self.TOKEN_EXPIRY_MINUTES)
        
        if datetime.utcnow() > expiry_time:
            conn.close()
            return {"valid": False, "error": "Reset token has expired. Please request a new one."}
        
        # Get user information
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (reset_record['user_id'],)
        ).fetchone()
        
        conn.close()
        
        if not user:
            return {"valid": False, "error": "User not found"}
        
        return {
            "valid": True,
            "user_id": user['id'],
            "username": user['username'],
            "email": user['email'],
            "token": token
        }
    
    def reset_password(self, token: str, new_password: str) -> dict:
        """
        Reset a user's password using a valid token.
        Returns: {success: bool, message: str, error: str}
        """
        # Verify the token first
        verification = self.verify_reset_token(token)
        if not verification['valid']:
            return {"success": False, "error": verification['error']}
        
        user_id = verification['user_id']
        
        # Hash the password
        from werkzeug.security import generate_password_hash
        hashed_password = generate_password_hash(new_password)
        
        conn = sqlite3.connect(self.db_path)
        try:
            # Update user password
            conn.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (hashed_password, user_id)
            )
            
            # Delete the reset token (mark as used)
            conn.execute(
                "DELETE FROM password_resets WHERE token = ?",
                (token,)
            )
            
            conn.commit()
            
            return {
                "success": True,
                "message": "Password reset successfully. You can now log in with your new password."
            }
        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Database error: {str(e)}"}
        finally:
            conn.close()
    
    def send_reset_email(self, email: str, username: str, reset_token: str, reset_url: str) -> dict:
        """
        Send password reset email via Resend.
        
        Args:
            email: User's email address
            username: User's username for greeting
            reset_token: The reset token
            reset_url: Full URL to password reset page (e.g., https://ilearn.com/reset?token=xyz)
        
        Returns: {success: bool, message: str, error: str}
        """
        if not self.resend_client:
            return {
                "success": False,
                "error": "Email service not configured. Set RESEND_API_KEY environment variable."
            }
        
        try:
            # Create HTML email template
            email_html = f"""
            <!DOCTYPE html>
            <html>
              <head>
                <style>
                  body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; }}
                  .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); }}
                  .header {{ background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); color: white; padding: 40px 20px; text-align: center; }}
                  .header h1 {{ margin: 0; font-size: 28px; font-weight: 800; }}
                  .content {{ padding: 40px 30px; color: #333; }}
                  .greeting {{ font-size: 16px; margin-bottom: 20px; }}
                  .message {{ font-size: 15px; line-height: 1.6; color: #666; margin-bottom: 30px; }}
                  .cta-button {{ background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); color: white; text-decoration: none; padding: 14px 30px; border-radius: 8px; display: inline-block; font-weight: 700; margin: 30px 0; }}
                  .cta-button:hover {{ opacity: 0.95; }}
                  .warning {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px; font-size: 14px; color: #333; }}
                  .footer {{ background-color: #f9f9f9; padding: 20px; text-align: center; font-size: 12px; color: #999; border-top: 1px solid #eee; }}
                  .token-info {{ background-color: #f0f0f0; padding: 15px; border-radius: 4px; font-family: monospace; font-size: 12px; color: #333; margin: 20px 0; word-break: break-all; }}
                </style>
              </head>
              <body>
                <div class="container">
                  <div class="header">
                    <h1>iLearn</h1>
                    <p>Password Reset Request</p>
                  </div>
                  
                  <div class="content">
                    <div class="greeting">
                      Hello <strong>{username}</strong>,
                    </div>
                    
                    <div class="message">
                      We received a request to reset your iLearn password. If you didn't make this request, you can safely ignore this email and your password will remain unchanged.
                    </div>
                    
                    <div style="text-align: center;">
                      <a href="{reset_url}" class="cta-button">Reset Password</a>
                      <p style="font-size: 13px; color: #999;">or copy this link if the button doesn't work:</p>
                      <p style="word-break: break-all; font-size: 12px; color: #666;">{reset_url}</p>
                    </div>
                    
                    <div class="warning">
                      <strong>⏱️ This link expires in 1 hour.</strong> After that, you'll need to request a new password reset.
                    </div>
                    
                    <div class="message" style="margin-top: 30px; font-size: 14px; color: #999;">
                      <strong>Didn't request this?</strong><br>
                      If you didn't ask to reset your password, please ignore this email or contact support immediately. Your account is safe.
                    </div>
                  </div>
                  
                  <div class="footer">
                    <p style="margin: 0;">© 2024 iLearn. All rights reserved.</p>
                    <p style="margin: 10px 0 0 0;">Powered by iLearn • Premium learning redefined</p>
                  </div>
                </div>
              </body>
            </html>
            """
            
            # Send via Resend
            print(f"[Resend Debug] Sending email to {email}")
            print(f"[Resend Debug] From: {self.resend_from_email}")
            print(f"[Resend Debug] Subject: Reset Your iLearn Password")
            
            response = self.resend_client.emails.send({
                "from": self.resend_from_email,
                "to": email,
                "subject": "Reset Your iLearn Password",
                "html": email_html,
            })
            
            print(f"[Resend Debug] Full response: {response}")
            print(f"[Resend Debug] Response type: {type(response)}")
            print(f"[Resend Debug] Response keys: {response.keys() if hasattr(response, 'keys') else 'N/A'}")
            
            if response.get('id'):
                print(f"[Resend Debug] SUCCESS - Email ID: {response.get('id')}")
                return {
                    "success": True,
                    "message": f"Password reset email sent to {email}"
                }
            else:
                error = response.get('error', {}).get('message', 'Unknown error') if isinstance(response.get('error'), dict) else str(response.get('error', 'Unknown error'))
                print(f"[Resend Debug] FAILURE - Error: {error}")
                return {
                    "success": False,
                    "error": f"Failed to send email: {error}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Email service error: {str(e)}"
            }
    
    def cleanup_expired_tokens(self):
        """Remove expired reset tokens from database (optional cleanup job)."""
        conn = sqlite3.connect(self.db_path)
        try:
            # Delete tokens older than 24 hours
            cutoff_time = (datetime.utcnow() - timedelta(hours=24)).isoformat()
            conn.execute(
                "DELETE FROM password_resets WHERE created_at < ?",
                (cutoff_time,)
            )
            conn.commit()
        finally:
            conn.close()