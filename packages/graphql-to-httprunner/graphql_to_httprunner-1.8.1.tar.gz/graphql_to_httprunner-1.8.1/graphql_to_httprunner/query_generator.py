#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL 查询语句生成器

该模块提供了从GraphQL Schema生成GraphQL查询语句的功能。
它分析GraphQL Schema中定义的查询、变更和订阅操作，为每个操作生成对应的查询语句。

主要功能：
1. 解析GraphQL Schema，提取所有可用操作
2. 为每个操作生成对应的GraphQL查询语句
3. 支持生成查询、变更和订阅操作的查询语句
4. 支持将生成的查询语句保存到YAML文件
"""

import os
import yaml
from typing import Dict, List, Any, Set

from .models import GraphQLSchema


class GraphQLQueryGenerator:
    """GraphQL查询语句生成器"""
    
    def __init__(self, schema: GraphQLSchema, max_depth: int = 2):
        """
        初始化查询生成器
        
        Args:
            schema: GraphQL Schema对象
            max_depth: 查询嵌套的最大深度
        """
        self.schema = schema
        self.max_depth = max_depth
        self.scalar_types = schema.scalar_types
        self.enum_types = schema.enum_types
        self.generated_types: Set[str] = set()
        
    def generate_queries(self, output_file: str = None, project_name: str = None, query_name: str = None):
        """
        生成所有操作的查询语句并可选择保存到文件
        
        Args:
            output_file: 输出文件路径，如果为None则不保存到文件
            project_name: 项目名称，用于保存时作为分组标识
            query_name: 要生成的查询名称，如果为None则生成所有查询
            
        Returns:
            Dict[str, str]: 操作名称到查询语句的映射
        """
        queries = {}
        
        if query_name:
            # 检查查询名称是否存在
            if query_name not in self.schema.root_fields:
                print(f"错误：查询名称 '{query_name}' 在Schema中不存在")
                return queries
            # 生成指定查询的查询语句
            field_info = self.schema.root_fields[query_name]
            query = self._generate_query(query_name, field_info)
            # 压缩查询语句中的空白，使其单行显示
            query = self._compress_query(query)
            queries[query_name] = query
        else:
            # 生成所有根字段的查询语句
            for field_name, field_info in self.schema.root_fields.items():
                # 跳过名为 _ 的字段，这些字段通常只是占位符
                if field_name == '_':
                    continue
                    
                query = self._generate_query(field_name, field_info)
                # 压缩查询语句中的空白，使其单行显示
                query = self._compress_query(query)
                queries[field_name] = query
        
        # 保存到文件（如果提供了文件路径）
        if output_file:
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)            
            
            # 检查文件是否已存在
            file_exists = os.path.exists(output_file)
            
            # 准备写入
            mode = 'a' if file_exists else 'w'
            with open(output_file, mode, encoding='utf-8') as f:
                # 如果是新文件或第一个项目，不需要添加额外换行
                if file_exists:
                    f.write(f"\n{project_name}:\n")
                else:
                    f.write(f"{project_name}:\n")
                # 写入缩进的查询
                for key, value in queries.items():
                    f.write(f"  {key}: '{value}'\n")
                
        return queries
    
    def _compress_query(self, query: str) -> str:
        """
        压缩查询语句，移除多余空白，使其一行显示
        
        Args:
            query: 原始查询语句
            
        Returns:
            str: 压缩后的查询语句
        """
        # 替换所有连续空白为单个空格
        import re
        query = re.sub(r'\s+', ' ', query)
        # 确保花括号前后有空格
        query = re.sub(r'{\s*', '{ ', query)
        query = re.sub(r'\s*}', ' }', query)
        return query.strip()
        
    def _generate_query(self, field_name: str, field_info: Dict[str, Any]) -> str:
        """
        为字段生成查询语句
        
        Args:
            field_name: 字段名称
            field_info: 字段信息
            
        Returns:
            str: 格式化的GraphQL查询语句
        """
        # 确定操作类型
        operation_type = self._determine_operation_type(field_name)
        
        # 构建查询参数
        args_str = ""
        if field_info['args']:
            args_parts = []
            for arg_name, arg_info in field_info['args'].items():
                arg_type = arg_info['type']
                # 生成所有参数，而不仅仅是必填参数
                args_parts.append(f"{arg_name}: ${arg_name}")
                    
            if args_parts:
                args_str = f"({', '.join(args_parts)})"
        
        # 构建变量定义
        variables_def = self._generate_variables_definition(field_name, field_info)
        
        # 构建查询字段
        return_type = field_info['type']
        fields_str = self._generate_fields_for_type(return_type)
        
        # 构建完整查询语句，确保字段之间有空格
        if variables_def:
            query = f"{operation_type} {field_name}{variables_def} {{ {field_name}{args_str} {{ {fields_str} }} }}"
        else:
            query = f"{operation_type} {field_name}{{ {field_name}{args_str} {{ {fields_str} }} }}"
            
        return query
        
    def _determine_operation_type(self, field_name: str) -> str:
        """
        确定字段所属的操作类型（查询、变更或订阅）
        
        Args:
            field_name: 字段名称
            
        Returns:
            str: 操作类型字符串，"query"、"mutation"或"subscription"
        """
        # 检查字段是否定义在Mutation类型中
        if self.schema.mutation_type and field_name in getattr(self.schema.types.get(self.schema.mutation_type), 'fields', {}):
            return "mutation"
        # 检查字段是否定义在Subscription类型中
        elif self.schema.subscription_type and field_name in getattr(self.schema.types.get(self.schema.subscription_type), 'fields', {}):
            return "subscription"
        # 默认为查询操作
        else:
            return "query"
            
    def _generate_variables_definition(self, field_name: str, field_info: Dict[str, Any]) -> str:
        """
        生成变量定义字符串
        
        Args:
            field_name: 字段名称
            field_info: 字段信息
            
        Returns:
            str: 变量定义字符串，形如"($arg1: Type1!, $arg2: Type2)"
        """
        var_defs = []
        
        if field_info['args']:
            for arg_name, arg_info in field_info['args'].items():
                arg_type = arg_info['type']
                # 为所有参数生成变量定义，不仅是必填参数
                var_defs.append(f"${arg_name}: {arg_type}")
                    
        if var_defs:
            return f"({', '.join(var_defs)})"
        return ""
    
    def _generate_fields_for_type(self, type_name: str, depth: int = 0) -> str:
        """
        为类型生成查询字段
        
        Args:
            type_name: 类型名称
            depth: 当前递归深度
            
        Returns:
            str: 格式化的字段字符串
        """
        # 防止无限递归
        if depth > self.max_depth:
            return "id"
        
        # 处理列表类型和非空类型
        orig_type_name = type_name
        if type_name.startswith('[') and type_name.endswith(']'):
            inner_type = type_name[1:-1]
            if inner_type.endswith('!'):
                inner_type = inner_type[:-1]
            type_name = inner_type
        
        if type_name.endswith('!'):
            type_name = type_name[:-1]
        
        # 标量和枚举类型不需要子字段
        if type_name in self.scalar_types or type_name in self.enum_types:
            return ""
            
        # 检查类型是否存在
        if type_name not in self.schema.types:
            return "id"
        
        # 防止循环引用
        if type_name in self.generated_types and depth > 0:
            return "id"
            
        self.generated_types.add(type_name)
        
        # 获取类型对象
        type_obj = self.schema.types[type_name]
        
        # 构建字段字符串
        fields = []
        
        # 添加id字段（如果存在）
        if 'id' in type_obj.fields:
            fields.append("id")
        
        # 添加其他标量字段和选择的复杂字段
        for field_name, field_info in type_obj.fields.items():
            if field_name == 'id':
                continue
                
            field_type = field_info['type']
            
            # 处理非空标记和列表类型
            if field_type.endswith('!'):
                field_type = field_type[:-1]
                
            if field_type.startswith('[') and field_type.endswith(']'):
                field_type = field_type[1:-1]
                if field_type.endswith('!'):
                    field_type = field_type[:-1]
                
            # 判断是否应该包含该字段
            is_scalar = field_type in self.scalar_types
            is_enum = field_type in self.enum_types
            is_complex_type = field_type in self.schema.types
            has_no_args = not field_info['args']
            
            # 标量类型和枚举类型直接添加
            if is_scalar or is_enum:
                fields.append(field_name)
            # 复杂类型需要递归处理
            elif has_no_args and is_complex_type and depth < self.max_depth:
                sub_fields = self._generate_fields_for_type(field_type, depth + 1)
                if sub_fields:
                    fields.append(f"{field_name} {{ {sub_fields} }}")
        
        # 确保至少有一个字段
        if not fields and 'id' in type_obj.fields:
            fields.append("id")
        elif not fields:
            # 如果连id字段都没有，选择第一个可用的标量字段
            for field_name, field_info in type_obj.fields.items():
                field_type = field_info['type']
                if field_type.endswith('!'):
                    field_type = field_type[:-1]
                if field_type in self.scalar_types or field_type in self.enum_types:
                    fields.append(field_name)
                    break
        
        # 移除类型，允许在其他分支中使用
        self.generated_types.remove(type_name)
        
        return ", ".join(fields) 