from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.db.models import Q

from board.models import Ad


def home(request):
    return redirect('board:index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')


class ProfileView(generic.ListView):
    template_name = 'accounts/profile.html'
    context_object_name = 'ad_list'
    # paginate_by = 3

    def get_queryset(self):
        return Ad.objects.filter(deleted=False, author=self.request.user).order_by('-created_at')

    def get_queryset(self):
        value = self.request.GET.get('filter', '')
        query = Ad.objects.filter(deleted=False, author=self.request.user).order_by('-created_at')
        if value == '':
            return query
        else:
            return query.filter(Q(ad_text__contains=value) | Q(title__contains=value))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context
