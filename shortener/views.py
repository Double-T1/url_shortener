from ast import parse
from operator import is_

import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms.shortener_form import ShortenedUrlForm
from .models import ShortenedUrl
from .utils.shortener import (
    generate_short_code,
    get_host,
    parse_form_errors,
    url_is_valid,
)


def index(request):
    if request.method == "POST":
        is_checked = request.POST.get("is_checked", False) == "true"
        ShortenedUrl.objects.filter()
        form = ShortenedUrlForm(request.POST)
        form_status = form.is_valid()
        if form_status:
            short_code = form.cleaned_data.get("short_code")
            if ShortenedUrl.has_short_code(short_code):
                instance = ShortenedUrl.objects.get(short_code=short_code)
                instance.published = is_checked
                instance.save()
            else:
                form.save()

            messages.success(
                request, "輸入成功，短網址已啟用" if is_checked else "已停用該短網址"
            )
        else:
            errors = parse_form_errors(form)
            for error in errors:
                messages.error(request, error)

        return render(request, "shortener/_message.html")

    host = get_host(request)
    form = ShortenedUrlForm()
    return render(request, "shortener/index.html", {"form": form, "host": host})


def shorten(request):
    host = get_host(request)
    short_code = generate_short_code()
    return render(
        request,
        "shortener/_short_url.html",
        {"short_code_value": short_code, "host": host},
    )


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
