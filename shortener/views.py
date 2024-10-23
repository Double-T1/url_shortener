from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms.shortener_form import ShortenedUrlForm
from .models import ShortenedUrl
from .utils.shortener import generate_short_url_hash


def index(request):
    if request.method == "POST":
        # update or create
        # check if short_url exists yet, if not, create one for it

        # has short_url
        # create or update if
        is_checked = request.POST.get("is_checked", False)
        if is_checked == "true":
            form = ShortenedUrlForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "輸入成功，短網址已啟用")
            else:
                messages.error(request, "輸入資料錯誤，請重新輸入")
        else:
            # disable the link
            pass
        return HttpResponse(status=204)
    form = ShortenedUrlForm()
    return render(request, "shortener/index.html", {"form": form})


# show existing matching short_url
# if the inserted url clashes => tell them no when checked box
# if no short_url => create one
#
def shorten(request):
    form = ShortenedUrlForm(request.GET)
    if form.is_valid():
        short_url = form.cleaned_data.get("short_url", "")
        if not short_url:
            short_url_hash = generate_short_url_hash()
            short_url = request.build_absolute_uri(
                reverse("shortener:redirect_url", args=[short_url_hash])
            )
        return render(
            request, "shortener/_short_url.html", {"short_url_value": short_url}
        )
    messages.error(request, "輸入資料錯誤，請重新輸入")
    return render(request, "shortener/_short_url.html")


def redirect_url(request, short_url):
    # original_url =
    # return redirect(original_url)
    # what happens if the short_url doesn't eixst?

    ShortenedUrl.objects.get(short_url=short_url)
    pass
