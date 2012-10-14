from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from blog.models import Post

def index(request):
    latest_post_list = Post.objects.all().order_by('pub_date')[:10]
    return render_to_response('blog/index.html', {'latest_post_list': latest_post_list}, context_instance=RequestContext(request))