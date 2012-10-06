# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
import sleep
import os

# get current working directory
cwd = os.getcwd()

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file  = forms.FileField()
    auto_variables = forms.BooleanField(required=False)
    replace_quotes = forms.BooleanField(required=False, initial=True)
    default_first_column = forms.BooleanField(required=False, initial=True)

def index(request):
    return render_to_response('sleep/index.html', context_instance=RequestContext(request))
    
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        auto_variable_on = request.POST.getlist('auto_variables')
        replace_quotes_on = request.POST.getlist('replace_quotes')
        default_first_column_on = request.POST.getlist('default_first_column')
        
        if 'on' in auto_variable_on:
          auto_variable_on = True
        else:
          auto_variable_on = False
        if 'on' in replace_quotes_on:
          replace_quotes_on = True
        else:
          replace_quotes_on = False
        if 'on' in default_first_column_on:
          default_first_column_on = True
        else:
          default_first_column_on = False
        if form.is_valid():
            uploaded_file = request.FILES['file']
            

            # try:
            handle_uploaded_file(uploaded_file)
            sleep.generate_ampscript(cwd + '/temp/temp.xls', auto_variable_on, replace_quotes_on, default_first_column_on)
            sleep.generate_subject_ampscript(cwd + '/temp/temp.xls', default_first_column_on)
            file = open(cwd + '/temp/sleep-ampscript.html', 'r')
            subject_file = open(cwd + '/temp/subject-ampscript.html', 'r')
            output = file.read()
            subject_output = subject_file.read()
            # except:
                # output = "Not valid file type"
                # subject_output = ""
                
            return render_to_response('sleep/upload_success.html', {'form' : form, 'output' : output, 'subject_output' : subject_output}, context_instance=RequestContext(request))
    else:
        form = UploadFileForm()
    return render_to_response('sleep/upload.html', {'form' : form}, context_instance=RequestContext(request))
    
def handle_uploaded_file(f):
    destination = open(cwd + '/temp/temp.xls', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()