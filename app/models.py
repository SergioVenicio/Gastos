from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    salario = models.FloatField()
    senha = models.TextField()

    def __str__(self):
        return(self.name)

class Item(models.Model):
    descricao = models.CharField(max_length=200)

class Gasto(models.Model):
    id_user = models.ForeignKey(User)
    valor = models.FloatField()
    data = models.DateField()
    items = models.ManyToManyField(Item)


#class GastoItem(models.Model):
#    gasto = models.ForeignKey(Gasto)
#    item = models.ForeignKey(Item)
