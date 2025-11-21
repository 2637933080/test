def divide(a, b):
	return a / b  # 缺陷1: 未检查除数为0


def find_max(lst):
	max_val = 0  # 缺陷2: 如果列表全是负数，返回结果错误
	for x in lst:
		if x > max_val:
			max_val = x
	return max_val


def get_item(lst, idx):
	return lst[idx]  # 缺陷3: 未检查索引越界


def run_tests():
	test_cases = [
		{
			"id": "TC1",
			"description": "divide 在正常正数输入下返回商",
			"callable": divide,
			"args": (10, 2),
			"expected": 5,
		},
		{
			"id": "TC2",
			"description": "divide 面对除数为0时应给出友好处理",
			"callable": divide,
			"args": (7, 0),
			"expected": "Error: divide by zero",
		},
		{
			"id": "TC3",
			"description": "find_max 在正数列表中应返回最大值",
			"callable": find_max,
			"args": ([1, 5, 3],),
			"expected": 5,
		},
		{
			"id": "TC4",
			"description": "find_max 在全负数列表中应返回最大(最接近0)的负数",
			"callable": find_max,
			"args": ([-5, -2, -9],),
			"expected": -2,
		},
		{
			"id": "TC5",
			"description": "get_item 用合法索引获取元素",
			"callable": get_item,
			"args": ([10, 20], 1),
			"expected": 20,
		},
		{
			"id": "TC6",
			"description": "get_item 索引越界时应做防护",
			"callable": get_item,
			"args": ([1, 2, 3], 5),
			"expected": "Error: index out of range",
		},
	]

	results = []
	for case in test_cases:
		try:
			actual = case["callable"](*case["args"])
			passed = actual == case["expected"]
			results.append({"actual": actual, "passed": passed, **case})
		except Exception as exc:  # 捕获异常以便记录缺陷行为
			results.append({"actual": f"Exception: {exc}", "passed": False, **case})

	return results


if __name__ == "__main__":
	for record in run_tests():
		print(
			f"{record['id']}: {record['description']}\n"
			f"  输入: {record['args']}\n"
			f"  期望: {record['expected']}\n"
			f"  实际: {record['actual']}\n"
			f"  结果: {'通过' if record['passed'] else '失败'}\n"
		)

