from django.db.models import Subquery, OuterRef
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from fileman.models import File, Log
from fileman.forms import UpdateFileForm


class FileListView(LoginRequiredMixin, ListView):
    context_object_name = 'file_list'
    template_name = 'file_list.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        last_log_qs = Log.objects.filter(file=OuterRef('pk')).order_by('-created')

        return File.objects.filter(
            created_by=self.request.user
        ).annotate(
            last_log=Subquery(last_log_qs.values('status')[:1])
        )


class CreateFileView(LoginRequiredMixin, CreateView):
    form_class = UpdateFileForm
    template_name = 'new_file.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('file_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
