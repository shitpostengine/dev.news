from django.shortcuts import render
from myapp1.models import Worker, Parser


def index_page(request):
    sites = Parser.objects.all()
    print(sites)
    return render(request, 'index.html')