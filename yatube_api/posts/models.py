from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import Truncator

from posts.constants import (MAX_TITLE_DISPLAY_LENGTH,
                             MAX_POST_DISPLAY_LENGTH,
                             MAX_COMMENT_POST_TEXT_LENGTH,
                             MAX_COMMENT_DISPLAY_LENGTH)

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание группы')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return Truncator(self.title).chars(MAX_TITLE_DISPLAY_LENGTH)


class Post(models.Model):
    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Группа"
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return Truncator(self.text).chars(MAX_POST_DISPLAY_LENGTH)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Пост"
    )
    text = models.TextField('Текст комментария', max_length=300)
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)
        default_related_name = 'comments'

    def __str__(self):
        post_text = Truncator(self.post.text).chars(
            MAX_COMMENT_POST_TEXT_LENGTH
        )
        comment_text = Truncator(self.text).chars(
            MAX_COMMENT_DISPLAY_LENGTH
        )
        return (f'Комментарий {comment_text} к посту "{post_text}" '
                f'от {self.author}')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
