from django.urls import path

from . import views


app_name='piazzapolls'
urlpatterns = [
    path('', views.index, name='index'),
    path('main_page', views.main_page, name='main_page'),
    path('<int:information_id>/analyze/', views.analyze, name='analyze'),
    path('<int:information_id>/results/', views.results, name='results')
]
