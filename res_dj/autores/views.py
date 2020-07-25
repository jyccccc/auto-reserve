from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def get_res(request):
    ctx = {}
    if(request.POST):
        for k in request.POST:
            ctx[k] = request.POST[k]
    print(ctx)
    return HttpResponse(ctx)

# default page
def default_page(request):
    return render(request,'index.html')


# hello world v1
def hello(request):
    return HttpResponse("hello world!")


# hello world v2
def hello2(request):
    context = {}  # 上下文信息
    context['hello'] = 'hello world'
    return render(request,'hello.html',context)