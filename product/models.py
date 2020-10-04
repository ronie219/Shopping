from django.db import models
from accounts.models import Accounts


def user_directory_path(instance, filename):
    return "Item/{}/{}".format(instance.item, filename)


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categery"
        # db_table = "super_category"


class Item(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='account',default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    prize = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    in_stock = models.BooleanField(default=False, editable=False)
    count = models.IntegerField(default=0)

    @property
    def image(self):
        return self.image_set.all()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        count = self.count
        if count > 0:
            self.in_stock = True
        return super(Item, self).save(*args, **kwargs)



class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='image')
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.item.name
