# TXQuant

TXQuant 是一个用于量化交易的Python库，提供数据处理、策略回测和实时交易等功能。

## 功能特性

- 📊 数据处理
  - 支持多种数据格式的导入导出
  - 提供数据清洗和预处理工具
  - 内置常用技术指标计算
- 📈 策略回测
  - 支持多周期回测
  - 提供详细的回测报告
  - 支持自定义交易成本
- 🔄 实时交易
  - 支持多交易所接入
  - 提供风险控制模块
  - 实时监控和预警

## 安装

```bash
pip install txquant
```

## 快速开始

```python
import txquant as tx

# 加载数据
data = tx.load_data("your_data.csv")

# 计算收益率
returns = tx.calculate_returns(data['close'])

# 更多示例代码将在这里展示
```

## 文档

详细的文档请访问：[文档链接](https://github.com/yourusername/txquant/docs)

## 开发环境设置

1. 克隆仓库
```bash
git clone https://github.com/yourusername/txquant.git
cd txquant
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行测试
```bash
pytest tests/
```

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 版本日志

### v0.1.0 (2024-03-xx)
- 🎉 首次发布
- ✨ 基础功能实现
  - 添加数据处理模块
  - 实现基础收益率计算
  - 添加单元测试

### 即将发布
- 🔜 策略回测模块
- 🔜 实时交易接口
- 🔜 更多技术指标

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者：[张礼涛]
- 邮箱：[445646258@qq.com]
- 项目链接：[https://github.com/95ge/txquant](https://github.com/95ge/txquant)

## 致谢

感谢所有为本项目做出贡献的开发者！ 