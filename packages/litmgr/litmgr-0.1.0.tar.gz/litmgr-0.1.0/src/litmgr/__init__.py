"""LitMgr - 一个简单的两位整数加法库"""

def add_two_digits(a: int, b: int) -> int:
    """
    计算两个两位整数的和
    
    参数:
        a: 第一个两位整数 (10-99)
        b: 第二个两位整数 (10-99)
        
    返回:
        两个数的和
        
    异常:
        ValueError: 如果输入不是两位整数
    """
    # 验证输入是否为两位整数
    if not (10 <= a <= 99):
        raise ValueError(f"第一个参数 {a} 不是两位整数 (10-99)")
    if not (10 <= b <= 99):
        raise ValueError(f"第二个参数 {b} 不是两位整数 (10-99)")
    
    # 计算并返回和
    return a + b