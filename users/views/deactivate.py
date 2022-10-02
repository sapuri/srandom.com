from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from main.models import Medal, Bad_Count, Extra_Option


@login_required
def deactivate(request):
    """
    アカウント削除
    """
    # 自ユーザーを取得
    myself = request.user

    # POSTでアクセスされた場合
    if request.method == 'POST':
        # クリアメダルを取得
        medal = Medal.objects.filter(user=myself)
        if medal:
            # メダルが存在すれば削除
            medal.delete()

        # BAD数を取得
        bad_count = Bad_Count.objects.filter(user=myself)
        if bad_count:
            # BAD数が存在すれば削除
            bad_count.delete()

        # エクストラオプションを取得
        extra_option = Extra_Option.objects.filter(user=myself)
        if extra_option:
            # エクストラオプションが存在すれば削除
            extra_option.delete()

        # アカウントを無効にする
        myself.is_active = False
        # 保存
        myself.save()

        # ログアウトページにリダイレクト
        return redirect('/auth/logout/?next=/')

    return render(request, 'users/deactivate.html')
