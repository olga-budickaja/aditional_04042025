from django import forms

from main.models import Comment

def valid_min_length(value):
    if len(value) < 3:
        raise forms.ValidationError("Мінімальна довжина коментарію 3 символи!")

def valid_max_length(value):
    if len(value) < 5000:
        raise forms.ValidationError("Максимальна довжина коментарію 5000 символи!")

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            "text": forms.Textarea({
                "class": "form-control",
                "placeholder": "Введіть текст...",
                "validators": [
                    valid_min_length, valid_max_length
                ]
                }),
        }
