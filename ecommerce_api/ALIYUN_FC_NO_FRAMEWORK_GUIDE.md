# 阿里云函数计算无框架部署方案指南

## 为什么推荐这个方案？

经过多次测试，我们发现使用Python标准库实现的HTTP服务器在阿里云函数计算环境中具有**最佳兼容性**。这个方案避免了任何外部框架（如FastAPI）可能带来的兼容性问题。

## 方案特点

- **最小依赖**：仅使用Python标准库，不需要安装任何第三方包
- **最高兼容性**：使用基础Python语法，确保在各种Python版本环境中都能运行
- **最简单配置**：部署步骤最少，配置要求最低
- **最稳定运行**：避免框架可能导致的内存泄漏或性能问题

## 部署包信息

- **最新部署包文件**：`C:\Users\jing9\aliyun_fc_deployment_final_no_framework_v5.zip`
- **包含文件**：
  - `simple_server_no_framework.py` - 仅使用Python标准库的HTTP服务器（已完全移除所有不兼容语法，包括f-string，并修复了响应格式问题，添加了Python 2/3兼容性支持）
  - `requirements_minimal.txt` - 最小化的依赖说明文件（仅使用Python标准库）

## 部署步骤

### 1. 上传部署包

- 登录阿里云函数计算控制台
- 进入您的函数配置页面
- 选择"上传ZIP包"选项
- 上传文件：`aliyun_fc_deployment_final_no_framework.zip`

### 2. 设置启动命令

**这是最关键的步骤！**

- 在"函数配置"页面找到"启动命令"设置
- **必须设置为**：`python simple_server_no_framework.py`
- 请确保没有任何拼写错误

### 3. 配置环境变量

- 添加以下环境变量（如果没有自动设置）：
  - `APP_HOST`: `0.0.0.0` （监听所有网络接口）
  - `APP_PORT`: `9000` （与控制台配置的监听端口保持一致）

### 4. 保存配置并部署

- 点击"保存"按钮
- 等待函数重新部署完成

## API端点说明

这个无框架版本实现了与原始版本相同的API端点：

### 1. 健康检查端点

```
GET /health
```
- **功能**：检查API是否正常运行
- **返回示例**：
  ```json
  {
    "status": "ok",
    "version": "1.0",
    "timestamp": "2023-07-01 12:34:56"
  }
  ```

### 2. 根端点

```
GET /
```
- **功能**：简单的欢迎消息
- **返回示例**：
  ```json
  {"message": "API is running"}
  ```

### 3. 产品描述生成端点

```
POST /generate-description
```
- **功能**：生成产品描述
- **请求体示例**：
  ```json
  {
    "product_name": "智能手表",
    "product_features": ["心率监测", "睡眠追踪", "防水50米"],
    "target_audience": "健身爱好者"
  }
  ```
- **返回示例**：
  ```json
  {
    "request_id": "mock_req_123",
    "descriptions": ["This is a sample description for 智能手表. It has features: 心率监测, 睡眠追踪, 防水50米. Targeting: 健身爱好者."],
    "generation_time": 0.5
  }
  ```

## 验证方法

部署完成后，使用以下命令验证API是否正常工作：

```powershell
cd C:\Users\jing9
python test_aliyun_api_auto.py https://productdesc-api-fgysjgufnw.cn-hangzhou.fcapp.run
```

## 常见问题排查

### 问题1：API返回412错误

**解决方法**：
- 确认启动命令正确设置为 `python simple_server_no_framework.py`
- 检查环境变量 `APP_HOST` 和 `APP_PORT` 是否正确配置
- 查看阿里云函数计算控制台的日志获取详细错误信息

### 问题2：API无法访问

**解决方法**：
- 确认函数计算的网络配置允许公网访问
- 检查安全组规则是否允许访问9000端口
- 确认函数是否已经成功部署并处于运行状态

### 问题3：响应超时

**解决方法**：
- 在函数计算控制台增加执行超时时间（推荐设置为60秒）
- 检查网络连接状况

## 技术说明

这个无框架版本使用了Python的标准库 `http.server` 来实现HTTP服务功能，完全不依赖任何第三方框架。代码结构简洁明了，易于维护，同时保持了与原始版本相同的API功能。

如果您在使用过程中遇到任何问题，请参考阿里云函数计算控制台的日志信息，或联系技术支持。