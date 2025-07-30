#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL 内省查询工具

该模块提供了通过内省查询(Introspection Query)获取GraphQL Schema的功能。
使用HTTP请求向GraphQL服务发送内省查询，获取完整的Schema信息，然后将其转换为
模型中的GraphQLSchema对象，供后续测试用例生成使用。

主要功能：
1. 向GraphQL服务发送内省查询请求
2. 解析内省查询结果
3. 将内省查询结果转换为GraphQLSchema对象
"""

import json
import requests
from typing import Dict, Any, Optional, List, Set

from .models import GraphQLType, GraphQLSchema


# GraphQL内省查询语句
INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
"""


class IntrospectionQueryError(Exception):
    """内省查询错误"""
    pass


def fetch_schema_from_introspection(url: str) -> GraphQLSchema:
    """
    通过内省查询获取GraphQL Schema
    
    Args:
        url: GraphQL服务的URL地址
        
    Returns:
        GraphQLSchema: 解析后的Schema对象
        
    Raises:
        IntrospectionQueryError: 内省查询失败时抛出
    """
    print(f"正在从 {url} 进行内省查询获取GraphQL Schema...")
    
    # 发送内省查询请求
    try:
        response = requests.post(
            url,
            json={
                "query": INTROSPECTION_QUERY,
                "operationName": "IntrospectionQuery",
                "variables": {}
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise IntrospectionQueryError(f"内省查询请求失败: {str(e)}")
    
    # 解析响应内容
    try:
        result = response.json()
        # 检查是否有错误
        if "errors" in result:
            errors = result["errors"]
            error_msg = "; ".join([str(error.get("message", "未知错误")) for error in errors])
            raise IntrospectionQueryError(f"GraphQL服务返回错误: {error_msg}")
            
        # 确保结果中包含schema信息
        if "data" not in result or "__schema" not in result["data"]:
            raise IntrospectionQueryError("响应中未包含Schema信息")
            
        schema_data = result["data"]["__schema"]
        
    except (json.JSONDecodeError, KeyError) as e:
        raise IntrospectionQueryError(f"解析内省查询结果失败: {str(e)}")
    
    # 将内省查询结果转换为GraphQLSchema对象
    return _convert_introspection_to_schema(schema_data)


def _get_type_string(type_ref: Dict[str, Any]) -> str:
    """
    递归处理类型引用，生成与schema解析一致的类型字符串表示
    
    Args:
        type_ref: 类型引用数据
        
    Returns:
        str: 类型的字符串表示
    """
    kind = type_ref.get("kind")
    name = type_ref.get("name")
    
    # 基本命名类型(SCALAR, OBJECT, ENUM, etc.)
    if kind in ["SCALAR", "OBJECT", "INTERFACE", "UNION", "ENUM", "INPUT_OBJECT"] and name:
        return name
    # 列表类型
    elif kind == "LIST" and "ofType" in type_ref:
        inner_type = _get_type_string(type_ref["ofType"])
        return f"[{inner_type}]"
    # 非空类型
    elif kind == "NON_NULL" and "ofType" in type_ref:
        inner_type = _get_type_string(type_ref["ofType"])
        return f"{inner_type}!"
    # 未知类型
    return "Unknown"


def _parse_type_reference(type_ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    解析类型引用，递归处理嵌套类型
    
    Args:
        type_ref: 类型引用数据
        
    Returns:
        Dict: 包含类型信息的字典
    """
    # 获取完整的类型字符串表示
    type_str = _get_type_string(type_ref)
    
    # 检查是否是列表类型
    is_list = False
    if type_str.startswith('[') and ']' in type_str:
        is_list = True
    
    # 检查是否是必需的(非空)
    required = False
    if type_str.endswith('!'):
        required = True
    
    # 提取基础类型名称
    # 对于列表类型[Type!]!，提取Type
    base_type = type_str
    if is_list:
        # 移除外层的[]
        base_type = type_str[1:type_str.rindex(']')]
        # 如果内部类型有非空标记，移除它
        if base_type.endswith('!'):
            base_type = base_type[:-1]
    # 如果类型有非空标记，移除它
    elif required:
        base_type = base_type[:-1]
    
    return {
        "type": base_type,        # 基础类型名称
        "type_str": type_str,     # 完整类型字符串表示
        "is_list": is_list,       # 是否是列表
        "required": required      # 是否是必需的
    }


def _update_arg_default_values(args: Dict[str, Dict[str, Any]], input_data: Dict[str, Any]) -> None:
    """
    从内省查询结果中提取参数的默认值
    
    Args:
        args: 参数字典，将被修改
        input_data: 包含defaultValue字段的内省数据
    """
    # 当defaultValue存在并且不为null时，记录默认值信息
    if input_data.get("defaultValue") is not None:
        arg_name = input_data.get("name")
        if arg_name in args:
            # 处理defaultValue，可能需要解析JSON字符串
            default_value = input_data.get("defaultValue")
            try:
                # 尝试解析JSON字符串
                if default_value and (default_value.startswith('{') or default_value.startswith('[')):
                    import json
                    default_value = json.loads(default_value)
            except:
                # 解析失败则保留原始字符串
                pass
                
            args[arg_name]["default_value"] = default_value


def _convert_introspection_to_schema(introspection_data: Dict[str, Any]) -> GraphQLSchema:
    """
    将内省查询结果转换为GraphQLSchema对象
    
    Args:
        introspection_data: 内省查询返回的Schema数据
        
    Returns:
        GraphQLSchema: 转换后的Schema对象
    """
    print("正在解析内省查询结果...")
    
    schema = GraphQLSchema()
    
    # 设置根类型
    if introspection_data.get("queryType") and introspection_data["queryType"].get("name"):
        schema.set_query_type(introspection_data["queryType"]["name"])
        
    if introspection_data.get("mutationType") and introspection_data["mutationType"].get("name"):
        schema.set_mutation_type(introspection_data["mutationType"]["name"])
        
    if introspection_data.get("subscriptionType") and introspection_data["subscriptionType"].get("name"):
        schema.set_subscription_type(introspection_data["subscriptionType"]["name"])
    
    # 处理所有类型
    type_map = {}  # 用于临时存储类型信息
    
    for type_data in introspection_data.get("types", []):
        kind = type_data.get("kind")
        name = type_data.get("name")
        
        if not name:  # 跳过没有名称的类型
            continue
            
        # 跳过内置类型
        if name.startswith("__"):
            continue
            
        # 处理SCALAR类型
        if kind == "SCALAR" and name not in ["String", "Int", "Float", "Boolean", "ID"]:
            schema.add_scalar_type(name)
            
        # 处理ENUM类型
        elif kind == "ENUM":
            schema.add_enum_type(name)
            enum_values = set()
            for enum_value in type_data.get("enumValues", []):
                enum_values.add(enum_value["name"])
            schema.add_enum_values(name, enum_values)
            
        # 处理OBJECT类型
        elif kind == "OBJECT":
            # 创建GraphQLType对象
            type_obj = GraphQLType(
                name=name,
                description=type_data.get("description")
            )
            
            # 解析实现的接口
            interfaces = []
            for interface in type_data.get("interfaces", []):
                if interface.get("name"):
                    interfaces.append(interface["name"])
            type_obj.implements = interfaces
            
            # 解析字段
            for field in type_data.get("fields", []):
                field_name = field["name"]
                type_info = _parse_type_reference(field["type"])
                
                # 解析参数
                args = {}
                for arg in field.get("args", []):
                    arg_name = arg["name"]
                    arg_type_info = _parse_type_reference(arg["type"])
                    
                    # 使用完整的类型字符串作为类型
                    args[arg_name] = {
                        "type": arg_type_info["type_str"],
                        "required": arg_type_info["required"],
                        "is_list": arg_type_info["is_list"]
                    }
                    
                    # 提取默认值
                    _update_arg_default_values(args, arg)
                
                # 添加字段信息
                field_info = {
                    "type": type_info["type_str"],  # 使用完整类型字符串
                    "is_list": type_info["is_list"],
                    "required": type_info["required"],
                    "args": args
                }
                type_obj.add_field(field_name, field_info)
            
            # 添加到Schema
            schema.add_type(type_obj)
            
            # 记录类型信息，用于后续处理根字段
            type_map[name] = type_obj
    
    # 添加根字段
    query_type_name = schema.query_type
    if query_type_name and query_type_name in type_map:
        for field_name, field_info in type_map[query_type_name].fields.items():
            schema.add_root_field(field_name, field_info)
    
    mutation_type_name = schema.mutation_type
    if mutation_type_name and mutation_type_name in type_map:
        for field_name, field_info in type_map[mutation_type_name].fields.items():
            schema.add_root_field(field_name, field_info)
    
    subscription_type_name = schema.subscription_type
    if subscription_type_name and subscription_type_name in type_map:
        for field_name, field_info in type_map[subscription_type_name].fields.items():
            schema.add_root_field(field_name, field_info)
    
    print(f"Schema解析完成，包含 {len(schema.types)} 个类型和 {len(schema.root_fields)} 个根字段")
    
    return schema 