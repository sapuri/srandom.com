from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404, HttpRequest
from google.cloud import storage


@login_required
def download(request: HttpRequest, file_type: str) -> HttpResponse:
    """
    ファイルダウンロード
    :param request:
    :param file_type: ダウンロードするファイルの種類
    """

    if file_type == 'csv':
        if request.user.premium:
            env = getattr(settings, 'ENV', None)
            if env is None:
                raise Exception('failed to read env')

            try:
                bucket = storage.Client().bucket(env('GCP_INTERNAL_BUCKET'))
                blob = bucket.blob(f'csv/export/{request.user.username}.csv')
                response = HttpResponse(blob.download_as_string(), content_type='text/csv; charset=utf-8')
            except FileNotFoundError:
                raise Http404
            except Exception as e:
                raise Exception(f'failed to download CSV: {e}')

            response['Content-Disposition'] = f'attachment; filename={request.user.username}.csv'
        else:
            raise PermissionDenied
        return response
    else:
        raise Http404
