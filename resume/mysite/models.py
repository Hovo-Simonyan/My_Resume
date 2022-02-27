from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Resume(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    age = models.SmallIntegerField(verbose_name='Возраст')
    city = models.CharField(max_length=100, verbose_name='Место проживания')
    position = models.CharField(max_length=200, verbose_name='Желаемая должность ')

    email = models.EmailField(max_length=200, verbose_name='Email')
    facebook = models.URLField(max_length=200, blank=True, verbose_name='Facebook-сылка')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Телеграм')
    phone_number = models.CharField(max_length=200, verbose_name='Телефон', blank=True)

    content = RichTextField(verbose_name='Биография опыт работы и.т.д')

    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    view = models.PositiveIntegerField(default=0)

    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.PROTECT, verbose_name='Основной язык программирования')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('read_more', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-time_update', 'name']


class Language(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название языка')
    photo_language = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('published_resume_by_languages', kwargs={'lang_slug': self.slug})

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'
        ordering = ['id']
