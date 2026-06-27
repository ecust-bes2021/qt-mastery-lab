// bindings.cpp
// pybind11 绑定代码 —— 这个文件是 C++ 世界和 Python 世界的桥梁
//
// 它的作用：
//   告诉 pybind11 "把哪些 C++ 类/函数暴露给 Python，以什么名字暴露"
//
// 编译后生成 crc_module.pyd（Windows）或 crc_module.so（Linux）
// Python 端直接 import crc_module 即可使用

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // 让 std::vector <-> Python list 自动转换

#include "crc_calculator.h"

namespace py = pybind11;

// PYBIND11_MODULE(模块名, m)
// 模块名: Python 端 import 时用的名字（import crc_module）
// m: 模块对象，用来注册类和函数
PYBIND11_MODULE(crc_module, m)
{
    // 模块的文档字符串（Python 中 help(crc_module) 会显示）
    m.doc() = "CRC Calculator - pybind11 demo";

    // ==========================================
    // 注册 CrcCalculator 类
    // ==========================================
    // py::class_<C++类>(模块, "Python中的类名")
    //
    // 这一行做了什么：
    //   在 Python 端创建一个叫 "CrcCalculator" 的类
    //   它内部持有一个真正的 C++ CrcCalculator 对象
    //   Python 调用方法时 → pybind11 转发到 C++ 方法 → 返回值自动转回 Python 类型
    py::class_<CrcCalculator>(m, "CrcCalculator")

        // .def(py::init<参数类型>())
        // 绑定构造函数
        // Python 端: calc = CrcCalculator("my_calc")
        // pybind11 会自动把 Python str 转成 std::string
        .def(py::init<const std::string &>(), py::arg("name") = "default")

        // .def("Python方法名", &C++方法指针)
        // 绑定普通成员函数
        .def("get_name", &CrcCalculator::getName,
             "Get calculator name")

        // crc8: Python 传入 list[int] → pybind11 自动转 vector<uint8_t>
        //       C++ 返回 uint8_t → pybind11 自动转 Python int
        .def("crc8", &CrcCalculator::crc8,
             py::arg("data"),
             "Calculate CRC8 checksum, input is a list of bytes")

        // crc16: 同上
        .def("crc16", &CrcCalculator::crc16,
             py::arg("data"),
             "Calculate CRC16-CCITT checksum, input is a list of bytes")

        // verify: 返回 bool → Python bool
        .def("verify", &CrcCalculator::verify,
             py::arg("data"), py::arg("expected_crc16"),
             "Verify data integrity, returns True/False")

        // 只读属性绑定
        // Python 端: calc.call_count（不是方法调用，是属性访问）
        // .def_property_readonly("属性名", &getter方法)
        .def_property_readonly("call_count", &CrcCalculator::getCallCount,
                               "Total number of CRC calculations")
        ;

    // ==========================================
    // 注册一个独立函数（不属于任何类）
    // ==========================================
    // 演示：不一定非要绑定类，普通函数也能暴露
    // Python 端: crc_module.quick_crc16([0x01, 0x02, 0x03])
    m.def("quick_crc16",
          [](const std::vector<uint8_t> &data) -> uint16_t {
              CrcCalculator calc("temp");
              return calc.crc16(data);
          },
          py::arg("data"),
          "Quick CRC16 calculation (no need to create object)");
}