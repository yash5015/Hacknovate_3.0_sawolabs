from django.db import models

# Create your models here.


class FoodItem(models.Model):
    Item_id = models.AutoField
    Item_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    Quantity = models.CharField(max_length=50, blank=True, default="")
    # description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="home/images", default="")

    def __str__(self):
        return self.Item_name


class Contact(models.Model):
    name = models.CharField(blank=False, max_length=122)
    email = models.CharField(blank=False, max_length=122)
    phone = models.CharField(blank=False, max_length=12)
    desc = models.TextField()
    feedback = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    amount = models.CharField(max_length=100, default='')
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Config(models.Model):
    api_key = models.CharField(max_length=200)
    identifier = models.CharField(max_length=200,
                                  choices=[("email", "Email"), ("phone_number_sms", "Phone")])
