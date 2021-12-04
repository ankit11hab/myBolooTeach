from django import forms

CHOICES = [('A', 'A'),
           ('B', 'B'),
           ('C', 'C'),
           ('D', 'D')]


class SubmissionForm(forms.Form):
    def __init__(self, n,  *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        for i in range(0, n):
            self.fields["Question %d" % (i+1)] = forms.ChoiceField(
                choices=CHOICES, widget=forms.RadioSelect, required=False)


class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    classs = forms.IntegerField()
    mobile_no = forms.CharField(widget=forms.TextInput
                                (attrs={'placeholder': 'eg:- +12196496984'}))
    school = forms.CharField()
