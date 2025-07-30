// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2023 The HepMC collaboration (see AUTHORS for details)
//
///
/// @file ReaderPlugin.cc
/// @brief Implementation of \b class ReaderPlugin
///
#ifdef WIN32
#define WIN32_LEAN_AND_MEAN
#define NOWINBASEINTERLOCK
#define NOMINMAX
#undef UNICODE
#include <intrin.h>
#include <windows.h>
#endif
#if defined(__linux__) || defined(__darwin__) || defined(__APPLE__) || defined(BSD) || defined(__sun)
#include <dlfcn.h>
#endif
#include <sstream>
#include <cstring>
#include "HepMC3/GenEvent.h"
#include "HepMC3/ReaderPlugin.h"

namespace HepMC3 {
ReaderPlugin::ReaderPlugin(std::shared_ptr<std::istream> stream, const std::string &libname, const std::string &newreader) {
#ifdef WIN32
    dll_handle = LoadLibrary(libname.c_str());
    if (!dll_handle) { printf("Error  while loading library %s. Error code %i\n", libname.c_str(), GetLastError()); m_reader = nullptr; return;  }
    typedef Reader* (__stdcall *f_funci)(std::shared_ptr<std::istream> stream);
    f_funci newReader = (f_funci)GetProcAddress((HINSTANCE)(dll_handle), newreader.c_str());
    if (!newReader) { printf("Error  while loading function %s from  library %s. Error code %i\n", newreader.c_str(), libname.c_str(), GetLastError()); m_reader = nullptr; return;  }
    m_reader = (Reader*)(newReader(stream));
#endif

#if defined(__linux__) || defined(__darwin__) || defined(__APPLE__) || defined(BSD) || defined(__sun)
    dll_handle = dlopen(libname.c_str(), RTLD_LAZY | RTLD_GLOBAL);
    if (!dll_handle) { printf("Error  while loading library %s: %s\n", libname.c_str(), dlerror()); m_reader = nullptr; return;  }
    using f_funci = Reader *(*)(std::shared_ptr<std::istream>);
    auto newReader = (f_funci)dlsym(dll_handle, newreader.c_str());
    if (!newReader) { printf("Error  while loading function %s from  library %s: %s\n", newreader.c_str(), libname.c_str(), dlerror()); m_reader = nullptr; return;   }
    m_reader = (Reader*)(newReader(stream));
#endif
}

ReaderPlugin::ReaderPlugin(std::istream & stream, const std::string &libname, const std::string &newreader) {
#ifdef WIN32
    dll_handle = LoadLibrary(libname.c_str());
    if (!dll_handle) { printf("Error  while loading library %s. Error code %i\n", libname.c_str(), GetLastError()); m_reader = nullptr; return;  }
    typedef Reader* (__stdcall *f_funci)(std::istream & stream);
    f_funci newReader = (f_funci)GetProcAddress((HINSTANCE)(dll_handle), newreader.c_str());
    if (!newReader) { printf("Error  while loading function %s from  library %s. Error code %i\n", newreader.c_str(), libname.c_str(), GetLastError()); m_reader = nullptr; return;  }
    m_reader = (Reader*)(newReader(stream));
#endif

#if defined(__linux__) || defined(__darwin__) || defined(__APPLE__) || defined(BSD) || defined(__sun)
    dll_handle = dlopen(libname.c_str(), RTLD_LAZY | RTLD_GLOBAL);
    if (!dll_handle) { printf("Error  while loading library %s: %s\n", libname.c_str(), dlerror()); m_reader = nullptr; return;  }
    using f_funci = Reader *(*)(std::istream &);
    auto newReader = (f_funci)dlsym(dll_handle, newreader.c_str());
    if (!newReader) { printf("Error  while loading function %s from  library %s: %s\n", newreader.c_str(), libname.c_str(), dlerror()); m_reader = nullptr; return;   }
    m_reader = (Reader*)(newReader(stream));
#endif
}
/** @brief Constructor */
ReaderPlugin::ReaderPlugin(const std::string& filename, const std::string &libname, const std::string &newreader) {
#ifdef WIN32
    dll_handle = LoadLibrary(libname.c_str());
    if (!dll_handle) { printf("Error  while loading library %s. Error code %i\n", libname.c_str(), GetLastError()); m_reader = nullptr; return;  }
    typedef Reader* (__stdcall *f_funci)(const std::string&);
    f_funci newReader = (f_funci)GetProcAddress((HINSTANCE)(dll_handle), newreader.c_str());
    if (!newReader) { printf("Error  while loading function %s from  library %s. Error code %i\n", newreader.c_str(), libname.c_str(), GetLastError()); m_reader = nullptr; return;  }
    m_reader = (Reader*)(newReader(filename));
#endif

#if defined(__linux__) || defined(__darwin__) || defined(__APPLE__) || defined(BSD) || defined(__sun)
    dll_handle = dlopen(libname.c_str(), RTLD_LAZY | RTLD_GLOBAL);
    if (!dll_handle) { printf("Error  while loading library %s: %s\n", libname.c_str(), dlerror()); m_reader = nullptr; return;  }
    using f_funci = Reader *(*)(const std::string&);
    auto newReader = (f_funci)dlsym(dll_handle, newreader.c_str());
    if (!newReader) { printf("Error  while loading function %s from  library %s: %s\n", newreader.c_str(), libname.c_str(), dlerror()); m_reader = nullptr; return;   }
    m_reader = (Reader*)(newReader(filename));
#endif
}
ReaderPlugin::~ReaderPlugin() {
    if (m_reader) m_reader->close();
    delete m_reader;
#ifdef WIN32
    if (dll_handle) {
        FreeLibrary((HINSTANCE)(dll_handle));
    }
#endif
#if defined(__linux__) || defined(__darwin__) || defined(__APPLE__) || defined(BSD) || defined(__sun)
    if (dll_handle) {
        dlclose(dll_handle);
        dll_handle = nullptr;
    }
#endif
}
} // namespace HepMC3
