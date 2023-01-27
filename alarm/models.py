from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class AlarmModel(models.Model):
    time = models.DateTimeField(blank=True,null=True)
    user_id = models.ForeignKey(User,related_name="user_alarm",on_delete=models.CASCADE,db_column="user_id")
    title = models.TextField(max_length=200)
    content = models.TextField()
    color = models.TextField()
    icon_class = models.TextField()
    more_info = models.BooleanField(default=False)
    herf = models.TextField()
    now = models.BooleanField(default=True)

    #username = request.user
    def panel_soiling_alarm(self,username,cctvnum,panelnum,soiling_area):
        self.time = timezone.now()
        self.user_id = User.objects.get(username = username)
        self.title = "태양광 패널 오염 감지"
        self.content = "현재 " + str(cctvnum) + "번 CCTV의 "+ str(panelnum)+ "번 Panel에서 " + str(soiling_area)+ " %의 오염이 감지되었습니다."
        self.color = "bg-orange"
        self.icon_class = "fas fa-solar-panel"
        self.more_info = True
        self.herf = "../CCTV/"
        self.save()


