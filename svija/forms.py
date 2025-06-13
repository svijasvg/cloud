
#:::::::::::::::::::::::::::::::::::::::: forms.py

from django import forms
from .models import Page, Section, Screen, Settings

class settingsSectionSelectorForm(forms.ModelForm):

  class Meta:
    model = Settings
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['section'].queryset = Section.objects.exclude(code="*")

class pageSectionSelectorForm(forms.ModelForm):

  class Meta:
    model = Page
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['section'].queryset = Section.objects.exclude(code="*")



#:::::::::::::::::::::::::::::::::::::::: fin

