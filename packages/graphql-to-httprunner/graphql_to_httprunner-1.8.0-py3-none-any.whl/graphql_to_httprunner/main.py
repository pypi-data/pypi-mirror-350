#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema to HttpRunner 测试用例转换工具

该模块是GraphQL Schema到HttpRunner测试用例转换工具的主入口。
处理命令行参数，读取GraphQL Schema文件，协调调用解析器和生成器模块。

主要功能：
1. 解析命令行参数，提供友好的命令行界面
2. 读取GraphQL Schema文件或通过内省查询获取Schema
3. 协调调用SchemaParser解析Schema
4. 协调调用TestCaseGenerator生成测试用例
5. 协调调用QueryGenerator生成查询语句列表
6. 支持通过配置文件批量生成多个项目的测试用例
7. 支持指定单个查询名称生成特定查询或测试用例
"""

import argparse
import sys
import os
import csv
import time
import shutil

from . import __version__
from .parser import GraphQLSchemaParser
from .generator import HttpRunnerTestCaseGenerator
from .query_generator import GraphQLQueryGenerator
from .introspection import fetch_schema_from_introspection, IntrospectionQueryError
from .utils import backup_queries_file, compare_query_files, auto_update_testcases


def process_single_project(introspection_url=None, schema_file=None, output='query.yml', base_url="http://localhost:8888",
                         max_depth=2, is_api=False, is_cite=False, required=False, is_skip=False, is_testcases=True, project_name=None, query_name=None):
    """处理单个项目"""
    schema = None
    
    # 生成用例时，重置默认输出目录
    if is_testcases and output == 'query.yml':
        if is_api:
            output = 'api'
        else:
            output = 'testcases'
    
    # 从Schema文件中读取
    if schema_file:
        # 检查Schema文件是否存在
        if not os.path.isfile(schema_file):
            print(f"错误：Schema文件 '{schema_file}' 不存在")
            return False
        
        # 读取Schema文件
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_content = f.read()
        except Exception as e:
            print(f"读取Schema文件时出错: {e}")
            return False
        
        # 解析Schema
        print(f"开始解析GraphQL Schema文件: {schema_file}")
        try:
            parser = GraphQLSchemaParser(schema_content)
            schema = parser.parse()
        except Exception as e:
            print(f"解析Schema文件时出错: {e}")
            return False
    
    # 通过内省查询获取Schema
    elif introspection_url:
        try:
            schema = fetch_schema_from_introspection(introspection_url)
        except IntrospectionQueryError as e:
            print(f"内省查询失败: {e}")
            return False
        except Exception as e:
            print(f"获取Schema时出错: {e}")
            return False
    
    # 如果指定了查询名称，检查它是否存在于Schema中
    if query_name and query_name not in schema.root_fields:
        print(f"错误：指定的查询名称 '{query_name}' 在Schema中不存在")
        print(f"可用的查询名称有: {', '.join(schema.root_fields.keys())}")
        return False
    
    # 生成测试用例
    if is_testcases:
        output_type = "API层" if is_api else "用例层"
        print(f"\n开始生成HttpRunner {output_type}测试用例...")
        try:
            generator = HttpRunnerTestCaseGenerator(schema, base_url, max_depth, required, is_skip, is_cite)

            if is_api:
                if query_name:
                    # 只生成指定查询的API层测试用例
                    testcase_count = generator.generate_single_api_test_case(output, query_name)
                    print(f"\n已生成{testcase_count}个API层测试用例到目录: {output}")
                else:
                    testcase_count = generator.generate_api_test_cases(output)
                    print(f"\n已生成{testcase_count}个API层测试用例到目录: {output}")
            else:
                if query_name:
                    # 只生成指定查询的用例层测试用例
                    testcase_count = generator.generate_single_test_case(output, query_name)
                    print(f"\n已生成{testcase_count}个用例层测试用例到目录: {output}")
                else:
                    testcase_count = generator.generate_test_cases(output)
                    print(f"\n已生成{testcase_count}个用例层测试用例到目录: {output}")

        except Exception as e:
            print(f"生成测试用例时出错: {e}")
            return False
    
    # 生成查询语句列表
    else:
        print(f"\n开始生成GraphQL查询语句列表...")
        try:
            generator = GraphQLQueryGenerator(schema, max_depth)
            
            if query_name:
                # 只生成指定查询的查询语句
                queries = generator.generate_queries(output, project_name, query_name)
                print(f"\n已生成{query_name}查询语句到文件: {output}")
            else:
                queries = generator.generate_queries(output, project_name)
                query_count = len(queries)
                print(f"\n已生成{query_count}个查询语句到文件: {output}")
        except Exception as e:
            print(f"生成查询语句时出错: {e}")
            return False
    
    print(f"使用的最大查询深度: {max_depth}")
    print(f"使用的基础URL或产品名: {base_url}")
    if is_testcases:
        print(f"是否只包含必选参数：{'是' if required else '否'}")
        print(f"是否包含skip关键词：{'是' if is_skip else '否'}")
        if is_api:
            print(f"是否生成引用API层测试用例：{'是' if is_cite else '否'}")
            if is_cite:
                print(f"引用API层测试用例输出目录：{output.replace('api', 'testcases', 1) if 'api' in output else output}")
    
    return True


def batch_generate(config_file, is_testcases=True, queries_file='query.yaml', is_generate_report=False):
    """
    批量生成HttpRunner测试用例
    
    Args:
        config_file (str): 批量处理配置文件路径
        is_testcases (bool): 是否生成测试用例
        queries_file (str): 指定批量处理模式生成查询语句文件路径，默认为query.yaml，当查询语句文件已存在时，会进行备份、与新文件对比并生成差异报告，以及可以更新测试用例
        is_generate_report (bool): 是否生成查询语句文件差异报告

    Returns:
        True or dict: 批量生成成功返回True，当批量生成查询语句列表且相对旧文件有变更时，返回差异变更结果字典，用于更新测试用例
    """
    
    if not os.path.exists(config_file):
        print(f"错误：配置文件 '{config_file}' 不存在")
        sys.exit(1)
    
    print(f"开始批量生成测试用例，配置文件：{config_file}")
    
    # 读取配置文件
    projects = []
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                projects.append(row)
    except Exception as e:
        print(f"读取配置文件时出错: {e}")
        sys.exit(1)
    
    if not projects:
        print("配置文件中没有发现项目")
        sys.exit(1)
    
    backup_file = None
    if not is_testcases and os.path.exists(queries_file):
        # 备份旧查询语句文件
        backup_file = backup_queries_file(queries_file)
    
    # 批量处理每个项目
    success_count = 0
    failed_count = 0
    skipped_count = 0
    for project in projects:
        project_name = project["project_name"]
        
        # 检查项目是否已下线，如果已下线则跳过
        if project.get("offline", "false").lower() == "true":
            print(f"\n{'='*80}")
            print(f"跳过已下线项目: {project_name}")
            skipped_count += 1
            continue
            
        introspection_url = project["introspection_url"]
        output = project["output"] if is_testcases else queries_file
        base_url = project["base_url"]
        max_depth = int(project.get("max_depth", 2))
        required = project.get("is_required", "false").lower() == "true"
        is_api = project.get("is_api", "false").lower() == "true"
        is_cite = project.get("is_cite", "false").lower() == "true"
        is_skip = project.get("is_skip", "false").lower() == "true"
        
        print(f"\n{'='*80}")
        print(f"开始处理项目: {project_name}")
        
        # 处理单个项目
        start_time = time.time()
        result = process_single_project(
            introspection_url=introspection_url,
            output=output,
            base_url=base_url,
            max_depth=max_depth,
            is_api=is_api,
            is_cite=is_cite,
            required=required,
            is_skip=is_skip,
            is_testcases=is_testcases,
            project_name=project_name
        )
        
        if result:
            success_count += 1
            end_time = time.time()
            print(f"生成完成，耗时: {end_time - start_time:.2f}秒")
        else:
            failed_count += 1
            print(f"生成失败，请稍后重新生成！")
        
    # 输出总结
    print(f"\n{'='*80}")
    print(f"批量生成任务完成")
    print(f"成功处理项目数: {success_count}")
    print(f"失败处理项目数: {failed_count}")
    print(f"跳过已下线项目数: {skipped_count}")
    print(f"总项目数: {len(projects)}")

    # 如果存在失败项目，则退出程序
    if failed_count > 0:
        # 如果生成查询语句文件失败且有备份文件，则删除新文件并恢复备份文件
        if not is_testcases and backup_file:
            if os.path.exists(queries_file):
                os.remove(queries_file)
            if backup_file:
                shutil.copy2(backup_file, queries_file)
                os.remove(backup_file)
            print(f"注意：生成查询语句文件时，存在失败项目，已删除新文件并恢复备份文件！")
        sys.exit(1)

    # 生成查询语句文件差异报告
    if is_generate_report:
        print(f"\n{'='*80}")
        diff_result = compare_query_files(backup_file, queries_file)
        return diff_result

    return True


def auto_update(config_file, queries_file):
    """根据差异报告自动更新测试用例"""
    if not os.path.exists(config_file):
        print(f"错误：配置文件 '{config_file}' 不存在")
        sys.exit(1)
        
    if not os.path.exists(queries_file):
        print(f"错误：查询语句文件 '{queries_file}' 不存在")
        sys.exit(1)

    # 批模式生成查询语句文件和进行差异对比
    diff_result = batch_generate(config_file, is_testcases=False, queries_file=queries_file, is_generate_report=True)
    
    # 有差异，根据变更内容自动更新测试用例
    if diff_result:
        auto_update_testcases(diff_result, config_file, queries_file)
    else:
        print("无差异，无需更新测试用例!")
        sys.exit(1)  # 注意：无差异和异常都返回 False，方便Jenkins命令行集成

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='将GraphQL Schema转换为HttpRunner测试用例或查询语句')
    
    # 添加版本信息选项
    parser.add_argument('-V', '--version', action='store_true', help='显示版本信息')
    
    # 添加批处理配置文件选项
    parser.add_argument('-b', '--batch', help='批量处理配置文件路径，如 config.csv')
    
    # 创建互斥组，schema文件和内省查询URL只能二选一
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument('-f', '--schema-file', help='GraphQL Schema文件路径')
    source_group.add_argument('-i', '--introspection-url', help='GraphQL内省查询URL，如http://localhost:9527/graphql')
    
    # 创建互斥组，生成测试用例或查询语句列表
    output_type_group = parser.add_mutually_exclusive_group()
    output_type_group.add_argument('-t', '--testcases', action='store_true', help='生成HttpRunner测试用例')
    output_type_group.add_argument('-q', '--queries', action='store_true', help='生成GraphQL查询语句列表')
    
    parser.add_argument('-o', '--output', default='query.yml', help='生成结果输出路径，根据生成类型默认为api、testcases、query.yml三种情况') # 批量处理模式生成的查询语句文件默认为query.yaml
    parser.add_argument('-u', '--base-url', default='http://localhost:8888', help='API基础URL或项目名，项目名用来作为自定义函数参数生成API基础URL')
    parser.add_argument('-d', '--max-depth', type=int, default=2, help='GraphQL查询嵌套的最大深度，默认为2')
    parser.add_argument('--api', action='store_true', help='生成API层测试用例而非用例层测试用例')
    parser.add_argument('--cite', action='store_true', help='生成引用API层测试用例（与--api选项一起使用）')
    parser.add_argument('--required', action='store_true', help='只包含必选参数，默认情况下包含所有参数')
    parser.add_argument('--skip', action='store_true', help='生成的测试用例是否包含skip关键词')
    parser.add_argument('--project', default='project_name', help='指定项目名称')
    parser.add_argument('--report', action='store_true', help='与旧查询语句文件对比生成差异报告（与-q选项一起使用）')
    parser.add_argument('-a', '--auto-update', action='store_true', help='自动更新测试用例（与-b选项一起使用）')
    parser.add_argument('--queries-file', default='query.yaml', help='指定批模式时查询语句文件生成路径，默认为query.yaml (与-b选项一起使用)')
    parser.add_argument('--query-name', help='指定要生成的单个查询名称，只生成该查询的测试用例或查询语句')
    
    args = parser.parse_args()
    
    # 如果指定了版本信息选项，显示版本信息后退出
    if args.version:
        print(f"{__version__}")
        return
    
    if args.report:
        if not args.queries:
            print("参数错误：生成查询语句文件差异报告需要与-q选项一起使用!")
            sys.exit(1)
        if args.batch:
            if not os.path.exists(args.queries_file):
                print("参数错误：差异对比文件不存在!")
                sys.exit(1)
        else:
            if not os.path.exists(args.output):
                print("参数错误：差异对比文件不存在!")
                sys.exit(1)

    # 如果指定了自动更新选项
    if args.auto_update:
        if not args.batch:
            print("参数错误：自动更新功能需要与-b/--batch选项一起使用")
            sys.exit(1)
        
        auto_update(args.batch, args.queries_file)
        return
    
    # 如果指定了批处理配置文件，进入批处理模式
    if args.batch:
        is_testcases = not args.queries  # 默认生成测试用例，除非指定了 -q 选项
        batch_result = batch_generate(args.batch, is_testcases, args.queries_file, args.report)
        if batch_result:
            return
        else:
            sys.exit(1)  # 注意：无差异和异常都返回 False，方便Jenkins命令行集成
    
    # 检查常规模式下必需的参数
    if not args.schema_file and not args.introspection_url:
        parser.error("参数错误：必须指定 -f/--schema-file 或 -i/--introspection-url 选项，或者使用 -b/--batch 批处理配置文件")
        
    if not args.testcases and not args.queries:
        parser.error("参数错误：必须指定 -t/--testcases 或 -q/--queries 选项")
    
    backup_file = None
    # 单项目模式下，如果生成查询语句并且输出文件已存在，则备份旧文件
    if args.queries and os.path.exists(args.output):
        backup_file = backup_queries_file(args.output)
    
    # 处理单个项目
    result = process_single_project(
        introspection_url=args.introspection_url,
        schema_file=args.schema_file,
        output=args.output,
        base_url=args.base_url,
        max_depth=args.max_depth,
        is_api=args.api,
        is_cite=args.cite,
        required=args.required,
        is_skip=args.skip,
        is_testcases=args.testcases,
        project_name=args.project,
        query_name=args.query_name
    )
    
    # 如果生成失败，则退出程序
    if not result:
        # 如果生成查询语句文件失败且有备份文件，则删除新文件并恢复备份文件
        if args.queries and backup_file:
            if os.path.exists(args.output):
                os.remove(args.output)
            if backup_file:
                shutil.copy2(backup_file, args.output)
                os.remove(backup_file)
            print(f"注意：生成查询语句文件失败，已删除新文件并恢复备份文件！")
        sys.exit(1)

    # 生成查询语句文件差异报告
    if args.report:
        single_result = compare_query_files(backup_file, args.output)
        if not single_result:
            sys.exit(1) # 注意：无差异和异常都返回 False，方便Jenkins命令行集成


if __name__ == '__main__':
    main() 