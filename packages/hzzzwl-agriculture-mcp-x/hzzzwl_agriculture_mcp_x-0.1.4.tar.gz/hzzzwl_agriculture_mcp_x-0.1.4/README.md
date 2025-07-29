# 农业信息服务 MCP Server

## 概述
农业信息服务MCP Server，包含16个符合MCP协议标准的API接口，涵盖农产品检测信息、农资产品购销信息、农事指导信息等。

依赖MCP Python SDK开发，任意支持MCP协议的智能体助手（如Claude、Cursor以及Cherry Studio等）都可以快速接入。

## 工具
### 农产品常见用药 get_medications_by_product
根据农产品名称，获得该农产品上的常见用药。
**输入**:
- `productName` 农产品
**输出**: 常见用药，包含`content`等

### 农产品药物检出限 get_medication_value
根据农产品名称和药物名称，获得该农产品上的该药物的检出限(检出上限)。  
**输入**:
- `productName` 农产品
- `medicationName` 药物
**输出**: 检出限，包含`name`, `value`, `unit`等

### 农事指导信息 get_agricultural_guidance_vector
根据用户问题，获得农事指导意见。
**输入**:
- `text` 问题
**输出**: 农事指导意见，包含`content`等

### 病虫测报及防治建议 get_agricultural_disease_report_vector
根据用户问题，获得病虫测报及防治建议。
**输入**: `text` 问题  
**输出**: 病虫测报及防治建议，包含`content`等

### 农业典型案例信息 get_agricultural_case_vector
根据用户问题，获得农业典型案例信息。
**输入**:
- `text` 问题
**输出**: 农业典型案例信息，包含`content`等

### 农作物生长模式信息 get_agricultural_growth_model_vector
根据用户问题，获得农作物生长模式信息。
**输入**:
- `text` 问题
**输出**: 农作物生长模式信息，包含`content`等

### 农药基本信息 getNyInfo
根据农药名称和登记证号获取农药的基本信息。
**输入**:
- `name` 农药
- `djzh` 登记证号  
**输出**: 农药基本信息，包含`name`, `jix`,`yxqz`等

### 农药成分 getNyChengF
根据农药名称和登记证号获取农药的主要成分。
**输入**: 
- `name` 农药
- `djzh` 登记证号    
**输出**：农药成分，包含`name_cn`, `hanl`等

### 农药生产企业 getNyShengCQY
根据农药名称和登记证号获取农药的生产企业。
**输入**: 
- `name` 农药
- `djzh` 登记证号    
**输出**：生产企业，包含`name`, `addr`,`contact`,`phone`等

### 农药使用范围和使用方法 getNyUseInfo
根据农药名称和登记证号获取农药的使用范围和使用方法。
**输入**: 
- `name` 农药
- `djzh` 登记证号    
**输出**：使用范围和使用方法，包含`crops`, `fzdx`,`dosage`,`syff`等

### 肥料基本信息 getFlInfo
根据肥料名称和备案号获取肥料的基本信息。
**输入**: 
- `name` 肥料
- `bah` 备案号    
**输出**：肥料基本信息，包含`tymcName`, `productfromname`,`enterprisename`等

### 肥料适用范围 getFlUseInfo
根据肥料名称和备案号获取肥料的适用范围。
**输入**: 
- `name` 肥料
- `bah` 备案号    
**输出**：肥料适用范围，包含`name`等

### 某地监测任务完成情况及后续任务安排 get_monitor_task_info
获得该地区该监测任务的完成情况，并给出后续的任务安排建议。 
**输入**: 
- `areaName` 区划
- `taskName` 任务
**输出**: `message`

### 某地农产品检测情况及近期降雨量 get_monitor_product_weather_info
获得该地区农产品检测情况，近期降雨量。
**输入**: 
- `areaName` 区划
- `productName` 产品名称
**输出**: 检测情况，包含`sampling_date`, `qualified_rat`等，近7日降雨量，包含`last_7days_rainfall`。

### 某地农资产品的购买量和销售量 get_agricultural_sale_buy_amount
获得该地区农资产品的购买量和销售量。
**输入**:
- `areaName` 区划
- `productName` 农资产品
**输出**: 购买量和销售量，包含`name`, `totalBuy`, `totalSale`等

### 某地农资产品在农产品上的检测情况 get_monitor_agricultural_info
获得该地区该农资产品在该农产品上的检测情况。
**输入**:
- `areaName` 区划
- `productName` 农产品
- `ypname` 农资产品
**输出**: 检测情况，包含`all_num`, `qualified_rat`等



## 开始使用
使用农业信息服务MCP Server主要是用Python，下面开始介绍。

### 获取KEY
通过KEY你才能够调用农业信息服务MCP Server能力，请联系0571-88816415获取。

### Python接入
我们通过pypi发布了农业信息服务MCP Server：`hzzzwl-agriculture-mcp-x`，你可以使用任意Python包管理工具轻松获取并快速配置使用。

### 安装
使用uv时不需要特殊安装，我们将使用uvx直接运行`hzzzwl-agriculture-mcp-x`

### 配置
在任意MCP客户端（如Claude.app）中添加如下配置，部分客户端下可能需要做一些格式化调整。
`{
  "mcpServers": {
    "hzzzwl-agriculture-mcp-x": {
      "command": "uvx",
      "args": ["hzzzwl-agriculture-mcp-x"],
      "env": {
        "KEY": "<YOUR_API_KEY>"
      }
    }
  }
}`
其中YOUR_API_KEY对应的值需要替换为你自己的KEY。保存配置后，重启你的MCP客户端，即可使用农业信息服务MCP Server。

### 示例
问题：我想知道草甘膦的使用方法
答案：
根据提供的数据，该农药的使用信息如下：

#### 适用作物
- 剑麻
- 林木
- 果园
- 桑园
- 橡胶园
- 甘蔗田
- 茶园

#### 防治对象
- 一年生杂草
- 多年生恶性杂草

#### 施用方法
- 喷雾

#### 用药量
- 每亩使用250-500毫升（所有适用作物及防治对象均相同）。

以上信息均来自数据中的具体条目。