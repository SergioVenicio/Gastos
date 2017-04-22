from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    salario = models.DecimalField(max_digits=10, 
                                  decimal_places=2)
    senha = models.TextField()

    def __str__(self):
        return(self.name)

class Item(models.Model):
    descricao = models.TextField(default='')
    valor = models.DecimalField(max_digits=10, 
                                decimal_places=2)
    id_user = models.ForeignKey(User)

    def __str__(self):
        return(self.descricao)

class Gasto(models.Model):
    id_user = models.ForeignKey(User)
    descricao = models.TextField(default='')
    data = models.DateField()
    items = models.ForeignKey(Item)
    quantidade = models.IntegerField()
    total = models.DecimalField(max_digits=10,
                                decimal_places=2)

    def __str__(self):
        return(self.descricao)

#class GastoItem(models.Model):
#    gasto = models.ForeignKey(Gasto)
#    item = models.ForeignKey(Item)
