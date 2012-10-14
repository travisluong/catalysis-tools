from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    fields = ['title','pub_date','content']
    
admin.site.register(Post, PostAdmin)