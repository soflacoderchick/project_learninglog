from typing import ContextManager
from django.shortcuts import render, redirect
from .models import Entry, Topic
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
       """Show all topics."""
       topics = Topic.objects.filter(owner=request.user).order_by('date_added')
       context = {'topics': topics}
       return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
        """Show a single topic and all its entries."""
        topic = Topic.objects.get(id=topic_id)
        # Make sure the topic belongs to the current user
        if topic.owner != request.user:
            raise Http404

        entries = topic.entry_set.order_by('-date_added')
        context = {'topic': topic, 'entries': entries}
        return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':    #this test determines whether the request method is GET or POST
           	# No data submitted (note empty paren./no arguments below); create a blank form for user to fill out.
        form = TopicForm()
    else:
           	# if the request is POST, it means data is being submitted; process data.
        form = TopicForm(data=request.POST)

    if form.is_valid():
        new_topic = form.save(commit=False) #pass the commmit=False arg bc we need to modify the new topic before saving it to the database
        new_topic.owner = request.user  #set owner attribute to the current user
        new_topic.save() #last step: call save() on the topic instance just defined
        return redirect('learning_logs:topics')

 	# Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):   # topic_id parameter is needed to store the value it received from the URL
    """add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #as above, indicates no data has been submitted, so create a blank form
        form = EntryForm()
    else:
        # POST data as been submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # we inc. the commit=False argument to tell Django to create a new entry object & 
            new_entry.topic = topic                             # assign it to new_entry w/o saving it to the database yet.
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)  #this redirect call requires 2 arguments: the name of the view we want to
                                                                        # redirect to - topic() - which needs the argument topic_id for the view function.
    
    #The context dictionary is created to display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):  
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)  #first we get the entry object the user wants to edit & its associated topic
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)



