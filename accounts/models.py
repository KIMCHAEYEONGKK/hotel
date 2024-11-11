import base64
import datetime
import hashlib
import hmac
import string
import time
from random import randint

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from .validators import validate_id
from .validators import validate_phone
from .validators import validate_email
from django.utils import timezone
from model_utils.models import TimeStampedModel
# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, user_id, name, email,address,eName1,eName2,postcode,detailAdress,birthday, password=None):
        if not name:
            raise ValueError("must have user name")
        if not user_id:
            raise ValueError("must have user_id")
        if not email:
            raise ValueError('must have email')
        user = self.model(
            name=name,
            user_id=user_id,
            address=address,
            eName1=eName1,
            eNaem2=eName2,
            postcode=postcode,
            detailAdress=detailAdress,
            birthday=birthday,
            email=email
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, user_id, name,email,address,eName1,eName2,postcode,detailAddress,birthday, password):
        user= self.create_user(
            user_id = user_id,
            password=password,
            name=name,
            email=email,
            address=address,
            eName1=eName1,
            eName2=eName2,
            birthday=birthday,
            postcode=postcode,
            detailAdress=detailAddress
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(user=self._db)
        return user

    @property
    def is_staff(self):
        return self.is_admin
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return self.is_admin

GENDER_CHOICES = (
        ('MEN', '남자'),
        ('WOMEN', '여자')
    )

class Account(AbstractBaseUser):
    id= None
    user_id = models.CharField(max_length=20, verbose_name='아이디', unique=True,default='', validators=[validate_id])
    name = models.CharField(max_length=10, verbose_name="이름",default='')
    # phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone = models.CharField(validators=[validate_phone], max_length=11, unique=True, null=True,verbose_name="전화번호")
    email = models.EmailField(unique=True,max_length=128, validators=[validate_email])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="성별")
    postcode=models.CharField(max_length=10,verbose_name='우편번호')
    detailAddress=models.CharField(max_length=100,verbose_name='자세한 주소')
    address = models.CharField(verbose_name = "주소", max_length=128)
    eName1 = models.CharField(max_length=20, verbose_name="영어 첫번째 이름")
    eName2 = models.CharField(max_length=20, verbose_name="영어 마지막 이름")
    birthday = models.CharField(null=True, max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELD = ['name','phone','email','gender','postcode','detailAddress','address','eName1','eName1','birthday',]


    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "UserAccounts"
        verbose_name = "accounts"

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
