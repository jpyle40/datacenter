from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("floor/<int:floor_id>/", views.floor_viewer, name="floor-viewer"),
    path("rack/<int:rack_id>/", views.rack_viewer, name="rack-viewer"),

    # NEW: equipment detail route
    path("equipment/<int:equipment_id>/", views.equipment_detail, name="equipment-detail"),

    path("admin/floor/<int:floor_id>/edit/", staff_member_required(views.floor_editor), name="floor-editor"),
    path("admin/box/<int:pk>/move/", staff_member_required(views.box_move), name="box-move"),
]
