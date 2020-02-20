from django.http import HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django.conf import settings
from random import shuffle
import requests
import simplejson as json
import os, ast
from .models import Student
from .forms import StudentPhoneForm
from django.views.generic.edit import FormView


class SearchView(FormView):
	template_name = 'searchphone/main_search.html'
	form_class = StudentPhoneForm
	success_url = '/'
	
	def form_valid(self, form):
		return super().form_valid(form)
	def post(self, request):
		req = request.POST
		context={'ret':'ok'}

		id = 0
		if ('phone' in req):
			phone = req['phone']
			phone.replace(" ", "")
			phone.replace("+", "")
			if (len(phone) >= 10):
				phone = phone[1:]
			student = Student.objects.filter(phone__contains=phone).values()
			if (len(student) > 0):
				context.update({'students':student})
				id = student[0]['id']

		context['colors'] = self.do_colors(id)
		context.update({'req': req})
		form = StudentPhoneForm()
		context.update({'form': form})
		return render(request, 'searchphone/main_search.html', context)
	
	def get_context_data(self, **kwargs):
		"""Use this to add extra context."""
		students = Student.objects.exclude(phone__isnull=True).exclude(phone__exact='')[:1000]
		context = super(SearchView, self).get_context_data(**kwargs)
		context['students'] = students
		context['colors'] = self.do_colors(0)

		return context
	
	def do_colors(self, number):
		students = Student.objects.exclude(phone__isnull=True).exclude(phone__exact='')[number:number + 1000]
		cnt = len(students)
		if (cnt != 1000):
			# student db need to be feed
			number = number - (1000 - cnt)
			students = Student.objects.exclude(phone__isnull=True).exclude(phone__exact='')[number:number+1000]

		colors = []
		for student in students:
			nums = student.phone
			if nums:
				nums.replace(" ", "")
				nums = int(nums)
				col=[]
				col.append(int(nums/10000000) * int(nums/10000000) % 255)
				col.append(int(nums/100000) * int(nums/100000) % 255)
				col.append(int(nums/1000) * int(nums/1000) % 255)
				col.append(int(nums/10) * int(nums/10) % 255)
				col.append(int(nums) * int(nums) % 255)
				shuffle(col)
				colors.append(col)
		return colors


class MyView(View):
	AUTH_TOKEN = ""

	def do_colors():
		colors = []
		users = settings.USERS_42_DEBUG
		for i in range(5):
			for user in users:
				color_base = user['phone']
				color_base = color_base[1:]
				nums = color_base.split(" ")
				nums[0] = int(nums[0]) * int(nums[0]) % 255
				nums[1] = int(nums[1]) * int(nums[1]) % 255
				nums[2] = int(nums[2]) * int(nums[2]) % 255
				nums[3] = int(nums[3]) * int(nums[3]) % 255
				nums[4] = int(nums[4]) * int(nums[4]) % 255
				nums[5] = int(nums[5]) * int(nums[5]) % 255
				shuffle(nums)
				colors.append(nums)
		return colors
		
	def get(self, request, *args, **kwargs):
		colors = MyView.do_colors()
		if request.GET and 'code' in request.GET:
			MyView.AUTH_TOKEN = request.GET['code']
		if MyView.AUTH_TOKEN == "":
			return redirect('https://api.intra.42.fr/oauth/authorize?client_id=ba080f64b6bea0941942813b34719aa57a7c182e29943e5f8c485d16f670cca7&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2F&response_type=code')
		else:
			test = requests.get("https://api.intra.42.fr/v2/users/")
			'''
			parse_users = json.load(test.text)
			'''
			print(test)
			response = render(request, "searchphone/search.html", {'colors':colors})
			response['Authorisation'] = 'Bearer ' + str(MyView.AUTH_TOKEN)
			return response




