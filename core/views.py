import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import YoutubeDownloadForm
import yt_dlp


def download_audio(request):
    if request.method == 'POST':
        form = YoutubeDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            output_folder = 'downloads'

            # Criar a pasta de downloads se não existir
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Configuração do yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            # Baixar o áudio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = f"{info['title']}.mp3"
                filepath = os.path.join(output_folder, filename)

            # Retornar o arquivo para download
            with open(filepath, 'rb') as f:
                response = HttpResponse(f.read(), content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            os.remove(filepath)
            return response

    else:
        form = YoutubeDownloadForm()

    return render(request, 'index.html', {'form': form})

