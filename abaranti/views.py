from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, EmployeeRegistrationForm, EmployeeUpdateForm, HospitalRegistrationForm, HospitalUpdateForm, PatientRegistrationForm, PatientInsuranceChangeForm, MedicationInstructionForm
from .models import Employee, Patient, Hospital, Treatment, Medicine
from django.db.models import Q
from datetime import date
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password

# -------------------------------------------------------------------
# ログイン機能 (L101)
# -------------------------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']

            user = authenticate(request, username=user_id, password=password)

            if user is not None:
                login(request, user)
                if user.role == Employee.Role.RECEPTION:
                    return redirect('menu_reception')
                elif user.role == Employee.Role.DOCTOR:
                    return redirect('menu_doctor')
            else:
                messages.error(request, 'ユーザーIDまたはパスワードが正しくありません。')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def error_view(request):
    error_message = "ユーザーIDまたはパスワードが正しくありません。"
    return render(request, 'error.html', {'error_message': error_message})

# -------------------------------------------------------------------
# 従業員管理機能 (E101, E102)
# -------------------------------------------------------------------
@login_required
def employee_register(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            # パスワードの一致確認と従業員IDの重複確認
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                messages.error(request, 'パスワードが一致しません。')
            elif Employee.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, 'この従業員IDは既に登録されています。')
            else:
                # ハッシュ化されたパスワードで保存
                form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
                # 登録確認画面にリダイレクト
                request.session['form_data'] = form.cleaned_data
                return redirect('employee_registration_confirm')
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'employee_registration.html', {'form': form})

@login_required
def employee_registration_confirm(request):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            # 登録処理
            form_data = request.session.get('form_data')
            Employee.objects.create_user(**form_data)
            del request.session['form_data']
            messages.success(request, '従業員を登録しました。')
            return redirect('employee_register')  # 登録画面に戻る
        elif 'back' in request.POST:
            # 登録画面に戻る
            return redirect('employee_register')
    else:
        form_data = request.session.get('form_data')
        if not form_data:
            # セッションにデータがない場合はエラー
            return redirect('employee_register')

    return render(request, 'employee_registration_confirm.html', {'form_data': form_data})

@login_required
def employee_update(request):
    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            # 変更確認画面にリダイレクト
            request.session['form_data'] = form.cleaned_data
            return redirect('employee_update_confirm')
    else:
        form = EmployeeUpdateForm(instance=request.user)
    return render(request, 'employee_update.html', {'form': form})

@login_required
def employee_update_confirm(request):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            # 変更処理
            form_data = request.session.get('form_data')
            employee = request.user
            employee.first_name = form_data['first_name']
            employee.last_name = form_data['last_name']
            employee.save()
            del request.session['form_data']
            messages.success(request, '従業員情報を変更しました。')
            return redirect('menu')  # メニュー画面に戻る
        elif 'back' in request.POST:
            # 変更画面に戻る
            return redirect('employee_update')
    else:
        form_data = request.session.get('form_data')
        if not form_data:
            # セッションにデータがない場合はエラー
            return redirect('employee_update')

    return render(request, 'employee_update_confirm.html', {'form_data': form_data})

# -------------------------------------------------------------------
# 他病院管理機能 (H101, H102, H104, H105)
# -------------------------------------------------------------------
@login_required
def hospital_register(request):
    if request.method == 'POST':
        form = HospitalRegistrationForm(request.POST)
        if form.is_valid():
            # 病院IDの重複確認
            if Hospital.objects.filter(hospital_id=form.cleaned_data['hospital_id']).exists():
                messages.error(request, 'この病院IDは既に登録されています。')
            else:
                # 登録確認画面にリダイレクト
                request.session['form_data'] = form.cleaned_data
                return redirect('hospital_registration_confirm')
    else:
        form = HospitalRegistrationForm()
    return render(request, 'hospital_registration.html', {'form': form})

@login_required
def hospital_registration_confirm(request):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            # 登録処理
            form_data = request.session.get('form_data')
            Hospital.objects.create(**form_data)
            del request.session['form_data']
            messages.success(request, '病院を登録しました。')
            return redirect('hospital_register')  # 登録画面に戻る
        elif 'back' in request.POST:
            # 登録画面に戻る
            return redirect('hospital_register')
    else:
        form_data = request.session.get('form_data')
        if not form_data:
            # セッションにデータがない場合はエラー
            return redirect('hospital_register')
    return render(request, 'hospital_registration_confirm.html', {'form_data': form_data})

@login_required
def hospital_list(request):
    hospitals = Hospital.objects.all()
    paginator = Paginator(hospitals, 10)  # 1ページあたり10件表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hospitalitiran.html', {'page_obj': page_obj})

@login_required
def hospital_search_by_capital(request):
    if request.method == 'POST':
        capital = request.POST['capital']
        try:
            capital = int(capital)
            hospitals = Hospital.objects.filter(capital__gte=capital)
            return render(request, 'hospital_search_result.html', {'hospitals': hospitals})
        except ValueError:
            messages.error(request, '資本金には数値を入力してください。')
    return render(request, 'hospital_search_by_capital.html')

@login_required
def hospital_update(request, hospital_id):
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    if request.method == 'POST':
        form = HospitalUpdateForm(request.POST, instance=hospital)
        if form.is_valid():
            # 変更確認画面にリダイレクト
            request.session['form_data'] = form.cleaned_data
            return redirect('hospital_update_confirm', hospital_id=hospital_id)
    else:
        form = HospitalUpdateForm(instance=hospital
