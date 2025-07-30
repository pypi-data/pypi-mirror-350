// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2023 The HepMC collaboration (see AUTHORS for details)
//
#ifndef HEPMC3_WRITERPROTOBUF_H
#define HEPMC3_WRITERPROTOBUF_H
/**
 *  @file  Writerprotobuf.h
 *  @brief Definition of \b class Writerprotobuf
 *
 *  @class HepMC3::Writerprotobuf
 *  @brief GenEvent I/O serialization for protobuf-based binary files
 *
 *  If HepMC was compiled with protobuf available, this class can be used
 *  for writing in the same manner as with HepMC::WriterAscii class.
 *
 *  @ingroup IO
 *
 */

#include "HepMC3/Writer.h"

#include "HepMC3/GenEvent.h"

#include <fstream>
#include <memory>
#include <string>

namespace HepMC3 {

class Writerprotobuf : public Writer {
  //
  // Constructors
  //
public:
  /** @brief New file constructor
   *  @warning If file exists, it will be overwritten
   */
  Writerprotobuf(
      const std::string &filename,
      std::shared_ptr<GenRunInfo> run = std::shared_ptr<GenRunInfo>());

  /** @brief ostream constructor
   *
   * @details Attempts to write a binary HepMC3 protobuf event stream to the
   * passed ostream object
   */
  Writerprotobuf(std::ostream &out_stream, std::shared_ptr<GenRunInfo> run =
                                               std::shared_ptr<GenRunInfo>());

  /** @brief ostream constructor
   *
   * @details Attempts to write a binary HepMC3 protobuf event stream to the
   * passed ostream object
   */
  Writerprotobuf(
      std::shared_ptr<std::ostream> out_stream,
      std::shared_ptr<GenRunInfo> run = std::shared_ptr<GenRunInfo>());

  //
  // Functions
  //
public:
  /** @brief Write event to file
   *
   *  @param[in] evt Event to be serialized
   */
  void write_event(const GenEvent &evt) override;

  /** @brief Close file stream */
  void close() override;

  /** @brief Get stream error state flag */
  bool failed() override;

  /** @brief Standard destructor */
  virtual ~Writerprotobuf() { close(); }

  /** @brief Write the GenRunInfo object to file. */
  void write_run_info();

private:
  /** @brief Write non-event front matter to the output stream. */
  void start_file();

  /** @brief The output file stream
   *
   * @details This is non-null and owned by this class if the instance was
   * constructed with the string constructor, it is null otherwise.
   */
  std::unique_ptr<std::ofstream> m_out_file;
  /** @brief Passed in shared_ptr to an output stream
   *
   * @details This is non-null and shared by this class if constructed with the
   * stream constructor
   */
  std::shared_ptr<std::ostream> m_shared_stream;
  /** @brief The stream object that is written to
   *
   * @details If constructed with the string constructor, this just points to
   * m_out_file.get())
   */
  std::ostream *m_out_stream;

  /** @brief The number of events written to the stream */
  size_t m_events_written;
  /** @brief The number of event bytes written to the stream */
  size_t m_event_bytes_written;
};

} // namespace HepMC3

#endif
