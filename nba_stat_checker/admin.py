from django.contrib import admin
from .models import Player,PlayerGeneralStatRecord,Team
# Register your models here.
#admin.site.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display=('last_name','first_name','full_name','num_stats','is_active','team')
admin.site.register(Player,PlayerAdmin)
admin.site.register(PlayerGeneralStatRecord)
admin.site.register(Team)