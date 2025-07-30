// -*- C++ -*-
//
// This file is part of HepMC
// Copyright (C) 2014-2023 The HepMC collaboration (see AUTHORS for details)
//
/**
 *  @file HEPEVT_Wrapper.cc
 *  @brief Implementation of helper functions used to manipulate with HEPEVT block
 */
#include <algorithm>
#include <array>
#include <set>
#include <vector>

#include "HepMC3/HEPEVT_Helpers.h"
#include "HepMC3/HEPEVT_Wrapper.h"
#include "HepMC3/HEPEVT_Wrapper_Runtime.h"
#include "HepMC3/HEPEVT_Wrapper_Runtime_Static.h"
namespace HepMC3
{


/** @brief comparison of two particles */
bool GenParticlePtr_greater::operator()(ConstGenParticlePtr lx, ConstGenParticlePtr rx) const
{
    /* Cannot use id as it could be different.*/
    if (lx->pid() != rx->pid()) return (lx->pid() < rx->pid());
    if (lx->status() != rx->status()) return (lx->status() < rx->status());
    /*Hopefully it will reach this point not too often.*/
    return (lx->momentum().e() < rx->momentum().e());
}

/** @brief  Order vertices with equal paths. If the paths are equal, order in other quantities.
 * We cannot use id, as it can be assigned in different way*/
bool pair_GenVertexPtr_int_greater::operator()(const std::pair<ConstGenVertexPtr, int>& lx, const std::pair<ConstGenVertexPtr, int>& rx) const
{
    if (lx.second != rx.second) return (lx.second < rx.second);
    if (lx.first->particles_in().size() != rx.first->particles_in().size()) return (lx.first->particles_in().size() < rx.first->particles_in().size());
    if (lx.first->particles_out().size() != rx.first->particles_out().size()) return (lx.first->particles_out().size() < rx.first->particles_out().size());
    /* The code below is usefull mainly for debug. Assures strong ordering.*/
    std::vector<int> lx_id_in;
    lx_id_in.reserve(lx.first->particles_in().size());
    std::vector<int> rx_id_in;
    rx_id_in.reserve(rx.first->particles_in().size());
    for (const ConstGenParticlePtr& pp: lx.first->particles_in()) lx_id_in.emplace_back(pp->pid());
    for (const ConstGenParticlePtr& pp: rx.first->particles_in()) rx_id_in.emplace_back(pp->pid());
    std::sort(lx_id_in.begin(), lx_id_in.end());
    std::sort(rx_id_in.begin(), rx_id_in.end());
    for (unsigned int i = 0; i < lx_id_in.size(); i++) if (lx_id_in[i] != rx_id_in[i]) return  (lx_id_in[i] < rx_id_in[i]);

    std::vector<int> lx_id_out;
    lx_id_out.reserve(lx.first->particles_out().size());
    std::vector<int> rx_id_out;
    rx_id_out.reserve(rx.first->particles_out().size());
    for (const ConstGenParticlePtr& pp: lx.first->particles_in()) lx_id_out.emplace_back(pp->pid());
    for (const ConstGenParticlePtr& pp: rx.first->particles_in()) rx_id_out.emplace_back(pp->pid());
    std::sort(lx_id_out.begin(), lx_id_out.end());
    std::sort(rx_id_out.begin(), rx_id_out.end());
    for (unsigned int i = 0; i < lx_id_out.size(); i++) if (lx_id_out[i] != rx_id_out[i]) return  (lx_id_out[i] < rx_id_out[i]);

    std::vector<double> lx_mom_in;
    std::vector<double> rx_mom_in;
    for (const ConstGenParticlePtr& pp: lx.first->particles_in()) lx_mom_in.emplace_back(pp->momentum().e());
    for (const ConstGenParticlePtr& pp: rx.first->particles_in()) rx_mom_in.emplace_back(pp->momentum().e());
    std::sort(lx_mom_in.begin(), lx_mom_in.end());
    std::sort(rx_mom_in.begin(), rx_mom_in.end());
    for (unsigned int i = 0; i < lx_mom_in.size(); i++) if (lx_mom_in[i] != rx_mom_in[i]) return  (lx_mom_in[i] < rx_mom_in[i]);

    std::vector<double> lx_mom_out;
    std::vector<double> rx_mom_out;
    for (const ConstGenParticlePtr& pp: lx.first->particles_in()) lx_mom_out.emplace_back(pp->momentum().e());
    for (const ConstGenParticlePtr& pp: rx.first->particles_in()) rx_mom_out.emplace_back(pp->momentum().e());
    std::sort(lx_mom_out.begin(), lx_mom_out.end());
    std::sort(rx_mom_out.begin(), rx_mom_out.end());
    for (unsigned int i = 0; i < lx_mom_out.size(); i++) if (lx_mom_out[i] != rx_mom_out[i]) return  (lx_mom_out[i] < rx_mom_out[i]);
    /* The code above is usefull mainly for debug*/

    //return (lx.first < lx.first); /*This  is random. This should never happen*/
    return false;
}
/** @brief Calculates the path to the top (beam) particles */
void calculate_longest_path_to_top(ConstGenVertexPtr v, std::map<ConstGenVertexPtr, int>& pathl)
{
    int p = 0;
    for (const ConstGenParticlePtr& pp: v->particles_in()) {
        ConstGenVertexPtr v2 = pp->production_vertex();
        if (v2 == v) continue; //LOOP! THIS SHOULD NEVER HAPPEN FOR A PROPER EVENT!
        if (!v2) { p = std::max(p, 1); }
        else
        {if (pathl.count(v2) == 0)  calculate_longest_path_to_top(v2, pathl); p = std::max(p, pathl[v2]+1);}
    }
    pathl[v] = p;
}

/** @brief pointer to the common block */
HEPMC3_EXPORT_API struct HEPEVT*  hepevtptr = nullptr;
HEPMC3_EXPORT_API std::shared_ptr<struct HEPEVT_Pointers<double> >  HEPEVT_Wrapper_Runtime_Static::m_hepevtptr = nullptr;
HEPMC3_EXPORT_API int HEPEVT_Wrapper_Runtime_Static::m_max_particles = 0;

/** @brief Set the address */
void HEPEVT_Wrapper_Runtime::set_hepevt_address(char *c) {
    m_hepevtptr = std::make_shared<struct HEPEVT_Pointers<double> >();
    char* x = c;
    m_hepevtptr->nevhep = reinterpret_cast<int*> (x);
    x += sizeof(int);
    m_hepevtptr->nhep = reinterpret_cast<int*> (x);
    x += sizeof(int);
    m_hepevtptr->isthep = reinterpret_cast<int*> (x);
    x += sizeof(int)*m_max_particles;
    m_hepevtptr->idhep = reinterpret_cast<int*> (x);
    x += sizeof(int)*m_max_particles;
    m_hepevtptr->jmohep = reinterpret_cast<int*> (x);
    x += sizeof(int)*m_max_particles*2;
    m_hepevtptr->jdahep = reinterpret_cast<int*> (x);
    x += sizeof(int)*m_max_particles*2;
    m_hepevtptr->phep = reinterpret_cast<double*> (x);
    x += sizeof(double)*m_max_particles*5;
    m_hepevtptr->vhep = reinterpret_cast<double*> (x);
}


void HEPEVT_Wrapper_Runtime::print_hepevt( std::ostream& ostr ) const
{
    ostr << " Event No.: " << *(m_hepevtptr->nevhep) << std::endl;
    ostr << "  Nr   Type   Parent(s)  Daughter(s)      Px       Py       Pz       E    Inv. M." << std::endl;
    for ( int i = 1; i <= *(m_hepevtptr->nhep); ++i )
    {
        print_hepevt_particle( i, ostr );
    }
}


void HEPEVT_Wrapper_Runtime::print_hepevt_particle( int index, std::ostream& ostr ) const
{
    std::array<char, 255> buf{};//Note: the format is fixed, so no reason for complicated treatment

    snprintf(buf.data(), buf.size(), "%5i %6i%4i - %4i  %4i - %4i %8.2f %8.2f %8.2f %8.2f %8.2f",
             index, m_hepevtptr->idhep[index-1],
             m_hepevtptr->jmohep[2*(index-1)], m_hepevtptr->jmohep[2*(index-1)+1],
             m_hepevtptr->jdahep[2*(index-1)], m_hepevtptr->jdahep[2*(index-1)+1],
             m_hepevtptr->phep[5*(index-1)], m_hepevtptr->phep[5*(index-1)+1], m_hepevtptr->phep[5*(index-1)+2], m_hepevtptr->phep[5*(index-1)+3], m_hepevtptr->phep[5*(index-1)+4]);
    ostr << buf.data() << std::endl;
}


void HEPEVT_Wrapper_Runtime::zero_everything()
{
    *(m_hepevtptr->nevhep) = 0;
    *(m_hepevtptr->nhep) = 0;
    memset(m_hepevtptr->isthep, 0, sizeof(int)*m_max_particles);
    memset(m_hepevtptr->idhep, 0, sizeof(int)*m_max_particles);
    memset(m_hepevtptr->jmohep, 0, sizeof(int)*m_max_particles*2);
    memset(m_hepevtptr->jdahep, 0, sizeof(int)*m_max_particles*2);
    memset(m_hepevtptr->phep, 0, sizeof(double)*m_max_particles*5);
    memset(m_hepevtptr->vhep, 0, sizeof(double)*m_max_particles*4);
}


int HEPEVT_Wrapper_Runtime::number_parents( const int index )  const
{
    return (m_hepevtptr->jmohep[2*(index-1)]) ? (m_hepevtptr->jmohep[2*(index-1)+1]) ? m_hepevtptr->jmohep[2*(index-1)+1]
           -m_hepevtptr->jmohep[2*(index-1)] : 1 : 0;
}


int HEPEVT_Wrapper_Runtime::number_children( const int index )  const
{
    return (m_hepevtptr->jdahep[2*(index-1)]) ? (m_hepevtptr->jdahep[2*(index-1)+1]) ? m_hepevtptr->jdahep[2*(index-1)+1]-m_hepevtptr->jdahep[2*(index-1)] : 1 : 0;
}

int HEPEVT_Wrapper_Runtime::number_children_exact( const int index )  const
{
    int nc = 0;
    for ( int i = 1; i <= *(m_hepevtptr->nhep); ++i ) {
        if (((m_hepevtptr->jmohep[2*(i-1)] <= index && m_hepevtptr->jmohep[2*(i-1)+1] >= index)) || (m_hepevtptr->jmohep[2*(i-1)] == index) ||
                (m_hepevtptr->jmohep[2*(index-1)+1]==index)) nc++;
    }
    return nc;
}

void HEPEVT_Wrapper_Runtime::set_parents( const int index,  const int firstparent, const int lastparent )
{
    m_hepevtptr->jmohep[2*(index-1)] = firstparent;
    m_hepevtptr->jmohep[2*(index-1)+1] = lastparent;
}

void HEPEVT_Wrapper_Runtime::set_children(  const int index,  const int  firstchild,  const int lastchild )
{
    m_hepevtptr->jdahep[2*(index-1)] = firstchild;
    m_hepevtptr->jdahep[2*(index-1)+1] = lastchild;
}


void HEPEVT_Wrapper_Runtime::set_momentum( const int index, const double px, const double py, const double pz, const double e )
{
    m_hepevtptr->phep[5*(index-1)] = px;
    m_hepevtptr->phep[5*(index-1)+1] = py;
    m_hepevtptr->phep[5*(index-1)+2] = pz;
    m_hepevtptr->phep[5*(index-1)+3] = e;
}


void HEPEVT_Wrapper_Runtime::set_mass( const int index, double mass )
{
    m_hepevtptr->phep[5*(index-1)+4] = mass;
}


void HEPEVT_Wrapper_Runtime::set_position( const int index, const double x, const double y, const double z, const double t )
{
    m_hepevtptr->vhep[4*(index-1)] = x;
    m_hepevtptr->vhep[4*(index-1)+1] = y;
    m_hepevtptr->vhep[4*(index-1)+2] = z;
    m_hepevtptr->vhep[4*(index-1)+3] = t;
}


bool HEPEVT_Wrapper_Runtime::fix_daughters()
{
    /*AV The function should be called  for a record that has correct particle ordering and mother ids.
    As a result it produces a record with ranges where the daughters can be found.
    Not every particle in the range will be a daughter. It is true only for proper events.
    The return tells if the record was fixed succesfully.
    */
    for ( int i = 1; i <= number_entries(); i++ ) {
        for ( int k=1; k <= number_entries(); k++ ) {
            if (i != k) {
                if ((first_parent(k) <= i) && (i <= last_parent(k))) {
                    set_children(i, (first_child(i) == 0 ? k : std::min(first_child(i), k)), (last_child(i) == 0 ? k : std::max(last_child(i), k)));
                }
            }
        }
    }
    bool is_fixed = true;
    for ( int i = 1; i <= number_entries(); i++ ) {
        is_fixed = (is_fixed && (number_children_exact(i) == number_children(i)));
    }
    return is_fixed;
}


void HEPEVT_Wrapper_Runtime::allocate_internal_storage()
{
    m_internal_storage.reserve(2*sizeof(int)+m_max_particles*(6*sizeof(int)+9*sizeof(double)));
    set_hepevt_address(m_internal_storage.data());
}

void HEPEVT_Wrapper_Runtime::copy_to_internal_storage(char *c, int N)
{
    if ( N < 1 || N > m_max_particles) return;
    char* dest = m_internal_storage.data();
    char* src = c;
    memcpy(dest, src, 2*sizeof(int));
    src  += 2*sizeof(int);
    dest += 2*sizeof(int);
    memcpy(dest, src, N*sizeof(int));
    src  += N*sizeof(int);
    dest += m_max_particles*sizeof(int);
    memcpy(dest, src, N*sizeof(int));
    src  += N*sizeof(int);
    dest += m_max_particles*sizeof(int);
    memcpy(dest, src, 2*N*sizeof(int));
    src  += 2*N*sizeof(int);
    dest += 2*m_max_particles*sizeof(int);
    memcpy(dest, src, 2*N*sizeof(int));
    src  += 2*N*sizeof(int);
    dest += 2*m_max_particles*sizeof(int);
    memcpy(dest, src, 5*N*sizeof(double));
    src  += 5*N*sizeof(double);
    dest += 5*m_max_particles*sizeof(double);
    memcpy(dest, src, 4*N*sizeof(double));
}

} // namespace HepMC3
