import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from news.forms import CommentForm


HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(news_set, client):
    """Количество новостей на главной странице — не более 10."""
    # Загружаем главную страницу.
    response = client.get(HOME_URL)
    # Код ответа не проверяем, его уже проверили в тестах маршрутов.
    # Получаем список объектов из словаря контекста.
    object_list = response.context['object_list']
    # Определяем количество записей в списке.
    news_count = object_list.count()
    # Проверяем, что на странице именно 10 новостей.
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


    # def test_news_order(self):
    #     response = self.client.get(self.HOME_URL)
    #     object_list = response.context['object_list']
    #     # Получаем даты новостей в том порядке, как они выведены на странице.
    #     all_dates = [news.date for news in object_list]
    #     # Сортируем полученный список по убыванию.
    #     sorted_dates = sorted(all_dates, reverse=True)
    #     # Проверяем, что исходный список был отсортирован правильно.
    #     self.assertEqual(all_dates, sorted_dates)
# # В тесте используем фикстуру заметки
# # и фикстуру клиента с автором заметки.
# def test_note_in_list_for_author(note, author_client):
#     url = reverse('notes:list')
#     # Запрашиваем страницу со списком заметок:
#     response = author_client.get(url)
#     # Получаем список объектов из контекста:
#     object_list = response.context['object_list']
#     # Проверяем, что заметка находится в этом списке:
#     assert note in object_list


# # В этом тесте тоже используем фикстуру заметки,
# # но в качестве клиента используем not_author_client;
# # в этом клиенте авторизован не автор заметки, 
# # так что заметка не должна быть ему видна.
# def test_note_not_in_list_for_another_user(note, not_author_client):
#     url = reverse('notes:list')
#     response = not_author_client.get(url)
#     object_list = response.context['object_list']
#     # Проверяем, что заметки нет в контексте страницы:
#     assert note not in object_list


# @pytest.mark.parametrize(
#     # Задаём названия для параметров:
#     'parametrized_client, note_in_list',
#     (
#         # Передаём фикстуры в параметры при помощи "ленивых фикстур":
#         (pytest.lazy_fixture('author_client'), True),
#         (pytest.lazy_fixture('not_author_client'), False),
#     )
# )
# def test_notes_list_for_different_users(
#         # Используем фикстуру заметки и параметры из декоратора:
#         note, parametrized_client, note_in_list
# ):
#     url = reverse('notes:list')
#     # Выполняем запрос от имени параметризованного клиента:
#     response = parametrized_client.get(url)
#     object_list = response.context['object_list']
#     # Проверяем истинность утверждения "заметка есть в списке":
#     assert (note in object_list) is note_in_list


# def test_create_note_page_contains_form(author_client):
#     url = reverse('notes:add')
#     # Запрашиваем страницу создания заметки:
#     response = author_client.get(url)
#     # Проверяем, есть ли объект form в словаре контекста:
#     assert 'form' in response.context
#     # Проверяем, что объект формы относится к нужному классу.
#     assert isinstance(response.context['form'], NoteForm)


# # В параметры теста передаём фикстуру slug_for_args и клиент с автором заметки:
# def test_edit_note_page_contains_form(slug_for_args, author_client):
#     url = reverse('notes:edit', args=slug_for_args)
#     # Запрашиваем страницу редактирования заметки:
#     response = author_client.get(url)
#     # Проверяем, есть ли объект form в словаре контекста:
#     assert 'form' in response.context
#     # Проверяем, что объект формы относится к нужному классу.
#     assert isinstance(response.context['form'], NoteForm)


# @pytest.mark.parametrize(
#     # В качестве параметров передаём name и args для reverse.
#     'name, args',
#     (
#         # Для тестирования страницы создания заметки 
#         # никакие дополнительные аргументы для reverse() не нужны.
#         ('notes:add', None),
#         # Для тестирования страницы редактирования заметки нужен slug заметки.
#         ('notes:edit', pytest.lazy_fixture('slug_for_args'))
#     )
# )
# def test_pages_contains_form(author_client, name, args):
#     # Формируем URL.
#     url = reverse(name, args=args)
#     # Запрашиваем нужную страницу:
#     response = author_client.get(url)
#     # Проверяем, есть ли объект формы в словаре контекста:
#     assert 'form' in response.context
#     # Проверяем, что объект формы относится к нужному классу.
#     assert isinstance(response.context['form'], NoteForm)
