from .forms import UpdateListForm
from django.views.generic.edit import FormView

class UpdateListView(FormView):
    template_name = 'friendtrack/update_list.html'
    form_class = UpdateListForm
    success_url = '/friendtrack/update'

    def form_valid(self, form):
        form.update_from_json(owner=self.request.user)
        return super().form_valid(form)
