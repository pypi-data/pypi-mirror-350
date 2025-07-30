#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema to HttpRunner 转换工具包

该包提供了将GraphQL Schema转换为HttpRunner测试用例的功能。
通过解析GraphQL Schema文件，自动生成适合HttpRunner执行的测试用例。

主要模块：
- models: 数据模型模块，定义了GraphQL Schema相关的数据结构
- parser: 解析器模块，负责解析GraphQL Schema文件
- introspection: 内省查询模块，通过内省查询获取GraphQL Schema
- generator: 生成器模块，负责生成HttpRunner测试用例
- query_generator: 查询语句生成器模块，负责生成GraphQL查询语句列表
- report_generator: 查询语句文件差异报告生成模块，用于在GraphQL Schema发生变更时生成详细的差异比较报告
- main: 主入口模块，提供命令行接口
"""

__version__ = '1.8.0'
__author__ = 'YouMi QA Team'

from .models import GraphQLType, GraphQLSchema
from .parser import GraphQLSchemaParser
from .introspection import fetch_schema_from_introspection, IntrospectionQueryError
from .generator import HttpRunnerTestCaseGenerator
from .query_generator import GraphQLQueryGenerator
from .report_generator import generate_markdown_diff_report, generate_html_diff_report
