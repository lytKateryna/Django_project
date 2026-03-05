from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse(
        '<h1>Hello Kateryna!</h1>'
    )

def homepage(request):
    return HttpResponse(
        '<h1>My Homepage!!!</h1>'
    )