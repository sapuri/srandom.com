from django import forms
from django.forms.fields import BooleanField, ChoiceField, IntegerField
from django.forms.models import ModelChoiceField
from django.forms.widgets import Select

from .models import Sran_Level, Medal, Bad_Count, Extra_Option

MEDAL_CHOICES = (
    (1, 'パーフェクト'),
    (2, 'フルコンボ ☆'),
    (3, 'フルコンボ ◇'),
    (4, 'フルコンボ ◯'),
    (5, 'クリア ☆'),
    (6, 'クリア ◇'),
    (7, 'クリア ◯'),
    (8, '未クリア ☆'),
    (9, '未クリア ◇'),
    (10, '未クリア ◯'),
    (11, 'イージー'),
    (12, '未プレイ')
)


class Sran_LevelForm(forms.ModelForm):
    sran_level_from = ModelChoiceField(
        label='S乱レベル (〜から)',
        queryset=Sran_Level.objects.all(),
        widget=Select,
        empty_label='---選択---',
        required=False
    )
    sran_level_to = ModelChoiceField(
        label='S乱レベル (〜まで)',
        queryset=Sran_Level.objects.all(),
        widget=Select,
        empty_label='---選択---',
        required=False
    )

    class Meta:
        model = Sran_Level
        fields = ('sran_level_from', 'sran_level_to')


class MedalForm(forms.ModelForm):
    medal = ChoiceField(label='クリアメダル', widget=Select,
                        choices=MEDAL_CHOICES, required=True)

    class Meta:
        model = Medal
        fields = ('medal',)


class Bad_CountForm(forms.ModelForm):
    bad_count = IntegerField(label='BAD数', min_value=0,
                             max_value=200, required=False)

    class Meta:
        model = Bad_Count
        fields = ('bad_count',)


class Extra_OptionForm(forms.ModelForm):
    hard = BooleanField(label='ハード', required=False)

    class Meta:
        model = Extra_Option
        fields = ('hard',)


class SearchForm(forms.Form):
    ''' 検索フォーム '''
    q = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"placeholder": "曲名で検索"}), required=False)
