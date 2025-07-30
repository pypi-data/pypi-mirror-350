#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL Schema to HttpRunner 工具类模块

此模块提供工具函数，主要包括：
1. 查询语句文件备份功能
2. 查询语句文件差异对比与报告生成功能
3. 测试用例自动更新功能

这些功能主要用于在生成新的GraphQL查询语句时，保留旧版本并生成详细的差异比较报告，
便于用户了解API变更情况，实现API变更的可视化跟踪，并自动更新维护测试用例。
"""

import os
import shutil
import datetime
import yaml
import glob
import csv

from .report_generator import generate_markdown_diff_report, generate_html_diff_report


def backup_queries_file(file_path):
    """
    备份查询语句文件
    
    将现有的查询语句文件备份为带时间戳的文件，并删除原文件
    
    Args:
        file_path (str): 需要备份的文件路径
        
    Returns:
        str or None: 备份文件的路径，失败时返回None
    """
    if not os.path.exists(file_path):
        return None
    
    # 分离文件名和扩展名
    file_name, file_ext = os.path.splitext(file_path)
    backup_path = f"{file_name}.bak.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{file_ext}"
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"备份旧的查询语句文件: {file_path} -> {backup_path}")
        os.remove(file_path)
        print(f"删除旧的查询语句文件: {file_path}")
        return backup_path
    except Exception as e:
        print(f"备份旧查询语句文件时出错: {e}")
        return None


def compare_query_files(old_file, new_file):
    """
    比较新旧查询语句文件的差异并保存差异结果
    
    分析新旧查询语句文件的差异，生成详细的Markdown格式差异报告，
    包括项目级变更、查询级变更以及详细的文本差异
    
    Args:
        old_file (str): 旧查询语句文件路径
        new_file (str): 新查询语句文件路径
        
    Returns:
        dict or False: 如果存在差异，返回差异结果字典，否则返回False
    """
    if not os.path.exists(old_file) or not os.path.exists(new_file):
        print(f"无法进行文件对比，旧文件或新文件不存在")
        return False
    
    # 读取旧文件内容
    try:
        with open(old_file, 'r', encoding='utf-8') as f:
            old_content = yaml.safe_load(f)
    except Exception as e:
        print(f"读取旧文件内容时出错: {e}")
        return False
    
    # 读取新文件内容
    try:
        with open(new_file, 'r', encoding='utf-8') as f:
            new_content = yaml.safe_load(f)
    except Exception as e:
        print(f"读取新文件内容时出错: {e}")
        return False
    
    # 分析差异
    diff_result = {
        "added_projects": [],
        "removed_projects": [],
        "modified_projects": {},
        "added_queries": {},
        "removed_queries": {},
        "modified_queries": {},
    }
    
    # 检查项目级差异
    old_projects = set(old_content.keys())
    new_projects = set(new_content.keys())
    
    diff_result["added_projects"] = list(new_projects - old_projects)
    diff_result["removed_projects"] = list(old_projects - new_projects)
    
    # 对于共同存在的项目，检查查询语句差异
    common_projects = old_projects.intersection(new_projects)
    for project in common_projects:
        old_queries = set(old_content[project].keys())
        new_queries = set(new_content[project].keys())
        
        # 检查是否有查询语句差异
        added_queries = new_queries - old_queries
        if added_queries:
            diff_result["added_queries"][project] = list(added_queries)
        
        removed_queries = old_queries - new_queries
        if removed_queries:
            diff_result["removed_queries"][project] = list(removed_queries)
        
        # 检查共同查询语句的内容差异
        common_queries = old_queries.intersection(new_queries)
        modified_queries = []
        
        for query in common_queries:
            if old_content[project][query] != new_content[project][query]:
                modified_queries.append(query)
        
        if modified_queries:
            diff_result["modified_queries"][project] = modified_queries
        
        # 如果项目有任何变化，记录到modified_projects
        if (project in diff_result["added_queries"] or 
            project in diff_result["removed_queries"] or 
            project in diff_result["modified_queries"]):
            diff_result["modified_projects"][project] = {
                "added_queries": diff_result["added_queries"].get(project, []),
                "removed_queries": diff_result["removed_queries"].get(project, []),
                "modified_queries": diff_result["modified_queries"].get(project, [])
            }
    
    # 判断是否存在差异
    has_difference = (diff_result["added_projects"] or 
                     diff_result["removed_projects"] or 
                     diff_result["modified_projects"])
    
    if has_difference:
        # 生成时间戳
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
        # 生成并保存Markdown格式差异结果报告
        md_diff_file = f"{new_file}.{timestamp}.diff.md"
        try:
            md_content = generate_markdown_diff_report(diff_result, old_content, new_content, old_file, new_file)
            with open(md_diff_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(md_content))
            print(f"生成查询语句差异报告(Markdown格式): {md_diff_file}")
        except Exception as e:
            print(f"保存查询语句差异报告(Markdown格式)时出错: {e}")
            return False
        
        # 生成并保存HTML格式差异结果
        html_diff_file = f"{new_file}.{timestamp}.diff.html"
        try:
            html_content = generate_html_diff_report(diff_result, old_content, new_content, old_file, new_file)
            with open(html_diff_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"生成查询语句差异报告(HTML格式): {html_diff_file}")
        except Exception as e:
            print(f"保存查询语句差异报告(HTML格式)时出错: {e}")
            return False
        
        # 输出汇总信息
        print(f"\n新旧查询语句文件差异比较结果:")
        if diff_result["added_projects"]:
            print(f"- 新增项目: {len(diff_result['added_projects'])}")
        if diff_result["removed_projects"]:
            print(f"- 移除项目: {len(diff_result['removed_projects'])}")
        
        modified_count = len(diff_result["modified_projects"])
        if modified_count:
            print(f"- 修改项目: {modified_count}")
            
            added_queries_count = sum(len(queries) for queries in diff_result["added_queries"].values())
            if added_queries_count:
                print(f"  - 新增查询: {added_queries_count}")
            
            removed_queries_count = sum(len(queries) for queries in diff_result["removed_queries"].values())
            if removed_queries_count:
                print(f"  - 移除查询: {removed_queries_count}")
            
            modified_queries_count = sum(len(queries) for queries in diff_result["modified_queries"].values())
            if modified_queries_count:
                print(f"  - 修改查询: {modified_queries_count}")
        
        print("详细差异报告已生成成功！")
        # 返回差异结果
        return diff_result
    else:
        print(f"\n查询语句文件比较结果: 没有发现差异！")
        return False


def find_testcase_files(output_dir, operation_type, query_name, is_api=False):
    """
    查找与指定查询对应的测试用例文件
    
    Args:
        output_dir (str): 输出目录路径
        operation_type (str): 操作类型（query或mutation）
        query_name (str): 查询名称
        is_api (bool): 是否查找API层测试用例
        
    Returns:
        list: 匹配的测试用例文件路径列表
    """
    file_suffix = "_api.yml" if is_api else "_test.yml"
    pattern = os.path.join(output_dir, f"{operation_type}_{query_name}{file_suffix}")
    return glob.glob(pattern)


def delete_testcase_files(output_dir, operation_type, query_name, is_api=False):
    """
    删除与指定查询对应的测试用例文件
    
    Args:
        output_dir (str): 输出目录路径
        operation_type (str): 操作类型（query或mutation）
        query_name (str): 查询名称
        is_api (bool): 是否删除API层测试用例
        
    Returns:
        int: 删除的文件数量
    """
    files = find_testcase_files(output_dir, operation_type, query_name, is_api)
    deleted_count = 0
    
    for file_path in files:
        try:
            os.remove(file_path)
            print(f"删除测试用例文件: {file_path}")
            deleted_count += 1
        except Exception as e:
            print(f"删除测试用例文件失败: {file_path}, 错误: {e}")
    
    return deleted_count


def update_testcase_query(file_path, new_query):
    """
    更新测试用例文件中的查询语句
    
    Args:
        file_path (str): 测试用例文件路径
        new_query (str): 新的查询语句
        
    Returns:
        bool: 更新是否成功
    """
    try:
        # 读取测试用例文件
        with open(file_path, 'r', encoding='utf-8') as f:
            testcase = yaml.safe_load(f)
        
        # 更新查询语句
        if 'teststeps' in testcase and isinstance(testcase['teststeps'], list) and len(testcase['teststeps']) > 0:
            # 用例层测试用例
            if 'request' in testcase['teststeps'][0] and 'json' in testcase['teststeps'][0]['request']:
                json_data = testcase['teststeps'][0]['request']['json']
                if 'query' in json_data:
                    # 转义GraphQL查询中的$符号，避免与HttpRunner变量语法冲突
                    json_data['query'] = new_query.replace("$", "$$")
        elif 'request' in testcase and 'json' in testcase['request']:
            # API层测试用例
            json_data = testcase['request']['json']
            if 'query' in json_data:
                # 转义GraphQL查询中的$符号，避免与HttpRunner变量语法冲突
                json_data['query'] = new_query.replace("$", "$$")
        
        # 保存更新后的测试用例
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(testcase, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=9999)
        
        print(f"更新测试用例文件查询语句: {file_path}")
        return True
    except Exception as e:
        print(f"更新测试用例文件查询语句失败: {file_path}, 错误: {e}")
        return False


def determine_operation_type(query):
    """
    根据查询语句确定操作类型
    
    Args:
        query (str): 查询语句
        
    Returns:
        str: 操作类型（"query"或"mutation"）
    """
    # 检查查询语句是否以mutation开头
    if query.strip().startswith("mutation"):
        return "mutation"
    return "query"


def auto_update_testcases(diff_result, config_file, queries_file):
    """
    根据差异报告自动更新测试用例
    
    Args:
        diff_result (dict): 差异比较结果
        config_file (str): 配置文件路径
        queries_file (str): 查询语句文件路径
        
    Returns:
        dict: 更新统计结果
    """
    if not diff_result:
        print("没有变更需要处理")
        return {}
    
    # 读取配置文件
    projects_config = {}
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                projects_config[row["project_name"]] = row
    except Exception as e:
        print(f"读取配置文件时出错: {e}")
        return {}
    
    # 读取查询语句文件
    try:
        with open(queries_file, 'r', encoding='utf-8') as f:
            queries_content = yaml.safe_load(f)
    except Exception as e:
        print(f"读取查询语句文件时出错: {e}")
        return {}
    
    # 更新统计
    stats = {
        "new_projects": 0,
        "removed_projects": 0,
        "added_queries": 0,
        "removed_queries": 0,
        "modified_queries": 0
    }
    
    print(f"\n{'='*80}")
    print("开始自动更新测试用例:")
    
    # 处理新增项目
    for project in diff_result.get("added_projects", []):
        if project in projects_config:
            config = projects_config[project]
            output_dir = config["output"]
            introspection_url = config["introspection_url"]
            base_url = config["base_url"]
            max_depth = int(config.get("max_depth", 2))
            required = config.get("is_required", "false").lower() == "true"
            is_api = config.get("is_api", "false").lower() == "true"
            
            print(f"\n处理新增项目: {project}")
            
            # 如果输出目录不存在，则创建
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # 导入process_single_project函数
            from .main import process_single_project
            
            # 生成新项目的测试用例
            result = process_single_project(
                introspection_url=introspection_url,
                output=output_dir,
                base_url=base_url,
                max_depth=max_depth,
                is_api=is_api,
                required=required,
                is_testcases=True,
                project_name=project
            )
            
            if result:
                stats["new_projects"] += 1
                print(f"新增项目 {project} 的测试用例生成成功")
            else:
                print(f"新增项目 {project} 的测试用例生成失败")
        else:
            print(f"新增项目 {project} 在配置文件中未找到，跳过处理")
    
    # 处理移除项目
    for project in diff_result.get("removed_projects", []):
        if project in projects_config:
            config = projects_config[project]
            output_dir = config["output"]
            
            if os.path.exists(output_dir):
                try:
                    print(f"\n处理移除项目: {project}")
                    
                    # 删除项目目录
                    shutil.rmtree(output_dir)
                    stats["removed_projects"] += 1
                    print(f"移除项目 {project} 的测试用例目录: {output_dir}")
                except Exception as e:
                    print(f"移除项目 {project} 的测试用例目录失败: {e}")
        else:
            print(f"移除项目 {project} 在配置文件中未找到，跳过处理")
    
    # 处理修改项目
    for project, changes in diff_result.get("modified_projects", {}).items():
        if project in projects_config:
            config = projects_config[project]
            output_dir = config["output"]
            is_api = config.get("is_api", "false").lower() == "true"
            
            print(f"\n处理修改项目: {project}")
            
            # 处理移除的查询
            for query in changes.get("removed_queries", []):
                # 确定操作类型
                if project in queries_content and query in queries_content[project]:
                    print(f"ERROR: 查询 {query} 在新的查询语句中存在，但在差异报告中被标记为移除！")
                    continue
                
                # 由于旧查询已不存在，无法确定操作类型，尝试删除query和mutation两种类型的文件
                deleted_count = delete_testcase_files(output_dir, "query", query, is_api)
                deleted_count += delete_testcase_files(output_dir, "mutation", query, is_api)
                
                if deleted_count > 0:
                    stats["removed_queries"] += 1
                    print(f"移除查询 {query} 的测试用例文件，共 {deleted_count} 个")
            
            # 处理新增的查询
            added_queries = changes.get("added_queries", [])
            if added_queries:
                # 导入需要的模块
                from .introspection import fetch_schema_from_introspection
                from .generator import HttpRunnerTestCaseGenerator
                try:
                    introspection_url = config["introspection_url"]
                    base_url = config["base_url"]
                    max_depth = int(config.get("max_depth", 2))
                    required = config.get("is_required", "false").lower() == "true"
                    is_skip = config.get("is_skip", "false").lower() == "true"
                    is_cite = config.get("is_cite", "false").lower() == "true"
                    # 获取GraphQL Schema
                    schema = fetch_schema_from_introspection(introspection_url)
                    # 创建生成器
                    generator = HttpRunnerTestCaseGenerator(schema, base_url, max_depth, required, is_skip, is_cite)
                    # 生成新增查询的测试用例
                    for query in added_queries:
                        result = generator.generate_single_test_case(output_dir, query)
                        if result == 1:
                            stats["added_queries"] += 1
                            print(f"新增查询 {query} 的测试用例文件生成成功")
                        else:
                            print(f"新增查询 {query} 的测试用例文件生成失败")
                except Exception as e:
                    print(f"获取{project}项目的GraphQL Schema失败: {e}，无法生成新增查询的测试用例：{added_queries}")
                    continue

            # 处理修改的查询
            for query in changes.get("modified_queries", []):
                if project in queries_content and query in queries_content[project]:
                    query_text = queries_content[project][query]
                    operation_type = determine_operation_type(query_text)
                    
                    print(f"处理修改查询: {query}")
                    
                    # 查找对应的测试用例文件
                    files = find_testcase_files(output_dir, operation_type, query, is_api)
                    
                    if files:
                        for file_path in files:
                            # 更新测试用例中的查询语句
                            if update_testcase_query(file_path, query_text):
                                stats["modified_queries"] += 1
                    else:
                        print(f"注意：未找到修改查询 {query} 对应的测试用例文件，跳过")
                        # # 未找到修改查询，作为新增查询处理
                        # from .introspection import fetch_schema_from_introspection
                        # from .generator import HttpRunnerTestCaseGenerator
                        # try:
                        #     introspection_url = config["introspection_url"]
                        #     base_url = config["base_url"]
                        #     max_depth = int(config.get("max_depth", 2))
                        #     required = config.get("is_required", "false").lower() == "true"
                        #     is_skip = config.get("is_skip", "false").lower() == "true"
                        #     is_cite = config.get("is_cite", "false").lower() == "true"
                        #     # 获取GraphQL Schema
                        #     schema = fetch_schema_from_introspection(introspection_url)
                        #     # 创建生成器
                        #     generator = HttpRunnerTestCaseGenerator(schema, base_url, max_depth, required, is_skip, is_cite)
                        #     result = generator.generate_single_test_case(output_dir, query)
                        #     if result == 1:
                        #         stats["added_queries"] += 1
                        #         print(f"修改查询 {query} 未找到原测试用例，直接创建新用例成功")
                        #     else:
                        #         print(f"修改查询 {query} 未找到原测试用例，直接创建新用例失败")
                        # except Exception as e:
                        #     print(f"生成修改查询 {query} 的测试用例失败: {e}")
        else:
            print(f"修改项目 {project} 在配置文件中未找到，跳过处理")
    
    # 输出更新统计
    print(f"\n{'='*80}")
    print("自动更新测试用例完成:")
    print(f"- 新增项目: {stats['new_projects']}")
    print(f"- 移除项目: {stats['removed_projects']}")
    print(f"- 新增查询: {stats['added_queries']}")
    print(f"- 移除查询: {stats['removed_queries']}")
    print(f"- 修改查询: {stats['modified_queries']}")
    
    return stats