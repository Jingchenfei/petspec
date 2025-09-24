# PetSpec 部署指南

## 1. 阿里云函数计算部署
1. 登录[阿里云控制台](https://fc.console.aliyun.com)
2. 创建新服务 `petspec-service`
3. 上传 `fc_handler.py` 作为函数代码
4. 设置触发器为HTTP触发器
5. 记下生成的访问端点（用于前端配置）

## 2. OSS静态网站配置
1. 创建Bucket `petspec-static`
2. 开启"静态网站托管"功能
3. 上传前端文件：
   ```bash
   ossutil cp -r D:/dev_workspace/ oss://petspec-static/
   ```
4. 获取网站访问地址

## 3. 文心千帆API配置
1. 登录[百度智能云](https://cloud.baidu.com)
2. 申请文心千帆API权限
3. 在函数计算环境变量中添加：
   - `WENXIN_ACCESS_KEY`
   - `WENXIN_SECRET_KEY`

## 测试验证
1. 访问OSS生成的网站URL
2. 输入测试文本：
   ```text
   盐酸多西环素片：每日两次，每次50mg
   ```
3. 确认返回优化后的说明书格式