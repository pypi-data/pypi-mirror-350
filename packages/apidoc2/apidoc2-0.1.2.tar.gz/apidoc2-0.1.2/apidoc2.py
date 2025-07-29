#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import argparse
import subprocess
import json

def is_apidoc_annotation(line):
    """判断一行是否包含ApiDoc注解标记"""
    return '@api' in line

def is_java_file(filename):
    """判断文件是否为Java文件"""
    return filename.lower().endswith('.java')

def process_api_version(apidoc_lines, version='master'):
    """处理API文档的版本号
    
    Args:
        apidoc_lines: API文档行列表
        version: 版本号，如果为'master'则使用1.0.0，否则需要符合major.minor.patch格式
    """
    # 验证版本号格式
    def is_valid_version(ver):
        if ver == 'master':
            return True
        parts = ver.split('.')
        if len(parts) != 3:
            return False
        try:
            return all(part.isdigit() for part in parts)
        except:
            return False
    
    # 确定使用的版本号
    target_version = '1.0.0' if version == 'master' else ('2.0.0' if not is_valid_version(version) else version)
    
    # if version == 'master':
    #     target_version = '1.0.0' 
    # else:
    #     target_version = '1.0.1'
    # 初始化结果数组和状态变量
    processed_lines = []
    in_api_block = False
    api_block_lines = []
    has_version = False
    has_group = False
    empty_group = False
    
    i = 0
    while i < len(apidoc_lines):
        line = apidoc_lines[i]
        
        # 检查是否是API注解开始
        if '@api ' in line and not in_api_block:
            in_api_block = True
            
            # 检查@api标签是否不完整（只有@api {类型}但没有接口名称和描述）
            if re.match(r'^\s*\*\s*@api\s+\{[^}]*\}\s*$', line):
                # 检查下一行是否包含接口名称
                if i+1 < len(apidoc_lines) and '*' in apidoc_lines[i+1] and not '@api' in apidoc_lines[i+1]:
                    next_line = apidoc_lines[i+1].strip()
                    # 合并@api行和下一行
                    line = line.rstrip() + ' ' + next_line.lstrip('* ') + '\n'
                    i += 1  # 跳过下一行，因为已经合并了
                    
                    # 如果还有下一行可能包含描述
                    if i+1 < len(apidoc_lines) and '*' in apidoc_lines[i+1] and not '@api' in apidoc_lines[i+1]:
                        next_line = apidoc_lines[i+1].strip()
                        if not next_line.startswith('* @'):  # 不是其他标签
                            line = line.rstrip() + ' ' + next_line.lstrip('* ') + '\n'
                            i += 1  # 再次跳过下一行
            
            api_block_lines = [line]
            has_version = False
            has_group = False
            empty_group = False
        # 检查是否已在API块内
        elif in_api_block:
            # 检查是否有版本信息
            if '@apiVersion' in line:
                # 替换版本号为目标版本号
                line = re.sub(r'@apiVersion\s+[^\s*]+', f'@apiVersion {target_version}', line)
                has_version = True
            
            # 检查是否有apiGroup
            if '@apiGroup' in line:
                has_group = True
                # 检查apiGroup是否为空
                if re.match(r'^\s*\*\s*@apiGroup\s*$', line.rstrip()):
                    # 将空的apiGroup替换为默认值
                    line = re.sub(r'@apiGroup\s*$', '@apiGroup cgi-default', line.rstrip()) + '\n'
                    empty_group = True
            
            # 如果是API注解块结束（通常是注释结束符）
            if '*/' in line:
                api_block_lines.append(line)
                # 如果没有版本号，添加版本号
                if not has_version:
                    # 在API块的开始后插入版本号
                    api_block_lines.insert(1, f' * @apiVersion {target_version}\n')
                
                # 如果没有apiGroup，添加apiGroup
                if not has_group:
                    # 在API块的版本号后插入apiGroup
                    insert_pos = 2 if has_version else 1
                    api_block_lines.insert(insert_pos, ' * @apiGroup cgi-default\n')
                
                # 将处理后的API块添加到结果中
                processed_lines.extend(api_block_lines)
                in_api_block = False
                api_block_lines = []
            else:
                api_block_lines.append(line)
        else:
            processed_lines.append(line)
        
        i += 1
    
    # 处理最后一个API块（如果有）
    if in_api_block:
        if not has_version:
            api_block_lines.insert(1, f' * @apiVersion {target_version}\n')
        
        if not has_group:
            insert_pos = 2 if has_version else 1
            api_block_lines.insert(insert_pos, ' * @apiGroup cgi-default\n')
        
        processed_lines.extend(api_block_lines)
    
    return processed_lines

