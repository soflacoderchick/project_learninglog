from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:   #meta data
        model = Topic
        fields = ['text']
        labels = {'text': ''}  #notice we are giving the field 'text' a blank label

class EntryForm(forms.ModelForm):  #EntryForm inherits from forms.ModelForm (same as TopicForm)
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}  # the text' field gets a blank label here as well
        widgets = {'text': forms.Textarea(attrs={'cols':80})}  # rgw widgets attribute is an HTML form element
                        # by using the forms.Textarea element, we're customizing the input widget for the 'text' field, giving the
                            # user an 80-column wide text area instead of the default 40 to give users enough room to make a sizeable entry.
        
    