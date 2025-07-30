// Guarding against multiple inclusions
#ifndef HQ_H
#define HQ_H

// Include Windows.h for WINAPI compatibility
#include <Windows.h>

// Define export/import macros for DLL usage
#ifdef HQ_EXPORTS
    #define HQ_API __declspec(dllexport)
#else
    #define HQ_API __declspec(dllimport)
#endif

// Ensure C linkage for C++ compatibility
#ifdef __cplusplus
extern "C" {
#endif

// Error codes for better error handling
#define HQ_SUCCESS          0
#define HQ_BUFFER_TOO_SMALL -1
#define HQ_INVALID_PARAM    -2
#define HQ_CONNECTION_FAIL  -3
#define HQ_QUERY_FAIL       -4
#define HQ_NOT_CONNECTED    -5

/**
 * Connects to a service using the provided configuration.
 *
 * @param config    Pointer to a null-terminated configuration string.
 * @param out       Pointer to the output buffer for connection details or error messages.
 * @param outLen    Length of the output buffer in bytes.
 * @return          HQ_SUCCESS on success, or a negative error code on failure.
 */
HQ_API int WINAPI Connect(const char* config, char* out, int outLen);

/**
 * Disconnects from the service.
 *
 * @return          HQ_SUCCESS on success, or a negative error code on failure.
 */
HQ_API int WINAPI Disconnect(void);

/**
 * Queries data from the service.
 *
 * @param req       Pointer to a null-terminated request string.
 * @param queryType Pointer to a null-terminated string specifying the query type.
 * @param out       Pointer to the output buffer for query results or error messages.
 * @param outLen    Length of the output buffer in bytes.
 * @return          HQ_SUCCESS on success, or a negative error code on failure.
 */
HQ_API int WINAPI QueryData(const char* req, const char* queryType, char* out, int outLen);

/**
 * Retrieves information about the library or service.
 *
 * @return          HQ_SUCCESS on success, or a negative error code on failure.
 */
HQ_API int WINAPI About(void);

// End C linkage
#ifdef __cplusplus
}
#endif

#endif // HQ_H