def extract_apidoc_from_file(file_path):
    """从单个文件中提取ApiDoc注解"""
    apidoc_lines = []
    in_comment_block = False
    apidoc_block = []
    is_apidoc_block = False
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # 检查是否为注释开始
                if '/**' in line and not in_comment_block:
                    in_comment_block = True
                    apidoc_block = [line]
                    is_apidoc_block = False  # 重置标记
                # 在注释块内
                elif in_comment_block:
                    apidoc_block.append(line)
                    # 检查该行是否包含ApiDoc注解标记
                    if is_apidoc_annotation(line):
                        is_apidoc_block = True
                    
                    # 检查是否为注释结束
                    if '*/' in line:
                        # 只有包含ApiDoc注解的注释块才会被添加
                        if is_apidoc_block:
                            apidoc_lines.extend(apidoc_block)
                        in_comment_block = False
                        apidoc_block = []
                # 单行注释中的ApiDoc注解
                elif '//' in line and is_apidoc_annotation(line):
                    apidoc_lines.append(line)
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}", file=sys.stderr)
    
    return apidoc_lines

def extract_all_apidoc(directory, version):
    """递归遍历目录，提取所有Java文件中的ApiDoc注解"""
    all_apidoc_lines = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if is_java_file(file):
                file_path = os.path.join(root, file)
                print(f"正在处理: {file_path}")
                file_apidoc = extract_apidoc_from_file(file_path)
                if file_apidoc:
                    # 添加文件标识注释
                    all_apidoc_lines.append(f"\n// 源文件: {file_path}\n")
                    all_apidoc_lines.extend(file_apidoc)
    
    # 处理所有API注解的版本号
    return process_api_version(all_apidoc_lines, version)

def write_to_js_file(lines, output_file):
    """将提取的ApiDoc注解写入JS文件"""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("/**\n")
        file.write(" *cgi-ehowbuy-server API文档\n")
        file.write(" * 此文件由脚本自动生成，包含从cgi-ehowbuy-server目录中所有Java文件提取的ApiDoc注解\n")
        file.write(" * 所有API版本已统一设置为1.0.0\n")
        file.write(" */\n\n")
        file.writelines(lines)

def run_main(app_name, version):
    """主函数
    
    Args:
        app_name (str): 应用名称
        version (str): 版本号
    """
    input_dir = app_name
    output_file = f"{app_name}-{version}.js"
    
    print(f"开始从 {input_dir} 提取ApiDoc注解...")
    apidoc_lines = extract_all_apidoc(input_dir, version)
    
    if apidoc_lines:
        write_to_js_file(apidoc_lines, output_file)
        print(f"提取完成! 共提取 {len(apidoc_lines)} 行注解到文件 {output_file}")
    else:
        print("未找到任何ApiDoc注解!")
import subprocess
import os

def clone_repository(app_name, repo_url, version):
    """克隆指定仓库并切换到指定版本
    
    Args:
        app_name (str): 应用名称，将作为克隆目录名
        repo_url (str): 仓库URL
        version (str): 要切换到的版本号或分支名
    """
    target_dir = app_name
    
    # 如果目录已存在，先删除
    if os.path.exists(target_dir):
        print(f"目录 {target_dir} 已存在，正在删除...")
        subprocess.run(["rm", "-rf", target_dir], check=True)
    
    print(f"正在克隆仓库 {repo_url}...")
    try:
        # 克隆仓库
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)
        
        # 切换到指定版本
        print(f"正在切换到版本 {version}...")
        subprocess.run(["git", "checkout", version], cwd=target_dir, check=True)
        
        print(f"仓库克隆成功并已切换到 {version} 版本!")
    except subprocess.CalledProcessError as e:
        print(f"操作仓库时出错: {str(e)}", file=sys.stderr)
        sys.exit(1)

