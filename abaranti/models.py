from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    class Role(models.IntegerChoices):
        RECEPTION = 0, '受付'
        DOCTOR = 1, '医師'

    # empidをusernameとして使う
    username = models.CharField(max_length=8, primary_key=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)  # ハッシュ化されたパスワードを保存
    role = models.IntegerField(choices=Role.choices)

    def __str__(self):
        return self.username


class Hospital(models.Model):
    hospital_id = models.CharField(max_length=8, primary_key=True)
    hospital_name = models.CharField(max_length=64)
    hospital_address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=13)
    capital = models.IntegerField()
    emergency = models.IntegerField(choices=((1, 'あり'), (0, 'なし')))  # 救急対応の有無（詳細設計書に従い1/0で表現）

    def __str__(self):
        return self.hospital_name


class Supplier(models.Model):
    supplier_id = models.CharField(max_length=8, primary_key=True)
    supplier_name = models.CharField(max_length=64)
    supplier_address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=13)
    capital = models.IntegerField()
    delivery_time = models.IntegerField()  # 納期（日数）

    def __str__(self):
        return self.supplier_name


class Patient(models.Model):
    patient_id = models.CharField(max_length=8, primary_key=True)
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    gender = models.IntegerField(choices=((0, '男'), (1, '女')))  # 性別（詳細設計書に従い0/1で表現）
    birthdate = models.DateField()
    insurance_number = models.CharField(max_length=64)
    insurance_exp = models.DateField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Medicine(models.Model):
    medicineid = models.CharField(max_length=8, primary_key=True)
    medicinename = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)

    def __str__(self):
        return self.medicinename


class Treatment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
