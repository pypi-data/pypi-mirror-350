// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2023 The HepMC collaboration (see AUTHORS for details)
//
#ifndef HEPMC3_READERGZ_H
#define HEPMC3_READERGZ_H
///
/// @file  ReaderGZ.h
/// @brief Definition of class \b ReaderGZ
///
/// @class HepMC3::ReaderGZ
/// @brief GenEvent I/O parsing for compressed files
///
/// @ingroup IO
///
#include <set>
#include <string>
#include <fstream>
#include <istream>
#include <iterator>
#include "HepMC3/Reader.h"
#include "HepMC3/GenEvent.h"
#include "HepMC3/CompressedIO.h"
namespace HepMC3 {

template <class T> class ReaderGZ : public Reader {
public:

    /// @brief Constructor
    ReaderGZ(const std::string& filename) {
        m_zstr = std::shared_ptr< std::istream >(new ifstream(filename.c_str()));
        m_reader = std::make_shared<T>(*(m_zstr.get()));
    }
    /// @brief The ctor to read from stdin
    ReaderGZ(std::istream & is) {
        m_zstr = std::shared_ptr< std::istream >(new istream(is));
        m_reader = std::make_shared<T>(*(m_zstr.get()));
    }
    /// @brief The ctor to read from shared pointer to stream
    ReaderGZ(std::shared_ptr<std::istream> s_stream) {
        m_zstr = s_stream;
        m_reader = std::make_shared<T>(*(m_zstr.get()));
    }

    /// @brief Destructor
    ~ReaderGZ() { close(); }

    /// @brief skip events
    bool skip(const int i) override { if (m_reader) return m_reader->skip(i); return false; }

    /// @brief Load event from file
    ///
    /// @param[out] evt Event to be filled
    bool read_event(GenEvent& evt) override { if (m_reader) return m_reader->read_event(evt); return false; }


    /// @brief Return status of the stream
    bool failed() override { if (m_reader) return m_reader->failed(); return false; }


    /// @brief Close file stream
    void close() override {
        if (m_reader) return m_reader->close();
        if(dynamic_pointer_cast<ifstream>(m_zstr)) dynamic_pointer_cast<ifstream>(m_zstr)->close();
    }

    /// Set the act reader's GenRunInfo object.
    void set_run_info(std::shared_ptr<GenRunInfo> run) override { if (m_reader) m_reader->set_run_info(run); }

    /// Get the act reader's GenRunInfo object.
    std::shared_ptr<GenRunInfo> run_info() const override { return m_reader?m_reader->run_info():nullptr; }

    /// Return reader
    std::shared_ptr<Reader> writer() { return m_reader;}

private:
    ///@brief Close file stream
    std::shared_ptr< std::istream > m_zstr = nullptr;  ///< Stream to read
    std::shared_ptr<Reader> m_reader = nullptr; ///< Actual reader

};

} // namespace HepMC3
#endif
