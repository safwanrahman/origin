from django.conf.urls import url

from .views import task_list, task_add, task_modify

urlpatterns = [
    url(r'^$', task_list, name='task_list'),
    url(r'^add$', task_add, name='task_add'),
    url(r'^(?P<task_id>\d+)$', task_modify, name='task_modify'),
]