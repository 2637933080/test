# Python + Pytest 单元测试项目

这是一个简单的Python项目，演示了如何使用Pytest进行单元测试，使用Coverage.py生成测试覆盖率报告，以及使用Pylint进行代码质量检查。

## 项目结构

- [palindrome.py](file:///C:/Users/lvpei/Desktop/test/5/work3/palindrome.py) - 包含回文检测函数的主代码文件
- [test_palindrome.py](file:///C:/Users/lvpei/Desktop/test/5/work3/test_palindrome.py) - 针对回文检测函数的测试用例
- [requirements.txt](file:///C:/Users/lvpei/Desktop/test/5/work3/requirements.txt) - 项目依赖列表
- [pytest.ini](file:///C:/Users/lvpei/Desktop/test/5/work3/pytest.ini) - pytest配置文件
- [.coveragerc](file:///C:/Users/lvpei/Desktop/test/5/work3/.coveragerc) - coverage.py配置文件
- [.pylintrc](file:///C:/Users/lvpei/Desktop/test/5/work3/.pylintrc) - pylint配置文件
- [run_tests.bat](file:///C:/Users/lvpei/Desktop/test/5/work3/run_tests.bat) - Windows批处理脚本，一键运行所有任务
- [run_tests.sh](file:///C:/Users/lvpei/Desktop/test/5/work3/run_tests.sh) - Unix/Linux/Mac脚本，一键运行所有任务

## 功能说明

### 回文检测函数

[palindrome.py](file:///C:/Users/lvpei/Desktop/test/5/work3/palindrome.py)中的`is_palindrome()`函数可以检测一个字符串是否为回文。它会忽略空格、大小写和标点符号。

示例：
- "level" → True
- "A man a plan a canal Panama" → True
- "hello" → False

## 安装和运行

### 手动安装和运行

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 运行测试：
   ```
   pytest
   ```

3. 生成覆盖率报告：
   ```
   coverage run -m pytest
   coverage report
   coverage html
   ```

4. 运行代码质量检查：
   ```
   pylint palindrome.py
   ```

### 自动运行（推荐）

#### 在Windows上：
双击运行 [run_tests.bat](file:///C:/Users/lvpei/Desktop/test/5/work3/run_tests.bat) 文件

#### 在Unix/Linux/Mac上：
在终端中运行以下命令：
```
chmod +x run_tests.sh
./run_tests.sh
```

## 输出结果

运行完成后，你将得到：
1. 测试结果输出
2. 覆盖率报告（在控制台显示）
3. HTML格式的详细覆盖率报告（在`htmlcov`目录中）
4. Pylint代码质量评分

请根据要求提交：
- 测试代码（[palindrome.py](file:///C:/Users/lvpei/Desktop/test/5/work3/palindrome.py)和[test_palindrome.py](file:///C:/Users/lvpei/Desktop/test/5/work3/test_palindrome.py)）
- 覆盖率报告截图
- Pylint评分截图