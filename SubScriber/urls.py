from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from app import views
from django.contrib import admin
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('auth/', views.auth_page, name='auth'),
    path('links/', views.links, name='links'),
    path('anketa/', views.anketa, name='anketa'),
    path('partners/', views.partner_list, name='partner_list'),
    path('partners/<int:pk>/', views.partner_detail, name='partner_detail'),
    path('partners/<int:pk>/comment/', views.partner_comment, name='partner_comment'),
    path('partners/add_partner/', views.add_partner, name='add_partner'),
    path('video/', views.video, name='video'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)