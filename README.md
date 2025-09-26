# PetSpec - AI宠物说明书优化工具

![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-1.0-blue)

🚀 3秒将专业宠物说明书转化为易懂指南

## 快速部署

```powershell
# 1. 克隆仓库
git clone https://github.com/Jingchenfei/petspec.git

# 2. 安装依赖
Install-Module -Name PSScriptAnalyzer -Force

# 3. 运行部署
./deploy_frontend.ps1
```

## 功能特性
- ✅ 智能术语转换（如"盐酸多西环素"→"抗生素"）
- 📝 自动生成【用法用量】【禁忌症】模块
- 🌍 支持中英文输出

## 自定义配置
修改`deploy_frontend.ps1`中的参数：
```powershell
# API设置
$apiEndpoint = "https://your-api.com"
```

## 参与开发
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature`)
3. 提交修改 (`git commit -m 'Add feature'`)
4. 推送分支 (`git push origin feature`)