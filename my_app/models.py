from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class News(models.Model):
    title  = models.CharField(max_length=150,verbose_name="Заголовок")
    slug = models.SlugField(max_length=150,unique=True,verbose_name="URL")
    content  = models.TextField(blank=True,verbose_name="Контекст")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата Создания")
    update_at = models.DateTimeField(auto_now=True,verbose_name="Дата обновления")
    #ниже указываем поле в котрым мы будем хранить только изображения, которые будут добавлены
    #в каталог в соответсвии со временем
    photo = models.ImageField(upload_to="photos/%Y/%m/%d",blank=True,verbose_name="Фото",null=True)
    is_published = models.BooleanField(default=True,verbose_name="Опубликовано")
    category = models.ForeignKey("Category",on_delete=models.PROTECT,null=True,verbose_name="Категория")
    views = models.IntegerField(default=0)
    user = models.ForeignKey(User,verbose_name="Пользователь",on_delete=models.CASCADE,blank=True,null=True)


    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("news",kwargs={"slug_news":self.slug})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "новости"
        ordering = ["created_at"]

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True,verbose_name="URL")

    def __str__(self):
        return f"{self.category_name}"

    def get_absolute_url(self):
        return reverse("category",kwargs={"slug_category":self.slug})


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]

