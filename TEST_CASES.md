# PetSpec 测试用例

## 功能测试
1. 基础功能测试
   - 输入：标准药品说明书
   - 验证：输出包含【用法用量】等核心模块

2. 错误处理测试
   - 输入：空文本/无效文本
   - 验证：返回友好错误提示

3. 性能测试
   - 并发10个请求
   - 验证：响应时间<3秒

## API测试示例
```python
import requests

def test_api():
    url = "YOUR_FC_ENDPOINT"
    payload = {
        "text": "盐酸多西环素片：每日两次，每次50mg"
    }
    response = requests.post(url, json=payload)
    assert "用法用量" in response.json()["result"]
```

## 前端测试要点
1. 表单验证
2. 加载状态显示
3. 移动端适配