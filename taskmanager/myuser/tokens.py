from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    '''

        Создание токена

    '''
    def _make_hash_value(self, user, timestamp):
        '''

        Создание хэша

        '''
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + str(user.is_active) + str(login_timestamp) + str(timestamp)


account_activation_token = TokenGenerator()