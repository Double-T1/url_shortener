from django import forms

from ..models import ShortenedUrl


class ShortenedUrlForm(forms.ModelForm):
    class Meta:
        model = ShortenedUrl
        fields = ["original_url", "short_code"]
        widgets = {
            "original_url": forms.URLInput(
                attrs={
                    "placeholder": "請輸入或貼上完整網址",
                    "required": "true",
                    "class": "input input-bordered rounded-none bg-white w-full",
                    "name": "url",
                }
            ),
        }
