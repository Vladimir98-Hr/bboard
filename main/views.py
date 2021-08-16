from django.http import HttpResponse, Http404

from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature

from .models import AdvUser
from .forms import ChangeUserInfoForm
from .forms import RegisterUserForm
from .utilities import signer


def user_activate(request, sing):
    try:
        username = signer.unsign(sing)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser,username=username)
    if user.is_activate:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)





class RegisterDoneViwe(TemplateView):
    template_name = 'main/register_done.html'


class RegisterUserViwe(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')



class BBPasswordChangeView(PasswordChangeView, SuccessMessageMixin, LoginRequiredMixin):

    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменён'



class ChangeUserInfoViwe(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info_form.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self,request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)




class BBLogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'main/logout.html'


@login_required
def profile(request):
    return render(request,'main/profile.html')



class BBLoginView(LoginView):
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('main:index')

def other_page(request,page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

def index (request):
    return render(request, 'main/index.html')