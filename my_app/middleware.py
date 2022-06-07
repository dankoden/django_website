from django.http import HttpResponse
import datetime

class FirstMiddleware:
    def __init__(self,get_responce):
        self.get_responce = get_responce
        self.time_user_request = {}

    def __call__(self, request):
        usr_ip = request.META['REMOTE_ADDR']
        if usr_ip in self.time_user_request:
            self.time_user_request[usr_ip].append(datetime.datetime.now())
        else:
            self.time_user_request[usr_ip] = [datetime.datetime.now()]
        period = datetime.datetime.now().hour - self.time_user_request[usr_ip][0].hour
        if period > 0:
            self.time_user_request[usr_ip] = []
        else:
            if len(self.time_user_request[usr_ip]) > 10000:
                return HttpResponse("so many request from yuor ip")
        responce =  self.get_responce(request)
        print("Hello after views from FirstMiddleware")
        return responce

    def process_exeption(self,request,exception):
        pass


