from dataclasses import dataclass
from re import template
from django.http import HttpResponse, JsonResponse
from hello.models import Requests
from django.template import loader
from django.shortcuts import render
import schedule, time


def index(request):
    result = get_rps()
    #result={}
    return render(request, 'hello/index.html', result)
  
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_post(request):
  if request.method =='GET':
    message = request.GET['message']
    data = {
      'message': message,
    }
    print(data)
    ip = get_client_ip(request);
    print('ip: ', ip)
    Requests.objects.create(who=ip)
    print(Requests.objects.all())
    return JsonResponse(data)
  
import psutil
from datetime import datetime, timedelta

def get_rps():
  now = datetime.now()
  before_1_sec = now - timedelta(seconds=1)
  before_1_min = now - timedelta(minutes=1)
  before_1_hour = now - timedelta(hours=1)
  cpu = psutil.cpu_percent();
  memory = psutil.virtual_memory();
  hour = Requests.objects.filter(date__range=[before_1_hour, now]).count()
  min = Requests.objects.filter(date__range=[before_1_min, now]).count()
  sec = Requests.objects.filter(date__range=[before_1_sec, now]).count()
  rps_result = {
    "cpu_usage" : cpu,
    "memory_usage" : memory[2],
    "requests_per_hour": hour,
    "requests_per_min": min,
    "requests_per_sec": sec
  }
  return rps_result

# schedule.every(1).seconds.do(get_rps)

# while True:
#   schedule.run_pending()
#   time.sleep(1)

def call_data(request):
  output = get_rps()
  return JsonResponse(output)