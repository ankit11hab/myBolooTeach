from django import forms

class SubmissionForm(forms.Form):
    CHOICES=[('A','A'),
         ('B','B'),
         ('C','C'),
         ('D','D')]
    question1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question4 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question5 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question6 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question7 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question8 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question9 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question10 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question11 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question12 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question13 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question14 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question15 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question16 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question17 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question18 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question19 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
    question20 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)

class ProfileUpdateForm(forms.Form):
     first_name = forms.CharField()
     last_name = forms.CharField()
     classs = forms.IntegerField()
     mobile_no = forms.CharField()
     school = forms.CharField()

