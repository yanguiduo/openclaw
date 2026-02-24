#!/usr/bin/env python3
"""
百度搜索工具 - 基于 baidusearch 库
更稳定、更简单的百度搜索方案

安装依赖:
    pip install baidusearch requests

使用方法:
    python baidu_search.py "关键词" --num 10
"""

import argparse
import json
import sys

# 尝试导入 baidusearch
try:
    from baidusearch.baidusearch import search as baidu_search
except ImportError:
    print("错误: 未安装 baidusearch 库")
    print("请运行: pip install baidusearch")
    sys.exit(1)


def search(query, num_results=10, debug=0):
    """
    执行百度搜索
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量
        debug: 是否开启调试模式 (0/1)
        
    Returns:
        list: 搜索结果列表
    """
    try:
        # 调用 baidusearch 库
        results = baidu_search(query, num_results=num_results, debug=debug)
        
        # 格式化结果
        formatted_results = []
        for result in results:
            # 清理摘要中的空白字符
            abstract = result.get("abstract", "")
            if abstract:
                abstract = abstract.strip()
            
            # 处理相对 URL
            url = result.get("url", "")
            if url.startswith("/"):
                url = f"https://www.baidu.com{url}"
            
            formatted_result = {
                "title": result.get("title", ""),
                "url": url,
                "abstract": abstract,
                "rank": result.get("rank", 0),
                "source": "百度"
            }
            formatted_results.append(formatted_result)
        
        return formatted_results
        
    except Exception as e:
        print(f"搜索出错: {e}")
        return []


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='百度搜索工具 (基于 baidusearch)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python baidu_search.py "横店 儿童演员 招募"
    python baidu_search.py "关键词" --num 20 --output json
    python baidu_search.py "关键词" --debug 1
        """
    )
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--num', '-n', type=int, default=10, 
                        help='结果数量 (默认10)')
    parser.add_argument('--output', '-o', default='text', 
                        choices=['text', 'json'], 
                        help='输出格式')
    parser.add_argument('--debug', '-d', type=int, default=0,
                        help='调试模式 (0或1)')
    
    args = parser.parse_args()
    
    print(f"🔍 搜索: {args.query}\n")
    
    results = search(args.query, num_results=args.num, debug=args.debug)
    
    if not results:
        print("未找到结果")
        return
    
    if args.output == 'json':
        # 输出标准 JSON
        output = {
            "web": {
                "results": results
            },
            "query": args.query,
            "total": len(results)
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        for i, r in enumerate(results, 1):
            print(f"[{i}] {r['title']}")
            print(f"    链接: {r['url']}")
            if r['abstract']:
                # 限制摘要长度
                abstract = r['abstract'][:200]
                if len(r['abstract']) > 200:
                    abstract += "..."
                print(f"    摘要: {abstract}")
            print()


if __name__ == '__main__':
    main()
