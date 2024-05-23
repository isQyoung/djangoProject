import pandas as pd
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from accountStorage.untils.forms import UserModelForm
from accountStorage.models import AccountPassword
from accountStorage.untils.auth import login_check


@login_check
def account_list(request):
    """用户列表"""
    # for i in range(20):
    #     account = {
    #         "name": "测试账号{}".format(i),
    #         "username": "test{}".format(i),
    #         "password": "password{}".format(i),
    #         "note": "测试备注{}".format(i)
    #     }
    #     AccountPassword.objects.create(**account)
    #     AccountPassword.objects.filter(username="test{}".format(i)).delete()
    data = {}
    search_data = request.GET.get('search', "")
    if search_data:
        data["username__contains"] = search_data
    form = UserModelForm()
    data_list = AccountPassword.objects.filter(**data).order_by("id")
    paginator = Paginator(data_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    keys = AccountPassword._meta.fields
    keys_list = [keys[i].verbose_name for i in range(len(keys))]
    # keys_list = [keys[i].name for i in range(len(keys))]
    context = {
        "title": "账号列表",
        "search_data": search_data,
        "key_list": keys_list,
        "data_list": data_list,
        "page_obj": page_obj,
        "form": form,
        "excel_url": "/media/excel/account.xlsx",
    }
    return render(request, 'accountStorage/account.html', context)


@login_check
@csrf_exempt
def account_add(request):
    """添加用户 (ajax请求)"""
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


@login_check
def account_detail(request):
    """获取账号详情"""
    account_id = request.GET.get("id")
    row_dict = AccountPassword.objects.filter(id=account_id).values("name", "username", "password", "note").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在"})
    result = {"status": True, 'data': row_dict}
    return JsonResponse(result)


@login_check
@csrf_exempt
def account_edit(request):
    """账号编辑"""
    account_id = request.GET.get("id")
    row_object = AccountPassword.objects.filter(id=account_id).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在"})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


@login_check
@csrf_exempt
def account_delete(request):
    """账号删除"""
    account_id = request.GET.get('id')
    if not AccountPassword.objects.filter(id=account_id).exists():
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在"})
    AccountPassword.objects.filter(id=account_id).delete()
    return JsonResponse({"status": True, 'msg': "删除成功"})


@login_check
@csrf_exempt
def upload_ajax_excel(request):
    """ajax上传excel，读取数据写入数据库"""
    if request.method == 'POST':
        file_object = request.FILES.get('files')
        df = pd.read_excel(file_object, keep_default_na=False)
        print(df)
        for i in df.index.values:
            df_dict = df.loc[i, ["name", "username", "password", "note"]].to_dict()
            print(df_dict)
            AccountPassword.objects.create(**df_dict)
        return redirect("accountStorage:account_list")
    return JsonResponse({'status': False, 'error': 'excel异常'})
