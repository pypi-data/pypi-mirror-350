# server.py
import os
from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any
import httpx
from datetime import datetime
import json

api_url = "https://report.hzzzwl.com"

# Create an MCP server
mcp = FastMCP("hzzzwl-agriculture-mcp-x")


def post_form_request(url: str, form_data: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
    """
    发送 x-www-form-urlencoded 格式的 POST 请求，并返回 JSON 响应
    
    :param url: 请求的目标 URL
    :param form_data: 表单参数字典（例如 {"key1": "value1"}）
    :param kwargs: 其他传递给 `httpx.post` 的参数（如 headers、timeout 等）
    :return: 解析后的 JSON 字典，请求失败时返回 None
    """
    try:
        # 发送 POST 请求
        response = httpx.post(
            url,
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            **kwargs
        )
        response.raise_for_status()  # 检查 4xx/5xx 错误
        return response.json()
    
    except httpx.RequestError as e:
        print(f"请求失败: {e}")  # 网络问题（如 DNS 解析失败、连接超时）
    except httpx.HTTPStatusError as e:
        print(f"HTTP 错误: {e.response.status_code} {e.response.text}")  # 状态码非 2xx
    except (ValueError, TypeError) as e:
        print(f"JSON 解析失败: {e}")  # 响应内容不是有效 JSON
    
    return None


def check_token() -> Optional[Dict[str, Any]]:

    api_key = os.getenv("KEY")

    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=checkToken"
    test_data = {"token": api_key}
    # 发送请求
    result = post_form_request(test_url, test_data)

    return result

@mcp.tool()
def get_now_time() -> Optional[Dict[str, Any]]:
    """获取当前时间"""

    check_t = check_token()
    if check_t['success'] != 1:
        mjson = {"data":'','code':'200','msg':'鉴权失败'}
        json_str = json.dumps(mjson, ensure_ascii=False)  # 关键设置
        return json_str,200,{"Content-Type":"application/json","Server":"None"}

    current_time = datetime.now()
    # 格式化时间（自定义输出格式）
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    mjson = {"data":formatted_time,'code':'200','msg':'ok'}
    json_str = json.dumps(mjson, ensure_ascii=False)  # 关键设置
    return json_str,200,{"Content-Type":"application/json","Server":"None"}

@mcp.tool()
def get_monitor_task_info(areaName: str,taskName:str) -> Optional[Dict[str, Any]]:
    """根据区划：areaName和任务：taskName，获得该地区该监测任务的完成情况，并给出下一年的任务安排建议。
    返回json格式的数据，详细内容都在message字段中。"""

    api_key = os.getenv("KEY")
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getJcQ4"
    test_data = {"areaName": areaName, "taskName": taskName,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_monitor_product_weather_info(areaName: str,productName:str) -> Optional[Dict[str, Any]]:
    """根据区划：areaName和产品名称：productName，获得该地区该产品的检测情况，以及近期的降雨量。
    探究降雨量与农产品检测情况的关系，返回json格式数据，其中list为jsonarray，里面包含sampling_date：抽样日期,
    all_num:抽样批次数量，qualified_num：合格批次数量，qualified_rat：合格率，last_7days_rainfall：近7日降雨量，单位mm。
    """
    api_key = os.getenv("KEY")
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getJcQ3"
    test_data = {"areaName": areaName, "cpname": productName,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_agricultural_sale_buy_amount(areaName: str,productName:str) -> Optional[Dict[str, Any]]:
    """根据区划：areaName和农资产品名称：productName，获得该地区该农资产品的购买量和销售量。
    返回json格式数据，其中list为jsonarray，里面包含year：年份,totalBuy：购买量kg，totalSale：销售量kg，
    name：农资产品名称。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/mcp_server1/api/zzchat/saleYearStatisticsAjax.do"
    test_data = {"areaName": areaName, "name": productName,"tag":"zz_chat_cbq","token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_monitor_agricultural_info(areaName: str,productName:str,ypname:str) -> Optional[Dict[str, Any]]:
    """根据区划：areaName和农资产品名称：ypname，农产品名称：productName，获得该地区该农资产品在该农产品上的检测情况。
    返回json格式数据，其中list为jsonarray，里面包含year：年份,all_num：检测批次，qualified_num：合格批次，
    qualified_rat：合格率。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getJcQ1"
    test_data = {"areaName": areaName, "cpname": productName,"ypname":ypname,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_medications_by_product(productName:str) -> Optional[Dict[str, Any]]:
    """根据农产品名称：productName，获得该农产品上的常见用药。
    返回json格式数据，其中list为jsonarray，里面包含content：常见用药。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getCjyy"
    test_data = {"cpname": productName,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_medication_value(productName:str,medicationName:str) -> Optional[Dict[str, Any]]:
    """根据农产品名称：productName和药物名称：medicationName，获得该农产品上的该药物的检出限(检出上限)。
    返回json格式数据，其中list为jsonarray，里面包含unit：单位，pd：检出限，aname：药物名称，name：农产品名称
    ，value：检出限具体的值。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/mcp_server2/cellphone/getData.do?sysCmd=getJcx"
    test_data = {"cpname": productName,"ypname":medicationName,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_agricultural_guidance_vector(text: str) -> Optional[Dict[str, Any]]:
    """根据用户的问题：text从农事指导的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """
    api_key = os.getenv("KEY")
    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"nszd"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_agricultural_disease_report_vector(text: str) -> Optional[Dict[str, Any]]:
    """根据用户的问题：text从病虫测报及防治建议的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """
    api_key = os.getenv("KEY")
    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"bccb"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_agricultural_case_vector(text: str) -> Optional[Dict[str, Any]]:
    """根据用户的问题：text从农业典型案件的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """
    api_key = os.getenv("KEY")
    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"nydxal"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def get_agricultural_growth_model_vector(text: str) -> Optional[Dict[str, Any]]:
    """根据用户的问题：text从农作物生长模式(如：生长环境选择，品种选择，生长期注意事项，常见病虫害防治等)的向量库中查找出几段最近似的内容，需要你归纳总结形成答案给用户。
    返回json格式数据，其中data为jsonarray，里面包含content：近似的内容。
    从content中选取跟用户的问题相关的内容总结后返回给用户，无关的舍弃不要。
    """
    api_key = os.getenv("KEY")
    test_url = api_url+"/getNszdContent"
    test_data = {"text": text,"token":api_key,"tag":"szms"}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result


@mcp.tool()
def getNyInfo(name:str,djzh:str) -> Optional[Dict[str, Any]]:
    """根据农药名称：name和登记证号：djzh，获得该农药的基本信息,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含hzrq：核准日期，ccysff：储存和运输方法，shengCQY：登记证持有人(生产企业)，
    dux：毒性，description：备注，cpxn：产品性能，yxqz：有效期至，nylb：农药类别，
    zxhzrq：重新核准日期，name：农药名称，jix：剂型，zdjjcs：中毒急救措施，bzq：质量保证期，
    djzh：登记证号，zyxcfhl：总有效成分含量，zysx：注意事项，syjsyq：使用技术要求。
    """
    api_key = os.getenv("KEY")
    test_url = api_url+"/zzdata/api/zzdata/getNyInfo.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def getNyChengF(name:str,djzh:str) -> Optional[Dict[str, Any]]:
    """根据农药名称：name和登记证号：djzh，获得该农药的主要有效成分,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含name_cn：有效成分中文名，name_en：有效成分英文名，hanl：有效成分含量。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/zzdata/api/zzdata/getNyChengF.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def getNyShengCQY(name:str,djzh:str) -> Optional[Dict[str, Any]]:
    """根据农药名称：name和登记证号：djzh，获得该农药的生产企业信息,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含name：企业名称，province：企业所在省份，country：企业所在国家，county：企业所在县，
    postcode：邮编，tel：电话，fox：传真，contact：联系人，phone：手机号码，addr：单位地址，
    email：邮箱。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/zzdata/api/zzdata/getNyShengCQY.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def getNyUseInfo(name:str,djzh:str) -> Optional[Dict[str, Any]]:
    """根据农药名称：name和登记证号：djzh，获得该农药的使用范围和使用方法,登记证号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含crops：作物/场所，fzdx：防治对象，dosage：用药量（制剂量/亩），syff：施用方法。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/zzdata/api/zzdata/getNyUseInfo.do"
    test_data = {"name": name,"djzh":djzh,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def getFlInfo(name:str,bah:str) -> Optional[Dict[str, Any]]:
    """根据肥料名称：name和备案号：bah，获得该肥料的基本信息,备案号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含tymcName：产品通用名称，productfromname：产品形态，enterprisename：企业名称，
    keeprecordnum：备案号，keeprecordtime：备案时间，technicalindex：技术指标，
    frmCpbaSyzwEntityList：适宜作物，commodityname：产品商品名称，effectivestrains：有效菌种名称，
    rtindicators：登记技术指标，suitablerange：适宜范围，rcnumber：登记证号，rcvp：登记证有效期。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/zzdata/api/zzdata/getFlInfo.do"
    test_data = {"name": name,"bah":bah,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

@mcp.tool()
def getFlUseInfo(name:str,bah:str) -> Optional[Dict[str, Any]]:
    """根据肥料名称：name和备案号：bah，获得该肥料适合施用的作物,备案号不必填。
    返回json格式数据，其中list为jsonarray，
    里面包含name：作物名称。"""
    api_key = os.getenv("KEY")
    test_url = api_url+"/zzdata/api/zzdata/getFlUseInfo.do"
    test_data = {"name": name,"bah":bah,"token":api_key}
    
    # 发送请求
    result = post_form_request(test_url, test_data)
    return result

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()