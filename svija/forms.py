import re
from django import forms
from .models import Settings

class MyModelForm(forms.ModelForm):
  class Meta:
    model = Settings
    fields = '__all__'

  def clean_adobe_project(self):
    raw_adobe_project = self.cleaned_data['adobe_project']
    matches = re.findall(r'"([^"]+)"', raw_adobe_project)
    if matches:
      return matches[0]
    return ''

# class MyModelForm(forms.ModelForm):
#   class Meta:
#     model = MyModel
#     fields = '__all__'
# 
#   def clean_content(self):
#     raw_content = self.cleaned_data['content']
#     # Extract first quoted string
#     matches = re.findall(r'"([^"]+)"', raw_content)
#     if matches:
#       return matches[0]  # Or join(matches) if you want all quotes
#     return ''
