from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from articleapp.decorators import article_ownership_required
from articleapp.forms import ArticleCreationForm
from articleapp.models import Article




# 게시글 작성할 때는 로그인만 해도 가능하게
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    # success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'articleapp/create.html'

    # ????? 뭐가 문제? writer id 가 자동생성이 안 된다고?
    def form_valid(self, form):
        # 검증 완료된 form의 instance에 접근해서 user를 wirter 에 할당
        form.instance.writer = self.request.user
        return super().form_valid(form)
    # 뭐 지우셨는데....
    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk':self.object.pk})


# 모두가 볼 수 있도록 인증과정 없음
class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'target_article'
    template_name = 'articleapp/detail.html'


# 게시글 작성자만 가능하도록
@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleCreationForm
    context_object_name = 'target_article'
    template_name = 'articleapp/update.html'


    # object == target_article 같다고 봐도 됨
    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk':self.object.pk})


@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleDeleteView(DeleteView):
    model = Article
    context_object_name = 'target_article'
    success_url = reverse_lazy('articleapp:list')
    template_name = 'articleapp/delete.html'

class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articleapp/list.html'
    paginate_by = 1