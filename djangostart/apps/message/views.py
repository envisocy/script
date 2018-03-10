from django.shortcuts import render

# Create your views here.

from .models import UserMessage

import uuid		# 借用uuid随机生成字符串

def getform(request):
	if request.method == "POST":
		user_message = UserMessage()

		user_message.name = request.POST.get('name', '')
		user_message.address = request.POST.get('address', '')
		user_message.email = request.POST.get('email', '')
		user_message.message = request.POST.get('message', '')
		user_message.object_id = str(uuid.uuid1())

		user_message.save()
	return render(request, 'message_form.html')