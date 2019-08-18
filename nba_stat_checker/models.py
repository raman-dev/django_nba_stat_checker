from django.db import models
from django.urls import reverse

class Team(models.Model):
    team_id=models.AutoField(primary_key=True,default=0)
    name=models.CharField(max_length=75,default="N/A")
    team_abbreviation=models.CharField(max_length=5,default="N/A")

    class Meta:
        ordering=['name']

    def get_absolute_url(self):
        return reverse('team-detail',args=[self.team_abbreviation,self.team_id])
    
    def __str__(self):
        return self.name+" ("+self.team_abbreviation+")"

# Create your models here.
class Player(models.Model):
    player_id = models.IntegerField(primary_key=True,default = 0)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=250)
    num_stats = models.IntegerField(default= 0)
    is_active = models.IntegerField(default=0)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,null=True)
    #create constraints on any column of the database
    class Meta:
        constraints =[
            models.CheckConstraint(check=models.Q(is_active__gte=0),name='is_active_gte_0'),
            models.CheckConstraint(check=models.Q(is_active__lte=1),name='is_active_lte_1')
        ]

        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        return reverse('player-detail',args=[self.last_name[0],str(self.player_id)])

    def get_player_id(self):
        return str(self.player_id)

    def __str__(self):
        return ', '.join([self.last_name,self.first_name,self.full_name,str(self.num_stats),str(self.is_active),str(self.player_id),str(self.team)])



class PlayerGeneralStatRecord(models.Model):
    #write all columns for each stat 
    player = models.ForeignKey(Player,on_delete=models.SET_NULL,null=True)
    stat_cid = models.IntegerField(default = 0)
    season_id= models.CharField("Year",max_length=15)
    team_abbreviation = models.CharField(max_length=25)
    player_age= models.IntegerField(default=0)

    gp = models.IntegerField("Games Played",default=0)
    gs = models.IntegerField("Games Started",default=0)
    minp = models.FloatField("Minutes Played",default=0)
    fgm = models.IntegerField("Field Goals Made",default=0)
    fga = models.IntegerField("Field Goals Attempted",default=0)

    @property
    def fg_pct(self):
        if self.fga == 0:
            return '0.0'
        return str('%.3f'%(self.fgm/self.fga))
    fg3m = models.IntegerField("3 Point Field Goals Made",default=0)
    fg3a = models.IntegerField("3 Point Field Goals Attempted",default=0)
    fg3_pct = models.FloatField("3 Point Field Goals Percentage",default=0)
    ftm = models.IntegerField("Free Throws Made",default=0)

    fta = models.IntegerField("Free Throws Attempted",default=0)
    ft_pct = models.FloatField("Free Throw Percentage",default=0)
    oreb = models.FloatField("Offensive Rebounds",default=0)
    dreb = models.FloatField("Defensive Rebounds",default=0)
    reb = models.IntegerField("Rebounds",default=0)

    ast = models.IntegerField("Assists",default=0)
    stl = models.FloatField("Steals",default=0)
    blk = models.FloatField("Blocks",default=0)
    tov =models.FloatField("Turnovers",default=0)
    pf = models.IntegerField("Personal Fouls",default=0)

    pts = models.IntegerField("Points",default=0)



    class Meta:
        ordering=['player_id','stat_cid']
    def __str__(self):
        return ', '.join([
            str(self.stat_cid),self.season_id,self.team_abbreviation,str(self.player_age),
            str(self.gp),str(self.gs),str(self.minp),str(self.fgm),str(self.fga),
            str(self.fg_pct),str(self.fg3m),str(self.fg3a),str(self.fg3_pct),str(self.ftm),
            str(self.fta),str(self.ft_pct),str(self.oreb),str(self.dreb),str(self.reb),
            str(self.ast),str(self.stl),str(self.blk),str(self.tov),str(self.pf),str(self.pts)
        ])

