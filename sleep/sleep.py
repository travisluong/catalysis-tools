# Super Localization Excel Extraction Program
# Author: Travis Luong

import xlrd
import os

cwd = os.getcwd()
row_offset = 2

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
  num_loc_ids = len(loc_ids)

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
  first = True  
  for i in range(col_offset, sh.ncols-1):

    if first and num_loc_ids > 2:
      target.write("IF ")
      first = False
    elif num_loc_ids > 2:
      target.write("ELSEIF ")
      first = False
      
    if num_loc_ids > 2:  
      target.write(loc_or_pref + " == \"")
      target.write(loc_ids[i+1] + "\"")
      target.write(" THEN\n")
    
    count = 1
    for j in range(len(loc_variables)-row_offset):
      val = sh.cell(j+row_offset,i+1).value

      # if next cell starts with period or comma, cut trailing right space for current cell
      try:
        next_cell_val = sh.cell(j+1+row_offset,i+1).value.encode('utf8')
        if next_cell_val.startswith(".") or next_cell_val.startswith(","):
          val = val.rstrip()
          print val
      except IndexError:
        pass

      if replace_quotes:
        val = val.replace('"', "&quot;")
      val = val.encode('utf8')
      if num_loc_ids > 2:
        target.write("\t")
      target.write("SET")
      if auto_variables:
        target.write(" @Body" + str(count) + " = ")
        count += 1
      else:
        target.write(" @"+loc_variables[j+row_offset]+" = ")
      target.write("\"" + val + "\"")
      target.write("\n")     
  
  if default_first_column:
    if num_loc_ids > 2:
      target.write("ELSE\n")
    for k in range(len(loc_variables)-row_offset):
      val = sh.cell(k+row_offset,1).value
      print val.encode('utf8')
      # if next cell starts with period or comma, cut trailing right space for current cell
      try:
        next_cell_val = sh.cell(k+1+row_offset,1).value.encode('utf8')
        if next_cell_val.startswith(".") or next_cell_val.startswith(","):
          val = val.rstrip()
      except IndexError:
        pass
      
      if replace_quotes:
        val = val.replace('"', "&quot;")
      val = val.encode('utf8')
      if num_loc_ids > 2:
        target.write("\t")
      target.write("SET")
      target.write(" @"+loc_variables[k+row_offset]+" = ")
      target.write("\"" + val + "\"")
      target.write("\n")
  
  if num_loc_ids != 2:
    target.write("ENDIF")
  target.write("\n\n]%% -->")
  target.close()
    

