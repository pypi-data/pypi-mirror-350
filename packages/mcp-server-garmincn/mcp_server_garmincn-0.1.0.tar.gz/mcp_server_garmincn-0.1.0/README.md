# How to use

1. clone repository
```bash
git clone https://github.com/guaidaoyiyoudao/garmincn-mcp.git
```

2. build distribution package
```bash
cd garmincn-mcp
uv build
```

3. install package
```bash
uv tool install dist/garmincn-mcp-0.0.1.tar.gz
```

4. use mcp server in client

这里以cherrt studio举例：
![alt text](img/image.png)

需要填写两个环境变量：
- EMAIL: 用于登录garmin connect的邮箱
- PASSWORD: 用于登录garmin connect的密码

5. enjoy it!


# License

本代码几乎全部由AI生成，可以随意使用！