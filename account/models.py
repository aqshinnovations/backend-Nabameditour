import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta


class Account(AbstractUser):
    USER = "U"
    ADMIN = "A"
    SUPERADMIN = "S"

    ADMIN_ROLES = [ADMIN, SUPERADMIN]

    ROLE = [(USER, "User"), (ADMIN, "Admin"), (SUPERADMIN, "SuperAdmin")]

    accountId = models.UUIDField(primary_key=False, unique=True, editable=False)
    role = models.CharField(max_length=1, choices=ROLE, default=USER)
    is_first_login = models.BooleanField(default=True)
    pswd = models.CharField(max_length=100, unique=False, null=True, blank=True)
    mobile = models.CharField(max_length=20, unique=False, null=True, blank=True)
    photo = models.ImageField(
        upload_to="media/users/photos", default=None, null=True, blank=True
    )
    verified = models.BooleanField(default=True)
    companyId = models.UUIDField(default=None, null=True, blank=True)
    addedBy = models.UUIDField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.accountId:
            self.accountId = uuid.uuid4()
        self.email = self.username
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.mobile) + " " + str(self.email)[:20]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    @staticmethod
    def getById(accountId):
        if Account.objects.filter(accountId=accountId).exists():
            return Account.objects.get(accountId=accountId)
        return None

    @staticmethod
    def getByAll():
        return Account.objects.all()

    @staticmethod
    def getByMobile(mobile):
        if Account.objects.filter(mobile=mobile).exists():
            return Account.objects.get(mobile=mobile)
        return None

    @staticmethod
    def getByEmail(email):
        email = str(email).lower()
        print("getByEmail >> ", email)
        if Account.objects.filter(email=email).exists():
            return Account.objects.get(email=email)
        return None

    @staticmethod
    def getMembers(companyId):
        return Account.objects.filter(companyId=companyId)

    @staticmethod
    def getByLogin(mobile, password):
        if Account.objects.filter(mobile=mobile, password=password).exists():
            return Account.objects.get(mobile=mobile)
        return None


class Company(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    owner = models.OneToOneField(
        Account, verbose_name="owner", null=False, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, unique=False, null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.name)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    @staticmethod
    def getById(id):
        if Company.objects.filter(id=id).exists():
            return Company.objects.get(id=id)
        return None

    @staticmethod
    def getByOwner(account):
        if Company.objects.filter(owner=account).exists():
            return Company.objects.get(owner=account)
        return None


class TokenEmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        Account, default=1, verbose_name="User", on_delete=models.CASCADE
    )
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.user.id)[:50]

    @staticmethod
    def getByTokenId(id):
        try:
            if TokenEmailVerification.objects.filter(id=id).exists():
                return TokenEmailVerification.objects.get(id=id)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getByUser(user):
        try:
            if TokenEmailVerification.objects.filter(user=user).exists():
                return TokenEmailVerification.objects.get(user=user)
            return None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def createToken(user):
        token = TokenEmailVerification.getByUser(user)
        if not token:
            token = TokenEmailVerification()
            token.user = user
        token.is_verified = False
        token.save()
        return token

    class Meta:
        verbose_name = "Token Email Verification"
        verbose_name_plural = "Tokens Email Verification"


# blacklist token(logout)
class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    invalidated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.token)

