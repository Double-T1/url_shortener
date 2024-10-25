from django import forms
from django.db.models import Q

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
                    "@input": "clearCheckBox()",
                }
            ),
        }

    def clean_short_code(self):
        original_url = self.cleaned_data.get("original_url", "")
        short_code = self.cleaned_data.get("short_code", "")

        if not short_code or short_code.strip() == "":
            raise forms.ValidationError("短網址不能空白")

        if ShortenedUrl.objects.filter(
            Q(short_code=short_code) & (~Q(original_url=original_url))
        ).exists():
            raise forms.ValidationError("此短網址已被使用，請輸入其他")

        return short_code
