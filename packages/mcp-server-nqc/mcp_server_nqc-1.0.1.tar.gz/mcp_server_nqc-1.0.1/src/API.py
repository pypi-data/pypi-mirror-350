# encoding=utf8
# import mcp_server_baidu_maps
import json
import os
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, create_model
from AsyncMyRequest import AsyncQueryCompany
from company_super_search import company_super_search

# 默认凭据
DEFAULT_CLIENT_ID = ""
DEFAULT_CLIENT_KEY = ""

# JSON Schema 到 Python 类型映射
type_mapping = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
}

schema = [
  {
    "url": "http://openapi.bainiudata.com/openapi/common/get_entid/",
    "function": {
      "name": "工商信息-A001-精确获取企业唯一标识(批量)",
      "description": "根据企业名称、注册号、统一社会信用代码或组织机构代码，批量获取企业唯一标识。唯一标识可用于查询这家企业的各维度数据！",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号（企业之间以英文逗号分隔） 示例：小米科技有限责任公司,蚂蚁科技集团股份有限公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/mohu/",
    "function": {
      "name": "工商信息-A002-企业模糊查询",
      "description": "提供企业信息的模糊查询服务，即通过部分或不完全的信息快速检索出符合条件的企业列表，支持用户进行初步筛选和识别。 ### 根据关键字名称模糊搜索匹配企业 ##### 参数说明 \"must\" : 包含以下所有条件， \"should\": 包含以下任意条件 \"any\": 只要满足筛选条件里面的一个就可以 \"all\":筛选条件都要满足 \"not\":排除筛选条件 ``` { \"dsl_query\": { \"should\": [ # 企业名称 {\"main__ENTNAME\": {\"any\": [\"小米\"]}}, # 企业统一代码 # {\"main__UNISCID\": {\"any\": [\"91420100MA4KWE6L5W\",]}}, # 企业类型 # {\"main__ENTTYPE\": {\"any\": [\"10300\",\"10200\"]}}, # 企业状态 # {\"main__ENTSTATUS\": {\"any\": [1,]}}, # 企业地区 # {\"main__region_id\": {\"any\": [\"360924\",]}}, # 统一社会信用代码 # {\"main__UNISCID\": {\"any\": [\"92410122MA9H5R2EPY\"]}}, # 企业规模 # {\"should\": [{\"mainclass__VENDINC\": {\"range\": [\"0\", \"100\"]}}, # {\"mainclass__VENDINC\": {\"range\": [\"500\", \"1000\"]}}]}, # 效益评估 # {\"should\": [{\"mainclass__RATGRO\": {\"range\": [\"0\", \"50\"]}}, # {\"mainclass__RATGRO\": {\"range\": [\"50\", \"50\"]}}]}, # # 有无融资事件 0表示无 1 有 # {\"if__vc\": {\"exist\": \"1\"}}, # # 联系方式筛选 55 手机 56 座机 57 邮箱 # {\"mainclass__SOCNUM\": {\"range\": [\"50\", \"99\"]}}, # {\"main__dataindex\": {\"all\": [\"-55-\", \"-56-\", \"-57-\"]}}, # # 地区筛选 # {\"main__region_id\": {\"any\": [\"110000\", \"120000\"]}}, # # 行业筛选 # {\"main__nic_id\": {\"any\": [\"I\", \"A\"]}}, # # 注册资本 # {\"should\": [{\"main__REGCAP\": {\"range\": [\"0\", \"50\"]}}]}, # # 行业筛选 # {\"others__nic_id\": {\"any\": [\"I\"]}}, # # 圆 # {\"others__gis\": {\"circle\": {\"radius\": \"1000\", \"center\": {\"lon\": 106.561305, \"lat\": 29.513027}}}}, # # 多边形 # {\"others__gis\": {\"polygon\": [ # {\"lon\": 106.561305, \"lat\": 29.513027}, {\"lon\": 107.561305, \"lat\": 29.513027}, # {\"lon\": 106.561305, \"lat\": 39.513027}, {\"lon\": 107.561305, \"lat\": 39.513027}]}}, # # 注册时间 range数组 第一位表示大于等于 第二位 小于等于 对应没有的传空字符串 # {\"should\": [{\"main__ESDATE\": {\"range\": [\"2021-01-01\", \"2022-01-01\"]}}, # {\"main__ESDATE\": {\"range\": [\"2018-01-01\", \"2022-01-01\"]}}]}, # # 上市状态 \"-10-\":A股 \"-11-\":B股 \"-12-\":新三板 \"-13-\":港股 \"-14-\":科创板 \"-15-\":美股 # {\"main__tags\": {\"any\": [\"-10-\", \"-11-\", \"-12-\"]}}, # # 科技标签 \"-1500390-\":高新技术企业 \"-10310403-\":瞪羚 \"-6694189-\":小巨人 \"-3488916-\":专精特新 \"-9785705-\":独角兽 \"-10526903-\":科技型中小企业 # {\"main__tags\": {\"any\": [\"-1500390-\", \"-6694189-\"]}}, # # 融资轮次 天使轮、A轮、B轮、C轮、D轮、E轮、F轮-上市前 # {\"vc__invse_round_name\": {\"any\": [\"A轮\", \"B轮\"]}}, ], }, \"sort\": {\"elindex_1\": {\"order\": \"desc\"}}, # 排序参数，算法排序 # \"sort\": {\"_geo_distance\": {\"geo\": {\"lat\": 29.513027,\"lon\": 106.561305},\"order\":\"asc\",\"unit\":\"m\",\"distance_type\": \"plane\"}}, # 排序参数，距离远近算法 \"highlight\": {\"fields\": {\"faren\": {}}}, # 高亮参数 \"page_index\": \"1\", \"page_size\": \"10\" }  通常情况下，企业模糊查询只用于匹配用户给的关键词，查询出与关键词相关的这些企业列表```",
      "parameters": {
        "type": "object",
        "properties": {
          "data": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号/经营范围/企业类型等 示例：{    \"dsl_query\": {        \"must\": [            {                \"main__ENTNAME\": {                    \"all\": [                        \"小米\",                        \"科技\"                    ]                }            }        ]    }}"
          }
        },
        "required": [
          "data"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/related_multi/",
    "function": {
      "name": "工商信息-A007-企业关系链",
      "description": "通过输入企业A、企业B的关系参数及查询方式，获取企业及其关联实体之间的关系链详情，默认查询深度为4层。",
      "parameters": {
        "type": "object",
        "properties": {
          "related_args": {
            "type": "string",
            "description": "关系参数||（\"e\"：企业类型，\"p\"：企业+人名类型；\"type\"为\"p\"时,\"key\"传参必须是\"Jou8WJXg4A-林斌\"格式） 示例：[{\"type\":\"e\",\"key\":\"CiNVInEzl2\"},{\"type\":\"e\",\"key\":\"KUdZyNoVbq\"}]"
          },
          "tab": {
            "type": "string",
            "description": "查询方式||（\"A\"：关联路径，\"B\"：关系追踪；默认为\"A\"） 示例：A"
          },
          "depth": {
            "type": "string",
            "description": "穿透层次||（\"tab\"传参为\"A\"时该传参才生效，默认为\"4\"） 示例：4"
          }
        },
        "required": []
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_bank/",
    "function": {
      "name": "工商信息-A018-税务发票抬头信息",
      "description": "跟据企业名称、统一社会信用代码或注册号等关键字进行搜索，查询企业的税务发票抬头信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/get_entid_individual/",
    "function": {
      "name": "工商信息-A031-精确获取企业唯一标识(单条)",
      "description": "根据企业名称、注册号、统一社会信用代码或组织机构代码，获取企业唯一标识。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/hk_enterprise_search/",
    "function": {
      "name": "工商信息-A053-香港企业查询",
      "description": "允许用户通过企业名称、注册日期和主体状态为入参，快速获取香港企业的详细信息，此接口提供的数据包括但不限于主体名称、企业编号、注册日期、主体类型、主体状态、注销日期、联系方式、官网地址及主要人员等。",
      "parameters": {
        "type": "object",
        "properties": {
          "entname": {
            "type": "string",
            "description": "企业名称 示例：成穎有限公司"
          },
          "esdate": {
            "type": "string",
            "description": "注册日期 示例：2014-10-15$2024-10-02"
          },
          "entstatus": {
            "type": "string",
            "description": "主体状态 ||（1：仍注册  :3：已告解散:5： 已终止营业地点:8：休止活动 9：不再是独立的实体） 示例：1"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": []
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_search_mohu/",
    "function": {
      "name": "工商信息-A067-企业模糊查询(简版)",
      "description": "通过搜索关键字（企业名或统一社会信用代码）获取匹配搜索条件的企业列表信息，返回包括但不限于企业名称、法定代表人名称、企业状态、成立日期、统一社会信用代码、注册号等信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业名称/统一社会信用代码 示例：小米科技有限公司"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": []
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/search_company_info/",
    "function": {
      "name": "工商信息-A068-组织机构查询-T",
      "description": "通过输入社会信用代码或组织机构代码（两者之一必传），获取组织机构的详细信息，包括但不限于经营范围、生产经营地址（参考项）、职工人数（参考项）、上级主管部门（参考项）、经营状态等信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "uniscid": {
            "type": "string",
            "description": "统一社会信用代码和组织机构代码必传其一 示例：52511900MJQ71099XD"
          },
          "org_code": {
            "type": "string",
            "description": "组织机构代码 示例：MJQ71099X"
          },
          "entname": {
            "type": "string",
            "description": "企业名称 示例：巴中残疾人康复医院"
          }
        },
        "required": [
          "uniscid",
          "org_code",
          "entname"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_info_deep_search/",
    "function": {
      "name": "工商信息-A071-企业信息深度查询",
      "description": "可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业多维度详细信息，包括但不限于企业名称、曾用名、英文名称、统一社会信用代码、注册号、法定代表人、成立日期、国民经济行业代码及名称、注册资本、实收资本、登记机关、经营状态、企业类型、经营期限、省份、城市、区县、邮箱、地址、许可经营项目、经营范围、年检年度、联系电话、员工人数、吊销日期、注销日期、核准日期、地区名称及编码、企业类型编码、行业门类代码及名称、法人类型、注册资本名称（GS）、经营场所、一般经营项目、纳税人类型、二级至四级行业分类、企业logo、参保人数、企业官网、地理坐标（高德经纬度）、纳税信用评级、组织机构批准单位、销售收入、是否上市、上市时间、A级纳税人年份、企业基本信息、主要管理人员及其职位、分支机构信息、变更事项及内容等。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          }
        },
        "required": []
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/enterprise_classification/",
    "function": {
      "name": "工商信息-A070-企业大中小微划型",
      "description": "通过输入企业名称或统一社会信用代码，快速获取企业的规模类型信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          }
        },
        "required": []
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/bid_professional_search/",
    "function": {
      "name": "经营信息-A021-招投标精准查询",
      "description": "通过输入企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行招投标信息的精准查询，返回包括但不限于公告标题、公告类型、区域、招标方、投标方、中标金额等关键数据。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/land_search/",
    "function": {
      "name": "经营信息-A027-土地资产查询",
      "description": "支持多个条件组合查询企业的土地资产详细信息，返回包括但不限于土地供应、项目位置、面积、用途、供地方式、土地使用年限等关键数据。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "sup_num\t": {
            "type": "string",
            "description": "电子监管号\t 示例：1102282010B00038,1102282010B00029"
          },
          "industry": {
            "type": "string",
            "description": "行业分类\t 示例：软件开发,专业技术服务业,医药制造业"
          },
          "tdate\t": {
            "type": "string",
            "description": "合同签订日期\t 示例：2012-10-15$2013-10-02"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": []
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/lesscredit_search/",
    "function": {
      "name": "法律诉讼-A025-失信被执行人查询",
      "description": "允许根据多个条件组合灵活查询失信被执行人（企业唯一标识、企业名称、统一社会信用代码或注册号、执行法院所在省份码值、被执行人姓名/名称、证件号码明文、案号及发布时间段），并返回案号、执行依据文号、履行情况等信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          },
          "sf": {
            "type": "string",
            "description": "执行法院所在省份码值 示例：343101"
          },
          "name": {
            "type": "string",
            "description": "被执行人姓名/名称 示例：杨朝荣"
          },
          "sfzh_all": {
            "type": "string",
            "description": "证件号码明文 示例："
          },
          "ah": {
            "type": "string",
            "description": "案号 示例：（2016）皖0102执1316号"
          },
          "fbdate_start": {
            "type": "string",
            "description": "发布时间(时间段开始值) 示例：2016-06-06"
          },
          "fbdate_end": {
            "type": "string",
            "description": "发布时间(时间段结束值) 示例：2017-06-06"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/execute_person/",
    "function": {
      "name": "法律诉讼-A060-被执行人（人员）查询",
      "description": "通过输入企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）以及被执行人姓名/名称，查询目标企业该人员的被执行相关数据。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          },
          "lp_name": {
            "type": "string",
            "description": "被执行人姓名/名称 示例：何勇"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": [
          "key",
          "lp_name"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/dishonest_execute_person/",
    "function": {
      "name": "法律诉讼-A061-失信被执行人（人员）查询",
      "description": "通过输入企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）以及失信被执行人姓名/名称，查询目标企业该人员的失信被执行相关数据。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：上海邵同实业有限公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          },
          "lp_name": {
            "type": "string",
            "description": "失信被执行人姓名/名称 示例：董文荣"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": [
          "key",
          "lp_name"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/officer_history_search/",
    "function": {
      "name": "幕后关联-A006-企业人员历史投资任职信息",
      "description": "可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取该人员在其他企业中担任的各种角色的具体情况，包括但不限于被投方企业名称、变更类型及日期、投资方个人/企业名称、变动前后的认缴金额和投资占比等详细信以及该人员作为历史股东的完整记录，包括其在不同企业的任职情况，如任职企业名称、职位中文、入职和离职日期等。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "name": {
            "type": "string",
            "description": "高管/股东名称 示例：雷军"
          },
          "is_out": {
            "type": "string",
            "description": "是否过滤未推出数据（\"0\": 不过滤，\"1\": 过滤） 示例：0"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/legal_inv_officer/",
    "function": {
      "name": "幕后关联-A019-法人对外投资任职信息",
      "description": "通过输入关键词（企业唯一标识、企业名称、统一社会信用代码或注册号以及法人姓名），获取法人在其他企业中担任法定代表人的信息，以及投资详情和对外任职情况。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "lp_name": {
            "type": "string",
            "description": "法人 示例：雷军"
          }
        },
        "required": [
          "key",
          "lp_name"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/inv_manager_individual/",
    "function": {
      "name": "幕后关联-A032-人员所有角色",
      "description": "全面获取特定人员在其他企业中的所有角色和活动情况，包括担任法定代表人、股东、高管以及个体工商户的详细信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "lp_name": {
            "type": "string",
            "description": "人员姓名 示例：雷军"
          }
        },
        "required": [
          "key",
          "lp_name"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/enterprise_genealogy/",
    "function": {
      "name": "幕后关联-A036-企业族谱",
      "description": "通过输入企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号），获取详尽的企业族谱数据，包含企业的基本信息和企业与关联实体（如股东、高管、投资公司等）之间的关系链。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/equity_penetration/",
    "function": {
      "name": "幕后关联-A059-股权穿透",
      "description": "通过输入企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号），并指定穿透层级（最多不超过四层），获取企业及其背后股东的多层次股权结构详情。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：苏宁电器集团有限公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "level": {
            "type": "string",
            "description": "穿透层级||最大不超过4层，不传默认返回4层 示例：2"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_lianxi_public/",
    "function": {
      "name": "通讯信息-A010-企业公开联系方式",
      "description": "通过输入企业相关参数（企业名称、统一社会信用代码或注册号），查询企业的公开联系方式，返回数据包括姓名、联系方式、职务及来源等关键信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "ltype": {
            "type": "string",
            "description": "联系方式类别||(\"1\", \"手机\"), (\"2\", \"座机\"), (\"3\", \"邮箱\") 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/lianxi_re_search/",
    "function": {
      "name": "通讯信息-A055-联系方式反查企业",
      "description": "通过输入一个或多个联系方式，快速查找并返回与之关联的企业信息。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "联系方式 示例：13343843120/67620540"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_lianxi_multi_source/",
    "function": {
      "name": "通讯信息-A066-企业多来源公开联系方式",
      "description": "可根据企业相关参数（企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号）及联系方式类别进行灵活查询，获得企业从多个来源获取的公开联系方式。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "ltype": {
            "type": "string",
            "description": "联系方式类别 ||(\"1\", \"手机\"), (\"2\", \"座机\"), (\"3\", \"邮箱\"), (\"4\", \"qq\"), (\"5\", \"微信号\"), (\"6\", \"传真\") 示例：1,2,4"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/investment_financing/",
    "function": {
      "name": "企业发展-A017-投融资事件查询",
      "description": "允许根据多个条件组合灵活查询目标企业在资本市场的活动情况，包括但不限于融资轮次、投资方、融资金额、投后估值等关键数据。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "page_index": {
            "type": "string",
            "description": "页码||不传默认1 示例：1"
          },
          "page_size": {
            "type": "string",
            "description": "页容量||不传默认20 示例：10"
          },
          "com_name": {
            "type": "string",
            "description": "融资公司简称 示例：小米集团"
          },
          "com_fullname": {
            "type": "string",
            "description": "融资公司全称 示例：小米科技有限责任公司"
          },
          "cat_name": {
            "type": "string",
            "description": "业务领域 示例：新工业"
          },
          "com_prov": {
            "type": "string",
            "description": "所属地区||（若是省级编码会过滤省级及以下所有地区，市区类似） 示例：110000,330000"
          },
          "invse_round_name": {
            "type": "string",
            "description": "融资轮次 示例：天使轮,A轮,B轮"
          },
          "invest_date": {
            "type": "string",
            "description": "融资时间 示例：2016-10-15$2021-12-16"
          }
        },
        "required": []
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/vc_search/",
    "function": {
      "name": "企业发展-A038-融资事件查询",
      "description": "支持多个条件组合灵活查询企业的融资事件，查询结果返回包括但不限于融资轮次、投资方、融资金额等关键数据。",
      "parameters": {
        "type": "object",
        "properties": {
          "ent_name": {
            "type": "string",
            "description": "融资公司 示例：小米科技"
          },
          "nic_name": {
            "type": "string",
            "description": "行业名称 示例：企业服务"
          },
          "vc_round": {
            "type": "string",
            "description": "投资的轮次ID 示例：A"
          },
          "region_name": {
            "type": "string",
            "description": "所在地区 示例：500000"
          },
          "vc_date": {
            "type": "string",
            "description": "投资日期 示例：2022"
          },
          "vc_country": {
            "type": "string",
            "description": "是否国内||(\"1\"国内，\"0\"国外,不传是全部) 示例：1"
          },
          "vc_currency": {
            "type": "string",
            "description": "投资金额的币种ID 示例：156"
          },
          "page_index": {
            "type": "string",
            "description": "页码 示例："
          },
          "page_size": {
            "type": "string",
            "description": "页容量 示例："
          }
        },
        "required": [
          "ent_name"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_growth_score_basic/",
    "function": {
      "name": "企业评价与标签-A014-企业基础成长得分",
      "description": "查询企业各个评分年份对应的基础成长得分（计算逻辑：int(纳税总额/20)。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_growth_score_senior/",
    "function": {
      "name": "企业评价与标签-A015-企业高级成长得分",
      "description": "查询企业各个评分年份对应的高级成长得分，返回数据包括企业详细的财务和运营指标。 得分算法取值范围：±0.03",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/f_asstesinfo/",
    "function": {
      "name": "企业评价与标签-A030-企业经营标签",
      "description": "根据年报年份获取企业的经营标签信息，返回企业的关键经营指标信息，如资产总额、负债总额、营业总收入等。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "ancheyear": {
            "type": "string",
            "description": "年报年份 示例：2022"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_operation_level/",
    "function": {
      "name": "企业评价与标签-A016-企业经营等级",
      "description": "根据评分年份获取企业的经营等级。 纳税总额登记说明： ``` { s == 0: \"A\", 0 < s < 2: \"B\", 2 <= s < 5: \"C\", 5 <= s < 20: \"D\", 20 <= s < 50: \"E\", 50 <= s < 100: \"F\", 100 <= s < 200: \"G\", 200 <= s < 300: \"H\", 300 <= s < 500: \"I\", 500 <= s < 800: \"J\", 800 <= s < 1000: \"K\", 1000 <= s < 1500: \"L\", 1500 <= s < 2000: \"M\", 2000 <= s < 3000: \"N\", 3000 <= s < 5000: \"O\", 5000 <= s < 10000: \"P\", 10000 <= s < 20000: \"Q\", 20000 <= s < 30000: \"R\", 30000 <= s < 50000: \"S\", s >= 50000: \"T\" } ```",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "ancheyear": {
            "type": "string",
            "description": "年报年份 示例：2020"
          }
        },
        "required": [
          "key",
          "ancheyear"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/ent_assets_tag_detail/",
    "function": {
      "name": "企业评价与标签-A033-企业经营资产标签",
      "description": "根据年报年份获取企业的经营资产标签信息，返回关键经营和资产指标信息。 ``` { value < -20000000: \"Q19\", -20000000 <= value < -13000000: \"Q18\", -13000000 <= value < -900000: \"Q17\", -900000 <= value < -600000: \"Q16\", -600000 <= value < -500000: \"Q15\", -500000 <= value < -400000: \"Q14\", -400000 <= value < -300000: \"Q13\", -300000 <= value < -250000: \"Q12\", -250000 <= value < -200000: \"Q11\", -200000 <= value < -190000: \"Q10\", -190000 <= value < -180000: \"Q9\", -180000 <= value < -170000: \"Q8\", -170000 <= value < -160000: \"Q7\", -160000 <= value < -150000: \"Q6\", -150000 <= value < -140000: \"Q5\", -140000 <= value < -130000: \"Q4\", -130000 <= value < -120000: \"Q3\", -120000 <= value < -110000: \"Q2\", -110000 <= value < -100000: \"Q1\", -100000 <= value < -90000: \"L184\", -90000 <= value < -80000: \"L183\", -80000 <= value < -70000: \"L182\", -70000 <= value < -60000: \"L181\", -60000 <= value < -50000: \"L180\", -50000 <= value < -40000: \"L179\", -40000 <= value < -30000: \"L178\", -30000 <= value < -20000: \"L177\", -20000 <= value < -15000: \"P2\", -15000 <= value < -10000: \"P1\", -10000 <= value < -9500: \"L175\", -9500 <= value < -9000: \"L174\", -9000 <= value < -8500: \"L173\", -8500 <= value < -8000: \"L172\", -8000 <= value < -7500: \"L171\", -7500 <= value < -7000: \"L170\", -7000 <= value < -6500: \"L169\", -6500 <= value < -6000: \"L168\", -6000 <= value < -5500: \"L167\", -5500 <= value < -5000: \"L166\", -5000 <= value < -4500: \"L165\", -4500 <= value < -4000: \"L164\", -4000 <= value < -3500: \"L163\", -3500 <= value < -3000: \"L162\", -3000 <= value < -2500: \"L161\", -2500 <= value < -2000: \"L160\", -2000 <= value < -1500: \"L159\", -1500 <= value < -1000: \"L158\", -1000 <= value < -900: \"L157\", -900 <= value < -800: \"L156\", -800 <= value < -700: \"L155\", -700 <= value < -600: \"L154\", -600 <= value < -500: \"L153\", -500 <= value < -400: \"L152\", -400 <= value < -300: \"L151\", -300 <= value < -200: \"L150\", -200 <= value < -100: \"L149\", -100 <= value < -90: \"L148\", -90 <= value < -80: \"L147\", -80 <= value < -70: \"L146\", -70 <= value < -60: \"L145\", -60 <= value < -50: \"L144\", -50 <= value < -40: \"L143\", -40 <= value < -30: \"L142\", -30 <= value < -25: \"L141\", -25 <= value < -20: \"L140\", -20 <= value < -15: \"L139\", -15 <= value < -12: \"N12\", -12 <= value < -11: \"N11\", -11 <= value < -10: \"N10\", -10 <= value < -9: \"N9\", -9 <= value < -8: \"N8\", -8 <= value < -7: \"N7\", -7 <= value < -6: \"N6\", -6 <= value < -5: \"N5\", -5 <= value < -4: \"N4\", -4 <= value < -3: \"N3\", -3 <= value < -2: \"N2\", -2 <= value < -1: \"N1\", -1 <= value < 0: \"L135\", value == 0.0: \"L0\", 0 < value < 0.2: \"L1\", 0.2 <= value < 0.4: \"L2\", 0.4 <= value < 0.6: \"L3\", 0.6 <= value < 0.8: \"L4\", 0.8 <= value < 1: \"L5\", 1 <= value < 2: \"L6\", 2 <= value < 3: \"L7\", 3 <= value < 4: \"L8\", 4 <= value < 5: \"L9\", 5 <= value < 6: \"L10\", 6 <= value < 7: \"L11\", 7 <= value < 8: \"L12\", 8 <= value < 9: \"L13\", 9 <= value < 10: \"L14\", 10 <= value < 12: \"L15\", 12 <= value < 14: \"L16\", 14 <= value < 16: \"L17\", 16 <= value < 18: \"L18\", 18 <= value < 20: \"L19\", 20 <= value < 22: \"L20\", 22 <= value < 24: \"L21\", 24 <= value < 26: \"L22\", 26 <= value < 28: \"L23\", 28 <= value < 30: \"L24\", 30 <= value < 32: \"L25\", 32 <= value < 34: \"L26\", 34 <= value < 36: \"L27\", 36 <= value < 38: \"L28\", 38 <= value < 40: \"L29\", 40 <= value < 42: \"L30\", 42 <= value < 44: \"L31\", 44 <= value < 46: \"L32\", 46 <= value < 48: \"L33\", 48 <= value < 50: \"L34\", 50 <= value < 52: \"L35\", 52 <= value < 54: \"L36\", 54 <= value < 56: \"L37\", 56 <= value < 58: \"L38\", 58 <= value < 60: \"L39\", 60 <= value < 62: \"L40\", 62 <= value < 64: \"L41\", 64 <= value < 66: \"L42\", 66 <= value < 68: \"L43\", 68 <= value < 70: \"L44\", 70 <= value < 72: \"L45\", 72 <= value < 74: \"L46\", 74 <= value < 76: \"L47\", 76 <= value < 78: \"L48\", 78 <= value < 80: \"L49\", 80 <= value < 82: \"L50\", 82 <= value < 84: \"L51\", 84 <= value < 86: \"L52\", 86 <= value < 88: \"L53\", 88 <= value < 90: \"L54\", 90 <= value < 92: \"L55\", 92 <= value < 94: \"L56\", 94 <= value < 96: \"L57\", 96 <= value < 98: \"L58\", 98 <= value < 100: \"L59\", 100 <= value < 110: \"L60\", 110 <= value < 120: \"L61\", 120 <= value < 130: \"L62\", 130 <= value < 140: \"L63\", 140 <= value < 150: \"L64\", 150 <= value < 160: \"L65\", 160 <= value < 170: \"L66\", 170 <= value < 180: \"L67\", 180 <= value < 190: \"L68\", 190 <= value < 200: \"L69\", 200 <= value < 210: \"L70\", 210 <= value < 220: \"L71\", 220 <= value < 230: \"L72\", 230 <= value < 240: \"L73\", 240 <= value < 250: \"L74\", 250 <= value < 260: \"L75\", 260 <= value < 270: \"L76\", 270 <= value < 280: \"L77\", 280 <= value < 290: \"L78\", 290 <= value < 300: \"L79\", 300 <= value < 310: \"L80\", 310 <= value < 320: \"L81\", 320 <= value < 330: \"L82\", 330 <= value < 340: \"L83\", 340 <= value < 350: \"L84\", 350 <= value < 360: \"L85\", 360 <= value < 370: \"L86\", 370 <= value < 380: \"L87\", 380 <= value < 390: \"L88\", 390 <= value < 400: \"L89\", 400 <= value < 410: \"L90\", 410 <= value < 420: \"L91\", 420 <= value < 430: \"L92\", 430 <= value < 440: \"L93\", 440 <= value < 450: \"L94\", 450 <= value < 460: \"L95\", 460 <= value < 470: \"L96\", 470 <= value < 480: \"L97\", 480 <= value < 490: \"L98\", 490 <= value < 500: \"L99\", 500 <= value < 600: \"L100\", 600 <= value < 700: \"L101\", 700 <= value < 800: \"L102\", 800 <= value < 900: \"L103\", 900 <= value < 1000: \"L104\", 1000 <= value < 1100: \"L105\", 1100 <= value < 1200: \"L106\", 1200 <= value < 1300: \"L107\", 1300 <= value < 1400: \"L108\", 1400 <= value < 1500: \"L109\", 1500 <= value < 1600: \"L110\", 1600 <= value < 1700: \"L111\", 1700 <= value < 1800: \"L112\", 1800 <= value < 1900: \"L113\", 1900 <= value < 2000: \"L114\", 2000 <= value < 3000: \"L115\", 3000 <= value < 4000: \"L116\", 4000 <= value < 5000: \"L117\", 5000 <= value < 6000: \"L118\", 6000 <= value < 7000: \"L119\", 7000 <= value < 8000: \"L120\", 8000 <= value < 9000: \"L121\", 9000 <= value < 10000: \"L122\", 10000 <= value < 15000: \"M1\", 15000 <= value < 20000: \"M2\", 20000 <= value < 25000: \"M3\", 25000 <= value < 30000: \"M4\", 30000 <= value < 40000: \"M5\", 40000 <= value < 50000: \"M6\", 50000 <= value < 60000: \"M7\", 60000 <= value < 70000: \"M8\", 70000 <= value < 80000: \"M9\", 80000 <= value < 90000: \"M10\", 90000 <= value < 100000: \"M11\", 100000 <= value < 110000: \"M12\", 110000 <= value < 120000: \"M13\", 120000 <= value < 130000: \"M14\", 130000 <= value < 140000: \"M15\", 140000 <= value < 150000: \"M16\", 150000 <= value < 160000: \"M17\", 160000 <= value < 170000: \"M18\", 170000 <= value < 200000: \"M19\", 200000 <= value < 250000: \"M20\", 250000 <= value < 300000: \"M21\", 300000 <= value < 400000: \"M22\", 400000 <= value < 600000: \"L130\", 600000 <= value < 900000: \"L131\", 900000 <= value < 1300000: \"L132\", 1300000 <= value < 2000000: \"L133\", 2000000 <= value: \"L134\", } ```",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          },
          "ancheyear": {
            "type": "string",
            "description": "年报年份 示例：2022,2020"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_science_technology_score/",
    "function": {
      "name": "企业评价与标签-A076-企业科创分",
      "description": "通过评估企业的技术创新、成长经营、对外合作和企业荣誉等多个方面，提供一个综合评分和行业排名。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_shell_index_score/",
    "function": {
      "name": "企业评价与标签-A077-企业空壳指数得分",
      "description": "通过分析一系列与企业经营状况相关的指标，如企业异常情况、经营地址异常、法定代表人异常、企业变更异常以及关联方异常等，来计算企业的空壳指数得分。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/dompany_comprehensive_assessment_score/",
    "function": {
      "name": "企业评价与标签-A078-企业综合评价得分",
      "description": "通过分析企业多领域数据，如行业地位、经营绩效、稳定性和创新能力等，计算出一个综合评分，以快速评估企业的市场竞争力、财务健康、发展潜力和潜在风险；此外，接口还提供具体指标得分，包括注册资本、营收、净利润、专利数及行政处罚记录等，帮助企业深入理解自身表现和经营状况。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||（\"0\"：企业唯一标识；\"1\"：企业名称；\"2\"：统一社会信用代码；\"3\"：注册号；\"4\"：组织机构代码），若为\"0\"该参数可不传 示例：1"
          }
        },
        "required": [
          "key"
        ]
      }
    }
  },
  {
    "url": "http://openapi.bainiudata.com/openapi/common/company_detail/",
    "function": {
      "name": "M001-企业详情信息查询",
      "description": "通过传入不同的version参数值，对企业数据相关维度的各种详情信息进行查询。",
      "parameters": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "description": "企业标准名称（非简称）/统一社会信用代码（唯一识别码）/注册号 示例：小米科技有限责任公司"
          },
          "key_type": {
            "type": "string",
            "description": "关键字类型||(\"0\"：企业唯一标识 \"1\"：企业名称  \"2\"：统一社会信用代码  \"3\"：注册号  \"4\"：组织机构代码）不填写默认是0 示例：1"
          },
          "version": {
            "type": "string",
              "description": "\n|可选取值|对应查询|取值说明|\n|---|---|---|\n|A1|工商信息-照面信息|通过输入企业的统一社会信用代码或注册号，获取该企业的基本工商登记信息，包括但不限于企业名称、组织机构代码、注册号、统一社会信用代码、法人代表、注册资本、成立日期、营业期限、地址、经营范围等；此外，还提供许可经营项目、一般经营项目、行业分类、员工人数、参保人数、官网链接、地理位置坐标等辅助信息，帮助企业用户全面了解目标公司的基本情况。此时无需传入page_index和page_size|\n|A2|工商信息-变更信息|用于查询企业的历史变更记录，涵盖变更事项（如法定代表人变更、注册资本变更等）、变更前后的具体内容及变更日期；返回的数据列表包含所有变更记录及其总数，帮助用户追踪企业的变更历程。|\n|A3|工商信息-数据源多渠道汇总的分支机构信息|汇总展示企业各分支机构的详细信息，包括分支名称、注册号、负责人、经营范围、地址、运营状态及来源类型等。|\n|A4|工商信息-工商非注册地址|提供企业可能使用的非注册办公地点信息，包括具体地址、来源、地理坐标及是否在注册地附近，此接口有助于识别企业的实际运营地点。|\n|A5|工商信息-核心团队|介绍组成企业核心管理团队的成员，列出姓名、职位、教育背景、个人简介等信息，通过数据列表和总数，用户可以获得完整的核心团队构成情况。|\n|A6|工商信息-国家企业信用信息公示系统公示的分支机构信息|展示企业工商公示中各分支机构的详情，涵盖分支名称、注册编号、负责人、经营项目、统一社会信用代码及登记机构等信息。|\n|E1|工商信息-年报基本信息|股权变更|对外担保|对外投资|出资信息|网站信息|涵盖了企业在特定报告年度内的多个重要方面，包括但不限于基本经营信息、股权结构变动、对外担保情况、对外投资动向、股东出资详情以及网站运营情况。|\n|E2|工商信息-年报资产|提供企业的年度资产信息，揭示企业的财务健康状况，如资产总额、负债总额、营业总收入、净利润及纳税总额等。|\n|E3|工商信息-年报社保|提供企业的年度社保缴纳信息，详细展示了企业在报告期内的社会保险缴纳情况，包括城镇职工养老保险、失业保险、职工医疗保险、工伤保险及生育保险的人数和缴费基数等；此外，还提供了具体的缴费明细，如是否公示、实际缴费金额及累计欠缴情况等。|\n|E4|工商信息-年报变更|提供企业的年度报告变更信息，揭示企业在报告期内的重要变动，如修改事项、修改前内容、修改后内容及修改日期等。|\n|B1|工商信息-股东高管信息|详细列出企业的股东与高管信息，包括股东的投资比例、出资方式、出资金额，高管的职位、是否担任法人等。|\n|B6|工商信息-历史股东高管|记录企业历史上股东和高管的变化，包括变动类型、日期、前后认缴金额和投资比例等，便于追溯企业领导层的历史变迁。|\n|C8|经营信息-知识产权出质变更|提供有关企业知识产权出质及变更的信息，如知识产权登记证号、名称、种类、出质人名称、质权人名称、状态、公示日期等。|\n|C11|经营信息-抽查检查|获取企业接受工商部门抽查检查的信息，包括巡查日期、类型、属地监管工商所、发现问题、处理情况及意见等。|\n|F6|经营信息-土地信息|查询企业持有的土地信息，包括电子监管号、项目名称、位置、面积、用途、使用年限等。|\n|G1|经营信息-中标信息|查询企业详细的中标信息，包括但不限于项目名称、项目编号、项目分类、预算金额、中标金额、发布时间、开标时间、标书截止时间、招标单位、中标单位、代理单位、招标进度等字段。|\n|G1-2|经营信息-标讯信息|提供有关企业参与招投标活动的详细标讯信息，包括中标或投标日期、公告标题及类型、采购方和代理方等关键数据。|\n|G1-3|经营信息-招投标关联关系|提供企业及其关联企业在招投标活动中的合作或竞争关系信息，揭示企业之间的关联互动情况。|\n|G2|经营信息-百科介绍|提供企业百科介绍信息，包括来源、介绍正文等，帮助用户快速了解企业的背景和发展历程。|\n|G11|经营信息-招聘信息|提供企业发布的招聘信息，包括招聘标题、职位、薪资、工作地点、工作要求、来源平台及收录日期等。|\n|G12|经营信息-重大舆情|揭示与企业相关的重大舆情事件，包括标题、作者、所属地区、摘要、事件日期及来源URL等。|\n|G13|经营信息-建筑工程|提供企业参与的建筑工程项目的详细信息，如项目编号、报备日期、项目名称、建设性质及工程用途等。|\n|G14|经营信息-B2B黄页|展示企业在B2B平台上的黄页信息，涵盖企业经营模式、主营产品、营业额及主要销售区域等。|\n|G15|经营信息-产品信息|提供企业产品的详细信息，包括图标、名称、分类、下载数、用户评分及发布日期等。|\n|G16|经营信息-店铺电商|展示企业在电商平台上的店铺信息，如店铺名称、平台ID、首页地址及经营地址等。|\n|G18|经营信息-新闻事件投诉举报|揭示与企业相关的新闻事件投诉举报信息，包括标题、事件日期、关键词、正文及来源URL等。|\n|G19|经营信息-12315投诉汇总信息|提供企业被投诉的基本信息汇总，如申诉举报基本问题、涉案客体类别及事发时间等。|\n|G20|经营信息-12315投诉详情信息|展示企业被投诉的具体详情，包括投诉时间、消费类型、调解结果及商家具体行为情形等。|\n|G21|经营信息-企业元搜索|提供综合的企业信息搜索功能，整合了来自多个数据源的企业基本信息、工商登记、经营状况、法律诉讼、知识产权、股权信息等多维度信息。|\n|G3|经营信息-icp备案|查询企业的互联网信息服务备案信息，如备案类型、开办者名称、备案号、网站域名、城市等，适用于互联网业务合规性审核。|\n|G5|经营信息-百度竞价|提供企业参与百度竞价广告的信息，包括推广关键词、省份、百度链接、推广网站及账户类型等。|\n|G4|经营信息-网站检测|获取企业网站的监测信息，如网址、关键词、描述以及更新日期等。|\n|G6|经营信息-安卓市场|展示企业在安卓应用市场的表现，如应用图标、名称、分类、下载数、开发者、用户评分及发布日期等。|\n|G7|经营信息-苹果市场|提供企业在苹果App Store的表现信息，包括应用图标、名称、分类、下载数、当前版本评论数量及发布日期等。|\n|G8|经营信息-微博蓝V|展示企业官方微博账号的认证信息，如微博logo、微博名、粉丝数、微博数、关注数及标签等。|\n|G9|经营信息-微信公众号|提供企业官方微信公众号的相关信息，如公众号logo、名称、认证名称、月发文数及最新文章标题等。|\n|G10|经营信息-微信小程序|展示企业开发的微信小程序详情，包括小程序logo、名称、类别和简介等。|\n|C5|经营风险-行政处罚|揭示企业受到的行政处罚记录，包括案发时间、违法行为类型、处罚决定书签发日期、处罚机关、处罚种类、金额等。|\n|C6|经营风险-欠税记录|用于查询企业的欠税情况，提供纳税人名称、欠缴税种、以前年度陈欠余额、本期新欠金额、总欠税额等信息，可用于评估企业的财政责任履行情况及其税务合规性。|\n|C7|经营风险-经营异常|用于核查企业经营异常情况，提供列入和移出经营异常名录的基本信息，如列入/移出日期、原因、文号作出决定机关等。|\n|C7-1|经营风险-经营异常（列出）|侧重于企业从经营异常名录中移出的细节，如移出日期、原因、文号及公告信息。|\n|C7-2|经营风险-经营异常（列入）|侧重于企业被列入经营异常名录的细节，包括列入日期、原因、文号及公告信息。|\n|C12|经营风险-大数据行政处罚|整合了来自多个来源（信用中国，地方工商局，各个部委）的行政处罚详情，如处罚决定日期、处罚种类、行政部门、事由、依据、结果、金额及处罚执行情况等。|\n|C13|经营风险-简易注销公告|查询企业的简易注销公告信息，包括统一社会信用代码、登记机关、公告开始和结束日期、核准日期、注销日期等。|\n|C14|经营风险-严重违法失信|提供企业被列入和移出严重违法失信名单的详细信息，包括列入和移出的原因、日期、决定机关及违法事实。|\n|C14-1|经营风险-严重违法失信（列入）|专注于企业被列入严重违法失信名单的具体信息，涵盖列入原因、日期、决定机关及公告内容。|\n|C14-2|经营风险-严重违法失信（列出）|专注于企业从严重违法失信名单中移出的信息，提供移出原因、日期及决定机关等详情。|\n|C22|经营风险-税务局行政处罚|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取税务局对企业实施的行政处罚记录，涵盖案件性质、主要违法事实、处罚结果及决定书文号等信息。|\n|C23|经营风险-环保部行政处罚|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取环保部对企业实施的行政处罚详情，包括处罚原因、处罚依据、措施及结果等。|\n|C24|经营风险-海关失信行政处罚信息|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取海关对企业实施的失信处罚信息，涵盖案件名称、处罚内容、日期及企业管理类别等。|\n|C25|经营风险-食药监行政处罚|提供食品药品监督管理部门对企业实施的行政处罚记录，包括违法行为类型、处罚种类、依据及结果等。|\n|C26|经营风险-银监会行政处罚|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取银监会对金融机构实施的行政处罚详情，涵盖违法违规事实、处罚依据及决定等。|\n|C27|经营风险-保监会行政处罚|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，提供保监会对保险机构实施的行政处罚信息，包括当事人、处罚内容、日期及决定机关等。|\n|C28|经营风险-证监会行政处罚|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取证监会对证券市场参与者实施的行政处罚记录，涵盖主要违法事实、处罚依据及决定机关等。|\n|C29|经营风险-人行行政处罚|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取中国人民银行对企业实施的行政处罚信息，包括违法行为类型、处罚内容及决定机关等。|\n|D3|经营风险-动产抵押|提供企业的动产抵押信息，揭示企业的动产抵押情况，如抵押登记ID、登记机关、状态标识、登记日期及抵押注销原因等。|\n|F14|经营风险-土地抵押|提供企业的土地抵押信息，揭示企业的土地资产抵押情况，如土地抵押权人、用途、面积、评估金额及抵押金额等。|\n|C1|法律诉讼-被执行人失信被执行人|查询被执行人的失信记录，返回的数据包括但不限于自增ID、案号、被执行人姓名/名称、执行法院名称、执行标的、立案时间、执行依据文号、失信行为的具体情形以及履行情况等。|\n|C2-1|法律诉讼-裁判文书|详细列出企业参与的所有裁判文书信息，包括但不限于案号、审结时间、标题、文书类型、案件状态、法院名称、原告被告、判决结果、法律依据等。|\n|C2-2|法律诉讼-开庭公告|提供企业即将或已经发生的开庭信息，如开庭日期、案号、当事人（被告）、法院名称等。|\n|C2-3|法律诉讼-法院公告|涵盖法院发布的各类公告，如公告日期、当事人、公告类型、公告内容等。|\n|C2-4|法律诉讼-曝光台|展示企业及人员被曝光的不良信息，如立案时间、案号、标的金额、执行情况和状态等。|\n|C2-5|法律诉讼-案件流程|追踪案件从立案到归档的整个流程，包括但不限于立案日期、当事人、主要法官、内容、流程状态等。|\n|C3|法律诉讼-股权冻结股权质押|提供有关企业股权冻结和质押的信息，包含冻结文号、冻结机关、起止日期、解冻说明，以及质押ID、质权人、质押金额等。|\n|C4|法律诉讼-清算信息|该接口专注于企业的清算过程，提供清算责任人、清算完结情况、债务承接人等信息，是评估企业终止运营时如何处理其资产和负债的关键数据。|\n|C9|法律诉讼-司法协助|展示司法机关对企业实施的协助措施，包括被执行股东ID、被执行公司、执行事项、冻结期限、续行冻结信息等。|\n|C10|法律诉讼-终本案件|查询企业的终本案件信息，包括但不限于案号、主体名称、性别、证件号码/组织机构代码、地址、法院名称、发布日期、立案日期、公示日期、案由及执行金额等。|\n|C15|法律诉讼-立案信息|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取与企业相关的立案信息，如角色（原告/被告）、立案时间、案件状态、类型、案号、案由等。|\n|C16|法律诉讼-破产重整|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业破产重整的相关信息，包括公开时间、案号、申请人、破产类型等。|\n|C17|法律诉讼-限制高消费|查询企业是否受限于高消费限制措施，返回包括但不限于相关案号、案由、发布时间、立案时间等关键信息。|\n|C18|法律诉讼-重大税收违法|获取企业涉及的重大税收违法行为信息，包括但不限于纳税人情况、法人身份信息、案件性质、税务机关、违法事实、法律依据、处罚情况等信息。|\n|C19|法律诉讼-税务局（非正常户）|查询企业的税务状态，特别是是否被列入税务局的非正常户名单，以及欠税情况、认定原因等。|\n|C20|法律诉讼-司法拍卖|提供企业参与的司法拍卖项目详细信息，包括但不限于拍品名称、拍品所有人、拍品类别、拍卖开始时间、拍卖结束时间、起拍价、评估价、法院名称、法院ID、所在地、权证情况、权利限制情况及瑕疵情况、成交结果、提供的文件、拍卖日期、权利来源、成交日期、成交价格、拍品介绍、正文内容等，此接口适用于资产处置监控、市场动态跟踪以及法律风险评估。|\n|C21|法律诉讼-行贿犯罪失信黑名单|提供有关企业或个人因行贿犯罪而被列入失信黑名单的信息，包括法人和其他组织名称、列入时间、处罚文号及处罚结果等。|\n|C30|法律诉讼-送达公告|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，展示法院或其他司法机关发布的送达公告信息，包括公告名称、发布日期、双方当事人、案号及原文等。|\n|B2|幕后关联-企业对外投资|提供详尽的企业对外投资信息，返回包括但不限于被投资企业的基本信息、注册资本、出资比例及方式等关键信息。|\n|B3|幕后关联-高管对外投资任职|显示企业高管在外的投资和任职情况，包括被投企业信息、高管职务等，有助于评估高管的商业活动范围和关联性，用于风险管理和合规审查等。|\n|B4|幕后关联-主要人员对外负责个体户|提供企业关键人物负责的个体商户信息，如商户名称、注册号、注册资本、状态等，帮助识别企业与个体商户之间的关联关系。|\n|B5|幕后关联-法人对外投资任职|展示企业法人在其他实体中的投资和任职情况，包括投资细节、任职公司等关键信息。|\n|B7|幕后关联-受益所有人|返回受益人名称、最终持股比例以及持股链条等信息,着重于提供详尽的企业受益所有人信息。|\n|B8|幕后关联-最终受益人|返回受益人名称、最终持股比例以及持股链条等详细数据，更专注于揭示站在企业所有权和控制权顶端的最终受益人。|\n|G17|通讯信息-常用联系方式|提供企业的常用联系方式，如手机、座机和邮箱等。|\n|L1|企业发展-小微企业扶持政策|提供小微企业享受的政府扶持政策详情，包括实施扶持政策的部门、日期、依据及具体内容和数额等。|\n|F10|资质许可-行政许可（工商）|提供企业工商类（来源企业公示系统）的行政许可信息，涵盖许可文件编号、名称、有效期、许可机关、有效期、许可状态等信息。|\n|F10-1|资质许可-行政工商许可（大数据）|提供企业获得的行政许可信息，特别侧重于通过各个部委收集和分析得到的许可详情，返回数据包括许可文件ID、编号及名称，有效期的起止日期，以及颁发许可的机关和许可状态等关键信息。|\n|F11|资质许可-企业荣誉|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，展示企业获得的各项荣誉，如荣誉名称、授予单位、授予日期等。|\n|F12|资质许可-管理体系认证|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业的管理体系认证信息，如证书编号、颁证日期、到期日期等。|\n|F13|资质许可-强制性产品认证|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业详细的认证记录，包括唯一标识符、颁证日期、证书到期日期、项目名称、证书编号、证书状态、机构编号等。|\n|F15|资质许可-食品经营许可|提供企业的食品经营许可信息，揭示企业在食品经营领域的合法资质，如许可资质名称、许可证编号、发证机关及有效期等。|\n|F16|资质许可-食品生产许可（QS）|提供企业的食品生产许可（QS）信息，揭示企业在食品生产领域的合法资质，如许可资质名称、许可证编号、发证机关及有效期等。|\n|F17|资质许可-食品生产许可（SC）|提供企业的食品生产许可（SC）信息，揭示企业在食品生产领域的合法资质，如许可资质名称、许可证编号、发证机关及有效期等。|\n|F1|知识产权-专利信息|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业拥有的专利详细信息，包括专利的申请号、名称、类型、申请日期、公开（公告）号、公开（公告）日期、摘要、法律状态、申请人、发明人、地址、代理机构、国别、优先权、主分类号、分类号、引用文献、专利图片等信息。|\n|F2|知识产权-商标信息|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业的商标注册信息，包括商标名称、注册号、注册人名称、申请日期、商标类型、类别、状态、专用期限等。|\n|F3|知识产权-驰名商标|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业拥有的驰名商标信息，包括商标名称、注册证号、认定日期、商品服务范围等。|\n|F4|知识产权-软件著作权|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业的软件著作权信息，包括著作权人、软件全称、登记号、首次发表日期等。|\n|F5|知识产权-作品著作权|可根据企业相关参数（企业唯一标识、企业名称、统一社会信用代码或注册号）进行查询，获取企业拥有的作品著作权信息，如登记号、作品名称、作者姓名、发布日期等。|\n|H1-1|上市公司-主板基本信息|提供在主板上市企业的基本信息，展示企业在资本市场的基本概况，如股票代码、简称、上市版块、法定代表人、公司官网及主营业务等。|\n|H1-2|上市公司-新三板基本信息|提供在新三板挂牌企业的基本信息，包括但不限于企业的运营状况，如股票代码、简称、法定代表人、经营范围、主营业务及办公地址等。|\n|H1-3|上市公司-港股基本信息|提供在香港交易所上市企业的基本信息，展示企业在香港资本市场的情况，如股票代码、简称、上市日期、法定代表人及主营业务等。|\n|H2|上市公司-港股财务简报|提供主板、新三板或港股上市企业的年度财务简报，涵盖营业总收入、净利润、资产总额及负债总额等关键财务指标。|\n|H6|上市公司-主板，新三板，港股公告公示|提供主板、新三板或港股上市企业的公告信息，展示企业的重大事项披露情况，如公告标题、日期、内容及类型等。|\n|H7-1|上市公司-上市事件抵押事项|提供上市企业涉及的抵押事项信息，揭示企业的融资活动和资产担保情况，如公告日期、参与方名称、抵押物类型及价值等。|\n|H3-1|上市公司-主板董监事成员信息|提供主板上市企业的董监事成员信息，展示企业的管理层构成，如姓名、职务、学历及任期以及董监事会届次等。|\n|H3-2|上市公司-新三板董监事成员信息|提供新三板挂牌企业的董监事成员信息，展示企业的管理层构成，如公告日期、姓名、职务名称及当前状态等。|\n|H3-3|上市公司-港股董监事成员信息|提供港股上市企业的董监事成员信息，展示企业的管理层构成，如公告日期、姓名、职务名称及离职原因等。|\n|H4-2|上市公司-新三板股东持股|查询新三板挂牌公司的股东持股信息，返回包括但不限于股东持股详情，公告日期、股东名称、持有数量、持有比例、质押或冻结的股份数等关键数据。|\n|H4-1|上市公司-主板股东持股|查询主板上市公司的股东持股信息，返回包括但不限于股东持股详情，公告日期、股东名称、持有数量、持有比例、质押或冻结的股份数等关键数据。|\n|H4-3|上市公司-港股股东持股|查询港股上市公司的股东持股信息，返回包括但不限于股东身份类型、权益详情、占股比、公告日期等关键数据。|\n|H5-1|上市公司-主板成员简介|提供主板上市企业的核心成员简介，展示企业高管团队的背景，如姓名、性别、政治面貌、最高学历及工作经历等。|\n|H5-2|上市公司-新三板成员简介|提供新三板挂牌企业的核心成员简介，展示企业高管团队的背景，如姓名、最高学历及工作经历等。|\n|H5-3|上市公司-港股成员简介|提供港股上市企业的核心成员简介，展示企业高管团队的背景，如姓名、曾用名、毕业院校及工作经历等。|\n|K1|企业评价与标签-企业标签|通过输入企业相关参数（企业名称、统一社会信用代码或注册号），查询企业的标签ID及标签名称。|\n|K2|企业评价与标签-企业标签详情|通过输入企业相关参数（企业名称、统一社会信用代码或注册号），查询企业的详细标签信息，返回包括但不限于是否为纳税A级企业、是否国有企业、是否国家级专精特新企业、是否规上企业等具体属性。|\n"
          }
        },
        "required": [
          "key",
          "key_type",
          "version"
        ]
      }
    }
  }
]
# 将外部自定义搜索函数也加入到 schema 列表
schema.append(company_super_search)

# MCP Server 的初始化说明
instructions = (
    "基于MCP协议(Model Context Protocol)构建的标准化企业信息服务平台，"
    "为LLM及开发者提供工商、司法、舆情等多维度企业数据查询能力，"
    "支持通过自然语言交互实现专业级企业尽调功能。\n"
    "注意: 请确保设置MCP_CLIENT_ID和MCP_CLIENT_KEY环境变量以提供认证信息。"
)

# 创建 FastMCP 实例
mcp = FastMCP(name="QueryAboutCompany", instructions=instructions)


def build_pydantic_model(
        name: str, properties: Dict[str, Any], required: List[str]
) -> BaseModel:
    """
    根据 JSON Schema properties 和 required 构建 Pydantic 模型
    """
    fields = {}

    # 添加原始字段
    for field_name, details in properties.items():
        json_type = details.get("type", "string")
        py_type = type_mapping.get(json_type, str)
        default = ... if field_name in required else None
        fields[field_name] = (
            Optional[py_type] if default is None else py_type,
            Field(default, description=details.get("description", ""))
        )

    return create_model(name, **fields)


def get_credentials_from_env() -> tuple:
    """
    从环境变量获取凭据
    """
    # 从环境变量获取凭据
    # 打印环境变量调试信息
    env_cid = os.getenv("MCP_CLIENT_ID")
    env_ckey = os.getenv("MCP_CLIENT_KEY")
    # 使用环境变量或默认值
    if env_cid and env_ckey:
        print("使用环境变量中的凭据")
        return env_cid, env_ckey
    else:
        # 如果环境变量未设置，使用默认值并发出警告

        return DEFAULT_CLIENT_ID, DEFAULT_CLIENT_KEY


def register_tool(item: dict):
    func_def = item["function"]
    name = func_def["name"]
    url = item["url"]
    props = func_def.get("parameters", {}).get("properties", {})
    required = func_def.get("parameters", {}).get("required", [])
    # 构建输入模型
    InputModel = build_pydantic_model(f"{name}Input", props, required)

    @mcp.tool(name=name, description=func_def["description"])
    async def handler(params: InputModel, ctx: Context) -> Any:
        # 从环境变量获取凭据
        cid, ckey = get_credentials_from_env()
        if not cid or not ckey:
            missing = []
            if not cid:
                missing.append("MCP_CLIENT_ID")
            if not ckey:
                missing.append("MCP_CLIENT_KEY")
            warning_info = (f'''警告: 环境变量 {', '.join(missing)} 未设置，使用默认凭据,按以下方式设置：
                    # Linux/macOS
                    echo 'export MCP_CLIENT_ID="aaaaaaaa"' >> ~/.bashrc
                    echo 'export MCP_CLIENT_KEY="bbbbbbbb"' >> ~/.bashrc
                    source ~/.bashrc  # 立即生效（仅 Bash）

                    # Windows (cmd)
                    setx MCP_CLIENT_ID aaaaaaaa
                    setx MCP_CLIENT_KEY bbbbbbbb

                    # Windows (PowerShell)
                    [System.Environment]::SetEnvironmentVariable("MCP_CLIENT_ID", "aaaaaaaa", "User")
                    [System.Environment]::SetEnvironmentVariable("MCP_CLIENT_KEY", "bbbbbbbb", "User")
        ''')
            return warning_info
        try:
            # 准备API参数
            payload = params.model_dump(exclude_none=True)
            # 使用凭据调用API
            query = AsyncQueryCompany(client_id=cid, client_key=ckey)
            result = await query.post_api(url, json.dumps(payload))
            return result
        except Exception as e:
            error_msg = f"调用工具 {name} 时出错: {str(e)}"
            print(error_msg)
            # 返回友好的错误信息
            return {
                "status": "error",
                "message": f"API调用失败: {str(e)}",
                "tool": name
            }

# 批量注册所有定义在 schema 中的函数
for item in schema:
    register_tool(item)

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="企业信息查询MCP服务")
    parser.add_argument("--transport", choices=["sse", "stdio"], default="stdio",
                        help="传输方式: sse或stdio (默认: stdio)")
    parser.add_argument("--host", default="0.0.0.0", help="主机地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8009, help="端口号 (默认: 8009)")

    # 向下兼容简单的命令行参数
    if len(sys.argv) == 2 and sys.argv[1] in ["sse", "stdio"]:
        args = parser.parse_args([f"--transport={sys.argv[1]}"])
    else:
        args = parser.parse_args()

    # 在启动前检查环境变量
    cid, ckey = get_credentials_from_env()
    print(f"使用凭据: client_id={cid[:3]}****, client_key={ckey[:3]}****")

    # 启动服务
    if args.transport == "sse":
        print(f"正在启动SSE服务 - 监听地址: {args.host}:{args.port}")
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        print("正在启动stdio服务")
        mcp.run(transport="stdio")