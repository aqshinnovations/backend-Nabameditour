import os
from django.utils import timezone
import base64
import re
from datetime import datetime
import uuid
from datetime import timedelta
from django.template.loader import render_to_string
from django.db.models import Q
from io import BytesIO
from django.core.files import File
from config.common.encoder import encode,decode
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


from .models import (
    Account,
    Company,
    TokenEmailVerification,
  
    BlacklistedToken,
   
)
from .serializer import (
    AccountSerializer,
    CompanySerializer,
  

)


# account
def getAccountDetails(account, createToken=False, request=None):
    serialized_account = AccountSerializer(account, context={'request': request})

    company = Company.getById(account.companyId)
    serialized_company = CompanySerializer(company, context={'request': request})

    data = {
        "code": "200",
        "account": serialized_account.data,
        "company": serialized_company.data,
    }

    if createToken:
        refresh = RefreshToken.for_user(account)
        access = AccessToken.for_user(account)

        data["refresh"] = str(refresh)
        data["access"] = str(access)
        data["is_first_login"] = account.is_first_login

    return data



def signUpAccount(request):
    data = request.data
    print("data", request.data)

    firstName = data.get("firstName", None)
    lastName = data.get("lastName", None)
    mobile = data.get("mobile", None)
    email = data.get("email", None)
    companyName = data.get("company", None)
    password = data.get("password", None)

    print("info", firstName, lastName, mobile, email, password)

    if not firstName or not lastName or not email or not password:
        return {"code": "SGN400", "msg": "invalid request"}

    account = None

    if mobile and Account.getByMobile(mobile):
        return {"code": "SGN401", "msg": "Mobile already exists"}

    if Account.getByEmail(email):
        return {"code": "SGN402", "msg": "Email already exists"}

    account = Account()
    account.first_name = firstName
    account.last_name = lastName
    account.mobile = mobile
    account.email = email
    account.role = Account.ADMIN
    account.username = email
    account.set_password(password)
    account.pswd = encode(password)

    account.is_staff = False
    account.is_active = True
    account.is_superuser = False
    account.verified = True
    account.is_first_login = False

    account.save()

    company = Company()
    company.owner = account
    company.name = companyName
    company.save()

    account.companyId = company.id
    account.save()
    return {
        "code": "200",
        "msg": "Account created successfully!",
    }


# signin
def signInAccount(request):
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if not username or not password:
        return {"code": "LGN400", "msg": "username and password required"}
    username = str(username).lower()

    print("lower", username, password)
    account = Account.getByEmail(username)

    if not account:
        return {"code": "LGN401", "msg": "Invalid username and password , "}

    if not account.check_password(password):
        return {"code": "LGN402", "msg": "Invalid username and password!"}
    if not account.pswd:
        account.pswd = encode(password)
        account.save()
    return getAccountDetails(account=account, createToken=True)


