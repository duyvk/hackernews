from django.contrib import admin

from stories.models import Story



class StoryAdmin(admin.ModelAdmin):
  list_display = ('__unicode__','domain','moderator','created_at','updated_at')
  list_filter = ('created_at','updated_at')
  search_fields = ('title','moderator__username','moderator__first_name')

  # fields= ('title','url')
  readonly_fields = ('created_at','updated_at')

  fieldsets=[
        ('Story',{
            'fields':('title','url','points')
          }),
        ('moderator',{
            'classes':('collapse',),
            'fields':('moderator',)
        }),
        ('Change History',{
          'fields':('created_at','updated_at')
          })

        ]

  def lower_case_title(self,obj):
    return obj.title.lower()
  lower_case_title.short_description = 'title'



admin.site.register(Story,StoryAdmin)
