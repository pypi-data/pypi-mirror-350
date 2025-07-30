#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema 数据模型

该模块定义了GraphQL Schema的核心数据模型，包括GraphQLType和GraphQLSchema两个类，
用于表示GraphQL Schema的基本结构和类型信息。这些模型被GraphQLSchemaParser使用，
用于解析GraphQL Schema文件，并为测试用例生成提供基础数据结构。

主要包括：
1. GraphQLType - 表示GraphQL中的类型，包含类型名称、字段、实现接口等信息
2. GraphQLSchema - 表示完整的GraphQL Schema，包含所有类型、接口、查询、变更等信息
"""

from typing import Dict, List, Any, Optional, Set


class GraphQLType:
    """表示GraphQL类型的类"""
    
    def __init__(self, name: str, fields: Dict[str, Dict[str, Any]] = None, 
                 implements: List[str] = None, description: str = None):
        self.name = name
        self.fields = fields or {}
        self.implements = implements or []
        self.description = description
        
    def add_field(self, name: str, type_info: Dict[str, Any]):
        """添加字段到类型"""
        self.fields[name] = type_info
        
    def __str__(self):
        return f"GraphQLType(name={self.name}, fields={len(self.fields)})"


class GraphQLSchema:
    """表示GraphQL Schema的类"""
    
    def __init__(self):
        self.types: Dict[str, GraphQLType] = {}
        self.query_type: Optional[str] = None
        self.mutation_type: Optional[str] = None
        self.subscription_type: Optional[str] = None
        self.interfaces: Dict[str, GraphQLType] = {}
        self.root_fields: Dict[str, Dict[str, Any]] = {}
        self.scalar_types: Set[str] = {'String', 'Int', 'Float', 'Boolean', 'ID'}
        self.enum_types: Set[str] = set()
        self.enum_values: Dict[str, Set[str]] = {}
        
    def add_type(self, type_obj: GraphQLType):
        """添加类型到Schema"""
        self.types[type_obj.name] = type_obj
        
    def add_interface(self, interface_obj: GraphQLType):
        """添加接口到Schema"""
        self.interfaces[interface_obj.name] = interface_obj
        
    def set_query_type(self, name: str):
        """设置查询类型"""
        self.query_type = name
        
    def set_mutation_type(self, name: str):
        """设置变更类型"""
        self.mutation_type = name
        
    def set_subscription_type(self, name: str):
        """设置订阅类型"""
        self.subscription_type = name
        
    def add_root_field(self, name: str, field_info: Dict[str, Any]):
        """添加根字段"""
        self.root_fields[name] = field_info
        
    def add_scalar_type(self, name: str):
        """添加自定义标量类型"""
        self.scalar_types.add(name)
        
    def add_enum_type(self, name: str):
        """添加枚举类型"""
        self.enum_types.add(name)
        
    def add_enum_values(self, type_name: str, values: Set[str]):
        """添加枚举值"""
        self.enum_values[type_name] = values 