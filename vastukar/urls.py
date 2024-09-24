from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from upload.views import swiper,index, project_view, detail_view, contact_view,NewsListView,NewsPDFView,load_more, about_us, privacy_policy,vastukar_architects,certified_constructions,vastukar_interiors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('projects/', project_view, name='projects'),
    path('detail/<slug:slug>/', detail_view, name='project-detail'),
    path('contact/', contact_view, name='contact'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('load-more',load_more,name='load-more'),
    path('news/<slug:slug>/pdf/', NewsPDFView.as_view(), name='news-pdf-view'),

    path('about_us/', about_us, name='about_us'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('branches/vastukar_architects/', vastukar_architects, name='vastukar_architects'),
    path('branches/certified_constructions/', certified_constructions, name='certified_constructions'),
    path('branches/vastukar_interiors/', vastukar_interiors, name='vastukar_interiors'),
    path('test/swiper/', swiper, name='swiper'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
