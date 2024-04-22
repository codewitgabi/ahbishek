from django.contrib import admin
from .models import Team, Document, UserDocument, StaffDocument, Staff

admin.site.register(Team)
admin.site.register(Document)
admin.site.register(UserDocument)
admin.site.register(StaffDocument)
admin.site.register(Staff)
