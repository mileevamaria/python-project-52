from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


def test_error(request):
    """Trigger a test error for Rollbar."""
    a = None
    # This will raise AttributeError for testing purposes
    a.hello()  # type: ignore
    return HttpResponse("This will not be reached")
