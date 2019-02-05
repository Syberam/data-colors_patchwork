from .models import Student
from django.forms import ModelForm


class StudentPhoneForm(ModelForm):
    class Meta:
        model = Student
        fields = ['phone']

'''
# Creating a form to add an article.
    form = ArticleForm()

# Creating a form to change an existing article.
    article = Article.objects.get(pk=1)
    form = ArticleForm(instance=article)
'''