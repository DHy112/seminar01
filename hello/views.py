import psutil
from django.http import JsonResponse
from hello.models import Requests
from django.shortcuts import render
import redis
from django.core.cache import cache
import uuid, time
import pickle

def index(request):
    result = results()
    return render(request, 'hello/index.html', result)
  
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

r = redis.StrictRedis(host='localhost', port=6379)

def get_post(request):
  if request.method =='GET':
    message = request.GET['message']
    data = {
      'message': message,
    }
    key = uuid.uuid4()
    time_stamp = time.time()
    cache.set(key, time_stamp, timeout=60*60, version='')
    return JsonResponse(data)  

def get_rps():
  now = time.time()
  before_1_sec = now - 1
  before_1_min = now - 1 * 60
  
  all_keys = r.keys(pattern='*')
  values = []
  for x in all_keys :
    values.append(pickle.loads(r.get(x)))
  perhour = len(values)
  permin = 0
  persec = 0
  for value in values:
    if value > before_1_min:
      permin += 1
      if value > before_1_sec:
        persec +=1
  rps_result = [persec, permin, perhour]
  return rps_result

def get_usage():
  cpu = psutil.cpu_percent();
  memory = psutil.virtual_memory();
  usage_result = [cpu, memory[2]]
  return usage_result

def results():
  usage = get_usage()
  rps = get_rps()
  output = {
    "cpu_usage" : usage[0],
    "memory_usage" : usage[1],
    "sec": rps[0],
    "min": rps[1],
    "hour": rps[2]
  }
  return output

def call_data(request):
  output = results()
  return JsonResponse(output)