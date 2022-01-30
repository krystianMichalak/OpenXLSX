from conans import ConanFile, CMake, tools
import os


class OpenXLSXConan(ConanFile):
    name = "OpenXLSX"
    version = "0.3.2"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone https://github.com/krystianMichalak/OpenXLSX.git")
        #self.run("git clone https://github.com/troldal/OpenXLSX.git")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="OpenXLSX")
        cmake.build()

    def package(self):
        self.copy("*.hpp", dst="include", src="OpenXLSX")
        self.copy("*OpenXLSX.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["OpenXLSX"]

