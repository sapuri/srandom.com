import zenhan
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.forms import CustomUserForm, PrivacyForm, ThemeForm


@login_required
def settings(request):
    """ 設定 """
    user = request.user

    # フォームの読み込み
    custom_user_form = CustomUserForm(instance=user)
    privacy_form = PrivacyForm(instance=user)
    theme_form = ThemeForm(instance=user)

    # POSTでアクセスされた場合
    if request.method == 'POST':
        if 'account' in request.POST:
            custom_user_form = CustomUserForm(request.POST, instance=user)

            if custom_user_form.is_valid():
                if custom_user_form.has_changed():
                    # 保存処理
                    if request.POST['player_name']:
                        custom_user = custom_user_form.save(commit=False)  # 後でまとめて保存
                        # 全角大文字に変換
                        custom_user.player_name = zenhan.h2z(request.POST['player_name']).upper()
                        custom_user.save()  # 保存
                    if request.POST['poputomo_id']:
                        custom_user = custom_user_form.save(commit=False)  # 後でまとめて保存
                        # 文字列に変換
                        custom_user.poputomo_id = str(request.POST['poputomo_id'])
                        custom_user.save()  # 保存
                    else:
                        custom_user_form.save()

        elif 'privacy' in request.POST:
            privacy_form = PrivacyForm(request.POST, instance=user)

            if privacy_form.is_valid() and privacy_form.has_changed():
                privacy_form.save()

        elif 'themes' in request.POST:
            theme_form = ThemeForm(request.POST, instance=user)

            if theme_form.is_valid() and theme_form.has_changed():
                theme_form.save()

        # メッセージを表示
        msg = '設定を更新しました！'
        messages.success(request, msg)

    context = {
        'custom_user_form': custom_user_form,
        'privacy_form': privacy_form,
        'theme_form': theme_form
    }
    return render(request, 'users/settings.html', context)
