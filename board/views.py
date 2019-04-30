from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Ad


class IndexView(generic.ListView):
    template_name = 'board/ad_list.html'
    context_object_name = 'latest_ad_list'
    paginate_by = 10

    def get_queryset(self):
        value = self.request.GET.get('filter', '')
        query = Ad.objects.filter(deleted=False).order_by('-created_at')
        if value == '':
            return query
        else:
            return query.filter(Q(ad_text__contains=value) | Q(title__contains=value))

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


class DetailView(generic.DetailView):
    model = Ad
    template_name = 'board/ad_detail.html'

    def get_object(self, queryset=None):
        ad = super(DetailView, self).get_object()
        if ad.deleted:
            raise Http404
        return ad

    def get(self, request, *args, **kwargs):
        ad = super(DetailView, self).get_object()
        ad_cookie_name = 'viewed_ad_%s' % ad.id
        if not request.session.get(ad_cookie_name, None):
            ad.view_count += 1
            ad.save()
            request.session[ad_cookie_name] = True
        return super().get(request, *args, **kwargs)


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    template_name = 'board/ad_create.html'
    fields = ('title', 'ad_text')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AdCreateView, self).form_valid(form=form)

    def get_success_url(self):
        return reverse('profile')


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    template_name = 'board/ad_update.html'
    fields = ('title', 'ad_text')

    def get_object(self, queryset=None):
        ad = super(AdUpdateView, self).get_object()
        if ad.author != self.request.user:
            raise Http404
        return ad

    def get_success_url(self):
        return reverse('board:detail', kwargs={'pk': self.object.id})


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'board/ad_confirm_delete.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        ad = super(AdDeleteView, self).get_object()
        if ad.author != self.request.user:
            raise Http404
        return ad

    def delete(self, request, *args, **kwargs):
        self.ad = self.get_object()
        self.ad.deleted = True
        self.ad.save()
        return HttpResponseRedirect(reverse('profile'))


@login_required
def special(request):
    return HttpResponse('You are logged in ! (%s)' % request.user.username)
