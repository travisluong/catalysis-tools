# Super Localization Excel Extraction Program
# Author: Travis Luong


import xlrd
import os

cwd = os.getcwd()

row_offset = 1
  
# user_input = int(raw_input("\n[1] has subject line\n[2] no subject line\n> "))
user_input = 1
if user_input == 1:
  has_subject = True
  row_offset = 2
elif user_input == 2:
  has_subject = False
else:
  print "Not a valid option."
  quit()
  



def generate_subject_ampscript(filename, default_first_column=True):
  wb = xlrd.open_workbook(filename)
  sh = wb.sheet_by_index(0)
  subjects = sh.row_values(1)
  loc_variables = sh.col_values(0)
  loc_ids = sh.row_values(0)
  loc_or_pref = sh.cell(0,0).value
  target = open(cwd + '/temp/subject-ampscript.html', 'wb+')
  if default_first_column:
    start_col = 2
    end_col = len(loc_ids)
  else:
    start_col = 1
    end_col = len(loc_ids)
  first = True
  for i in range(start_col,end_col):
    if first:
      if_or_elseif = "IF "
      first = False
    else:
      if_or_elseif = "ELSEIF "
    target.write("%%[" + if_or_elseif + loc_or_pref + " == \"" + loc_ids[i] + "\" THEN]%%\n")
    target.write(subjects[i].encode('utf8') + "\n")
  
  if default_first_column:
    target.write("%%[ELSE]%%\n")
    target.write(subjects[1].encode('utf8') + "\n")
    
  target.write("%%[ENDIF]%%\n\n")
  
  target.close()

  
def generate_ampscript(filename, auto_variables=False, replace_quotes=True, default_first_column=True):

  wb = xlrd.open_workbook(filename)
  sh = wb.sheet_by_index(0)
  loc_variables = sh.col_values(0)
  loc_ids = sh.row_values(0)

  loc_or_pref = sh.cell(0,0).value

  target = open(cwd + '/temp/sleep-ampscript.html', 'wb+')

  target.write("<!-- Localizations %%[\n\n")
  count = 1
  
  if default_first_column:
    col_offset = 1
  else:
    col_offset = 0
  
  for loc_var in loc_variables:
    if count > row_offset:
      if auto_variables:
        target.write("VAR @Body" + str(count-row_offset) + "\n")
      else:
        target.write("VAR @" + loc_var + "\n")
    count += 1
    
  target.write("\n")
    
  for i in range(col_offset, sh.ncols-1):

    if i == 1:
      target.write("IF ")
    else:
      target.write("ELSEIF ")
      
    target.write(loc_or_pref + " == \"")
    target.write(loc_ids[i+1] + "\"")
    target.write(" THEN\n")
    
    count = 1
    for j in range(len(loc_variables)-row_offset):
      val = sh.cell(j+row_offset,i+1).value
      if replace_quotes:
        val = val.replace('"', "&quot;")
      val = val.encode('utf8')
      target.write("\tSET")
      if auto_variables:
        target.write(" @Body" + str(count) + " = ")
        count += 1
      else:
        target.write(" @"+loc_variables[j+row_offset]+" = ")
      target.write("\"" + val + "\"")
      target.write("\n")     
  
  if default_first_column:
    target.write("ELSE\n")
    for k in range(len(loc_variables)-row_offset):
      val = sh.cell(k+row_offset,1).value
      if replace_quotes:
        val = val.replace('"', "&quot;")
      val = val.encode('utf8')
      target.write("\tSET")
      target.write(" @"+loc_variables[k+row_offset]+" = ")
      target.write("\"" + val + "\"")
      target.write("\n")
    
  target.write("ENDIF")
  target.write("\n\n]%% -->")
  target.close()
    

