from text_api import settings

from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework import status
from text_service.models import BookChapter


def processing_get_chapter(request):
    chapter_id = request.query_params.get('chapter_id')

    if not chapter_id:
        return Response({'error': 'chapter_id is a required parameter'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        # Находим главу по ид (uuid) //поменять модель на id TODO
        chapter = BookChapter.objects.get(id=chapter_id)
    except BookChapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Загрузить содержимое текстового файла
    try:
        chapter_path = os.path.join(settings.MEDIA_ROOT, chapter.file_path.replace('/media/', ''))
        with open(chapter_path, 'r', encoding='utf-8') as f:
            chapter_text = f.read()
    except Exception as e:
        return Response({'error': f'Failed to load chapter text: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Возвращаем содержимое нашей главы
    return Response({'chapter_title': chapter.chapter_title, 'chapter_text': chapter_text},
                    status=status.HTTP_200_OK)
