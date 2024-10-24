import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms.shortener_form import ShortenedUrlForm
from .models import ShortenedUrl
from .utils.shortener import generate_short_code, get_host, url_is_valid


def index(request):
    if request.method == "POST":
        # update or create
        # check if short_url exists yet, if not, create one for it

        # has short_url
        # create or update if
        is_checked = request.POST.get("is_checked", False)
        form = ShortenedUrlForm(request.POST)
        form_status = form.is_valid()
        if is_checked == "true":
            if form_status:
                # better way of writing this logic
                if form.cleaned_data.get("short_code", "") == "":
                    return render(
                        request, "shortener/index.html", {"form": form, "host": host}
                    )
                form.save()
                messages.success(request, "輸入成功，短網址已啟用")
            else:
                messages.error(request, "輸入資料錯誤，請重新輸入")
        else:
            print("here")
            print(form.errors)
            if form_status:
                print("aloha")
                url = form.save(commit=False)
                url.published = False
                url.save()
                messages.success(request, "已停用該短網址")

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
        url = ShortenedUrl.objects.get(short_code=short_code)
        if url.published:
            return redirect(url.original_url)

    messages.error(request, "您輸入短網址並不存在")
    return redirect("shortener:index")


def info(request):
    url = request.GET.get("original_url", "")
    if not url_is_valid(url):
        return HttpResponse("無效連結，請重新嘗試")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else "無標題"
        description = "無相關描述"
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag:
            description = description_tag.get("content", "無相關描述")
        else:
            og_description_tag = soup.find("meta", attrs={"property": "og:description"})
            if og_description_tag:
                description = og_description_tag.get("content", "無相關描述")
        return render(
            request,
            "shortener/_info_area.html",
            {"title": title, "description": description},
        )
    except requests.RequestException:
        return HttpResponse("無效連結，請重新嘗試")
