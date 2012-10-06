from sys import argv
from HTMLParser import HTMLParser
import fnmatch, os, pythoncom, sys, win32com.client

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    a_found = False
    p_found = False
    b_found = False
    var_prefix = "@Body"
    count = 1
    ampscript = ""
    ampscript_urls = ""
    html_template = ""
    declare_amp_var = ""
    
    def handle_starttag(self, tag, attrs):
        ampscript = getattr(self, 'ampscript')
        count = getattr(self, 'count')
        var_prefix = getattr(self, 'var_prefix')
        html_template = getattr(self, 'html_template')
        ampscript_urls = getattr(self, 'ampscript_urls')   
        declare_amp_var = getattr(self, 'declare_amp_var')
        # print "Encountered a start tag:", tag
        if tag == 'a':
          url_var = var_prefix + str(count) + "URL"
          ampscript_url_var =  "\tSET " + url_var + " = \"" + attrs[0][1] + "\""
          ampscript_urls += ampscript_url_var
          html_template_var = "<a href=\"%%=RedirectTo(" + url_var + ")=%%\">"
          html_template += html_template_var
          # print 'start a'
          # print attrs[0][1]
          setattr(self, 'ampscript_urls', ampscript_url_var)
          setattr(self, 'html_template', html_template)
          setattr(self, 'a_found', True)
          setattr(self, 'declare_amp_var', declare_amp_var + "\tVAR " + url_var + "\n")
        elif tag == 'p':
          # print 'start p'
          setattr(self, 'p_found', True)
        elif tag == 'b':
          # print 'start b'
          setattr(self, 'html_template', html_template + "<strong>")
          setattr(self, 'b_found', True)
          
    def handle_endtag(self, tag):
        ampscript = getattr(self, 'ampscript')
        count = getattr(self, 'count')
        var_prefix = getattr(self, 'var_prefix')
        html_template = getattr(self, 'html_template')
        ampscript_urls = getattr(self, 'ampscript_urls')
        # print "Encountered an end tag :", tag
        if tag == 'a':
          # print 'end a'
          setattr(self, 'html_template', html_template + "</a>")
          setattr(self, 'a_found', False)
        elif tag == 'p':
          # print 'end p'
          setattr(self, 'p_found', False)
          setattr(self, 'html_template', getattr(self, 'html_template') + '\n<br/><br/>\n\n')
        elif tag == 'b':
          # print 'end b'
          setattr(self, 'html_template', html_template + '</strong>')
          setattr(self, 'b_found', False)
          
    def handle_data(self, data):
        ampscript = getattr(self, 'ampscript')
        var_prefix = getattr(self, 'var_prefix')
        count = getattr(self, 'count')
        html_template = getattr(self, 'html_template')
        declare_amp_var = getattr(self, 'declare_amp_var')
        # print "Encountered some data  :", data
        if getattr(self, 'p_found'):
          var = var_prefix + str(count)
          ampscript_var = "\tSET " + var + " = " + "\"" + data + "\"\n"
          ampscript += ampscript_var
          html_template_var = "%%=v(" + var + ")=%%"
          html_template += html_template_var
          setattr(self, 'ampscript', ampscript)
          setattr(self, 'count', count+1)
          setattr(self, 'html_template', html_template)
          setattr(self, 'declare_amp_var', declare_amp_var + "\tVAR " + var + "\n")

script, filename = argv
          
wordapp = win32com.client.gencache.EnsureDispatch("Word.Application")

#command: python tat3.py .
doc = os.getcwd() + "\\" + filename

wordapp.Documents.Open(doc)
docashtm = doc + '.htm'
ampscript_template = filename + "-ampscript.html"
wordapp.ActiveDocument.SaveAs(docashtm, FileFormat=win32com.client.constants.wdFormatFilteredHTML)

# instantiate the parser and feed it some HTML
parser = MyHTMLParser()

file = open(docashtm, 'r')
html = file.read()
#print html

parser.feed(html)

ampscript_html = ""

ampscript_html += "<!-- Localizations %%[\n\n"
ampscript_html += parser.declare_amp_var + "\n"
ampscript_html += parser.ampscript + "\n"
ampscript_html += parser.ampscript_urls + "\n"
ampscript_html += "\n]%% -->"
ampscript_html += "\n\n"
ampscript_html += parser.html_template


target = open(ampscript_template, 'w')
target.write(ampscript_html)

print "file created: " + ampscript_template

target.close()

# for running script with command line
# os.system("start " + ampscript_template)

#needs only 1 of the following to work
# wordapp.ActiveWindow.Close()
wordapp.Quit()          
