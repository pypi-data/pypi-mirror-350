// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2023 The HepMC collaboration (see AUTHORS for details)
//
#ifndef HEPMC3_WRITERROOTTREEOPAL_H
#define HEPMC3_WRITERROOTTREEOPAL_H
///
/// @file  WriterRootTreeOPAL.h
/// @brief Definition of class \b WriterRootTreeOPAL
///
/// @class HepMC3::WriterRootTreeOPAL
/// @brief GenEvent I/O output to files similar to these produced by OPAL software
///
/// @ingroup Examples
///
#include "HepMC3/WriterRootTree.h"
#include "HepMC3/GenEvent.h"
#include "HepMC3/GenParticle.h"
#include "HepMC3/Data/GenEventData.h"
namespace HepMC3
{
class WriterRootTreeOPAL : public WriterRootTree
{
public:
    /** @brief Constructor */
    WriterRootTreeOPAL(const std::string &filename,std::shared_ptr<GenRunInfo> run = std::shared_ptr<GenRunInfo>());
    /** @brief Init ROOT branches */
    void init_branches();
    /** @brief Write event */
    void write_event(const GenEvent &evt);
    /** @brief Set run number */
    void set_run_number(const int nr);
private:
    float  m_Ebeam = 0.0; ///< Beam energy in GEV
    int    m_Irun = 0;  ///< Run number
    int    m_Ievnt = 0; ///< Event number
};
}
#endif
