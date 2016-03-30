#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

# form = """
# <form method="post" action="/testform">
# 	<input name="q">
# 	<input type="submit">
# </form>
# """

# class TestHandler(webapp2.RequestHandler):
# 	def post(self):
# 		#q = self.request.get("q")
# 		#self.response.out.write(q)
# 		self.response.headers['Content-Type'] = 'text/plain'
# 		self.response.out.write(self.request)



# def escape_html(s):
#     new_s = ""
#     for c in s:
#         if c == '&':
#             new_s += "&amp;"
#         elif c == '<':
#             new_s += "&lt;"
#         elif c == '"':
#             new_s += "&quot;"
#         elif c == '>':
#             new_s += "&gt;"
#         else:
#             new_s += c
#     return new_s

def escape_html(s):
	return cgi.escape(s, quote = True)

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December',
          '1','2','3','4','5','6','7','8','9','10','11','12']
def valid_month(month):
    if not month:
        return False
    if month in months:
    	return True
    if month.upper()[0] + month.lower()[1:] in months:
        return True

def valid_day(day):

    if day.isdigit() and int(day) in range(1, 31+1):
        return True
    else:
        return False

def valid_year(year):
    if year and year.isdigit() and int(year) in range(1900, 2020+1):
        return True
    else:
        return False


form = """
<form method="post">
	What is your birthday?
	<br>

	<label> month <input name="month" value="%(month)s"> </label>
	<label> day <input name="day" value="%(day)s">  </label>
	<label> year <input name="year" value="%(year)s">  </label>
	<div style="color: red">%(error)s</div>

	<br>
	<br>
	<input type="submit">
</form>
"""
s = "haha"
class MainHandler(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.write(form % {"error" : error,
									"month" : escape_html(month),
									"day" : escape_html(day),
									"year" : escape_html(year),
									})

	def get(self):
	    self.write_form()

	def post(self):
		user_month = self.request.get("month")
		user_day = self.request.get("day")
		user_year = self.request.get("year")

		month = valid_month(user_month)
		day = valid_day(user_day)
		year = valid_year(user_year)
		print user_month, ' ', user_day, ' ', user_year
		if not (month and day and year):
			self.write_form("That doesn't look valid to me, friend", user_month, user_day, user_year)
		else:
			self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("Thanks, that's a valid date")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler) 
#    ('/testform', TestHandler)
], debug=True)