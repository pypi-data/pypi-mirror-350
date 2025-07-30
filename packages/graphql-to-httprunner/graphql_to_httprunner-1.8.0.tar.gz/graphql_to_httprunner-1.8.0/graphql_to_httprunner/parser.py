#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema 解析器

该模块提供了GraphQL Schema文件的解析功能，将schema.graphql文件内容解析为
GraphQLSchema对象。支持解析类型定义、接口、枚举、标量等GraphQL Schema元素。

主要功能：
1. 解析GraphQL类型定义
2. 解析GraphQL接口定义
3. 解析GraphQL枚举和标量类型
4. 提取类型和字段的描述信息
5. 识别根查询、变更和订阅类型
"""

import re
from typing import Dict, Any, Optional, Set

from .models import GraphQLType, GraphQLSchema


class GraphQLSchemaParser:
    """GraphQL Schema解析器"""
    
    def __init__(self, schema_content: str):
        self.schema_content = schema_content
        self.schema = GraphQLSchema()
        
    def parse(self) -> GraphQLSchema:
        """解析GraphQL Schema"""
        # 解析自定义标量类型
        self._parse_scalar_types()
        
        # 解析枚举类型
        self._parse_enum_types()
        
        # 解析schema定义
        schema_match = re.search(r'schema\s*{([^}]*)}', self.schema_content)
        if schema_match:
            schema_def = schema_match.group(1)
            query_match = re.search(r'query:\s*(\w+)', schema_def)
            if query_match:
                self.schema.set_query_type(query_match.group(1))
            
            mutation_match = re.search(r'mutation:\s*(\w+)', schema_def)
            if mutation_match:
                self.schema.set_mutation_type(mutation_match.group(1))
                
            subscription_match = re.search(r'subscription:\s*(\w+)', schema_def)
            if subscription_match:
                self.schema.set_subscription_type(subscription_match.group(1))
        else:
            # Apollo GraphQL可能没有显式的schema定义，尝试找到Query类型
            print("未找到schema定义，尝试寻找Query类型...")
            query_type_match = re.search(r'type\s+Query\s*{', self.schema_content)
            if query_type_match:
                print("找到Query类型定义，设置为根查询类型")
                self.schema.set_query_type('Query')
            else:
                print("警告：未找到Query类型定义")

            mutation_type_match = re.search(r'type\s+Mutation\s*{', self.schema_content)
            if mutation_type_match:
                print("找到Mutation类型定义，设置为根变更类型")
                self.schema.set_mutation_type('Mutation')
                
            subscription_type_match = re.search(r'type\s+Subscription\s*{', self.schema_content)
            if subscription_type_match:
                print("找到Subscription类型定义，设置为根订阅类型")
                self.schema.set_subscription_type('Subscription')
        
        # 解析类型定义
        type_pattern = r'type\s+(\w+)(?:\s+implements\s+([^{]+))?\s*{([^}]*)}'
        for match in re.finditer(type_pattern, self.schema_content):
            type_name = match.group(1)
            implements_str = match.group(2) or ""
            fields_str = match.group(3)
            
            # 获取类型描述
            description = self._get_description_before(match.start())
            
            # 解析implements
            implements = [i.strip() for i in implements_str.split('&') if i.strip()]
            
            # 创建类型对象
            type_obj = GraphQLType(type_name, implements=implements, description=description)
            
            # 解析字段
            self._parse_fields(fields_str, type_obj)
            
            # 添加到schema
            self.schema.add_type(type_obj)
            
            # 如果是Root类型，解析根字段
            if type_name == self.schema.query_type:
                # 提取Root类型中直接定义的字段（不包括参数）
                root_fields = self._extract_top_level_fields(fields_str)
                
                for field_name, field_info in type_obj.fields.items():
                    # 只有在顶级字段列表中的字段才被添加为root字段
                    if field_name in root_fields:
                        self.schema.add_root_field(field_name, field_info)
                    else:
                        print(f"字段 {field_name} 不在顶级字段列表中，被忽略")
                
                # 打印最终的root_fields
                print(f"查询类型字段: {list(self.schema.root_fields.keys())}")
            
            # 如果是Mutation类型，也解析其字段
            elif type_name == self.schema.mutation_type:
                # 提取Mutation类型中直接定义的字段
                mutation_fields = self._extract_top_level_fields(fields_str)
                
                for field_name, field_info in type_obj.fields.items():
                    if field_name in mutation_fields:
                        # 将Mutation字段也添加到root_fields中
                        self.schema.add_root_field(field_name, field_info)
                    else:
                        print(f"字段 {field_name} 不在Mutation字段列表中，被忽略")
                
                print(f"添加变更类型字段: {list(self.schema.root_fields.keys())}")
            
            # 同样处理Subscription类型
            elif type_name == self.schema.subscription_type:
                # 提取Subscription类型中直接定义的字段
                subscription_fields = self._extract_top_level_fields(fields_str)
                
                for field_name, field_info in type_obj.fields.items():
                    if field_name in subscription_fields:
                        # 将Subscription字段也添加到root_fields中
                        self.schema.add_root_field(field_name, field_info)
                    else:
                        print(f"字段 {field_name} 不在Subscription字段列表中，被忽略")
                
                print(f"添加订阅类型字段: {list(self.schema.root_fields.keys())}")
        
        # 解析接口定义
        interface_pattern = r'interface\s+(\w+)\s*{([^}]*)}'
        for match in re.finditer(interface_pattern, self.schema_content):
            interface_name = match.group(1)
            fields_str = match.group(2)
            
            # 获取接口描述
            description = self._get_description_before(match.start())
            
            # 创建接口对象
            interface_obj = GraphQLType(interface_name, description=description)
            
            # 解析字段
            self._parse_fields(fields_str, interface_obj)
            
            # 添加到schema
            self.schema.add_interface(interface_obj)
        
        # 打印识别到的自定义标量类型和枚举类型
        print(f"识别到的标量类型: {self.schema.scalar_types}")
        print(f"识别到的枚举类型: {self.schema.enum_types}")
        
        return self.schema
        
    def _parse_scalar_types(self):
        """解析自定义标量类型定义"""
        scalar_pattern = r'scalar\s+(\w+)'
        for match in re.finditer(scalar_pattern, self.schema_content):
            scalar_name = match.group(1)
            self.schema.add_scalar_type(scalar_name)
            
    def _parse_enum_types(self):
        """解析枚举类型定义"""
        enum_pattern = r'enum\s+(\w+)\s*{([^}]*)}'
        for match in re.finditer(enum_pattern, self.schema_content):
            enum_name = match.group(1)
            self.schema.add_enum_type(enum_name)
            
            # 解析枚举值
            enum_values = [value.strip() for value in match.group(2).split('\n') if value.strip()]
            self.schema.add_enum_values(enum_name, enum_values)
    
    def _get_description_before(self, pos: int) -> Optional[str]:
        """获取位置前的描述注释"""
        # 向前查找最近的三引号注释
        content_before = self.schema_content[:pos].strip()
        desc_match = re.search(r'"""([^"]*)"""s*$', content_before, re.DOTALL)
        if desc_match:
            return desc_match.group(1).strip()
        return None
    
    def _parse_fields(self, fields_str: str, type_obj: GraphQLType):
        """解析字段定义"""
        # 预处理字段字符串，移除注释干扰
        cleaned_fields = []
        in_comment = False
        for line in fields_str.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 处理注释行
            if '"""' in line:
                # 检查是否是注释的开始或结束
                if line.count('"""') % 2 == 1:  # 奇数个引号，表示开始或结束注释
                    in_comment = not in_comment
                
                # 提取行中的非注释部分
                non_comment_parts = line.split('"""')
                if len(non_comment_parts) > 2:  # 有开始和结束引号
                    clean_line = non_comment_parts[0] + non_comment_parts[-1]
                    if clean_line.strip():
                        cleaned_fields.append(clean_line.strip())
                continue
                
            # 跳过完整的注释行
            if in_comment:
                continue
                
            cleaned_fields.append(line)
        
        # 合并处理后的字段字符串，便于多行字段的解析
        processed_fields_str = '\n'.join(cleaned_fields)
        
        # 使用正则表达式匹配所有字段定义
        # 字段模式：字段名(参数): 类型
        field_pattern = r'(\w+)(?:\s*\(([^)]*)\))?\s*:\s*([^\s,{]+)(!?)'
        
        # 查找所有匹配的字段
        for match in re.finditer(field_pattern, processed_fields_str):
            field_name = match.group(1)
            args_str = match.group(2) or ""
            field_type = match.group(3)
            required = bool(match.group(4))
            
            # 解析参数
            args = {}
            if args_str:
                args_pattern = r'(\w+)\s*:\s*([^\s,]+)(!?)'
                for arg_match in re.finditer(args_pattern, args_str):
                    arg_name = arg_match.group(1)
                    arg_type = arg_match.group(2)
                    arg_required = bool(arg_match.group(3))
                    args[arg_name] = {
                        'type': arg_type,
                        'required': arg_required
                    }
            
            # 检查是否是列表类型
            is_list = False
            if field_type.startswith('[') and field_type.endswith(']'):
                is_list = True
                field_type = field_type[1:-1]
            
            # 添加字段
            type_obj.add_field(field_name, {
                'type': field_type,
                'required': required,
                'is_list': is_list,
                'args': args,
                'description': None  # 简化处理，不保留描述
            })

    def _extract_top_level_fields(self, fields_str: str) -> Set[str]:
        """
        提取字段定义字符串中的顶级字段名称
        
        Args:
            fields_str: 字段定义字符串
            
        Returns:
            顶级字段名称集合
        """
        # 将字段字符串按行分割
        lines = [line.strip() for line in fields_str.split('\n')]
        
        # 存储顶级字段名称
        top_level_fields = set()
        
        # 当前正在处理的字段
        current_field = None
        in_field_def = False
        in_comment = False
        open_parens = 0
        
        # 逐行处理，识别顶级字段定义
        for line in lines:
            # 跳过空行
            if not line:
                continue
                
            # 处理注释
            if line.startswith('"""'):
                # 如果是注释的开始或结束
                if line.count('"""') % 2 == 1:  # 奇数个引号，表示开始或结束注释
                    in_comment = not in_comment
                continue
                
            # 在注释中，跳过处理
            if in_comment:
                continue
                
            # 检查是否是字段定义的开始（在行首，不缩进）
            if not in_field_def:
                # 字段定义模式: 字段名(可能有参数): 类型
                field_match = re.match(r'^(\w+)', line)
                if field_match and not line.startswith(' '):
                    current_field = field_match.group(1)
                    in_field_def = True
                    
                    # 计算括号数量 - 帮助识别多行参数定义
                    open_parens += line.count('(') - line.count(')')
                    
                    # 如果这行包含冒号且括号已关闭，表示字段定义完成
                    if ':' in line and open_parens == 0:
                        top_level_fields.add(current_field)
                        in_field_def = False
                        current_field = None
            
            # 如果在字段定义过程中，继续处理直到定义结束
            elif in_field_def:
                # 更新括号数量
                open_parens += line.count('(') - line.count(')')
                
                # 如果找到冒号且括号已平衡，那么字段定义结束
                if ':' in line and open_parens <= 0:
                    top_level_fields.add(current_field)
                    in_field_def = False
                    current_field = None
        
        # 创建一个全局字段模式匹配，用于捕获可能被上面方法遗漏的字段
        # 特别是对于有多行复杂定义和注释的字段
        field_pattern = r'^\s*(\w+)\s*\('
        
        # 使用正则表达式查找所有可能的字段定义
        raw_content = '\n'.join(line for line in fields_str.split('\n') if line.strip())
        for match in re.finditer(field_pattern, raw_content, re.MULTILINE):
            top_level_fields.add(match.group(1))
        
        return top_level_fields 