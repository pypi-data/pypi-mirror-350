#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "HepMC3::HepMC3" for configuration "Release"
set_property(TARGET HepMC3::HepMC3 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(HepMC3::HepMC3 PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/HepMC3.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/HepMC3.dll"
  )

list(APPEND _cmake_import_check_targets HepMC3::HepMC3 )
list(APPEND _cmake_import_check_files_for_HepMC3::HepMC3 "${_IMPORT_PREFIX}/lib/HepMC3.lib" "${_IMPORT_PREFIX}/lib/HepMC3.dll" )

# Import target "HepMC3::HepMC3_static" for configuration "Release"
set_property(TARGET HepMC3::HepMC3_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(HepMC3::HepMC3_static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/HepMC3-static.lib"
  )

list(APPEND _cmake_import_check_targets HepMC3::HepMC3_static )
list(APPEND _cmake_import_check_files_for_HepMC3::HepMC3_static "${_IMPORT_PREFIX}/lib/HepMC3-static.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
