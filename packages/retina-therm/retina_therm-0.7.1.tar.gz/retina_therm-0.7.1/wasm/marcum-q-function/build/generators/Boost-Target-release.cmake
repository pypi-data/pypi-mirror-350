# Avoid multiple calls to find_package to append duplicated properties to the targets
include_guard()########### VARIABLES #######################################################################
#############################################################################################
set(boost_FRAMEWORKS_FOUND_RELEASE "") # Will be filled later
conan_find_apple_frameworks(boost_FRAMEWORKS_FOUND_RELEASE "${boost_FRAMEWORKS_RELEASE}" "${boost_FRAMEWORK_DIRS_RELEASE}")

set(boost_LIBRARIES_TARGETS "") # Will be filled later


######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
if(NOT TARGET boost_DEPS_TARGET)
    add_library(boost_DEPS_TARGET INTERFACE IMPORTED)
endif()

set_property(TARGET boost_DEPS_TARGET
             APPEND PROPERTY INTERFACE_LINK_LIBRARIES
             $<$<CONFIG:Release>:${boost_FRAMEWORKS_FOUND_RELEASE}>
             $<$<CONFIG:Release>:${boost_SYSTEM_LIBS_RELEASE}>
             $<$<CONFIG:Release>:Boost::headers>)

####### Find the libraries declared in cpp_info.libs, create an IMPORTED target for each one and link the
####### boost_DEPS_TARGET to all of them
conan_package_library_targets("${boost_LIBS_RELEASE}"    # libraries
                              "${boost_LIB_DIRS_RELEASE}" # package_libdir
                              "${boost_BIN_DIRS_RELEASE}" # package_bindir
                              "${boost_LIBRARY_TYPE_RELEASE}"
                              "${boost_IS_HOST_WINDOWS_RELEASE}"
                              boost_DEPS_TARGET
                              boost_LIBRARIES_TARGETS  # out_libraries_targets
                              "_RELEASE"
                              "boost"    # package_name
                              "${boost_NO_SONAME_MODE_RELEASE}")  # soname

# FIXME: What is the result of this for multi-config? All configs adding themselves to path?
set(CMAKE_MODULE_PATH ${boost_BUILD_DIRS_RELEASE} ${CMAKE_MODULE_PATH})

