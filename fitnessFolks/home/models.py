from django.db import models


class Categories(models.Model):
	name = models.CharField(max_length=300)

	def __str__(self):
		return self.name


class Faq(models.Model):
	question 	= models.TextField()
	answer 		= models.TextField()
	category 	= models.ForeignKey(Categories, on_delete=models.CASCADE, 
									related_name='questions')

	def __str__(self):
		return f'{self.category}_{self.id}'