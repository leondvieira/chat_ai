from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, first_name, last_name, password, superuser, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            superuser=superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, first_name, last_name, password, **extra_fields):
        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            superuser=False,
            **extra_fields
        )

        return user

    def create_superuser(self, username, email, first_name, last_name, password, **extra_fields):
        user = self._create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            superuser=True,
            **extra_fields
        )

        return user