########## COMPONENTS TARGET PROPERTIES Release ########################################

    ########## COMPONENT Boost::boost #############

        set(boost_Boost_boost_FRAMEWORKS_FOUND_RELEASE "")
        conan_find_apple_frameworks(boost_Boost_boost_FRAMEWORKS_FOUND_RELEASE "${boost_Boost_boost_FRAMEWORKS_RELEASE}" "${boost_Boost_boost_FRAMEWORK_DIRS_RELEASE}")

        set(boost_Boost_boost_LIBRARIES_TARGETS "")

        ######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
        if(NOT TARGET boost_Boost_boost_DEPS_TARGET)
            add_library(boost_Boost_boost_DEPS_TARGET INTERFACE IMPORTED)
        endif()

        set_property(TARGET boost_Boost_boost_DEPS_TARGET
                     APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Release>:${boost_Boost_boost_FRAMEWORKS_FOUND_RELEASE}>
                     $<$<CONFIG:Release>:${boost_Boost_boost_SYSTEM_LIBS_RELEASE}>
                     $<$<CONFIG:Release>:${boost_Boost_boost_DEPENDENCIES_RELEASE}>
                     )

        ####### Find the libraries declared in cpp_info.component["xxx"].libs,
        ####### create an IMPORTED target for each one and link the 'boost_Boost_boost_DEPS_TARGET' to all of them
        conan_package_library_targets("${boost_Boost_boost_LIBS_RELEASE}"
                              "${boost_Boost_boost_LIB_DIRS_RELEASE}"
                              "${boost_Boost_boost_BIN_DIRS_RELEASE}" # package_bindir
                              "${boost_Boost_boost_LIBRARY_TYPE_RELEASE}"
                              "${boost_Boost_boost_IS_HOST_WINDOWS_RELEASE}"
                              boost_Boost_boost_DEPS_TARGET
                              boost_Boost_boost_LIBRARIES_TARGETS
                              "_RELEASE"
                              "boost_Boost_boost"
                              "${boost_Boost_boost_NO_SONAME_MODE_RELEASE}")


        ########## TARGET PROPERTIES #####################################
        set_property(TARGET Boost::boost
                     APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Release>:${boost_Boost_boost_OBJECTS_RELEASE}>
                     $<$<CONFIG:Release>:${boost_Boost_boost_LIBRARIES_TARGETS}>
                     )

        if("${boost_Boost_boost_LIBS_RELEASE}" STREQUAL "")
            # If the component is not declaring any "cpp_info.components['foo'].libs" the system, frameworks etc are not
            # linked to the imported targets and we need to do it to the global target
            set_property(TARGET Boost::boost
                         APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                         boost_Boost_boost_DEPS_TARGET)
        endif()

        set_property(TARGET Boost::boost APPEND PROPERTY INTERFACE_LINK_OPTIONS
                     $<$<CONFIG:Release>:${boost_Boost_boost_LINKER_FLAGS_RELEASE}>)
        set_property(TARGET Boost::boost APPEND PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                     $<$<CONFIG:Release>:${boost_Boost_boost_INCLUDE_DIRS_RELEASE}>)
        set_property(TARGET Boost::boost APPEND PROPERTY INTERFACE_LINK_DIRECTORIES
                     $<$<CONFIG:Release>:${boost_Boost_boost_LIB_DIRS_RELEASE}>)
        set_property(TARGET Boost::boost APPEND PROPERTY INTERFACE_COMPILE_DEFINITIONS
                     $<$<CONFIG:Release>:${boost_Boost_boost_COMPILE_DEFINITIONS_RELEASE}>)
        set_property(TARGET Boost::boost APPEND PROPERTY INTERFACE_COMPILE_OPTIONS
                     $<$<CONFIG:Release>:${boost_Boost_boost_COMPILE_OPTIONS_RELEASE}>)

    ########## COMPONENT Boost::headers #############

        set(boost_Boost_headers_FRAMEWORKS_FOUND_RELEASE "")
        conan_find_apple_frameworks(boost_Boost_headers_FRAMEWORKS_FOUND_RELEASE "${boost_Boost_headers_FRAMEWORKS_RELEASE}" "${boost_Boost_headers_FRAMEWORK_DIRS_RELEASE}")

        set(boost_Boost_headers_LIBRARIES_TARGETS "")

        ######## Create an interface target to contain all the dependencies (frameworks, system and conan deps)
        if(NOT TARGET boost_Boost_headers_DEPS_TARGET)
            add_library(boost_Boost_headers_DEPS_TARGET INTERFACE IMPORTED)
        endif()

        set_property(TARGET boost_Boost_headers_DEPS_TARGET
                     APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Release>:${boost_Boost_headers_FRAMEWORKS_FOUND_RELEASE}>
                     $<$<CONFIG:Release>:${boost_Boost_headers_SYSTEM_LIBS_RELEASE}>
                     $<$<CONFIG:Release>:${boost_Boost_headers_DEPENDENCIES_RELEASE}>
                     )

        ####### Find the libraries declared in cpp_info.component["xxx"].libs,
        ####### create an IMPORTED target for each one and link the 'boost_Boost_headers_DEPS_TARGET' to all of them
        conan_package_library_targets("${boost_Boost_headers_LIBS_RELEASE}"
                              "${boost_Boost_headers_LIB_DIRS_RELEASE}"
                              "${boost_Boost_headers_BIN_DIRS_RELEASE}" # package_bindir
                              "${boost_Boost_headers_LIBRARY_TYPE_RELEASE}"
                              "${boost_Boost_headers_IS_HOST_WINDOWS_RELEASE}"
                              boost_Boost_headers_DEPS_TARGET
                              boost_Boost_headers_LIBRARIES_TARGETS
                              "_RELEASE"
                              "boost_Boost_headers"
                              "${boost_Boost_headers_NO_SONAME_MODE_RELEASE}")


        ########## TARGET PROPERTIES #####################################
        set_property(TARGET Boost::headers
                     APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                     $<$<CONFIG:Release>:${boost_Boost_headers_OBJECTS_RELEASE}>
                     $<$<CONFIG:Release>:${boost_Boost_headers_LIBRARIES_TARGETS}>
                     )

        if("${boost_Boost_headers_LIBS_RELEASE}" STREQUAL "")
            # If the component is not declaring any "cpp_info.components['foo'].libs" the system, frameworks etc are not
            # linked to the imported targets and we need to do it to the global target
            set_property(TARGET Boost::headers
                         APPEND PROPERTY INTERFACE_LINK_LIBRARIES
                         boost_Boost_headers_DEPS_TARGET)
        endif()

        set_property(TARGET Boost::headers APPEND PROPERTY INTERFACE_LINK_OPTIONS
                     $<$<CONFIG:Release>:${boost_Boost_headers_LINKER_FLAGS_RELEASE}>)
        set_property(TARGET Boost::headers APPEND PROPERTY INTERFACE_INCLUDE_DIRECTORIES
                     $<$<CONFIG:Release>:${boost_Boost_headers_INCLUDE_DIRS_RELEASE}>)
        set_property(TARGET Boost::headers APPEND PROPERTY INTERFACE_LINK_DIRECTORIES
                     $<$<CONFIG:Release>:${boost_Boost_headers_LIB_DIRS_RELEASE}>)
        set_property(TARGET Boost::headers APPEND PROPERTY INTERFACE_COMPILE_DEFINITIONS
                     $<$<CONFIG:Release>:${boost_Boost_headers_COMPILE_DEFINITIONS_RELEASE}>)
        set_property(TARGET Boost::headers APPEND PROPERTY INTERFACE_COMPILE_OPTIONS
                     $<$<CONFIG:Release>:${boost_Boost_headers_COMPILE_OPTIONS_RELEASE}>)

    ########## AGGREGATED GLOBAL TARGET WITH THE COMPONENTS #####################
    set_property(TARGET boost::boost APPEND PROPERTY INTERFACE_LINK_LIBRARIES Boost::boost)
    set_property(TARGET boost::boost APPEND PROPERTY INTERFACE_LINK_LIBRARIES Boost::headers)

########## For the modules (FindXXX)
set(boost_LIBRARIES_RELEASE boost::boost)
