#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wadas_runtime/model.h"
#include "wadas_runtime/server.h"

using namespace wadas_runtime;

PYBIND11_MODULE(_core, m) {
    m.doc() = "Wadas Runtime Core Module";

    m.def("load_and_compile_model", &load_and_compile_model, "Compile Encrypted Model", py::arg("model_xml_path"),
          py::arg("model_bin_path") = py::str(), py::arg("device_name") = py::str("AUTO"),
          py::arg("config") = py::dict());

    py::class_<WadasModelServer>(m, "WADASModelServer")
            .def(py::init<std::string, std::string>(), py::arg("url"), py::arg("version") = "v1")
            .def("login", &WadasModelServer::login, "Login User to Wadas Runtime Server, return the organization code",
                 py::arg("username"), py::arg("password"))
            .def("register_node", &WadasModelServer::register_node,
                 "Register User to Wadas Runtime Server, return the user ID", py::arg("org_code"))
            .def(
                    "available_models",
                    [](WadasModelServer& self, const std::string& user_id) {
                        auto models = self.list_models(user_id);
                        std::vector<py::dict> result;
                        for (const auto& model : models) {
                            result.push_back(model.to_dict());
                        }
                        return result;
                    },
                    "List models from Wadas Runtime Server", py::arg("user_id") = py::str())
            .def("status", &WadasModelServer::status, "Check Wadas Runtime Server Status")
            .def("download_model", &WadasModelServer::download_model, "Download model from Wadas Runtime Server",
                 py::arg("user_id"), py::arg("model_name"), py::arg("model_path"));
}