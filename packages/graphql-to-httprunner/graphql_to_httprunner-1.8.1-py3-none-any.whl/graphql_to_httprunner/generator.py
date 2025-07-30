#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HttpRunner 测试用例生成器

该模块提供了从GraphQL Schema生成HttpRunner测试用例的功能。它根据GraphQL Schema中
定义的查询、变更和订阅操作，生成对应的HttpRunner YAML格式测试用例文件。

主要功能：
1. 为GraphQL操作生成HttpRunner测试用例
2. 支持生成查询、变更和订阅操作的测试用例
3. 根据GraphQL类型自动生成合适的示例值
4. 递归处理嵌套类型，生成适当的查询字段
5. 生成符合HttpRunner格式要求的YAML测试用例
6. 支持生成指定单个查询的测试用例
"""

import os
import yaml
import random
import datetime
from typing import Dict, List, Any, Set
import re

from .models import GraphQLSchema


class HttpRunnerTestCaseGenerator:
    """HttpRunner测试用例生成器"""
    
    def __init__(self, schema: GraphQLSchema, base_url: str = "http://localhost:8888", max_depth: int = 2, required_only: bool = False, is_skip: bool = False, is_cite: bool = False):
        self.schema = schema
        self.base_url = base_url
        self.max_depth = max_depth
        self.required_only = required_only       # 是否只包含必选参数，默认为False（包含所有参数）
        self.is_skip = is_skip                   # 是否包含skip关键词，默认为False
        self.is_cite = is_cite                   # 是否生成API层引用测试用例，默认为False
        self.scalar_types = schema.scalar_types  # 使用从schema中解析到的标量类型集合
        self.enum_types = schema.enum_types      # 添加对枚举类型的引用
        self.generated_types: Set[str] = set()
        
    def generate_test_cases(self, output_dir: str):
        """生成所有查询操作的用例层测试用例"""
        return self._generate_cases(output_dir, is_api_layer=False)
    
    def generate_api_test_cases(self, output_dir: str):
        """生成所有查询操作的API层测试用例"""
        return self._generate_cases(output_dir, is_api_layer=True)
    
    def generate_single_test_case(self, output_dir: str, query_name: str):
        """生成单个查询操作的用例层测试用例
        
        Args:
            output_dir: 输出目录路径
            query_name: 要生成的查询名称
            
        Returns:
            int: 生成的测试用例数量，成功为1，失败为0
        """
        return self._generate_single_case(output_dir, query_name, is_api_layer=False)
    
    def generate_single_api_test_case(self, output_dir: str, query_name: str):
        """生成单个查询操作的API层测试用例
        
        Args:
            output_dir: 输出目录路径
            query_name: 要生成的查询名称
            
        Returns:
            int: 生成的测试用例数量，成功为1，失败为0
        """
        return self._generate_single_case(output_dir, query_name, is_api_layer=True)
    
    def _generate_single_case(self, output_dir: str, query_name: str, is_api_layer: bool = False):
        """生成单个查询测试用例的通用方法
        
        Args:
            output_dir: 输出目录路径
            query_name: 要生成的查询名称
            is_api_layer: 是否生成API层测试用例，默认为False（生成用例层测试用例）
            
        Returns:
            int: 生成的测试用例数量，成功为1，失败为0
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 检查查询是否存在
        if query_name not in self.schema.root_fields:
            print(f"错误：查询名称 '{query_name}' 在Schema中不存在")
            return 0
        
        field_info = self.schema.root_fields[query_name]
        # 保存测试用例
        self._save_test_case(output_dir, is_api_layer, query_name, field_info)
        print(f"生成测试用例: {output_dir}")
        return 1
    
    def _generate_cases(self, output_dir: str, is_api_layer: bool = False):
        """生成测试用例的通用方法
        
        Args:
            output_dir: 输出目录路径
            is_api_layer: 是否生成API层测试用例，默认为False（生成用例层测试用例）
            
        Returns:
            int: 生成的测试用例数量
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 记录生成的测试用例数量
        testcase_count = 0
        
        # 生成根查询测试用例
        for field_name, field_info in self.schema.root_fields.items():
            # 跳过名为 _ 的字段，这些字段通常只是占位符，没有实际测试意义
            if field_name == '_':
                print(f"跳过生成下划线字段测试用例: {field_name}")
                continue

            # 保存测试用例
            self._save_test_case(output_dir, is_api_layer, field_name, field_info)
            # 增加计数器
            testcase_count += 1
        
        # 返回生成的测试用例数量
        return testcase_count
    
    def _save_test_case(self, output_dir: str, is_api_layer: bool, field_name: str, field_info: Dict[str, Any]):
        """保存测试用例"""
        # 确定操作类型前缀
        operation_type = self._determine_operation_type(field_name)

        # 根据层级生成相应的测试用例
        if is_api_layer:
            api_definition, api_cite = self._generate_api_definition(field_name, field_info, output_dir)
            with open(os.path.join(output_dir, f"{operation_type}_{field_name}_api.yml"), 'w', encoding='utf-8') as f:
                yaml.dump(api_definition, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=9999)
            if api_cite:
                cite_output_dir = output_dir.replace("api", "testcases", 1) if 'api' in output_dir else output_dir
                os.makedirs(cite_output_dir, exist_ok=True)
                with open(os.path.join(cite_output_dir, f"{operation_type}_{field_name}_test.yml"), 'w', encoding='utf-8') as f:
                    yaml.dump(api_cite, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=9999)
        else:
            test_case = self._generate_query_test_case(field_name, field_info)
            with open(os.path.join(output_dir, f"{operation_type}_{field_name}_test.yml"), 'w', encoding='utf-8') as f:
                yaml.dump(test_case, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=9999)


    def _determine_operation_type(self, field_name: str) -> str:
        """确定字段所属的操作类型（查询、变更或订阅）"""
            
        # 检查字段是否定义在Mutation类型中
        if self.schema.mutation_type and field_name in getattr(self.schema.types.get(self.schema.mutation_type), 'fields', {}):
            return "mutation"
        # 检查字段是否定义在Subscription类型中
        elif self.schema.subscription_type and field_name in getattr(self.schema.types.get(self.schema.subscription_type), 'fields', {}):
            return "subscription"
        # 默认为查询操作
        else:
            return "query"
    
    def _compress_query(self, query: str) -> str:
        """
        压缩查询语句，移除多余空白，使其一行显示
        
        Args:
            query: 原始查询语句
            
        Returns:
            str: 压缩后的查询语句
        """
        # 替换所有连续空白为单个空格
        query = re.sub(r'\s+', ' ', query)
        # 确保花括号前后有空格
        query = re.sub(r'{\s*', '{ ', query)
        query = re.sub(r'\s*}', ' }', query)
        return query.strip()

    def _prepare_graphql_query(self, field_name: str, field_info: Dict[str, Any]) -> tuple:
        """准备GraphQL查询信息
        
        Args:
            field_name: 字段名称
            field_info: 字段信息
            
        Returns:
            tuple: 包含以下元素的元组
                - operation_type: 操作类型（查询、变更或订阅）
                - operation_name: 操作名称（"query"、"mutation"或"subscription"）
                - operation_description: 操作描述（中文）
                - variables: 变量字典
                - query: 构造的GraphQL查询语句
        """
        # 确定操作类型
        operation_type = self._determine_operation_type(field_name)
        operation_name = "query" if operation_type == "query" else "mutation" if operation_type == "mutation" else "subscription"
        operation_description = "查询" if operation_type == "query" else "变更" if operation_type == "mutation" else "订阅"
        
        # 构建查询参数
        variables = {}
        args_str = ""
        var_defs_parts = []  # 用于保存变量定义部分
        
        if field_info['args']:
            args_parts = []
            for arg_name, arg_info in field_info['args'].items():
                # 获取原始参数类型
                arg_type = arg_info['type']
                
                # 默认为所有参数生成适合该类型的示例值
                variables[arg_name] = self._generate_example_value(arg_type)

                # 当只需要为必选参数生成示例值，则删除可选参数示例值
                if self.required_only and not arg_type.endswith('!'):
                    del variables[arg_name]
                
                # 构建参数字符串
                args_parts.append(f"{arg_name}: ${arg_name}")
                
                # 添加变量定义，使用原始类型
                var_defs_parts.append(f"${arg_name}: {arg_type}")

            if args_parts:
                args_str = f"({', '.join(args_parts)})"
        
        # 构建变量定义部分
        var_defs_str = f"({', '.join(var_defs_parts)})" if var_defs_parts else ""
        
        # 构建查询字段
        return_type = field_info['type']
        fields_str = self._generate_fields_for_type(return_type)
        
        # 构建GraphQL查询
        query = f"""{operation_name} {field_name}{var_defs_str} {{
  {field_name}{args_str} {{
{fields_str}
  }}
}}"""
        
        # 压缩查询为一行
        query = self._compress_query(query)
        
        # 转义GraphQL查询中的$符号，避免与HttpRunner变量语法冲突
        query = query.replace("$", "$$")
        
        return operation_type, operation_name, operation_description, variables, query

    def _generate_query_test_case(self, field_name: str, field_info: Dict[str, Any]) -> Dict[str, Any]:
        """生成查询测试用例"""
        # 准备GraphQL查询
        _, _, operation_description, variables, query = self._prepare_graphql_query(field_name, field_info)
        
        # 构建HttpRunner测试用例
        test_case = {
            'config': {
                'name': f"{field_name} {operation_description}测试",
                'base_url': self.base_url if self.base_url.startswith('http') else f"${{get_config({self.base_url},graphql_url)}}",
                'variables': {
                    'user': 'xxx_user' if self.base_url.startswith('http') else f"${{get_config({self.base_url},v0_user)}}",
                    'pwd': 'xxx_pwd' if self.base_url.startswith('http') else f"${{get_config({self.base_url},v0_pwd)}}",
                    'sessionId': 'xxx' if self.base_url.startswith('http') else f"${{get_login({self.base_url},$user,$pwd,{self.base_url}_token)}}"
                }
            },
            'teststeps': [
                {
                    'name': f"执行 {field_name} {operation_description}",
                    'request': {
                        'method': 'POST',
                        'url': "/graphql",
                        'headers': {
                            'Content-Type': 'application/json; charset=utf-8',
                            'Accept-Language': 'zh',
                            'x-operation-name': f"{field_name}"
                        },
                        'cookies': {
                            'sessionId': '$sessionId'
                        },
                        'json': {
                            'operationName': f"{field_name}",
                            'query': query,
                            'variables': variables
                        }
                    },
                    'extract': [{'data': 'content.data'}],
                    'validate': [
                        {'eq': ['status_code', 200]},
                        {'eq': ['headers.Content-Type', 'application/json']},
                        {'ne': ['content.data', None]}
                    ]
                }
            ]
        }
        if self.is_skip:
            api_items = list(test_case['teststeps'][0].items())
            api_items.insert(1, ('skipIf', '${skip_test_in_production_env()}'))
            test_case['teststeps'][0] = dict(api_items)

        return test_case

    def _generate_api_definition(self, field_name: str, field_info: Dict[str, Any], output_dir: str) -> tuple:
        """生成API层定义"""
        # 准备GraphQL查询
        operation_type, _, operation_description, variables, query = self._prepare_graphql_query(field_name, field_info)

        # 构建API定义
        api_definition = {
            'name': f"{field_name}_{operation_description}",
            'base_url': self.base_url if self.base_url.startswith('http') else f"${{get_config({self.base_url},graphql_url)}}",
            'variables': {
                'user': 'xxx_user' if self.base_url.startswith('http') else f"${{get_config({self.base_url},v0_user)}}",
                'pwd': 'xxx_pwd' if self.base_url.startswith('http') else f"${{get_config({self.base_url},v0_pwd)}}",
                'sessionId': 'xxx' if self.base_url.startswith('http') else f"${{get_login({self.base_url},$user,$pwd,{self.base_url}_token)}}"
            },
            'request': {
                'method': 'POST',
                'url': "/graphql",
                'headers': {
                    'Content-Type': 'application/json; charset=utf-8',
                    'Accept-Language': 'zh',
                    'x-operation-name': f"{field_name}"
                },
                'cookies': {
                    'sessionId': '$sessionId'
                },
                'json': {
                    'operationName': f"{field_name}",
                    'query': query,
                    'variables': variables
                }
            },
            'validate': [
                {'eq': ['status_code', 200]},
                {'eq': ['headers.Content-Type', 'application/json']},
                {'ne': ['content.data', None]}
            ]
        }
        if self.is_skip:
            api_items = list(api_definition.items())
            api_items.insert(1, ('skipIf', '${skip_test_in_production_env()}'))
            api_definition = dict(api_items)

        # 构建API引用用例
        api_cite = None
        if self.is_cite:
            api_cite = {
                'config': {
                    'name': f"{field_name} {operation_description}测试"
                },
                'teststeps': [
                    {
                        'name': f"执行 {field_name} {operation_description}",
                        'api': f'{output_dir}/{operation_type}_{field_name}_api.yml',
                        'extract': [{'data': 'content.data'}],
                        'validate': [
                            {'eq': ['status_code', 200]},
                            {'eq': ['headers.Content-Type', 'application/json']},
                            {'ne': ['content.data', None]}
                        ]
                    }
                ]
            }
            if self.is_skip:
                api_items = list(api_cite['teststeps'][0].items())
                api_items.insert(1, ('skipIf', '${skip_test_in_production_env()}'))
                api_cite['teststeps'][0] = dict(api_items)

        return api_definition, api_cite

    def _generate_variables_definition(self, variables: Dict[str, Any]) -> str:
        """生成变量定义字符串"""
        if not variables:
            return ""
            
        var_defs = []
        for var_name, var_value in variables.items():
            # 从参数信息中获取原始类型
            original_type = None
            for field_name, field_info in self.schema.root_fields.items():
                if field_info['args'] and var_name in field_info['args']:
                    original_type = field_info['args'][var_name]['type']
                    break
            
            # 始终使用原始类型定义，不要从值推断类型
            if original_type:
                var_defs.append(f"${var_name}: {original_type}")
            else:
                # 如果找不到原始类型，才使用推断类型
                var_type = self._get_graphql_type_for_value(var_value)
                var_defs.append(f"${var_name}: {var_type}")
            
        return f"({', '.join(var_defs)})"
    
    def _get_graphql_type_for_value(self, value: Any, original_type: str = None) -> str:
        """根据值获取GraphQL类型
        
        Args:
            value: 要判断类型的值
            original_type: 原始GraphQL类型定义（如果有）
        """
        # 如果提供了原始类型，优先使用原始类型
        if original_type:
            return original_type
            
        if isinstance(value, str):
            return "String"
        elif isinstance(value, int):
            return "Int"
        elif isinstance(value, float):
            return "Float"
        elif isinstance(value, bool):
            return "Boolean"
        elif value is None:
            return "String"
        elif isinstance(value, list):
            if value:
                item_type = self._get_graphql_type_for_value(value[0])
                return f"[{item_type}]"
            return "[String]"
        return "String"  # 默认为字符串类型
    
    def _generate_example_value(self, type_name: str) -> Any:
        """为给定类型生成示例值"""
        # 处理列表类型，提取内部类型
        orig_type_name = type_name
        is_list = False
        if type_name.startswith('[') and type_name.endswith(']'):
            is_list = True
            type_name = type_name[1:-1].rstrip('!')
        
        # 处理非空类型，移除'!'后缀
        is_non_null = False
        if type_name.endswith('!'):
            type_name = type_name[:-1]
            is_non_null = True
            
        # 为基本类型生成示例值
        if type_name == 'ID':
            # 使用统一的 ID 格式
            value = f"{random.randint(1, 1000)}"
        elif type_name == 'String':
            value = f"example-{random.randint(1, 1000)}"
        elif type_name == 'Int':
            value = random.randint(1, 100)
        elif type_name == 'Float':
            value = round(random.uniform(1.0, 100.0), 2)
        elif type_name == 'Boolean':
            value = random.choice([True, False])
        elif type_name == 'JSON':
            # 为JSON类型生成一个简单的JSON对象
            value = {"key": f"value-{random.randint(1, 100)}"}
        elif type_name == 'LocalDate':
            # 生成YYYY-MM-DD格式的日期
            today = datetime.date.today()
            delta = datetime.timedelta(days=random.randint(-30, 30))
            random_date = today + delta
            value = random_date.strftime("%Y-%m-%d")
        elif type_name == 'LocalDateTime':
            # 生成YYYY-MM-DDTHH:mm:ss格式的日期时间
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=random.randint(-30, 30), 
                                    hours=random.randint(0, 23),
                                    minutes=random.randint(0, 59),
                                    seconds=random.randint(0, 59))
            random_datetime = now + delta
            value = random_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        elif type_name == 'MixID':
            # 生成满足/^[\w-]*$/格式的ID
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
            value = ''.join(random.choice(chars) for _ in range(random.randint(5, 10)))
        elif type_name == 'NumID' or type_name == 'NumStr':
            # 生成纯数字ID
            value = f"{random.randint(1, 1000)}"
        elif type_name == 'Void':
            # Void类型通常表示null
            value = None
        elif type_name in self.enum_types:
            # 为枚举类型生成一个合适的值
            # 如果有enum_values可用，从中随机选择一个
            if hasattr(self.schema, 'enum_values') and type_name in self.schema.enum_values:
                enum_values = list(self.schema.enum_values[type_name])
                if enum_values:
                    value = random.choice(enum_values)
                else:
                    # 如果没有定义enum值，生成一个占位符
                    value = f"{type_name.upper()}_VALUE_{random.randint(1, 10)}"
            else:
                # 如果没有定义enum值，生成一个占位符
                value = f"{type_name.upper()}_VALUE_{random.randint(1, 10)}"
        elif type_name.endswith('Type') and type_name not in self.schema.types:
            # 处理未在Schema中明确定义但以Type结尾的类型
            value = f"{type_name.lower()}-{random.randint(1, 100)}"
        else:
            # 如果是自定义类型但不在已知自定义标量列表中，使用默认ID格式
            if type_name in self.scalar_types:
                # 对于其他自定义标量类型，默认生成字符串
                value = f"custom-{type_name.lower()}-{random.randint(1, 1000)}"
            else:
                # 对于对象类型，返回纯数字格式的ID
                value = f"{random.randint(1, 1000)}"
        
        # 如果是列表类型，生成1-3个元素的列表
        if is_list:
            list_len = random.randint(1, 3)
            # 对于基本类型，生成多个不同的值
            if type_name in self.scalar_types or type_name in self.enum_types:
                return [self._generate_example_value(type_name) for _ in range(list_len)]
            # 对于对象类型，返回多个相同的值
            return [value] * list_len
                
        return value
    
    def _generate_fields_for_type(self, type_name: str, depth: int = 0, max_depth: int = None) -> str:
        """为类型生成查询字段"""
        # 使用实例的max_depth或传入的max_depth
        if max_depth is None:
            max_depth = self.max_depth
            
        # 防止无限递归
        if depth > max_depth:
            return "    id\n"
        
        # 如果是标量类型或枚举类型，直接返回空
        if type_name in self.scalar_types or type_name in self.schema.enum_types:
            return ""
        
        # 如果是列表类型，处理内部类型
        if type_name.startswith('[') and type_name.endswith(']'):
            inner_type = type_name[1:-1]
            return self._generate_fields_for_type(inner_type, depth, max_depth)
        
        # 检查类型是否存在
        if type_name not in self.schema.types:
            return "    id\n"
        
        # 防止重复生成相同类型
        if type_name in self.generated_types and depth > 0:
            return "    id\n"
        
        self.generated_types.add(type_name)
        
        # 获取类型对象
        type_obj = self.schema.types[type_name]
        
        # 构建字段字符串
        fields = []
        
        # 添加id字段（如果存在）
        if 'id' in type_obj.fields:
            fields.append("    id")
        
        # 添加其他标量字段和选择的复杂字段
        for field_name, field_info in type_obj.fields.items():
            if field_name == 'id':
                continue
                
            field_type = field_info['type']
            
            # 处理字段类型中的非空标记
            if field_type.endswith('!'):
                field_type = field_type[:-1]
                
            # 处理列表类型
            if field_type.startswith('[') and field_type.endswith(']'):
                field_type = field_type[1:-1]
                if field_type.endswith('!'):
                    field_type = field_type[:-1]
                
            # 判断是否应该包含该字段
            is_scalar = field_type in self.scalar_types
            is_enum = field_type in self.schema.enum_types
            is_type_suffix = field_type.endswith('Type')  # 处理以Type结尾的类型
            is_complex_type = field_type in self.schema.types
            has_no_args = not field_info['args']
            
            # 标量类型、枚举类型或以Type结尾的类型都直接添加
            if is_scalar or is_enum or (is_type_suffix and not is_complex_type):
                fields.append(f"    {field_name}")
            # 复杂类型需要递归处理
            elif has_no_args and is_complex_type and depth < max_depth:
                sub_fields = self._generate_fields_for_type(field_type, depth + 1, max_depth)
                if sub_fields:
                    fields.append(f"    {field_name} {{\n{sub_fields}    }}")
        
        # 确保至少有一个字段
        if not fields:
            if 'id' in type_obj.fields:
                fields.append("    id")
            else:
                # 如果连id字段都没有，选择第一个可用的标量字段
                for field_name, field_info in type_obj.fields.items():
                    field_type = field_info['type']
                    # 处理非空类型
                    if field_type.endswith('!'):
                        field_type = field_type[:-1]
                    if field_type in self.scalar_types or field_type in self.schema.enum_types:
                        fields.append(f"    {field_name}")
                        break
        
        # 移除类型，允许在其他分支中使用
        self.generated_types.remove(type_name)
        
        return "\n".join(fields) + "\n"