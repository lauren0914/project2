from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from articleapp.models import Article
from likeapp.models import LikeRecord


@transaction.atomic
def db_transaction(user, article):
    likeRecord = LikeRecord.objects.filter(user=user,
                                           article=article)

    if likeRecord.exists():
        # 좋아요 반영 X
        # django.contrib
        # ValidationError : 장고에 있는 에러 클래스. 데이터를 검증하면서 생긴 에러가 발생했을 때
        raise ValidationError('like already exists')
        #                     request, messages level, 보여줄 문구
    else:
        LikeRecord(user=user, article=article).save()
        article.like += 1
        # 실제 DB에 반영
        article.save()


@method_decorator(login_required, 'get')
class LikeArticleView(RedirectView):

    def get(self, request, *args, **kwargs):
        # 어떤 user가 요청을 보냈는지, 어떤 게시글에 좋아요를 눌렀는지
        user = request.user
        article = Article.objects.get(pk=kwargs['article_pk'])

        try:
            db_transaction(user, article)
            # 좋아요 반영 O 메세지 출력
            messages.add_message(request, messages.SUCCESS, '좋아요가 반영되었습니다')

        except ValidationError:
            messages.add_message(request, messages.ERROR, '좋아요는 한 번만 가능합니다.')
            return HttpResponseRedirect(reverse('articleapp:detail', kwargs={'pk': kwargs['article_pk']}))

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('articleapp:detail', kwargs={'pk' : kwargs['article_pk']})