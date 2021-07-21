from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.forms import AccountCreationForm
from accountapp.models import HelloWorld

# url에서 마지막에 숫자가 계정을 의미하는데. 그러니까 그 숫자만 바꾸면 다른 계정으로 접근 가능. 이거를 막자!!
def hello_world(request):
    # 인증 과정 적어주기(다른 아이디에는 접근 안 되게). request 에는 요청에 대한 모든 정보가 들어있음. 누가 요청 보냈는지 객체. 가 들어있음
    # 이 요청을 보내는 user가 로그인이 되어있다면, 아래 과정을 실행시키고 아니라면~~ 아래에 작성.
    if request.user.is_authenticated:
        # return HttpResponse('Hello World!')
        if request.method == 'POST':
            temp = request.POST.get('input')

            new_data = HelloWorld()
            new_data.text = temp
            new_data.save()

            return HttpResponseRedirect(reverse('accountapp:hello_world'))

        else:
            data_list = HelloWorld.objects.all()
            return render(request, 'accountapp/hello_world.html',
                          context={'data_list': data_list})
    else:
        # redirect 해라. 어디로? reverse ~~
        # 이렇게 하면, 로그아웃 상태에서 hello_world로 가려고 하면 안 넘어가고 login 페이지로 감.
        # 이 인증과정을 어디에 추가해야할까? update, detail veiw에!
        return HttpResponseRedirect(reverse('accountapp:login'))

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'

class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountCreationForm
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'

    # def get(self, request, *args, **kwargs):
    #     # and : 이 user가 해당 페이지 주인이 맞는지 확인. self.get_object() self는 저 view 자체를 의미 -> target user를 가져오기
    #     if request.user.is_authenticated and self.get_object() == request.user:
    #         return super().get(request, *args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()
    #
    #     def post(self, request, *args, **kwargs):
    #         if request.user.is_authenticated and self.get_object() == request.user:
    #             return super().post(request, *args, **kwargs)  # 부모 메소드에서 pos 불러오기
    #         else:
    #             return HttpResponseForbidden()

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/delete.html'
    
    # def get(self, request, *args, **kwargs):
    #     # and : 이 user가 해당 페이지 주인이 맞는지 확인. self.get_object() self는 저 view 자체를 의미 -> target user를 가져오기
    #     if request.user.is_authenticated and self.get_object() == request.user:
    #         return super().get(request, *args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()
    #
    #     def post(self, request, *args, **kwargs):
    #         if request.user.is_authenticated and self.get_object() == request.user:
    #             return super().post(request, *args, **kwargs)  # 부모 메소드에서 pos 불러오기
    #         else:
    #             return HttpResponseForbidden()