from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Floor, Box, Rack, RackEquipment


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ("name", "open_editor")

    def open_editor(self, obj):
        url = reverse("floor-editor", args=[obj.id])
        return format_html('<a class="button" href="{}">Open Editor</a>', url)
    open_editor.short_description = "Editor"


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    # NEW: show rack link in list
    list_display = ("name", "floor", "rack", "x", "y", "w", "h", "is_visible")
    list_filter = ("floor", "is_visible")
    search_fields = ("name",)


# NEW: Rack admin to manage rack objects
@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ("name", "total_units")


# NEW: RackEquipment admin to add equipment under racks
@admin.register(RackEquipment)
class RackEquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "rack", "category", "u_start", "u_end")
    list_filter = ("category", "rack")
    search_fields = ("name",)