class Test2015View(View):
	'''
	debug=True
	cheat_mode = True
	args = [
		'grant_type=client_credentials',
		'client_id=' + settings.API_42_CONFIG['client_ID'],
		'client_secret=' + settings.API_42_CONFIG['client_secret'],
		]

	status = requests.post("https://api.intra.42.fr/oauth/token?%s" % ("&".join(args)))
	response = status.json()

	if status.status_code == 200:
		print ("""
		***********************
		Connected to the 42 API
		***********************
		""")
	else:
		print ("You are not connecting to the 42 API please check README.md")
		sys.exit()

	if debug:
		print ("Token: " + response['access_token'])

	args = [
		'access_token=%s' % (response['access_token']),
		'token_type=bearer',
		'filter[primary_campus_id]=1',		
		'filter[pool_year]=2015',		
		'per_page=100',
		]

	
	#status = requests.get("https://api.intra.42.fr/v2/users/" + 'sbonnefo' + "/locations?%s" % ("&".join(args)))
	
	i = 1
	status = requests.get("https://api.intra.42.fr/v2/users" + "?%s" % ("&".join(args)) + "&page=" + str(i))
	response = []
	#while status.status_code == 200:
	while i < 2:
		response.append(status.json())		
		i = i + 1
		status = requests.get("https://api.intra.42.fr/v2/users" + "?%s" % ("&".join(args)) + "&page=" + str(i))
	ret = str(response)
	'''
	'''
	module_dir = os.path.dirname(__file__)  
	file_path = os.path.join(module_dir, 'users.txt')
	f = open(file_path, 'r')
	ret = f.read() 
	users = []
	with open(file_path, "r") as dump_42:
		for line in dump_42:
			users.append(ast.literal_eval(line))
	f.close()
	#ret = json.dumps(ret)
	#print(ret)
	#ret = response
	args = [
		'access_token=%s' % (response['access_token']),
		'token_type=bearer',
		#'filter[phone]=+33610587883',
	]
	file_path = os.path.join(module_dir, 'users_info.txt')
	f = open(file_path, 'w')
	for user in users:
		login = user['login']
		status = requests.get("https://api.intra.42.fr/v2/users/" + login + "?%s" % ("&".join(args)))
		f.write(str(status.json()))
	f.close()
	'''
	'''
	if len(response) > 0:
		if debug:
			ret += str(json.dumps(response, indent=4, sort_keys=True))
		ret += 'sbonnefo' + " is at computer " + response[0]['host']
	else:
		if status.status_code == 200:
			ret = 'sbonnefo' + " is not showing up on a computer, ask around!"
		else:
			ret = "sbonnefo is not a student login on the 42 API"
	'''
	ret = 'silent'
	def get(self, request, *args, **kwargs):
		return (HttpResponse(TestView.ret))

def viewFeedDb(request):
	args = [
		'grant_type=client_credentials',
		'client_id=' + settings.API_42_CONFIG['client_ID'],
		'client_secret=' + settings.API_42_CONFIG['client_secret'],
		]

	status = requests.post("https://api.intra.42.fr/oauth/token?%s" % ("&".join(args)))
	response = status.json()

	if status.status_code == 200:
		print ("""
		***********************
		Connected to the 42 API
		***********************
		""")
	else:
		print ("You are not connecting to the 42 API")
		sys.exit()
	args = [
		'access_token=%s' % (response['access_token']),
		'token_type=bearer',
	]

	students = Student.objects.filter(mail="")


	for student in students:
		
		st = Student.objects.get(login=student)
		status = requests.get("https://api.intra.42.fr/v2/users/" + st.login + "?%s" % ("&".join(args)))
		new_st = status.json()
		if 'phone' in new_st and new_st['phone'] != 'None':
			st.phone = new_st['phone']
		if 'email' in new_st and new_st['email'] != 'None':
			st.mail = new_st['email']
		print(new_st['email'])
		if 'first_name' in new_st and new_st['first_name'] != 'None':
			st.first_name = new_st['first_name']
		if 'last_name' in new_st and new_st['last_name'] != 'None':
			st.last_name = new_st['last_name']
		if 'image_url' in new_st and new_st['image_url'] != 'None':
			st.image_url = new_st['image_url']
		st.save()
	return (HttpResponse(students[0]))


	'''
	login = models.CharField(max_length=20, unique=True)
    id_42 = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    mail = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250)
    detail_url = models.CharField(max_length=250, unique=True)
    intra_url = models.CharField(max_length=250)
	'''

def viewInitDb(request):
	module_dir = os.path.dirname(__file__)  
	file_path_2015 = os.path.join(module_dir, 'users_2015.txt')
	file_path_2016 = os.path.join(module_dir, 'users_2016.txt')
	file_path_2017 = os.path.join(module_dir, 'users_2017.txt')
	users = []
	with open(file_path_2015, "r") as dump_42_15:
		for line in dump_42_15:
			users.append(ast.literal_eval(line))
	with open(file_path_2016, "r") as dump_42_15:
		for line in dump_42_15:
			users.append(ast.literal_eval(line))
	with open(file_path_2017, "r") as dump_42_15:
		for line in dump_42_15:
			users.append(ast.literal_eval(line))
	for user in users:
		student = Student(
						login=user['login'],
						id_42=user['id'],
						detail_url=user['url'],
						)
		student.save()
		print(user)
	return (HttpResponse(users[0]))


	'''
	login = models.CharField(max_length=20, unique=True)
    id_42 = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    mail = models.CharField(max_length=100)
    image_url = models.CharField(max_length=250)
    detail_url = models.CharField(max_length=250, unique=True)
    intra_url = models.CharField(max_length=250)
	'''
'''
	for user in users:
		login = user['login']
		status = requests.get("https://api.intra.42.fr/v2/users/" + login + "?%s" % ("&".join(args)))
		f.write(str(status.json()))
	f.close()
'''