#
def logout_user(request):
    access_token = request.data.get("access_token", None)

    if not access_token:
        return {
            "code": "LGOUT400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }

    accessToken = AccessToken(access_token)
    if BlacklistedToken.objects.filter(token=accessToken).exists():
        return {"code": "LGOUT401", "msg": "Access token is already blacklisted"}

    BlacklistedToken.objects.create(token=accessToken)
    accessToken.set_exp(int(datetime.now().timestamp()))
    return {"code": "200", "msg": "Access token successfully blacklisted"}


# profile
def getAccountProfile(request):
    account = request.user

    return getAccountDetails(account=account, createToken=False, request=request)


# change password
def changePassword(request):
    account = request.user

    data = request.data

    accountId = data.get("accountId", None)
    old_password = data.get("old_password", None)
    new_password = data.get("new_password", None)
    confirm_password = data.get("confirm_password", None)

    if not accountId or not old_password or not new_password or not confirm_password:
        return {
            "code": "CHPSWD400",
            "msg": "Bad request. Please ensure all required fields are provided",
        }

    user_accountId = str(request.user.accountId)
    if user_accountId != accountId:
        return {
            "code": "CHPSWDD401",
            "msg": "Provided accountId does not match the user",
        }

    if not account.check_password(old_password):
        return {"code": "CHPSWD402", "msg": "please enter correct old password "}

    if new_password != confirm_password:
        return {
            "code": "CHPSWD403",
            "msg": "New password and confirm password do not match",
        }

    account.set_password(new_password)
    account.is_first_login = False
    account.save()

    return {"code": "200", "msg": "Password updated successfully"}


def listMembrs(request):
    account = request.user

    members = Account.getMembers(account.companyId)
    accountSerializer = AccountSerializer(members, many=True,context={'request': request})
    return {"code": "200", "list": accountSerializer.data}


def addMember(request):
    adminUser = request.user
    data = request.data

    print("addMember", request.data)

    firstName = data.get("first_name", None)
    lastName = data.get("last_name", None)
    mobile = data.get("mobile", None)
    email = data.get("email", None)
    role = data.get("role", None)
    password = data.get("password", f"{firstName}@123")

    if not firstName or not lastName or not email or not role:
        return {"code": "ADM400", "msg": "invalid request"}

    if (
        adminUser.role == Account.SUPERADMIN
        and Account.objects.filter(companyId=adminUser.companyId).count() >= 21
    ):
        return {
            "code": "ADM405",
            "msg": "Maximum number of members reached (20). Cannot add more members.",
        }

    accountId = data.get("accountId", None)
    if accountId:
        return updateMember(request)
    print("role", adminUser.role)

    if adminUser.role not in Account.ADMIN_ROLES:
        return {"code": "ADM401", "msg": "Only admin can add members"}

    if mobile:
        if Account.getByMobile(mobile):
            return {"code": "ADM402", "msg": "Mobile already exists"}

    if Account.getByEmail(email):
        return {"code": "ADM403", "msg": "Email already exists"}

    if role not in [Account.ADMIN, Account.USER, Account.SUPERADMIN]:
        return {"code": "ADM404", "msg": "Invalid role"}

    account = Account()
    account.first_name = firstName
    account.last_name = lastName
    account.mobile = mobile
    account.email = email
    account.role = role
    account.username = email
    account.addedBy = adminUser.accountId

    account.is_staff = False
    account.is_active = True
    account.is_superuser = False
    account.verified = False
    account.save()

    account.companyId = adminUser.companyId
    account.set_password(password)

    account.save()

    # token = TokenEmailVerification.createToken(account)
    # sendMail = EmailVerificationMailer(token)
    # sendMail.start()

    data = {
        "code": "200",
        "msg": "User added successfully!.",
    }

    return data


def updateMember(request):
    adminUser = request.user
    data = request.data

    print("updateMember", data)

    first_name = data.get("first_name", None)
    last_name = data.get("last_name", None)
    mobile = data.get("mobile", None)
    email = data.get("email", None)
    role = data.get("role", None)
    accountId = data.get("accountId", None)

    if (
        not first_name
        or not last_name
        or not email
        or not accountId
        or role not in [Account.ADMIN, Account.USER, Account.SUPERADMIN]
    ):
        return {"code": "UPDMEM400", "msg": "Invalid Request !!!"}
    if adminUser.role not in Account.ADMIN_ROLES:
        return {"code": "UPDMEM403", "msg": "Only admin can Update members"}

    account = Account.getById(accountId)
    if not account:
        return {"code": "UPDMEM404", "msg": "Member not found"}

    account.first_name = first_name
    account.last_name = last_name

    if mobile:
        new_account = Account.getByMobile(mobile)

        if new_account:
            if new_account.id != account.id:
                return {"code": "UPDMEM405", "msg": "Mobile Number Already Exist !!! "}

    new_account = Account.getByEmail(email)
    if new_account:
        if account.id != new_account.id:
            return {"code": "UPDMEM404", "msg": "Email Already Exist !!! "}

    account.email = email
    account.username = email
    account.mobile = mobile
    account.role = role
    photo = None

    if request.FILES != None:
        if photo in request.FILES:
            photo = request.FILES["photo"]
            try:
                if updateAccount.photo != None:
                    if os.path.isfile(updateAccount.photo.path):
                        os.remove(updateAccount.photo.path)
            except Exception:
                pass
            updateAccount.photo = photo

    account.save()

    return {"code": "200", "msg": "Member details updated sucessfully!"}


def activateMember(request):
    adminUser = request.user
    data = request.data
    print("activate >> ", data)

    status = data.get("status", None)
    accountId = data.get("id", None)

    if adminUser.role not in Account.ADMIN_ROLES:
        return {"code": "ACTMEM400", "msg": "Only admin Activate/Deactivate members"}

    print("activate >> ", adminUser.accountId, accountId)

    if not status or not accountId:
        return {"code": "ACTMEM401", "msg": "Bad request!"}

    account = Account.getById(accountId)
    if not account:
        return {"code": "ACTMEM402", "msg": "Member not found"}

    print("activate >> ", adminUser, account)

    if adminUser == account:
        return {"code": "ACTMEM403", "msg": "Cannot deactivate account of yourself"}

    if status not in ["A", "D"]:
        return {"code": "ACTMEM404", "msg": "Invalid status"}

    msg = ""
    if status == "A":
        msg = "Account activated successfully!"
        account.is_active = True
    else:
        msg = "Account deactivated successfully!"
        account.is_active = False

    account.save()

    return {"code": "200", "msg": msg}


def deleteMember(request):
    adminUser = request.user
    data = request.GET

    accountId = data.get("id", None)

    print("account delete", adminUser.accountId, accountId)

    if adminUser.role not in Account.ADMIN_ROLES:
        return {"code": "DELMEM400", "msg": "Only admin can Delete members"}

    if not accountId:
        return {"code": "DELMEM401", "msg": "Bad request!"}

    if adminUser.accountId == accountId:
        return {"code": "DELMEM402", "msg": "Cannot delete account of yourself"}

    account = Account.getById(accountId)
    if not account:
        return {"code": "DELMEM403", "msg": "Member not found"}

    if account.role == Account.SUPERADMIN:
        return {"code": "DELMEM404", "msg": "Cannot delete a super admin account"}

    print("activate >> ", adminUser, account)

    if adminUser == account:
        return {"code": "DELMEM404", "msg": "Cannot delete account of yourself"}

    account.delete()

    return {"code": "200", "msg": "Member deleted successfully!"}


def activateAccount(request):
    tokenId = request.data.get("token")
    password = request.data.get("password")

    print("token", tokenId)
    if tokenId:
        tokenId = decode(tokenId)

    if not isValidUuid(tokenId):
        return {"code": 400, "msg": "Bad request"}

    token = TokenEmailVerification.getByTokenId(tokenId)
    print("token", token)

    if not token or not password:
        return {"code": "ACTACC400", "msg": "Bad request!"}

    if token.user:
        user = token.user
        user.verified = True
        user.set_password(password)
        user.save()
        token.delete()

        return {"code": "200", "msg": "Account activated succefully!"}

    return {"code": "ACTACC401", "msg": "Bad request!!"}

