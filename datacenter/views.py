from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
import json
from .models import Floor, Box, Rack


def home(request):
    floors = Floor.objects.all()
    return render(request, "datacenter/home.html", {"floors": floors})


def floor_viewer(request, floor_id):
    floor = get_object_or_404(Floor, pk=floor_id)
    boxes = floor.boxes.filter(is_visible=True)
    return render(request, "datacenter/viewer.html", {"floor": floor, "boxes": boxes})


def floor_editor(request, floor_id):
    floor = get_object_or_404(Floor, pk=floor_id)
    boxes = floor.boxes.all()
    return render(request, "datacenter/editor.html", {"floor": floor, "boxes": boxes})


# NEW: rack viewer to show 46U rack with equipment
# datacenter/views.py
def rack_viewer(request, rack_id):
    rack = get_object_or_404(Rack.objects.prefetch_related("equipment"), pk=rack_id)

    equipment_list = []
    for eq in rack.equipment.all():
        equipment_list.append({
            "name": eq.name,
            "category": eq.category,
            "u_start": eq.u_start,
            "u_end": eq.u_end,
            # pre-calc values instead of doing math in template
            "row_start": rack.total_units - eq.u_end + 1,
            "row_span": eq.u_end - eq.u_start + 1,
        })

    return render(request, "datacenter/rack.html", {
        "rack": rack,
        "equipment_list": equipment_list,
    })



@require_POST
def box_move(request, pk):
    box = get_object_or_404(Box, pk=pk)
    try:
        data = json.loads(request.body.decode())
        box.x, box.y = int(data["x"]), int(data["y"])
        box.save(update_fields=["x", "y"])
        return JsonResponse({"ok": True})
    except Exception as e:
        return HttpResponseBadRequest(str(e))



