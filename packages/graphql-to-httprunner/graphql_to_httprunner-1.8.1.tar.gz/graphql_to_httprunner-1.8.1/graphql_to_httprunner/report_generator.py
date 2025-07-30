#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GraphQL 查询语句文件差异报告生成模块

此模块提供了差异报告生成功能，主要包括：
1. Markdown格式的差异报告生成
2. HTML格式的差异报告生成

这些功能用于在GraphQL Schema发生变更时，生成详细的差异比较报告，
便于用户直观地了解API变更情况，实现API变更的可视化跟踪。
"""

import datetime
import difflib


def generate_markdown_diff_report(diff_result, old_content, new_content, old_file, new_file):
    """
    基于结构化的差异数据生成Markdown格式报告
    
    Args:
        diff_result (dict): 差异结果字典
        old_content (dict): 旧文件内容
        new_content (dict): 新文件内容
        old_file (str): 旧文件路径
        new_file (str): 新文件路径
        
    Returns:
        str: Markdown格式的差异报告
    """    
    # 生成详细的文本差异
    diff_lines = []
    diff_lines.append("# GraphQL API 变更监测报告")
    diff_lines.append(f"## 旧文件: {old_file}")
    diff_lines.append(f"## 新文件: {new_file}")
    diff_lines.append("")
    
    # 添加项目级差异信息
    if diff_result["added_projects"]:
        diff_lines.append("## 新增项目")
        for project in diff_result["added_projects"]:
            diff_lines.append(f"- {project}")
        diff_lines.append("")
    
    if diff_result["removed_projects"]:
        diff_lines.append("## 移除项目")
        for project in diff_result["removed_projects"]:
            diff_lines.append(f"- {project}")
        diff_lines.append("")
    
    # 添加查询语句差异信息
    if diff_result["modified_projects"]:
        diff_lines.append("## 修改项目")
        for project, changes in diff_result["modified_projects"].items():
            diff_lines.append(f"### {project}")
            
            if changes["added_queries"]:
                diff_lines.append("#### 新增查询")
                for query in changes["added_queries"]:
                    diff_lines.append(f"- {query}")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {new_content[project][query]}")
                    diff_lines.append(f"  ```")
                diff_lines.append("")
            
            if changes["removed_queries"]:
                diff_lines.append("#### 移除查询")
                for query in changes["removed_queries"]:
                    diff_lines.append(f"- {query}")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {old_content[project][query]}")
                    diff_lines.append(f"  ```")
                diff_lines.append("")
            
            if changes["modified_queries"]:
                diff_lines.append("#### 修改查询")
                for query in changes["modified_queries"]:
                    diff_lines.append(f"- {query}")
                    diff_lines.append(f"  1. 旧语句")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {old_content[project][query]}")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  2. 新语句")
                    diff_lines.append(f"  ```")
                    diff_lines.append(f"  {new_content[project][query]}")
                    diff_lines.append(f"  ```")
                    
                    # 生成详细的文本差异
                    old_lines = old_content[project][query].splitlines()
                    new_lines = new_content[project][query].splitlines()
                    differ = difflib.Differ()
                    diff = list(differ.compare(old_lines, new_lines))
                    if len(diff) > 1:  # 如果有多于一行的差异
                        diff_lines.append(f"  3. 差异详情")
                        diff_lines.append(f"  ```diff")
                        for line in diff:
                            diff_lines.append(f"  {line}")
                        diff_lines.append(f"  ```")
                diff_lines.append("")
            
            diff_lines.append("")
    
    return diff_lines

def generate_html_diff_report(diff_result, old_content, new_content, old_file, new_file):
    """
    基于结构化的差异数据生成HTML格式报告
    
    Args:
        diff_result (dict): 差异结果字典
        old_content (dict): 旧文件内容
        new_content (dict): 新文件内容
        old_file (str): 旧文件路径
        new_file (str): 新文件路径
        
    Returns:
        str: HTML格式的差异报告
    """
    # 获取当前时间，用于报告标题
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # HTML头部
    html = [
        "<!DOCTYPE html>",
        "<html lang='zh-CN'>",
        "<head>",
        "    <meta charset='utf-8'>",
        "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "    <title>GraphQL API 变更监测报告</title>",
        "    <!-- Tailwind CSS CDN -->",
        "    <script src='https://cdn.tailwindcss.com'></script>",
        "    <!-- FontAwesome CDN -->",
        "    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'>",
        "    <!-- 代码高亮 Highlight.js -->",
        "    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css'>",
        "    <script src='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js'></script>",
        "    <script src='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/languages/graphql.min.js'></script>",
        "    <style>",
        "        /* 自定义样式补充 */",
        "        .diff-added { color: #22863a; background-color: #e6ffed; padding: 1px 5px; white-space: pre; }",
        "        .diff-removed { color: #cb2431; background-color: #ffeef0; padding: 1px 5px; white-space: pre; }",
        "        .diff-unchanged { color: #6a737d; padding: 1px 5px; white-space: pre; }",
        "        .code-block { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; position: relative; }",
        "        .code-block > div { line-height: 1.5; white-space: pre; }",
        "        .collapsible-content { max-height: 0; overflow: hidden; transition: max-height 0.3s ease-out; }",
        "        .expanded .collapsible-content { max-height: 2000px; transition: max-height 0.5s ease-in; }",
        "        .code-container { position: relative; }",
        "        .copy-btn { position: absolute; top: 5px; right: 5px; background: rgba(255,255,255,0.8); border: none; border-radius: 4px; padding: 3px 8px; cursor: pointer; font-size: 12px; display: flex; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }",
        "        .copy-btn:hover { background: rgba(255,255,255,1); }",
        "        .copy-btn i { margin-right: 3px; }",
        "    </style>",
        "    <script>",
        "        // 页面加载完成后初始化",
        "        document.addEventListener('DOMContentLoaded', function() {",
        "            // 初始化代码高亮",
        "            document.querySelectorAll('pre code').forEach(block => {",
        "                hljs.highlightElement(block);",
        "            });",
        "            ",
        "            // 初始化折叠面板",
        "            document.querySelectorAll('.collapsible-header').forEach(header => {",
        "                header.addEventListener('click', function() {",
        "                    this.parentElement.classList.toggle('expanded');",
        "                    const icon = this.querySelector('.toggle-icon');",
        "                    if (icon) {",
        "                        icon.classList.toggle('fa-chevron-down');",
        "                        icon.classList.toggle('fa-chevron-right');",
        "                    }",
        "                });",
        "            });",
        "            ",
        "            // 添加复制按钮到所有代码块",
        "            document.querySelectorAll('.code-container').forEach(container => {",
        "                const copyBtn = container.querySelector('.copy-btn');",
        "                if (copyBtn) {",
        "                    copyBtn.addEventListener('click', function() {",
        "                        const codeElement = container.querySelector('pre code') || container.querySelector('.code-block');",
        "                        let text = '';",
        "                        ",
        "                        if (codeElement.tagName.toLowerCase() === 'code') {",
        "                            text = codeElement.innerText;",
        "                        } else {",
        "                            // 对于差异详情，我们只获取非注释行的文本",
        "                            const divs = codeElement.querySelectorAll('div:not(.diff-unchanged)');",
        "                            const lines = Array.from(divs).map(div => {",
        "                                // 移除差异标记",
        "                                return div.innerText;",
        "                            });",
        "                            text = lines.join('\\n');",
        "                        }",
        "                        ",
        "                        navigator.clipboard.writeText(text).then(() => {",
        "                            const icon = this.querySelector('i');",
        "                            const originalClass = icon.className;",
        "                            icon.className = 'fas fa-check';",
        "                            this.classList.add('bg-green-100');",
        "                            setTimeout(() => {",
        "                                icon.className = originalClass;",
        "                                this.classList.remove('bg-green-100');",
        "                            }, 2000);",
        "                        }, () => {",
        "                            alert('复制失败，请手动复制');",
        "                        });",
        "                    });",
        "                }",
        "            });",
        "        });",
        "    </script>",
        "</head>",
        "<body class='bg-gray-50 text-gray-900 min-h-screen'>",
        "    <div class='container mx-auto px-4 py-8 max-w-6xl'>",
        "        <!-- 报告标题 -->",
        "        <header class='mb-8'>",
        "            <div class='flex items-center justify-between'>",
        "                <h1 class='text-3xl font-bold text-indigo-700'>",
        "                    <i class='fas fa-code-compare mr-2'></i>GraphQL API 变更监测报告",
        "                </h1>",
        "                <span class='text-gray-500'><i class='far fa-clock mr-1'></i>" + current_time + "</span>",
        "            </div>",
        "            <div class='mt-4 p-4 bg-white rounded-lg shadow-sm border-l-4 border-indigo-500'>",
        "                <div class='grid grid-cols-1 md:grid-cols-2 gap-4'>",
        "                    <div>",
        "                        <p class='text-sm text-gray-500'>旧文件:</p>",
        "                        <p class='font-mono text-sm truncate'>" + old_file + "</p>",
        "                    </div>",
        "                    <div>",
        "                        <p class='text-sm text-gray-500'>新文件:</p>",
        "                        <p class='font-mono text-sm truncate'>" + new_file + "</p>",
        "                    </div>",
        "                </div>",
        "            </div>",
        "        </header>",
        "",
        "        <!-- 报告内容 -->",
        "        <main class='space-y-6'>"
    ]
    
    # 处理新增项目
    if diff_result["added_projects"]:
        html.append("""
            <section class='bg-white rounded-lg shadow-sm overflow-hidden'>
                <h2 class='text-xl font-semibold p-4 bg-gray-100 flex items-center'>
                    <i class='fas fa-square-plus text-green-600 mr-2'></i>新增项目
                </h2>
                <div class='p-4 space-y-2'>
        """)
        
        for project in diff_result["added_projects"]:
            html.append(f"""
                    <div class='p-2 bg-gray-50 rounded-md flex items-center'>
                        <i class='fas fa-folder-plus text-green-500 mr-2'></i>
                        <span>{project}</span>
                    </div>
            """)
        
        html.append("</div></section>")
    
    # 处理移除项目
    if diff_result["removed_projects"]:
        html.append("""
            <section class='bg-white rounded-lg shadow-sm overflow-hidden'>
                <h2 class='text-xl font-semibold p-4 bg-gray-100 flex items-center'>
                    <i class='fas fa-square-minus text-red-600 mr-2'></i>移除项目
                </h2>
                <div class='p-4 space-y-2'>
        """)
        
        for project in diff_result["removed_projects"]:
            html.append(f"""
                    <div class='p-2 bg-gray-50 rounded-md flex items-center'>
                        <i class='fas fa-folder-minus text-red-500 mr-2'></i>
                        <span>{project}</span>
                    </div>
            """)
        
        html.append("</div></section>")
    
    # 处理修改项目
    if diff_result["modified_projects"]:
        html.append("""
            <section class='bg-white rounded-lg shadow-sm overflow-hidden'>
                <h2 class='text-xl font-semibold p-4 bg-gray-100 flex items-center'>
                    <i class='fas fa-pen-to-square text-blue-600 mr-2'></i>修改项目
                </h2>
                <div class='p-4'>
        """)
        
        for project, changes in diff_result["modified_projects"].items():
            html.append(f"""
                <section class='bg-white rounded-lg shadow-sm overflow-hidden mt-4'>
                    <h3 class='text-lg font-medium p-3 bg-blue-50 border-l-4 border-blue-500 flex items-center justify-between'>
                        <div><i class='fas fa-project-diagram mr-2'></i>{project}</div>
                        <span class='text-sm text-gray-500'>项目</span>
                    </h3>
                    <div class='p-4'>
            """)
            
            # 处理新增查询
            if changes["added_queries"]:
                html.append("""
                        <div class='mb-4'>
                            <h4 class='text-md font-medium mb-2 flex items-center text-green-600'>
                                <i class='fas fa-plus-circle mr-2'></i>新增查询
                            </h4>
                            <div class='space-y-3'>
                """)
                
                for query in changes["added_queries"]:
                    query_content = new_content[project][query]
                    escaped_content = query_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    
                    html.append(f"""
                                <div class='border border-gray-200 rounded-md overflow-hidden'>
                                    <div class='collapsible-header cursor-pointer bg-gray-50 p-2 flex justify-between items-center hover:bg-gray-100'>
                                        <span class='font-medium'>{query}</span>
                                        <i class='fas fa-chevron-down toggle-icon text-gray-500'></i>
                                    </div>
                                    <div class='collapsible-content'>
                                        <div class='p-3'>
                                            <div class='code-container'>
                                                <button class='copy-btn'><i class='far fa-copy'></i>复制</button>
                                                <pre class='m-0 p-0 bg-gray-50'><code class='language-graphql p-3 block overflow-x-auto'>{escaped_content}</code></pre>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                    """)
                
                html.append("</div></div>")
            
            # 处理移除查询
            if changes["removed_queries"]:
                html.append("""
                        <div class='mb-4'>
                            <h4 class='text-md font-medium mb-2 flex items-center text-red-600'>
                                <i class='fas fa-minus-circle mr-2'></i>移除查询
                            </h4>
                            <div class='space-y-3'>
                """)
                
                for query in changes["removed_queries"]:
                    query_content = old_content[project][query]
                    escaped_content = query_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    
                    html.append(f"""
                                <div class='border border-gray-200 rounded-md overflow-hidden'>
                                    <div class='collapsible-header cursor-pointer bg-gray-50 p-2 flex justify-between items-center hover:bg-gray-100'>
                                        <span class='font-medium'>{query}</span>
                                        <i class='fas fa-chevron-down toggle-icon text-gray-500'></i>
                                    </div>
                                    <div class='collapsible-content'>
                                        <div class='p-3'>
                                            <div class='code-container'>
                                                <button class='copy-btn'><i class='far fa-copy'></i>复制</button>
                                                <pre class='m-0 p-0 bg-gray-50'><code class='language-graphql p-3 block overflow-x-auto'>{escaped_content}</code></pre>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                    """)
                
                html.append("</div></div>")
            
            # 处理修改查询
            if changes["modified_queries"]:
                html.append("""
                        <div class='mb-4'>
                            <h4 class='text-md font-medium mb-2 flex items-center text-amber-600'>
                                <i class='fas fa-pencil mr-2'></i>修改查询
                            </h4>
                            <div class='space-y-3'>
                """)
                
                for query in changes["modified_queries"]:
                    old_query_content = old_content[project][query]
                    new_query_content = new_content[project][query]
                    
                    # 转义内容
                    old_escaped = old_query_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    new_escaped = new_query_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    
                    # 生成差异内容
                    old_lines = old_query_content.splitlines()
                    new_lines = new_query_content.splitlines()
                    differ = difflib.Differ()
                    diff = list(differ.compare(old_lines, new_lines))
                    
                    # 差异内容HTML
                    diff_html = []
                    for line in diff:
                        if line.startswith('+ '):
                            diff_html.append(f"<div class='diff-added'>{line[2:].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</div>")
                        elif line.startswith('- '):
                            diff_html.append(f"<div class='diff-removed'>{line[2:].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</div>")
                        elif line.startswith('? '):
                            diff_html.append(f"<div class='diff-unchanged'>{line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</div>")
                        else:
                            diff_html.append(f"<div>{line[2:].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</div>")
                    
                    html.append(f"""
                                <div class='border border-gray-200 rounded-md overflow-hidden'>
                                    <div class='collapsible-header cursor-pointer bg-gray-50 p-2 flex justify-between items-center hover:bg-gray-100'>
                                        <span class='font-medium'>{query}</span>
                                        <i class='fas fa-chevron-down toggle-icon text-gray-500'></i>
                                    </div>
                                    <div class='collapsible-content'>
                                        <div class='p-3'>
                                            <div class='mt-2 mb-1 flex items-center'>
                                                <i class='fas fa-history text-blue-600 mr-2'></i>
                                                <span class='font-medium'>1. 旧语句</span>
                                            </div>
                                            <div class='code-container'>
                                                <button class='copy-btn'><i class='far fa-copy'></i>复制</button>
                                                <pre class='m-0 p-0 bg-gray-50'><code class='language-graphql p-3 block overflow-x-auto'>{old_escaped}</code></pre>
                                            </div>
                                            
                                            <div class='mt-2 mb-1 flex items-center'>
                                                <i class='fas fa-code text-blue-600 mr-2'></i>
                                                <span class='font-medium'>2. 新语句</span>
                                            </div>
                                            <div class='code-container'>
                                                <button class='copy-btn'><i class='far fa-copy'></i>复制</button>
                                                <pre class='m-0 p-0 bg-gray-50'><code class='language-graphql p-3 block overflow-x-auto'>{new_escaped}</code></pre>
                                            </div>
                    """)
                    
                    if len(diff) > 1:
                        html.append(f"""
                                            <div class='mt-2 mb-1 flex items-center'>
                                                <i class='fas fa-code-compare text-purple-600 mr-2'></i>
                                                <span class='font-medium'>3. 差异详情</span>
                                            </div>
                                            <div class='code-container'>
                                                <button class='copy-btn'><i class='far fa-copy'></i>复制</button>
                                                <div class='code-block p-3 bg-gray-50 overflow-x-auto whitespace-pre' style="max-width: 100%;">{''.join(diff_html)}</div>
                                            </div>
                        """)
                    
                    html.append("""
                                        </div>
                                    </div>
                                </div>
                    """)
                
                html.append("</div></div>")
            
            html.append("</div></section>")
        
        html.append("</div></section>")
    
    # 添加页脚和关闭标签
    html.extend([
        "        </main>",
        "",
        "        <!-- 页脚 -->",
        "        <footer class='mt-8 pt-4 border-t border-gray-200 text-center text-gray-500 text-sm'>",
        "            <p>由 GraphQL Schema to HttpRunner 工具生成</p>",
        f"            <p class='mt-1'>© {datetime.datetime.now().year} GraphQL to HttpRunner</p>",
        "        </footer>",
        "    </div>",
        "</body>",
        "</html>"
    ])
    
    return "\n".join(html)