from django import forms
from .models import Employee, Hospital, Supplier, Patient, Medicine, Treatment

# ログインフォーム
class LoginForm(forms.Form):
    user_id = forms.CharField(label='ユーザーID', max_length=8, required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)

# 従業員登録フォーム
class EmployeeRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='パスワード（確認用）')

    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'password', 'role']
        labels = {
            'username': '従業員ID',
            'first_name': '名',
            'last_name': '姓',
            'password': 'パスワード',
            'role': 'ロール',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("パスワードが一致しません")
        return cleaned_data

# 従業員更新フォーム（従業員登録フォームからパスワードとロールを除いたもの）
class EmployeeUpdateForm(EmployeeRegistrationForm):
    class Meta(EmployeeRegistrationForm.Meta):
        fields = ['first_name', 'last_name']

# 他病院登録フォーム
class HospitalRegistrationForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['hospital_id', 'hospital_name', 'hospital_address', 'phone_number', 'capital', 'emergency']
        labels = {
            'hospital_id': '病院ID',
            'hospital_name': '病院名',
            'hospital_address': '住所',
            'phone_number': '電話番号',
            'capital': '資本金',
            'emergency': '救急対応',
        }

# 他病院更新フォーム（他病院登録フォームから病院IDを除いたもの）
class HospitalUpdateForm(HospitalRegistrationForm):
    class Meta(HospitalRegistrationForm.Meta):
        exclude = ['hospital_id']

# 患者登録フォーム
class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_id', 'last_name', 'first_name', 'gender', 'birthdate', 'insurance_number', 'insurance_exp']
        labels = {
            'patient_id': '患者ID',
            'last_name': '姓',
            'first_name': '名',
            'gender': '性別',
            'birthdate': '生年月日',
            'insurance_number': '保険証番号',
            'insurance_exp': '保険証有効期限',
        }

# 患者保険証変更フォーム
class PatientInsuranceChangeForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['insurance_number', 'insurance_exp']
        labels = {
            'insurance_number': '保険証番号',
            'insurance_exp': '保険証有効期限',
        }

# 薬剤投与指示フォーム
class MedicationInstructionForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['medicine', 'quantity']
        labels = {
            'medicine': '薬剤',
            'quantity': '数量',
        }
