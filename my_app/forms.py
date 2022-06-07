from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
import re


class Contact_Us(forms.Form):
    subject = forms.CharField(label='Тема',widget=forms.TextInput(attrs={'class': "form-control"}))
    content = forms.CharField(label='Контент',widget=forms.Textarea(attrs={'class': "form-control","raws":5}))
    captcha = CaptchaField()


class AuthenticateLoginUser(AuthenticationForm):
    username = forms.CharField(label='Введите имя пользователя',widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(label='Введите пароль',widget=forms.PasswordInput(attrs={'class':"form-control"}))


class RegisterUser(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=150,label="Email",widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Подтверждение пароля',widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']




class NewsForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["category"].empty_label = "выберите категорию"


    class Meta:
        model = News
        fields = ["title","content","photo","is_published","category"]
        widgets = {
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "content":forms.Textarea(attrs={"class":"form-control",
                                           "rows":5}),
            "category":forms.Select(attrs={"class":"form-control"})
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if re.match(r"\d",title):
            raise ValidationError("В заголовке не может быть цифр")
        return title

    def clean_is_published(self):
        is_published = self.cleaned_data["is_published"]
        if is_published:
            return is_published
        raise ValidationError("Отметка опубликованно являеться обьязательной")

