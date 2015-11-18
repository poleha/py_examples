"""
<<<<<<<<<<<<<СПИСОК КЛАССОВ
*****************************************************************
NEW
*****************************************************************
class Form
https://docs.djangoproject.com/en/1.7/ref/forms/api/#django.forms.Form

class ModelForm
https://docs.djangoproject.com/en/1.7/topics/forms/modelforms/#django.forms.ModelForm

*****************************************************************

reverse
from django.core.urlresolvers import reverse

https://docs.djangoproject.com/en/1.7/ref/urlresolvers/#reverse
reverse(viewname[, urlconf=None, args=None, kwargs=None, current_app=None])

url(r'^archive/$', 'news.views.archive', name='news_archive')
you can use any of the following to reverse the URL:

# using the Python path
reverse('news.views.archive')

# using the named URL
reverse('news_archive')

# passing a callable object
from news import views
reverse(views.archive)

#************************************
slugify
from django.utils.text import slugify

Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.

#***************************************

from django.contrib.auth.decorators import login_required
https://docs.djangoproject.com/en/1.7/topics/auth/default/#the-login-required-decorator

#*******************************
from django.contrib.auth.decorators import permission_required
https://docs.djangoproject.com/en/1.7/topics/auth/default/#the-permission-required-decorator

#**************************


OLD
*****************************************************************
**
class Model(**kwargs)
https://docs.djangoproject.com/en/1.7/ref/models/instances/#django.db.models.Model
https://docs.djangoproject.com/en/1.7/topics/db/models/
A model is the single, definitive source of information about your data. It contains
the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.
**



**
class QuerySet([model=None, query=None, using=None])
https://docs.djangoproject.com/en/1.7/ref/models/querysets/#django.db.models.query.QuerySet
Набор моделей, выдаваемый, как правило, менеджером модели методами типа filter, exclude
**

**
class Manager - класс для создания запросов. Имеет методы filter, exclude. Основной источкик QuerySet
https://docs.djangoproject.com/en/1.7/topics/db/managers/#django.db.models.Manager
**


**
class RelatedManager
https://docs.djangoproject.com/en/1.7/ref/models/relations/,
через который можно получить разные QuerySets подчиненных моделей, в зависимости от
        фильтра, порядка итд
**


**
class django.views.generic.detail.DetailView
https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView
While this view is executing, self.object will contain the object that the view is operating upon
**

**
django.views.generic.list.ListView
https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView
A page representing a list of objects.
**

**
class HttpResponse
https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpResponse
In contrast to HttpRequest objects, which are created automatically by Django,
HttpResponse objects are your responsibility. Each view you write is responsible for instantiating, populating
and returning an HttpResponse.
Это то, что создают view. html, выводимый на страницу
**

**
class HttpRequest
https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpRequest
Параметры запроса
Например
HttpRequest.GET
HttpRequest.POST
**

**
class HttpResponseRedirect
 Always return an HttpResponseRedirect after successfully dealing
 with POST data. This prevents data from being posted twice if a
 user hits the Back button.
Возвращаем код 302(страница изменена) после обработки post-даты
**

**
class django.template.Context
Context как правило получает словарь, который передает в template system
**

**
А RequestContext - это суб-класс django.template.Context, отличается тем, что
1) Принимает HttpRequest в качестве первого параметра;
2) The second difference is that it automatically populates the context with a few variables,
according to your TEMPLATE_CONTEXT_PROCESSORS setting.
По умолчанию это кортеж:
("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages")

То есть этот класс не просто выдает текст, а передает в template system еще дополнительные переменные
**


**
class django.http.Http404
When you return an error such as HttpResponseNotFound, you’re responsible for defining the HTML of the resulting error page:

return HttpResponseNotFound('<h1>Page not found</h1>')
For convenience, and because it’s a good idea to have a consistent 404 error page across your site,
Django provides an Http404 exception. If you raise Http404 at any point in a view function, Django will catch it
and return the standard error page for your application, along with an HTTP error code 404.
**

СПИСОК КЛАССОВ>>>>>>>>>>>>>>>>>>>>>>>


"""






































