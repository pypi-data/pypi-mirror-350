from setuptools import setup, find_packages

setup(
    name="mcp_bill_track",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "mcp"
    ],
    description="个人记账 MCP 服务",
    keywords="bill, track, mcp",
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'mcp_bill_track = mcp_bill_track.server:run_server',
        ],
    },
)
