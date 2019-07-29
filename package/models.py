from django.db import models

class TripType(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.name)


class Trip(models.Model):
    title = models.CharField(max_length = 200)
    starting_point = models.CharField(max_length = 200)
    ending_point = models.CharField(max_length = 200)
    price = models.PositiveIntegerField()
    details = models.TextField()
    type_of_trip = models.ForeignKey(TripType, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.title)