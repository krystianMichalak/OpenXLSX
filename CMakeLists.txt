cmake_minimum_required(VERSION 3.15)
PROJECT(OpenXLSX LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)
SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR}/bin)
SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_SOURCE_DIR}/bin)

SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib)
SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY})
SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY})

add_library(NoWide INTERFACE IMPORTED)
target_include_directories(NoWide SYSTEM INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/external/nowide/>)

add_library(Zippy INTERFACE IMPORTED)
target_include_directories(Zippy SYSTEM INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/external/zippy/>)

add_library(PugiXML INTERFACE IMPORTED)
target_include_directories(PugiXML SYSTEM INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/external/pugixml/>)

set(OPENXLSX_SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLCell.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLCellIterator.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLCellRange.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLCellReference.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLCellValue.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLColor.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLColumn.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLContentTypes.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLDateTime.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLDocument.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLFormula.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLProperties.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLRelationships.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLRow.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLRowData.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLSharedStrings.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLSheet.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLWorkbook.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLXmlData.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLXmlFile.cpp
        ${CMAKE_CURRENT_LIST_DIR}/sources/XLZipArchive.cpp
        )        
        add_library(OpenXLSX STATIC "")
        add_library(OpenXLSX::OpenXLSX ALIAS OpenXLSX)
        target_sources(OpenXLSX PRIVATE ${OPENXLSX_SOURCES})
        target_include_directories(OpenXLSX
                PUBLIC
                $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}>
                $<BUILD_INTERFACE:${CMAKE_CURRENT_LIST_DIR}/OpenXLSX>
                $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>)     # For export header
        target_link_libraries(OpenXLSX
                PRIVATE
                $<BUILD_INTERFACE:Zippy>
                $<BUILD_INTERFACE:PugiXML>
                $<BUILD_INTERFACE:NoWide>)
    
        target_compile_definitions(OpenXLSX PUBLIC OPENXLSX_STATIC_DEFINE)

        set_property(TARGET OpenXLSX PROPERTY
                MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

        include(GenerateExportHeader)
        generate_export_header(OpenXLSX
        BASE_NAME openxlsx
        EXPORT_FILE_NAME OpenXLSX-Exports.hpp
        EXPORT_MACRO_NAME OPENXLSX_EXPORT
        NO_EXPORT_MACRO_NAME OPENXLSX_HIDDEN)

        add_custom_command(
        TARGET OpenXLSX POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                ${CMAKE_CURRENT_BINARY_DIR}/OpenXLSX-Exports.hpp
                ${CMAKE_SOURCE_DIR}/OpenXLSX/OpenXLSX-Exports.hpp)
