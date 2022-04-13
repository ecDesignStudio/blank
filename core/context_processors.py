# import git
import re

from django import db
from django.conf import settings
from django.urls import resolve


def custom_context(request):
    url_name = resolve(request.path).view_name
    view_name = resolve(request.path_info).url_name or 'home'
    if ':' in url_name:
        app, view = url_name.split(":")
    else:
        app, view = '', ''

    # if request.user.is_superuser:
    #     git_repo = git.Repo(search_parent_directories=True)
    #     git_commit = git_repo.head.reference.commit
    # else:
    #     git_commit = None

    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)",
        re.IGNORECASE
    )
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        mobile = True
    else:
        mobile = False


    database_name = db.utils.settings.DATABASES['default']['NAME']

    debug_mode = settings.DEBUG

    context = {
        'url_name': url_name,
        'view_name': view_name,
        'show_admin': False,
        'database_name': database_name,
        'debug_mode': debug_mode,
        'mobile': mobile
        # 'git_commit'         : git_commit,
    }
    return context
