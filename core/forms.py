from django import forms

class YoutubeDownloadForm(forms.Form):
    url = forms.URLField(label="URL do vídeo", max_length=200, widget=forms.URLInput(attrs={
        "class": "form-controls",
        "placeholder": "Insíra a URL do vídeo, porra!"
    }))