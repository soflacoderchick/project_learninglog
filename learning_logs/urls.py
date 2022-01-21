"""Defines URL patterns for learning_logs."""

from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [
       path('', views.index, name='index'),
       
       # Page that shows all topics:
        path('topics/', views.topics, name='topics'),

        # Detail page for a single topic.
        path('topics/<int:topic_id>/', views.topic, name='topic'),

        path('new_topic/', views.new_topic, name='new_topic'),

        #Page for adding a new entry (we include a topic_id bc new entries must be associate w a particular topic argument in the URL):
        path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),

        #Page for editing an entry:
        path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
   ]


