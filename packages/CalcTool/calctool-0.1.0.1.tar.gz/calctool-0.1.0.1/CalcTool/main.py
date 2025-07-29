import math
from typing import *
import heapq

def sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> None:
	"""使用内省排序对列表进行原地排序"""
	if len(arr) <= 1:
		return  # 已经有序或为空
	
	# 比较函数 - 使用 lambda 避免类型变量问题
	compare = lambda a, b: key(a) > key(b) if reverse else key(a) < key(b)
	
	# 计算最大递归深度
	max_depth = 2 * math.log2(len(arr)) if len(arr) > 0 else 0
	
	# 内省排序主循环
	def introsort(start: int, end: int, depth: float) -> None:
		while start < end:
			# 小规模数据使用插入排序
			if end - start <= 16:
				for i in range(start + 1, end + 1):
					current = arr[i]
					j = i - 1
					while j >= start and compare(current, arr[j]):
						arr[j + 1] = arr[j]
						j -= 1
					arr[j + 1] = current
				return
			
			# 递归深度过大时使用堆排序
			if depth <= 0:
				heap_size = end - start + 1
				
				# 构建堆
				for i in range(heap_size // 2 - 1, -1, -1):
					heapify(start, heap_size, i)
				
				# 一个个交换元素
				for i in range(heap_size - 1, 0, -1):
					arr[start], arr[start + i] = arr[start + i], arr[start]
					heapify(start, i, 0)
				return
			
			# 否则使用快速排序
			mid = (start + end) // 2
			a, b, c = start, mid, end
			
			# 三数取中法
			if compare(arr[b], arr[a]):
				arr[a], arr[b] = arr[b], arr[a]
			if compare(arr[c], arr[b]):
				arr[b], arr[c] = arr[c], arr[b]
			if compare(arr[b], arr[a]):
				arr[a], arr[b] = arr[b], arr[a]
			
			# 将基准值放到开头
			arr[start], arr[mid] = arr[mid], arr[start]
			pivot = arr[start]
			
			# 分区过程
			left = start + 1
			right = end
			
			while True:
				while left <= right and compare(arr[left], pivot):
					left += 1
				while left <= right and compare(pivot, arr[right]):
					right -= 1
				if left > right:
					break
				arr[left], arr[right] = arr[right], arr[left]
				left += 1
				right -= 1
			
			# 将基准值放到正确位置
			arr[start], arr[right] = arr[right], arr[start]
			pivot_index = right
			
			# 尾递归优化
			if pivot_index - start < end - pivot_index:
				introsort(start, pivot_index - 1, depth - 1)
				start = pivot_index + 1
			else:
				introsort(pivot_index + 1, end, depth - 1)
				end = pivot_index - 1
	
	# 堆排序辅助函数
	def heapify(start: int, heap_size: int, i: int) -> None:
		largest = i
		left = 2 * i + 1
		right = 2 * i + 2
		
		if left < heap_size and compare(arr[start + largest], arr[start + left]):
			largest = left
		
		if right < heap_size and compare(arr[start + largest], arr[start + right]):
			largest = right
		
		if largest != i:
			arr[start + i], arr[start + largest] = arr[start + largest], arr[start + i]
			heapify(start, heap_size, largest)
	
	# 启动内省排序
	introsort(0, len(arr) - 1, max_depth)