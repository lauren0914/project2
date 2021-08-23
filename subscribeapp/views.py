from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, ListView

from articleapp.models import Article
from projectapp.models import Project
from subscribeapp.models import Subscription

@method_decorator(login_required, 'get')
class SubscriptionView(RedirectView):
    # get 요청을 처리해주는 http 머시기
    def get(self, request, *args, **kwargs):
        # user가 누구인지. 어떤 게시판의 구독정보를 요청했는지가 필요함
        user = request.user
        project = Project.objects.get(pk=kwargs['project_pk'])

        subscription = Subscription.objects.filter(user=user, project=project)
        # 구독돼있으면 구독취소
        if subscription.exists():
            subscription.delete()
        else:
            Subscription(user=user, project=project).save()
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('projectapp:detail', kwargs={'pk':kwargs['project_pk']})

@method_decorator(login_required, 'get')
class SubscriptionListView(ListView) :
    model = Article
    context_object_name = 'article_list'
    template_name = 'subscribeapp/list.html'
    paginate_by = 20

    def get_queryset(self):
        project_list = Subscription.objects.filter(user=self.request.user).values_list('project')
        article_list = Article.objects.filter(project__in=project_list)
        return article_list