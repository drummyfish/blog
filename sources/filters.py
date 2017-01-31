#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file implements custom filters to be used by Jinja in templates.
#
# by tastyfish

import re

#============== macro functions ==============

def fit_but_cheatsheet(course_abbreviation="",page_number="",imgur_id=""):
  caption = course_abbreviation + u" tahák, str." + page_number

  result  = "<figure>\n"
  result += "  <a href=\"http://i.imgur.com/" + imgur_id + "\" target=\"blank\">\n"
  result += "    <img src=\"http://i.imgur.com/" + imgur_id + "m.jpg\" alt=\"" + caption + "\" width=\"200\" height=\"160\">\n"
  result += "  </a>\n"
  result += "  <figcaption> " + caption + "</figcaption>\n"
  result += "</figure>\n"
  return result

#=============================================

MACROS = [fit_but_cheatsheet]

# Expands all macros in the input text. The macros in the input_text are
# in format
#
# $func(param1,param2,...)
#
# where func is a name of function from this MACROS list. The function
# will be executed with python with given params and the macro will be
# replaced with the function return value.
#
# Escaped '$' symbols (\$) are replaced with '$'.

def process_macros(input_text):
  expansions = []    # list of tuples (position_from,position_to,expanded_text,macro_call_length)

  for match in re.finditer("([^\\\]|^)\$([^\\(]*)\\(([^\\)]*)\\)",input_text):
    function_name = input_text[match.start(2):match.end(2)]
    function_params = input_text[match.start(3):match.end(3)].split(",")
    complete_match = input_text[match.start(0):match.end(0)]

    macro = None

    for func in MACROS:
      if func.__name__ == function_name:
        macro = func
        break

    if macro == None:
      print("Warning: macro \"" + function_name + "\" is not defined.")
    else:
      expansions.append((match.start(0),match.end(0),macro(*function_params),len(complete_match)))
   
  extra_length = 0

  for expansion in expansions:
    input_text = input_text[:expansion[0] + extra_length + 1] + expansion[2] + input_text[expansion[1] + extra_length:]
    extra_length += len(expansion[2]) - expansion[3] + 1
 
  return input_text

if __name__ == '__main__':
  print(process_macros("$img(url)$img(url)Asasasdas dsa das\$ dasaaasd sda sdasdasaasdasda \n$img(url,200,100,meirl)| asasasa |$img(url,200,100,meirl2)| sasass$img(url,200,100,meirl)"))
