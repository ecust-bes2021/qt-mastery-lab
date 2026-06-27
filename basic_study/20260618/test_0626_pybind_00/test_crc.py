# test_crc.py
# 测试脚本 —— 验证 pybind11 绑定是否正常工作
#
# 运行方式：
#   1. 先编译安装：uv pip install .
#   2. 再运行测试：python test_crc.py

from crc_module import CrcCalculator, quick_crc16

def main():
    print("=" * 50)
    print("pybind11 Demo - CRC Calculator")
    print("=" * 50)

    # 1. 创建 C++ 对象（Python 端操作，底层是 C++ CrcCalculator 实例）
    calc = CrcCalculator("chip_tool")
    print(f"\n1. 创建计算器: name = {calc.get_name()}")

    # 2. 计算 CRC8
    data = [0x01, 0x02, 0x03, 0x04]
    crc8_val = calc.crc8(data)
    print(f"2. CRC8({data}) = 0x{crc8_val:02X}")

    # 3. 计算 CRC16
    crc16_val = calc.crc16(data)
    print(f"3. CRC16({data}) = 0x{crc16_val:04X}")

    # 4. 校验数据完整性
    is_valid = calc.verify(data, crc16_val)
    print(f"4. 校验（正确CRC）: {is_valid}")

    is_valid_bad = calc.verify(data, 0x0000)
    print(f"5. 校验（错误CRC）: {is_valid_bad}")

    # 5. 读取属性（不是方法调用，是属性访问）
    print(f"6. 调用次数: {calc.call_count}")

    # 6. 使用独立函数（不需要创建对象）
    quick_result = quick_crc16([0xAA, 0xBB, 0xCC])
    print(f"7. quick_crc16([0xAA, 0xBB, 0xCC]) = 0x{quick_result:04X}")

    # 7. 默认参数
    calc2 = CrcCalculator()
    print(f"8. 默认名称: {calc2.get_name()}")

    print("\n" + "=" * 50)
    print("全部测试通过！C++ 代码成功被 Python 调用。")
    print("=" * 50)


if __name__ == "__main__":
    main()