from .API import mcp,get_credentials_from_env


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="企业信息查询MCP服务")
    parser.add_argument("--transport", choices=["sse", "stdio"], default="stdio",
                        help="传输方式: sse或stdio (默认: stdio)")
    parser.add_argument("--host", default="0.0.0.0", help="主机地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8009, help="端口号 (默认: 8009)")

    # 向下兼容简单的命令行参数
    if len(sys.argv) == 2 and sys.argv[1] in ["sse", "stdio"]:
        args = parser.parse_args([f"--transport={sys.argv[1]}"])
    else:
        args = parser.parse_args()

    # 在启动前检查环境变量
    cid, ckey = get_credentials_from_env()
    print(f"使用凭据: client_id={cid[:3]}****, client_key={ckey[:3]}****")

    # 启动服务
    if args.transport == "sse":
        print(f"正在启动SSE服务 - 监听地址: {args.host}:{args.port}")
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        print("正在启动stdio服务")
        mcp.run(transport="stdio")