from django.db import models
from django.core.validators import RegexValidator
import re
# phone_regex = RegexValidator(regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?
# [0-9]{4,6}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
# phone_regex = re.search('^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$','')

class Sponser(models.Model):

    class StatusChoice(models.TextChoices):
        MODERATION = 'Moderation', 'Moderatsiya'
        NEW = "New", 'Yangi'
        APPROVED = 'Approved', 'Tasdiqlangan'
        CANCELLED = 'Cancelled', 'Bekor qilingan'

    class TypeChoice(models.TextChoices):
        LEGAL = 'legal', 'yuridik'
        PHYSICAL = 'physical', 'jismoniy'
    
    class TransactionType(models.TextChoices):
        CASH = 'cash', 'Naqd'
        CARD = 'card', 'Karta orqali'


    full_name = models.CharField(max_length=100, 
                                 verbose_name="To'liq ism")
    organization_name = models.CharField(max_length=100, 
                                         verbose_name="Tashkilot nomi", 
                                         null=True, blank=True)
    phone_number = models.CharField(max_length=50, 
                                    validators=[RegexValidator(r'^\998\d{9}$')], 
                                    verbose_name="Telefon raqami")
    
    amount = models.PositiveIntegerField(verbose_name="Homiylik summasi")
    created_at = models.DateField(auto_now=True, verbose_name="Ariza sanasi")
    status = models.CharField(max_length=50,
                            choices = StatusChoice.choices,
                            default=StatusChoice.NEW,
                            verbose_name="Homiylik holeti")
    type = models.CharField(max_length=50,
                            choices = TypeChoice.choices,
                            verbose_name="Shahs turi")
    transaction_type = models.CharField(max_length=50,
                                        verbose_name="To'lov turi",
                                        choices=TransactionType.choices,
                                        default=TransactionType.CARD)



    def __str__(self) -> str:
        return f"{self.full_name} - {self.phone_number}"


class University(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nomi")

    def __str__(self) -> str:
        return self.name

class Student(models.Model):

    class DegreeChoice(models.TextChoices):
        BACHELOR = 'bachelor', 'bakalavr'
        MASTER = 'master', 'magistr'

    full_name = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)   # on_delete (Cascade - hammasini o'chiradi) (Set_null - tanlanmagan qilib qo'yadi) (Protect - o'chirtirmaydi (boshidan o'chirib kel) didi)
    contract = models.PositiveIntegerField(default=1, verbose_name="Kontrakt summasi")
    degree = models.CharField(max_length=50,
                              choices=DegreeChoice.choices,
                              default=DegreeChoice.BACHELOR,
                              verbose_name="Darajasi")

    def __str__(self) -> str:
        return self.full_name

class StudentSponser(models.Model):
    
    sponser = models.ForeignKey(Sponser, 
        on_delete=models.PROTECT, 
        verbose_name="Sponser",
        related_name="student_sponsers"
    )
    
    student = models.ForeignKey(Student, 
        on_delete=models.PROTECT, 
        verbose_name="Student",
        related_name="student_sponsers"
    )
    
    amount = models.PositiveIntegerField(verbose_name="Ajratilgan summa")

    def __str__(self) -> str:
        return f"{self.sponser} - {self.student}"



# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
# phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list