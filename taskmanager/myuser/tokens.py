from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + str(user.is_active) + str(login_timestamp) + str(timestamp)
"""
    Redefine function _make_hash_value
    Here we want to change state of user.is_active
    """

account_activation_token = TokenGenerator()