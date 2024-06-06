from django import forms
from .models import Employee, Hospital, Supplier, Patient, Medicine, Treatment


class LoginForm(forms.Form):
    user_id = forms.CharField(label='ユーザーID', max_length=8, required=True)
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput, required=True)


# 従業員登録フォーム (E101)
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


# 従業員更新フォーム (E102)
class EmployeeUpdateForm(EmployeeRegistrationForm):
    class Meta(EmployeeRegistrationForm.Meta):
        fields = ['first_name', 'last_name']  # パスワードとロールは変更不可


# 他病院登録フォーム (H101)
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

    def clean_capital(self):
        capital = self.cleaned_data['capital']
        try:
            capital = int(capital)
            if capital < 0:
                raise forms.ValidationError('資本金は0以上の数値を入力してください。')
            return capital
        except ValueError:
            raise forms.ValidationError('資本金には数値を入力してください。')


# 他病院更新フォーム (H105)
class HospitalUpdateForm(HospitalRegistrationForm):
    class Meta(HospitalRegistrationForm.Meta):
        exclude = ['hospital_id']  # 病院IDは変更不可


# 患者登録フォーム (P101)
class PatientRegistrationForm(forms.ModelForm):
    confirm_insurance_number = forms.CharField(label='保険証記号番号（確認用）', max_length=64, required=True)

    class Meta:
        model = Patient
        fields = ['patient_id', 'last_name', 'first_name', 'gender', 'birthdate', 'insurance_number', 'insurance_exp']
        labels = {
            'patient_id': '患者ID',
            'last_name': '姓',
            'first_name': '名',
            'gender': '性別',
            'birthdate': '生年月日',
            'insurance_number': '保険証記号番号',
            'insurance_exp': '有効期限',
        }

    def clean(self):
        cleaned_data = super().clean()
        insurance_number = cleaned_data.get("insurance_number")
        confirm_insurance_number = cleaned_data.get("confirm_insurance_number")

        if insurance_number and confirm_insurance_number and insurance_number != confirm_insurance_number:
            raise forms.ValidationError("保険証記号番号が一致しません")
        return cleaned_data


# 患者保険証変更フォーム (P102)
class PatientInsuranceChangeForm(forms.ModelForm):
    confirm_insurance_number = forms.CharField(label='保険証記号番号（確認用）', max_length=64, required=True)

    class Meta:
        model = Patient
        fields = ['insurance_number', 'insurance_exp']
        labels = {
            'insurance_number': '保険証記号番号',
            'insurance_exp': '有効期限',
        }

    def clean(self):
        cleaned_data = super().clean()
        insurance_number = cleaned_data.get("insurance_number")
        confirm_insurance_number = cleaned_data.get("confirm_insurance_number")

        if insurance_number and confirm_insurance_number and insurance_number != confirm_insurance_number:
            raise forms.ValidationError("保険証記号番号が一致しません")
        return cleaned_data


# 薬剤投与指示フォーム (D101)
class MedicationInstructionForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['medicine', 'quantity']
        labels = {
            'medicine': '薬剤',
            'quantity': '数量',
        }

    def __init__(self, *args, medicines=None, **kwargs):  # medicines を引数に追加
        super().__init__(*args, **kwargs)
        if medicines:
            self.fields['medicine'].queryset = medicines  # ビュー関数から渡された medicines を使用する


# forms.py
class HospitalUpdateForm(HospitalRegistrationForm):
    class Meta(HospitalRegistrationForm.Meta):
        exclude = ['hospital_id']  # hospital_id を除外
