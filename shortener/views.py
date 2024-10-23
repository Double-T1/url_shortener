from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms.shortener_form import ShortenedUrlForm
from .models import ShortenedUrl
from .utils.shortener import generate_short_code, get_host


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
    host = get_host(request)
    form = ShortenedUrlForm()
    return render(request, "shortener/index.html", {"form": form, "host": host})


# show existing matching short_url
# if the inserted url clashes => tell them no when checked box
# if no short_url => create one
#
def shorten(request):
    form = ShortenedUrlForm(request.GET)
    host = get_host(request)
    if form.is_valid():
        short_code = form.cleaned_data.get("short_code", "")
        if not short_code:
            short_code = generate_short_code()
        print(short_code)
        return render(
            request,
            "shortener/_short_url.html",
            {"short_code_value": short_code, "host": host},
        )
    messages.error(request, "輸入資料錯誤，請重新輸入")
    return render(request, "shortener/_short_url.html", {"host": host})


def redirect_url(request, short_code):
    # original_url =
    # return redirect(original_url)
    # what happens if the short_url doesn't eixst?
    if ShortenedUrl.has_short_code(short_code):
        original_url = ShortenedUrl.objects.get(short_code=short_code).original_url
        return redirect(original_url)

    messages.error(request, "您輸入短網址並不存在")
    return redirect("shortener:index")
