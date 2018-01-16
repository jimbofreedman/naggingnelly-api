import json
from django.http import HttpResponse
from django.template import loader
from django.db.models import QuerySet, Count
from .models import Scent
from .models import TestResult


def index(request):
    template = loader.get_template('smelltest/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def data(request):
    scents = Scent.objects.order_by('id')
    test_results = TestResult.objects.values('scent', 'guess').annotate(Count('scent'))

    ret = {
        'nodes': [{
            'name': s.name,
            'group': 1,
            'testCount': s.tests.count()
        } for s in scents],
        'links': [{
            'source': r['scent'] - 1,  # 0-index array vs 1-index table PK
            'target': r['guess'] - 1,
            'value': r['scent__count']
        } for r in test_results]
    }

    return HttpResponse(json.dumps(ret), content_type="application/json")
