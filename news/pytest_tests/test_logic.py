from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.parametrize(
    'parametrized_client, expected_comments_count',
    (
        (pytest.lazy_fixture('client'), 0),
        (pytest.lazy_fixture('author_client'), 1)
    ),
)
@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        parametrized_client, expected_comments_count,
        detail_url, comment_form_data
):
    """
    Анонимный пользователь не может отправить комментарий.
    Авторизованный пользователь может отправить комментарий.
    """
    # в POST-запросе отправляем
    # предварительно подготовленные данные формы с текстом комментария.
    parametrized_client.post(detail_url, data=comment_form_data)
    # Считаем количество комментариев.
    comments_count = Comment.objects.count()
    # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
    assert comments_count == expected_comments_count


def test_user_cant_use_bad_words(author_client, detail_url):
    """
    Если комментарий содержит запрещённые слова, он не будет опубликован,
    а форма вернёт ошибку.
    """
    # Формируем данные для отправки формы; текст включает
    # первое слово из списка стоп-слов.
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    # Отправляем запрос через авторизованный клиент.
    response = author_client.post(detail_url, data=bad_words_data)
    # Проверяем, есть ли в ответе ошибка формы.
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    # Дополнительно убедимся, что комментарий не был создан.
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.parametrize(
    'parametrized_client, expected_comments_count',
    (
        (
            pytest.lazy_fixture('not_author_client'),
            1,
        ),
        (
            pytest.lazy_fixture('author_client'),
            0,
        )
    ),
)
def test_possibility_to_delete_for_different_users(
        parametrized_client, comment_id,
        detail_url, expected_comments_count
):
    """
    Авторизованный пользователь может удалять свои комментарии.
    Авторизованный пользователь не может удалять чужие комментарии.
    """
    action_url = reverse('news:delete', args=comment_id)
    url_to_comments = detail_url + '#comments'
    response = parametrized_client.delete(action_url)
    # Проверяем, что редирект привёл к разделу с комментариями.
    # Заодно проверим статус-коды ответов.
    if response.status_code == HTTPStatus.FOUND:
        assertRedirects(response, url_to_comments)
    else:
        assert response.status_code == HTTPStatus.NOT_FOUND
    # Считаем количество комментариев в системе.
    comments_count = Comment.objects.count()
    assert comments_count == expected_comments_count


@pytest.mark.parametrize(
    'parametrized_client, expected_comment_text',
    (
        (
            pytest.lazy_fixture('not_author_client'),
            pytest.lazy_fixture('comment_text'),
        ),
        (
            pytest.lazy_fixture('author_client'),
            pytest.lazy_fixture('comment_new_text'),
        )
    ),
)
def test_possibility_to_edit_for_different_users(
        parametrized_client, comment_id, comment_form_data,
        detail_url, expected_comment_text
):
    """
    Авторизованный пользователь может редактировать свои комментарии.
    Авторизованный пользователь не может редактировать чужие комментарии.
    """
    action_url = reverse('news:edit', args=comment_id)
    url_to_comments = detail_url + '#comments'
    response = parametrized_client.post(action_url, data=comment_form_data)
    if response.status_code == HTTPStatus.FOUND:
        assertRedirects(response, url_to_comments)
    else:
        assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get()
    assert comment.text == expected_comment_text
