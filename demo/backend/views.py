from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .algorithm.searchByName import searchByName
from .algorithm.eventDetection import eventDetection
from .algorithm.getGraph import getGraph


@csrf_exempt    # 声明视图可以跨域访问
def search(request):
    response = HttpResponse()
    name = request.POST['name']
    searchResult = searchByName(name)
    response.write(searchResult)
    return response


@csrf_exempt    # 声明视图可以跨域访问
def detect(request):
    response = HttpResponse()
    text = request.POST['text']
    edResult = eventDetection(text)
    response.write(edResult)
    return response


@csrf_exempt
def graph(request):
    response = HttpResponse()
    graph_id = request.POST['id']
    graphResult = getGraph(graph_id)
    response.write(graphResult)
    return response
