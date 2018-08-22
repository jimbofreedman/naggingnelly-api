from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.template import loader

from .forms import UpdateListForm
from .models import Friend, Category


class UpdateListView(FormView):
    template_name = 'friendtrack/update_list.html'
    form_class = UpdateListForm
    success_url = '/friendtrack/update'

    def form_valid(self, form):
        form.update_from_json(owner=self.request.user)
        return super().form_valid(form)



def categorize(request, friend_id, category_id):
    if friend_id is not None and category_id is not None:
        f = Friend.objects.get(id=friend_id)
        f.category_id = category_id
        f.save()

    friend = Friend.objects.filter(category__isnull=True).order_by('-added_at')[0]
    categories = Category.objects.all()
    template = loader.get_template('friendtrack/categorize.html')

    context = {
        'friend': friend,
        'categories': categories
    }

    return HttpResponse(template.render(context, request))


def list(request):
    categories = Category.objects.prefetch_related('friend_set').all()
    template = loader.get_template('friendtrack/list.html')

    context = {
        'categories': categories
    }

    return HttpResponse(template.render(context, request))
