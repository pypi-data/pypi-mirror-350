#include <HepMC3/Setup.h>
#include <sstream> // __str__

#include <functional>
#include <pybind11/pybind11.h>
#include <string>
#include <HepMC3/Version.h>
#include <HepMC3/Reader.h>
#include <HepMC3/Writer.h>
#include <HepMC3/Print.h>
#include <src/stl_binders.hpp>
#include <src/binders.h>


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>, false)
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*, false)
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>)
#endif

void bind_pyHepMC3_0(std::function< pybind11::module &(std::string const &namespace_) > &M)
{

	binder::custom_deduce_reader(M("HepMC3"));
	{ // HepMC3::Setup file:HepMC3/Setup.h line:
		pybind11::class_<HepMC3::Setup, HepMC3::Setup*> cl(M("HepMC3"), "Setup", "Configuration for HepMC\n\n Contains macro definitions for printing debug output, feature deprecation, etc.\n Static class - configuration is shared among all HepMC events\n and program threads");
		cl.def_static("print_errors", (bool (*)()) &HepMC3::Setup::print_errors, "Get error messages printing flag\n\nC++: HepMC3::Setup::print_errors() --> bool");
		cl.def_static("set_print_errors", (void (*)(const bool)) &HepMC3::Setup::set_print_errors, "set error messages printing flag\n\nC++: HepMC3::Setup::set_print_errors(const bool) --> void", pybind11::arg("flag"));
		cl.def_static("errors_level", (int (*)()) &HepMC3::Setup::errors_level, "Get error messages printing level\n\nC++: HepMC3::Setup::errors_level() --> int");
		cl.def_static("set_errors_level", (void (*)(const int)) &HepMC3::Setup::set_errors_level, "set error messages printing level\n\nC++: HepMC3::Setup::set_errors_level(const int) --> void", pybind11::arg("flag"));
		cl.def_static("print_warnings", (bool (*)()) &HepMC3::Setup::print_warnings, "Get warning messages printing flag\n\nC++: HepMC3::Setup::print_warnings() --> bool");
		cl.def_static("set_print_warnings", (void (*)(const bool)) &HepMC3::Setup::set_print_warnings, "Set warning messages printing flag\n\nC++: HepMC3::Setup::set_print_warnings(const bool) --> void", pybind11::arg("flag"));
		cl.def_static("warnings_level", (int (*)()) &HepMC3::Setup::warnings_level, "Get warning messages printing level\n\nC++: HepMC3::Setup::warnings_level() --> int");
		cl.def_static("set_warnings_level", (void (*)(const int)) &HepMC3::Setup::set_warnings_level, "Set warning messages printing level\n\nC++: HepMC3::Setup::set_warnings_level(const int) --> void", pybind11::arg("flag"));
		cl.def_static("debug_level", (int (*)()) &HepMC3::Setup::debug_level, "Get debug level\n\nC++: HepMC3::Setup::debug_level() --> int");
		cl.def_static("set_debug_level", (void (*)(const int)) &HepMC3::Setup::set_debug_level, "Set debug level\n\nC++: HepMC3::Setup::set_debug_level(const int) --> void", pybind11::arg("level"));
	}
}
