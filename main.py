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

import re
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

	<input type="submit">
	<br>
	<a href="/rot13"> click here for rot13 </a>
	<br>
	<a href="signup"> click here for signup </a>
</form>
"""

form_rot13 = """
<form method="post">

    <h2>Enter some text to ROT13:</h2>
    <!input name="text" value="%(text)s">
    <textarea name="text" style="height: 100px; width: 400px;" >%(text)s</textarea>
    <br>
    <br>
    <input type="submit">

</form>

"""

form_signup = """
<form method="post">

	<h2>Signup</h2>
	<label> Username <input name="username" value="%(username)s"> </label>
		<div style="color: red">%(wrong_username)s</div>
	<label> Password <input type="password" name="password" value="%(password)s"> </label>
		<div style="color: red">%(wrong_password)s</div>
	<label> Verify Password <input type="password" name="verify" value="%(verify)s"> </label>
		<div style="color: red">%(wrong_password_verify)s</div>
	<label> Email(optional) <input name="email" value="%(email)s"> </label>
		<div style="color: red">%(wrong_email_verify)s</div>
	<input type="submit" value="log in"> 
</form>
"""

form_success_login = """

	<h2>Welcome, %(username)s</h2>

"""

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

class Rot13Handler(webapp2.RequestHandler):
	def rot13(self, s):
		if not s:
			return ""
		new_s = ""
		for c in s:
			if c >= 'a' and c <= 'z':
				#if in half, + 13, otherwise chr(ord('a') + (ord('z') - ord(c)))
				if c <= 'm':
					new_s += chr(ord(c) + 13)
				else:
					new_s += chr(ord('a') + (ord(c) - ord('n')))
			elif c >= 'A' and c <= 'Z': 
				if c <= 'M':
					new_s += chr(ord(c) + 13)
				else:
					new_s += chr(ord('A') + (ord(c) - ord('N')))
			else:
				new_s += c		
		return new_s		
	
	def write_form(self, text=""):
		#print escape_html(self.rot13(text))
		self.response.write(form_rot13 % {"text":escape_html(self.rot13(text))} )

	
	def get(self):
	# will only be invoked first time, with text_to_rot to empty string
		self.write_form()
	
	def post(self):
	# will run everytime submit is clicked
		text = self.request.get("text")
		self.write_form(text)

class SignupHandler(webapp2.RequestHandler):
	def valid_username(self, username):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		return USER_RE.match(username)
	
	def valid_password(self, password):
		PASSWORD_RE = re.compile(r"^.{3,20}$")
		return PASSWORD_RE.match(password)

	def valid_email(self, email):
		EMAIL_RE = re.compile(r"(^[\S]+@[\S]+\.[\S]+$)")
		return not email or EMAIL_RE.match(email)

	def write_form(self, username="", wrong_username="", password="", wrong_password="", 
					verify="", wrong_password_verify="", email="", wrong_email_verify=""):
		self.response.write(form_signup % {
					"username" : escape_html(username), "wrong_username" : wrong_username,
					"password" : escape_html(password), "wrong_password" : wrong_password,
					"verify" : escape_html(verify), "wrong_password_verify": wrong_password_verify,
					"email" : escape_html(email), "wrong_email_verify": wrong_email_verify
			})

	def get(self):
		self.write_form()

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		wrong_username = ""
		wrong_password = ""
		wrong_password_verify = ""
		wrong_email_verify = ""

		success = True

		if not self.valid_username(username):
			wrong_username = "That's not a valid username."
			success = False
		if not self.valid_password(password):
			wrong_password = "That wasn't a valid password."
			success = False
		if password!="" and password!=verify:
			wrong_password_verify = "Your passwords didn't match."
			success = False
		if email!="" and not self.valid_email(email):
			wrong_email_verify = "That's not a valid email."
			success = False

		if not success:
			self.write_form(username, wrong_username, password, wrong_password, 
				verify, wrong_password_verify, email, wrong_email_verify)
		else:
			self.redirect('/welcome?username=' + username)

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		signupHandler = SignupHandler()
		username = self.request.get('username')
		if signupHandler.valid_username(username):
			self.response.write(form_success_login % {"username" : username})
		else:
			self.redirect('signup')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler), 
    ('/rot13', Rot13Handler),
    ('/signup', SignupHandler),
    ('/welcome', WelcomeHandler)
#    ('/testform', TestHandler)
], debug=True)
