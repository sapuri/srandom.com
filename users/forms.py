from django import forms
from django.forms.fields import CharField, ChoiceField, EmailField
from django.forms.models import ModelChoiceField
from django.forms.widgets import Select, RadioSelect, Textarea
from django.core.validators import RegexValidator

from .models import *

class CustomUserForm(forms.ModelForm):
    player_name = CharField(
        label='プレイヤー名',
        help_text='全角ひらがなカタカナ英数字6文字以内',
        widget=forms.TextInput(attrs={'placeholder': 'なまえ'}),
        max_length=6,
        validators=[RegexValidator('^[a-zA-Zａ-ｚＡ-Ｚ0-9０-９ぁ-んァ-ヴー]+$')],
        required=False
    )
    poputomo_id = CharField(
        label='ポプともID',
        help_text='半角数字12文字',
        max_length=12,
        min_length=12,
        widget=forms.TextInput(attrs={'placeholder': '111122223333'}),
        validators=[RegexValidator('^[0-9]+$')],
        required=False
    )
    email = EmailField(
        label='メールアドレス',
        help_text='重要な連絡をする場合に使用します (公開されません)',
        widget=forms.TextInput(attrs={'placeholder': 'abc@example.com'}),
        required=False
    )
    location = ModelChoiceField(
        label='都道府県',
        queryset=Location.objects.all(),
        widget=Select,
        empty_label='---選択---',
        required=False
    )
    profile = CharField(
        label='プロフィール',
        widget=Textarea(attrs={'placeholder': 'ポップン楽しい！'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ('player_name', 'poputomo_id', 'email', 'location', 'profile')

class PrivacyForm(forms.ModelForm):
    PRIVACY_CHOICES = (
        (1, '公開する'),
        (2, '公開しない'),
    )

    player_name_privacy = ChoiceField(label='プレイヤー名', help_text='ランキングにプレイヤー名とプロフィールページへのリンクが掲載されます。(非公開の場合は"匿名希望さん"と表示されます)', widget=RadioSelect, choices=PRIVACY_CHOICES)
    cleardata_privacy = ChoiceField(label='クリアデータ', help_text='プロフィールページにクリアデータを表示します。', widget=RadioSelect, choices=PRIVACY_CHOICES)
    updated_recently_privacy = ChoiceField(label='最近更新した曲', help_text='プロフィールページに最近更新した曲を表示します。', widget=RadioSelect, choices=PRIVACY_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('player_name_privacy', 'cleardata_privacy', 'updated_recently_privacy')

class ThemeForm(forms.ModelForm):
    theme = ModelChoiceField(
        label='テーマ',
        queryset=Theme.objects.all(),
        widget=Select,
        initial=1
    )

    class Meta:
        model = CustomUser
        fields = ('theme',)
