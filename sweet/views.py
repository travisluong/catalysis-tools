# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
import os
from subprocess import call

cwd = os.getcwd()

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def index(request):
    return render_to_response('sweet/index.html', context_instance=RequestContext(request))
    
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            handle_uploaded_file(uploaded_file)
            
            # print os.getcwd()
            
            command = 'python ' + cwd + '\sweet.py sweet-temp.docx'
            print command
            
            # call the python script with system
            os.system(command)
           
            
            file = open('sweet-temp.docx-ampscript.html', "r+")
            
            ampscript_html = file.read()
            
            
            # ampscript_html = "test"
            print ampscript_html
       
            return render_to_response('sweet/upload_success.html', {'form' : form, 'ampscript_html' : ampscript_html}, context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
    return render_to_response('sweet/upload.html', {'form' : form}, context_instance=RequestContext(request))
    
def handle_uploaded_file(f):
    destination = open(cwd + '/sweet-temp.docx', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()