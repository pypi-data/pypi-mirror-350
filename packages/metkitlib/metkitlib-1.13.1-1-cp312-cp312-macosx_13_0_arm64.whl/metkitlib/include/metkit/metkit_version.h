#ifndef metkit_version_h
#define metkit_version_h

#define metkit_VERSION_STR "1.13.1"
#define metkit_VERSION     "1.13.1"

#define metkit_VERSION_MAJOR 1
#define metkit_VERSION_MINOR 13
#define metkit_VERSION_PATCH 1

#define metkit_GIT_SHA1 "2fb11d65f6ea0e6cd972f0ca1820c261ec636e7e"

#ifdef __cplusplus
extern "C" {
#endif

const char * metkit_version();

unsigned int metkit_version_int();

const char * metkit_version_str();

const char * metkit_git_sha1();

#ifdef __cplusplus
}
#endif


#endif // metkit_version_h
