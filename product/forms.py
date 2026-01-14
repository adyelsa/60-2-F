from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ["title", "content", "image", "category"]

    def clean_title(self):

        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 5:

            raise forms.ValidationError("Заголовок должен быть минимум 5 символов.")
        
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if len(content) < 20:
            raise forms.ValidationError("Текст должен быть минимум 20 символов.")
        return content