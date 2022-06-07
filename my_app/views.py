from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView,CreateView
from .models import News,Category
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout
from .utils import MyMixin
from django.contrib import messages
from .forms import NewsForm,RegisterUser,AuthenticateLoginUser,Contact_Us
from .serializers import NewsSerializer
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import F
from .permissions import *



def contact_us(request):
    if request.method == 'POST':
        form = Contact_Us(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],form.cleaned_data['content'],
                      "i.ok.danko@gmail.com",["igordanko421@gmail.com",],fail_silently=True)
            if mail:
                messages.success(request,"Письмо успешно отправлено")
                return redirect("contact")
            else:
                messages.error(request,"Ошибка отправки письма")
    else:
        form = Contact_Us()
    return render(request, 'my_app/contact_us.html', {'form': form})


def user_register(request):
    print(type(request.session))
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Регистрация прошла успешно")
            return redirect('login')
        else:
            messages.error(request,"Не-удалось завершить регистрацию")
    else:
        form = RegisterUser()
    return render(request,'my_app/register.html',{'form':form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticateLoginUser(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = AuthenticateLoginUser()
    return render(request,'my_app/login.html',{"form":form})


def user_logout(request):
    logout(request)
    return redirect('home')


class HomeNews(ListView):
    model = News
    paginate_by = 2
    template_name = "my_app/index.html"
    context_object_name = "data"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новини"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class GetCategory(ListView):
    paginate_by = 2
    model = News
    context_object_name = "news"
    template_name = "my_app/category.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(slug=self.kwargs['slug_category'])
        return context

    def get_queryset(self):
        return News.objects.select_related('category').filter(category__slug = self.kwargs['slug_category'])


class GetNews(ListView):
    model = News
    template_name = "my_app/get_news.html"
    context_object_name = "news"

    def get_queryset(self):
        News.objects.filter(slug = self.kwargs['slug_news']).update(views=F('views') + 1)
        return get_object_or_404(News,slug = self.kwargs['slug_news'])


class AddNews(LoginRequiredMixin,CreateView,MyMixin):
    form_class = NewsForm
    template_name = 'my_app/add_news.html'
    login_url = "/admin/"
    to_upper = "добавить новость"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_upper()
        return context


class NewsListAPI(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsAdminReadOnly,)


class NewsUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class NewsDestroyAPI(generics.DestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # authentication_classes = TokenAuthentication
    permission_classes = (IsAdminUser,)






class NewsApiViews(APIView):

    def get(self,request):
        data = News.objects.all()
        return Response({"get":NewsSerializer(data,many=True).data})

    def post(self,request):
        mews_serializer = NewsSerializer(data=request.data)
        mews_serializer.is_valid(raise_exception=True)
        mews_serializer.save()
        return Response({"post":mews_serializer.data})

    def delete(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"})
        try:
            instance = News.objects.get(pk=pk)
            instance.delete()
        except Exception as exc:
            return Response({"error": "Object does not exists"})

        return Response({"delete":f"successful delete {pk} objects"})

    def put(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return Response({"error": "Method PUT is not allowed"})
        try:
            instance = News.objects.get(pk=pk)
        except Exception as exc:
            return Response({"error": "Object does not exists"})

        serializer = NewsSerializer(data=request.data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)