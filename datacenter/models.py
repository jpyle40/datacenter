from django.db import models


class Floor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    width_px = models.PositiveIntegerField(default=1000)
    height_px = models.PositiveIntegerField(default=600)

    def __str__(self):
        return self.name


class Box(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="boxes")
    name = models.CharField(max_length=100)
    x = models.PositiveIntegerField(default=10)
    y = models.PositiveIntegerField(default=10)
    w = models.PositiveIntegerField(default=120)
    h = models.PositiveIntegerField(default=80)
    color = models.CharField(max_length=16, default="#cde")
    is_visible = models.BooleanField(default=True)

    # NEW: link this Box to a Rack (optional)
    rack = models.OneToOneField(
        "Rack", on_delete=models.SET_NULL, null=True, blank=True, related_name="box"
    )

    def __str__(self):
        return f"{self.name} ({self.floor.name})"


# NEW: separate Rack model, each with fixed total units
class Rack(models.Model):
    name = models.CharField(max_length=100)
    total_units = models.PositiveIntegerField(default=46)  # default 46U racks

    def __str__(self):
        return self.name


# NEW: categories for equipment dropdown
class EquipmentCategory(models.TextChoices):
    VMWARE = "VMware", "VMware"
    AIX = "AIX", "AIX"
    WINDOWS = "Windows", "Windows"
    STORAGE = "Storage", "Storage"
    NETWORK = "Network", "Network"


# NEW: equipment model for items inside a rack
class RackEquipment(models.Model):
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="equipment")
    category = models.CharField(max_length=20, choices=EquipmentCategory.choices)
    name = models.CharField(max_length=200)
    u_start = models.PositiveIntegerField()   # starting U position
    u_end = models.PositiveIntegerField()     # ending U position

    def __str__(self):
        return f"{self.name} [{self.category}] in {self.rack.name}"

    class Meta:
        ordering = ["-u_start"]  # draw top-down