def delete_target_dir(app_name):
    """删除目标目录"""
    target_dir = app_name
    if os.path.exists(target_dir):
        print(f"正在删除目录 {target_dir}...")
        subprocess.run(["rm", "-rf", target_dir], check=True)
        print(f"目录 {target_dir} 删除成功!")
    else:
        print(f"目录 {target_dir} 不存在")

def generate_apidoc():
    """执行apidoc命令生成API文档"""
    print("正在生成API文档...")
    try:
        subprocess.run(["apidoc", "-i", ".", "-o", "output"], check=False)
        print("API文档生成成功!")
    except subprocess.CalledProcessError as e:
        print(f"生成API文档时出错: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
def switch_to_version(app_name: str, version: str):
        """
        切换到指定版本
        
        Args:
            app_name (str): 应用目录名
            version (str): 要切换到的版本号或分支名
        """
        if not os.path.exists(app_name):
            print(f"目录 {app_name} 不存在")
            return
            
        print(f"正在切换到版本 {version}...")
        try:
            subprocess.run(["git", "checkout", version], cwd=app_name, check=True)
            print(f"成功切换到 {version} 版本!")
        except subprocess.CalledProcessError as e:
            print(f"切换版本时出错: {str(e)}", file=sys.stderr)
            sys.exit(1)
            
def compare_api_docs():
        """比较不同版本间的API文档差异并输出到diff.js文件和output.log文件"""
        print("开始比较API文档差异...")
        
        # 获取当前目录下所有.js文件
        js_files = [f for f in os.listdir('.') if f.endswith('.js') and f != 'diff.js']
        
        if len(js_files) < 2:
            print("需要至少两个.js文件才能进行比较")
            return
            
        # 用于存储所有API文档的字典
        api_docs = {}
        # 用于存储差异的字典
        diffs = {}
        
        # 获取版本信息
        versions = sorted([f.replace('.js', '') for f in js_files])
        old_version = versions[0]
        new_version = versions[1]
        
        # 用于存储API变更信息
        added_apis = set()
        modified_apis = set()
        deleted_apis = set()
        
        # 解析每个文件中的API文档
        for js_file in js_files:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 使用正则表达式匹配API块
            api_blocks = re.finditer(r'/\*\*\s*\n(?:\s*\*[^\n]*\n)+', content)
            
            for block in api_blocks:
                api_text = block.group(0)
                
                # 提取API名称
                api_name_match = re.search(r'@apiName\s+(\w+)', api_text)
                if not api_name_match:
                    continue
                    
                api_name = api_name_match.group(1)
                
                # 存储API文档
                if api_name not in api_docs:
                    api_docs[api_name] = {}
                api_docs[api_name][js_file] = api_text
        
        # 比较API文档差异
        for api_name, versions in api_docs.items():
            if len(versions) == 1:  # 只在单个版本中存在的API
                if f"{old_version}.js" in versions:
                    deleted_apis.add(api_name)
                else:
                    added_apis.add(api_name)
            else:  # 在两个版本中都存在的API
                old_text = versions[f"{old_version}.js"]
                new_text = versions[f"{new_version}.js"]
                
                # 移除apiVersion行后再比较
                old_text_no_version = re.sub(r'\s*\*\s*@apiVersion\s+[^\n]*\n', '', old_text)
                new_text_no_version = re.sub(r'\s*\*\s*@apiVersion\s+[^\n]*\n', '', new_text)
                
                if old_text_no_version != new_text_no_version:
                    modified_apis.add(api_name)
                    diffs[api_name] = versions
        
        # 将API变更信息写入output.log文件
        with open('output.log', 'w', encoding='utf-8') as log_file:
            log_file.write("=== API变更统计 ===\n")
            
            if added_apis:
                log_file.write(f"\n新增的API ({len(added_apis)}个):\n")
                for api in sorted(added_apis):
                    log_file.write(f"- {api}\n")
            
            if modified_apis:
                log_file.write(f"\n修改的API ({len(modified_apis)}个):\n")
                for api in sorted(modified_apis):
                    log_file.write(f"- {api}\n")
            
            if deleted_apis:
                log_file.write(f"\n删除的API ({len(deleted_apis)}个):\n")
                for api in sorted(deleted_apis):
                    log_file.write(f"- {api}\n")
            
            if not (added_apis or modified_apis or deleted_apis):
                log_file.write("\n未发现API变更\n")
        
        # 打印API变更信息到控制台
        print("\n=== API变更统计 ===")
        if added_apis:
            print(f"\n新增的API ({len(added_apis)}个):")
            for api in sorted(added_apis):
                print(f"- {api}")
        
        if modified_apis:
            print(f"\n修改的API ({len(modified_apis)}个):")
            for api in sorted(modified_apis):
                print(f"- {api}")
        
        if deleted_apis:
            print(f"\n删除的API ({len(deleted_apis)}个):")
            for api in sorted(deleted_apis):
                print(f"- {api}")
        
        if not (added_apis or modified_apis or deleted_apis):
            print("\n未发现API变更")
        
        print("\nAPI变更统计已写入output.log文件")
        
        # 将差异写入diff.js文件
        if diffs:
            with open('diff.js', 'w', encoding='utf-8') as f:
                f.write('// API文档差异比较结果\n\n')
                for api_name, versions in diffs.items():
                    f.write(f'// API: {api_name}\n')
                    for file_name, api_text in versions.items():
                        f.write(f'// 来自文件: {file_name}\n')
                        f.write(api_text + '\n\n')
            print("\n差异已写入diff.js文件")
        
        # 删除原始js文件
        for js_file in js_files:
            try:
                os.remove(js_file)
                print(f"已删除文件: {js_file}")
            except OSError as e:
                print(f"删除文件 {js_file} 时出错: {str(e)}")
    
def generate_apidoc_json(app_name,version):
    """生成apidoc.json配置文件
    
    Args:
        output_dir (str): 输出目录名称
    """ 
    apidoc_config = {
        "name": app_name,
        "version": version,
        "description": app_name + " API文档",
        "title": app_name,
        "url": "/",
        "order": [
            "Error",
            "Define",
            "PostTitleAndError",
            "PostError"
        ]
    }
    with open(os.path.join("./", 'apidoc.json'), 'w', encoding='utf-8') as f:
        json.dump(apidoc_config, f, ensure_ascii=False, indent=2)
    print(f"apidoc.json文件已生成到./目录")
    

def main():

    parser = argparse.ArgumentParser(description='apidoc扩展，支持多仓库和版本差异对比')
    parser.add_argument('-r','--repourl', type=str, required=True, help='git代码仓库，格式：http://gitlab-code.howbuy.pa/ftx/xxx.git')
    parser.add_argument('-v1','--version1', type=str, required=True, help='需要生成的分支版本')
    parser.add_argument('-v2','--version2', type=str, required=False,default=None, help='需要对比的分支版本，可选')
    parser.add_argument('-o','--output', type=str, required=False, default="output", help='apidoc输出文件目录')
    args = parser.parse_args()
    
     # 在main()之前执行克隆
    #repo_url = "http://gitlab-code.howbuy.pa/ftx/ftx-order.git"
    repo_url = args.repourl
    app_name = repo_url.split('/')[-1].replace('.git', '')
    generate_apidoc_json(app_name,args.version1)
    clone_repository(app_name, repo_url, args.version1)
    switch_to_version(app_name, args.version1)
    run_main(app_name,args.version1) 
    if args.version2:
        version2 = args.version2
        switch_to_version(app_name, version2)
        run_main(app_name,version2)
        compare_api_docs()
    delete_target_dir(app_name)
    generate_apidoc()


