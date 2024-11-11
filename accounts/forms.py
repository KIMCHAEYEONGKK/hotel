from django import forms
from django.contrib.auth.models import User
from . import models
from accounts.models import Account
from accounts.validators import CustomPasswordValidator


class SignupForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('MEN', '남자'),
        ('WOMEN', '여자')
    )
    name = forms.CharField(max_length=10, label='이름', required=True)
    user_id = forms.CharField(max_length =20, label='아이디', required =True)
    gender = forms.ChoiceField(label="성별", widget=forms.Select(), choices=GENDER_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput,
                               validators =[CustomPasswordValidator()])
    password1 = forms.CharField(widget=forms.PasswordInput,
                                validators=[CustomPasswordValidator()])
    email = forms.EmailField(max_length=128, required=True,)
    postcode = forms.CharField(max_length=10, required=True, label="우편번호")
    detailAddress = forms.CharField(max_length=100, required=True, label="자세한 주소")

    address=forms.CharField(label='주소',required=True,max_length=128)
    eName1 = forms.CharField(max_length=20, label="첫번째 영어 이름", required=True)
    eName2 = forms.CharField(max_length=20, label="두번째 영어 이름", required=True)
    birthday = forms.CharField(label="생일", required=True)
    phone=forms.CharField(label='전화번호',required=True)


    class Meta:
        model = Account
        fields = ("user_id", "name", "password", "password1",'gender','email','birthday','postcode','detailAddress','address','eName1','eName2',"phone")

    def clean_password1(self):
        min_length=8
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        if len(password) < min_length:
            raise forms.ValidationError("비밀번호를 최소 8자리 이상으로 해주세요.")
        if password != password1:
            raise forms.ValidationError("비밀번호가 서로 다릅니다.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("최소 1자리 이상의 숫자를 포함해주세요.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("최소 1자리 이상의 알파벳을 포함해주세요.")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            models.Account.objects.get(email=email)
            raise forms.ValidationError('이미 사용중인 이메일 입니다.')
        except models.Account.DoesNotExist:
            return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),
        error_messages={'required': '아이디을 입력해주세요.'},
        label='아이디'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', }),
        error_messages={'required': '비밀번호를 입력해주세요.'},
        label='비밀번호'
    )

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError("Passwords don't match")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            try:
                user = Account.objects.get(user_id=user_id)
            except User.DoesNotExist:
                self.add_error('username', '아이디가 존재하지 않습니다.')
                return

            from django.contrib.auth.hashers import check_password
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')

    def clean(self):
        user_id = self.cleaned_data.get("user_id")
        password = self.cleaned_data.get("password")
        try:
            user = models.Account.objects.get(user_id=user_id)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("잘못된 비밀번호입니다."))

        except models.Account.DoesNotExist:
            self.add_error("user_id", forms.ValidationError("계정이 존재하지 않습니다."))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     user_id = cleaned_data.get('user_id')
    #     password = cleaned_data.get('password')
    #
    #     if user_id and password:
    #         try:
    #             account = Account.objects.get(user_id=user_id)
    #         except Account.DoesNotExist:
    #             self.add_error('user_id', '아이디가 존재하지 않습니다.')
    #             return
    #
    #         from django.contrib.auth.hashers import check_password
    #         if not check_password(password, account.password):
    #             self.add_error('password', '비밀번호가 틀렸습니다.')


