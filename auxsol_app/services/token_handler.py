from django.utils import timezone
from datetime import timedelta
from auxsol_app.models import AuxsolToken
from .client import AuxsolClient
import logging

logger = logging.getLogger(__name__)


def get_valid_token():
    """
    ✅ FIXED: Proper token management with fallback
    Returns the access token string or None if unable to get one
    """

    # 1. Check if we have a valid token in database
    token_obj = AuxsolToken.objects.order_by('-created_at').first()

    if token_obj and token_obj.is_valid():
        logger.info(f"✅ Using existing token (expires at {token_obj.expires_at})")
        return token_obj.access_token

    logger.warning("⚠️ No valid token found, attempting fresh login...")

    # 2. Get fresh token via login
    client = AuxsolClient()
    login_response = client.login()

    # ✅ FIXED: Properly check if login was successful
    if not login_response:
        logger.error("❌ Login failed: No response from server")
        return None

    if login_response.get('code') != "AWX-0000":
        error_msg = login_response.get('msg', 'Unknown error')
        logger.error(f"❌ Login failed: {login_response.get('code')} - {error_msg}")
        return None

    # 3. Extract token from response
    try:
        new_token = login_response.get('data', {}).get('token')

        if not new_token:
            logger.error("❌ Login successful but no token in response")
            return None

        # 4. Save new token to database
        AuxsolToken.objects.all().delete()  # Remove old tokens

        # ✅ FIXED: Set proper expiration (usually 24 hours for Auxsol)
        expires_at = timezone.now() + timedelta(hours=23)  # Slightly less than actual

        new_obj = AuxsolToken.objects.create(
            access_token=new_token,
            expires_at=expires_at
        )

        logger.info(f"✅ New token created (expires at {expires_at})")
        return new_obj.access_token

    except Exception as e:
        logger.error(f"❌ Error processing login response: {e}")
        return None