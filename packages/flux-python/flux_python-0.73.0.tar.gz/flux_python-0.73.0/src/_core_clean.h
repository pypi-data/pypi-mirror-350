/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_H
#define _FLUX_CORE_H

/* NOTE: these programming interfaces should be considered EXPERIMENTAL
 * and are subject to change in flux-core releases prefixed with "0."
 */

/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_FLUX_H
#define _FLUX_CORE_FLUX_H

/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_TYPES_H
#define _FLUX_CORE_TYPES_H

#ifdef __cplusplus
extern "C" {
#endif

typedef void (*flux_free_f)(void *arg);

/*  Generic container for holding textual errors from selected libflux
 *   functions:
 */
typedef struct {
    char text[160];
} flux_error_t;

/* libflux convenience typedefs
 */
typedef struct flux_msg flux_msg_t;
typedef struct flux_handle flux_t;
typedef struct flux_watcher flux_watcher_t;
typedef struct flux_reactor flux_reactor_t;
typedef struct flux_future flux_future_t;

/* FLUX_DEPRECATED may be altered during pre-processing, check for
 * definition */
#ifndef FLUX_DEPRECATED
#define FLUX_DEPRECATED(...) __VA_ARGS__ __attribute__((deprecated))
#endif

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_TYPES_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_MESSAGE_H
#define _FLUX_CORE_MESSAGE_H


#ifdef __cplusplus
extern "C" {
#endif

enum {
    FLUX_MSGTYPE_REQUEST    = 0x01,
    FLUX_MSGTYPE_RESPONSE   = 0x02,
    FLUX_MSGTYPE_EVENT      = 0x04,
    FLUX_MSGTYPE_CONTROL    = 0x08,
    FLUX_MSGTYPE_ANY        = 0x0f,
    FLUX_MSGTYPE_MASK       = 0x0f,
};

enum {
    FLUX_MSGFLAG_TOPIC      = 0x01, /* message has topic string */
    FLUX_MSGFLAG_PAYLOAD    = 0x02, /* message has payload */
    FLUX_MSGFLAG_NORESPONSE = 0x04, /* request needs no response */
    FLUX_MSGFLAG_ROUTE      = 0x08, /* message is routable */
    FLUX_MSGFLAG_UPSTREAM   = 0x10, /* request nodeid is sender (route away) */
    FLUX_MSGFLAG_PRIVATE    = 0x20, /* private to instance owner and sender */
    FLUX_MSGFLAG_STREAMING  = 0x40, /* request/response is streaming RPC */
    FLUX_MSGFLAG_USER1      = 0x80, /* user-defined message flag */
};

/* N.B. FLUX_NODEID_UPSTREAM should be used in the RPC interface only.
 * The resulting request message is constructed with flags including
 * FLUX_MSGFLAG_UPSTREAM and nodeid set set to local broker rank.
 */
enum {
    FLUX_NODEID_ANY      = 0xFFFFFFFF, //(~(uint32_t)0),
    FLUX_NODEID_UPSTREAM = 0xFFFFFFFE  //(~(uint32_t)1)
};

struct flux_match {
    int typemask;           /* bitmask of matching message types (or 0) */
    uint32_t matchtag;      /* matchtag (or FLUX_MATCHTAG_NONE) */
    const char *topic_glob; /* glob matching topic string (or NULL) */
};

struct flux_match flux_match_init (int typemask,
                                   uint32_t matchtag,
                                   const char *topic_glob);

void flux_match_free (struct flux_match m);

int flux_match_asprintf (struct flux_match *m,
                         const char *topic_glob_fmt,
                         ...);

#define FLUX_MATCH_ANY flux_match_init( \
    FLUX_MSGTYPE_ANY, \
    FLUX_MATCHTAG_NONE, \
    NULL \
)
#define FLUX_MATCH_EVENT flux_match_init( \
    FLUX_MSGTYPE_EVENT, \
    FLUX_MATCHTAG_NONE, \
    NULL \
)
#define FLUX_MATCH_REQUEST flux_match_init( \
    FLUX_MSGTYPE_REQUEST, \
    FLUX_MATCHTAG_NONE, \
    NULL \
)
#define FLUX_MATCH_RESPONSE flux_match_init( \
    FLUX_MSGTYPE_RESPONSE, \
    FLUX_MATCHTAG_NONE, \
    NULL \
)

/* Create a new Flux message.  If the type of the message is not yet
 * known at creation time, FLUX_MSGTYPE_ANY can be used.
 *
 * Returns new message or null on failure, with errno set (e.g. ENOMEM, EINVAL)
 * Caller must destroy message with flux_msg_destroy() or equivalent.
 */
flux_msg_t *flux_msg_create (int type);
void flux_msg_destroy (flux_msg_t *msg);

/* Access auxiliary data members in Flux message.
 * These are for convenience only - they are not sent over the wire.
 */
int flux_msg_aux_set (const flux_msg_t *msg,
                      const char *name,
                      void *aux,
                      flux_free_f destroy);
void *flux_msg_aux_get (const flux_msg_t *msg, const char *name);

/* Duplicate msg, omitting payload if 'payload' is false.
 */
flux_msg_t *flux_msg_copy (const flux_msg_t *msg, bool payload);

/* Manipulate msg reference count..
 */
const flux_msg_t *flux_msg_incref (const flux_msg_t *msg);
void flux_msg_decref (const flux_msg_t *msg);

/* Encode a flux_msg_t to buffer (pre-sized by calling flux_msg_encode_size()).
 * Returns 0 on success, -1 on failure with errno set.
 */
ssize_t flux_msg_encode_size (const flux_msg_t *msg);
int flux_msg_encode (const flux_msg_t *msg, void *buf, size_t size);

/* Decode a flux_msg_t from buffer.
 * Returns message on success, NULL on failure with errno set.
 * Caller must destroy message with flux_msg_destroy().
 */
flux_msg_t *flux_msg_decode (const void *buf, size_t size);

/* Get/set message type
 * For FLUX_MSGTYPE_REQUEST: set_type initializes nodeid to FLUX_NODEID_ANY
 * For FLUX_MSGTYPE_RESPONSE: set_type initializes errnum to 0
 */
int flux_msg_set_type (flux_msg_t *msg, int type);
int flux_msg_get_type (const flux_msg_t *msg, int *type);

/* Get/set privacy flag.
 * Broker will not route a private message to connections not
 * authenticated as message sender or with instance owner role.
 */
int flux_msg_set_private (flux_msg_t *msg);
bool flux_msg_is_private (const flux_msg_t *msg);

/* Get/set streaming flag.
 * Requests to streaming RPC services should set this flag.
 * Streaming RPC services should return an error if flag is not set.
 */
int flux_msg_set_streaming (flux_msg_t *msg);
bool flux_msg_is_streaming (const flux_msg_t *msg);

/* Get/set noresponse flag.
 * Request is advisory and should not receive a response.
 */
int flux_msg_set_noresponse (flux_msg_t *msg);
bool flux_msg_is_noresponse (const flux_msg_t *msg);

/* Get/set/compare message topic string.
 * set adds/deletes/replaces topic frame as needed.
 */
int flux_msg_set_topic (flux_msg_t *msg, const char *topic);
int flux_msg_get_topic (const flux_msg_t *msg, const char **topic);

/* Get/set payload.
 * Set function adds/deletes/replaces payload frame as needed.
 * The new payload will be copied (caller retains ownership).
 * Any old payload is deleted.
 * flux_msg_get_payload returns pointer to msg-owned buf.
 */
int flux_msg_get_payload (const flux_msg_t *msg,
                          const void **buf,
                          size_t *size);
int flux_msg_set_payload (flux_msg_t *msg, const void *buf, size_t size);
bool flux_msg_has_payload (const flux_msg_t *msg);

/* Test/set/clear message flags
 */
bool flux_msg_has_flag (const flux_msg_t *msg, int flag);
int flux_msg_set_flag (flux_msg_t *msg, int flag);
int flux_msg_clear_flag (flux_msg_t *msg, int flag);

/* Get/set string payload.
 * flux_msg_set_string() accepts a NULL 's' (no payload).
 * flux_msg_get_string() will set 's' to NULL if there is no payload
 * N.B. the raw payload includes C string \0 terminator.
 */
int flux_msg_set_string (flux_msg_t *msg, const char *);
int flux_msg_get_string (const flux_msg_t *msg, const char **s);

/* Get/set JSON payload (encoded as string)
 * pack/unpack functions use jansson pack/unpack style arguments for
 * encoding/decoding the JSON object payload directly from/to its members.
 */
int flux_msg_pack (flux_msg_t *msg, const char *fmt, ...);
int flux_msg_vpack (flux_msg_t *msg, const char *fmt, va_list ap);

int flux_msg_unpack (const flux_msg_t *msg, const char *fmt, ...);
int flux_msg_vunpack (const flux_msg_t *msg, const char *fmt, va_list ap);

/* Return a string representation of the last error encountered for `msg`.
 *
 * If no last error is available, an empty string will be returned.
 *
 * Currently, only flux_msg_pack/unpack() (and related) functions will set
 * the last error for `msg`. (Useful to get more detail from EPROTO errors)
 */
const char *flux_msg_last_error (const flux_msg_t *msg);

/* Get/set nodeid (request only)
 */
int flux_msg_set_nodeid (flux_msg_t *msg, uint32_t nodeid);
int flux_msg_get_nodeid (const flux_msg_t *msg, uint32_t *nodeid);

/* Get/set userid
 */
enum {
    FLUX_USERID_UNKNOWN = 0xFFFFFFFF
};
int flux_msg_set_userid (flux_msg_t *msg, uint32_t userid);
int flux_msg_get_userid (const flux_msg_t *msg, uint32_t *userid);

/* Get/set rolemask
 */
enum {
    FLUX_ROLE_NONE = 0,
    FLUX_ROLE_OWNER = 1,
    FLUX_ROLE_USER = 2,
    FLUX_ROLE_LOCAL = 4,
    FLUX_ROLE_ALL = 0xFFFFFFFF,
};
int flux_msg_set_rolemask (flux_msg_t *msg, uint32_t rolemask);
int flux_msg_get_rolemask (const flux_msg_t *msg, uint32_t *rolemask);

/* Combined rolemask, userid access for convenience
 */
struct flux_msg_cred {
    uint32_t userid;
    uint32_t rolemask;
};
int flux_msg_get_cred (const flux_msg_t *msg, struct flux_msg_cred *cred);
int flux_msg_set_cred (flux_msg_t *msg, struct flux_msg_cred cred);

/* Simple authorization for service access:
 * If cred rolemask includes OWNER, grant (return 0).
 * If cred rolemask includes USER and userid matches 'userid',
 * and userid is not FLUX_USERID_UNKNOWN, grant (return 0).
 * Otherwise deny (return -1, errno = EPERM).
 */
int flux_msg_cred_authorize (struct flux_msg_cred cred, uint32_t userid);

/* Convenience function that calls
 * flux_msg_get_cred() + flux_msg_cred_authorize().
 */
int flux_msg_authorize (const flux_msg_t *msg, uint32_t userid);

/* Return true if 'msg' credential carries FLUX_ROLE_LOCAL, indicating
 * that the message has not traversed brokers.
 */
bool flux_msg_is_local (const flux_msg_t *msg);

/* Get/set errnum (response only)
 */
int flux_msg_set_errnum (flux_msg_t *msg, int errnum);
int flux_msg_get_errnum (const flux_msg_t *msg, int *errnum);

/* Get/set sequence number (event only)
 */
int flux_msg_set_seq (flux_msg_t *msg, uint32_t seq);
int flux_msg_get_seq (const flux_msg_t *msg, uint32_t *seq);

/* Get/set type, status (control only)
 */
int flux_msg_set_control (flux_msg_t *msg, int type, int status);
int flux_msg_get_control (const flux_msg_t *msg, int *type, int *status);

/* Get/set/compare match tag (request/response only)
 */
enum {
    FLUX_MATCHTAG_NONE = 0,
};
int flux_msg_set_matchtag (flux_msg_t *msg, uint32_t matchtag);
int flux_msg_get_matchtag (const flux_msg_t *msg, uint32_t *matchtag);
bool flux_msg_cmp_matchtag (const flux_msg_t *msg, uint32_t matchtag);

/* Match a message.
 */
bool flux_msg_cmp (const flux_msg_t *msg, struct flux_match match);

/* Print a Flux message on specified output stream.
 */
void flux_msg_fprint (FILE *f, const flux_msg_t *msg);
void flux_msg_fprint_ts (FILE *f, const flux_msg_t *msg, double timestamp);

/* Convert a numeric FLUX_MSGTYPE value to string,
 * or "unknown" if unrecognized.
 */
const char *flux_msg_typestr (int type);

/* NOTE: routing frames are pushed on a message traveling dealer
 * to router, and popped off a message traveling router to dealer.
 * A message intended for dealer-router sockets must first be enabled for
 * routing.
 */

/* Enable routes on a message by setting FLUX_MSGFLAG_ROUTE.  This
 * function is a no-op if the flag is already set.
 */
void flux_msg_route_enable (flux_msg_t *msg);

/* Disable routes on a message by clearing the FLUX_MSGFLAG_ROUTE
 * flag.  In addition, clear all presently stored routes.  This
 * function is a no-op if the flag is already set.
 */
void flux_msg_route_disable (flux_msg_t *msg);

/* Clear all routes stored in a message.  This function is a no-op if
 * routes are not enabled.
 */
void flux_msg_route_clear (flux_msg_t *msg);

/* Push a route frame onto the message (mimic what dealer socket does).
 * 'id' is copied internally.
 * Returns 0 on success, -1 with errno set (e.g. EINVAL) on failure.
 */
int flux_msg_route_push (flux_msg_t *msg, const char *id);

/* Delete last route frame off the message.  Effectively performs the
 * "opposite" of flux_msg_route_push().
 *
 * Returns 0 on success, -1 with errno set (e.g. EPROTO) on failure.
 */
int flux_msg_route_delete_last (flux_msg_t *msg);

/* Return the first route (e.g. first pushed route) or NULL if there
 * are no routes.
 * For requests, this is the sender; for responses, this is the recipient.
 * Returns route id on success, NULL for no route or error.
 */
const char *flux_msg_route_first (const flux_msg_t *msg);

/* Return the last route (e.g. most recent pushed route) or NULL if there
 * are no routes.
 * For requests, this is the last hop; for responses: this is the next hop.
 * Returns route id on success, NULL for no route or error.
 */
const char *flux_msg_route_last (const flux_msg_t *msg);

/* Return the number of route frames in the message.
 * It is an EPROTO error if there is no route stack.
 * Returns 0 on success, -1 with errno set (e.g. EPROTO) on failure.
 */
int flux_msg_route_count (const flux_msg_t *msg);

/* Return a string representing the route stack in message.
 * Return NULL if routes are not enabled; empty string if
 * the route stack contains no route frames).
 * Caller must free the returned string.
 */
char *flux_msg_route_string (const flux_msg_t *msg);

/* Return true if messages have the same first routing frame.
 * (For requests, the sender)
 */
bool flux_msg_route_match_first (const flux_msg_t *msg1,
                                 const flux_msg_t *msg2);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_MESSAGE_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */

/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_HANDLE_H
#define _FLUX_CORE_HANDLE_H


#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int request_tx;
    int request_rx;
    int response_tx;
    int response_rx;
    int event_tx;
    int event_rx;
    int control_tx;
    int control_rx;
} flux_msgcounters_t;

typedef int (*flux_comms_error_f)(flux_t *h, void *arg);

/* Flags for handle creation and flux_flags_set()/flux_flags_unset.
 */
enum {
    FLUX_O_TRACE = 1,       /* send message trace to stderr */
    FLUX_O_CLONE = 2,       /* handle was created with flux_clone() */
    FLUX_O_NONBLOCK = 4,    /* handle should not block on send/recv */
    FLUX_O_MATCHDEBUG = 8,  /* enable matchtag debugging */
    FLUX_O_TEST_NOSUB = 16, /* for testing: make (un)subscribe a no-op */
    FLUX_O_RPCTRACK = 32,   /* track RPCs for recovery after reconnect */
    FLUX_O_NOREQUEUE = 64,  /* disable flux_requeue() to save file descr. */
};

/* Flags for flux_requeue().
 */
enum {
    FLUX_RQ_HEAD = 1,   /* requeue message at head of queue */
    FLUX_RQ_TAIL = 2,   /* requeue message at tail of queue */
};

/* Flags for flux_pollevents().
 */
enum {
    FLUX_POLLIN = 1,
    FLUX_POLLOUT = 2,
    FLUX_POLLERR = 4,
};

/* Options for flux_opt_set().
 * (Connectors may define custom option names)
 */
#define FLUX_OPT_TESTING_USERID     "flux::testing_userid"
#define FLUX_OPT_TESTING_ROLEMASK   "flux::testing_rolemask"
#define FLUX_OPT_ROUTER_NAME        "flux::router_name"
#define FLUX_OPT_SEND_QUEUE_COUNT   "flux::send_queue_count"
#define FLUX_OPT_RECV_QUEUE_COUNT   "flux::recv_queue_count"

/* Create/destroy a broker handle.
 * The 'uri' scheme name selects a connector to dynamically load.
 * The rest of the URI is parsed in an connector-specific manner.
 * A NULL uri selects the "local" connector with path stored
 * in the environment variable FLUX_URI.
 */
flux_t *flux_open (const char *uri, int flags);

/* Like flux_open(), but if optional flux_error_t parameter is non-NULL,
 * then any errors normally emitted to stderr will instead be returned
 * in error->text.
 */
flux_t *flux_open_ex (const char *uri, int flags, flux_error_t *error);

void flux_close (flux_t *h);

/* Increment internal reference count on 'h'.
 */
flux_t *flux_incref (flux_t *h);
void flux_decref(flux_t *h);

/* Create a new handle that is an alias for 'orig' in all respects
 * except it adds FLUX_O_CLONE to flags and has its own 'aux' hash
 * (which means it has its own reactor and dispatcher).
 */
flux_t *flux_clone (flux_t *orig);

/* Get/set the reactor associated with the handle.
 * A reactor is created with flags=0 if 'get' is called before one is set.
 * 'set' fails if there is already a reactor.
 */
flux_reactor_t *flux_get_reactor (flux_t *h);
int flux_set_reactor (flux_t *h, flux_reactor_t *r);

/* Drop connection to broker and re-establish, if supported by connector.
 */
int flux_reconnect (flux_t *h);

/* Get/set handle options.  Options are interpreted by connectors.
 * Returns 0 on success, or -1 on failure with errno set (e.g. EINVAL).
 */
int flux_opt_set (flux_t *h, const char *option, const void *val, size_t len);
int flux_opt_get (flux_t *h, const char *option, void *val, size_t len);

/* Register a callback to flux_send() / flux_recv() errors.
 * The callback return value becomes the send/receive function return value.
 */
void flux_comms_error_set (flux_t *h, flux_comms_error_f fun, void *arg);

/* A mechanism is provide for users to attach auxiliary state to the flux_t
 * handle by name.  The destructor, if non-NULL, will be called
 * to destroy this state when the handle is destroyed.
 * Key names used internally by flux-core are prefixed with "flux::".
 *
 * N.B. flux_aux_get does not scale to a large number of items, and
 * broker module handles may persist for a long time.
 */
void *flux_aux_get (flux_t *h, const char *name);
int flux_aux_set (flux_t *h, const char *name, void *aux, flux_free_f destroy);

/* Set/clear FLUX_O_* on a flux_t handle.
 */
void flux_flags_set (flux_t *h, int flags);
void flux_flags_unset (flux_t *h, int flags);
int flux_flags_get (flux_t *h);

/* Alloc/free matchtag for matched request/response.
 * This is mainly used internally by the rpc code.
 */
uint32_t flux_matchtag_alloc (flux_t *h);
void flux_matchtag_free (flux_t *h, uint32_t matchtag);
uint32_t flux_matchtag_avail (flux_t *h);

/* Send a message
 * flags may be 0 or FLUX_O_TRACE or FLUX_O_NONBLOCK (FLUX_O_COPROC is ignored)
 * Returns 0 on success, -1 on failure with errno set.
 */
int flux_send (flux_t *h, const flux_msg_t *msg, int flags);

/* Send a message - same as above but '*msg' ownership is transferred to 'h'.
 * N.B. this fails with EINVAL if '*msg' reference count is greater than 1.
 */
int flux_send_new (flux_t *h, flux_msg_t **msg, int flags);

/* Receive a message
 * flags may be 0 or FLUX_O_TRACE or FLUX_O_NONBLOCK (FLUX_O_COPROC is ignored)
 * flux_recv reads messages from the handle until 'match' is matched,
 * then requeues any non-matching messages.
 * Returns message on success, NULL on failure.
 * The message must be destroyed with flux_msg_destroy().
 */
flux_msg_t *flux_recv (flux_t *h, struct flux_match match, int flags);

/* Requeue a message
 * flags must be either FLUX_RQ_HEAD or FLUX_RQ_TAIL.
 * A message that is requeued will be seen again by flux_recv() and will
 * cause FLUX_POLLIN to be raised in flux_pollevents().
 */
int flux_requeue (flux_t *h, const flux_msg_t *msg, int flags);

/* Obtain a bitmask of FLUX_POLL* bits for the flux handle.
 * Returns bitmask on success, -1 on error with errno set.
 * See flux_pollfd() comment below.
 */
int flux_pollevents (flux_t *h);

/* Obtain a file descriptor that can be used to integrate a flux_t handle
 * into an external event loop.  When one of FLUX_POLLIN, FLUX_POLLOUT, or
 * FLUX_POLLERR is raised in flux_pollevents(), this file descriptor will
 * become readable in an edge triggered fashion.  The external event loop
 * should then call flux_pollevents().  See src/common/libflux/ev_flux.[ch]
 * for an example of a libev "composite watcher" based on these interfaces,
 * that is used internally by the flux reactor.
 * Returns fd on success, -1 on failure with errno set.
 */
int flux_pollfd (flux_t *h);

/* Get/clear handle message counters.
 */
void flux_get_msgcounters (flux_t *h, flux_msgcounters_t *mcs);
void flux_clr_msgcounters (flux_t *h);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_HANDLE_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_REACTOR_H
#define _FLUX_CORE_REACTOR_H


#ifdef __cplusplus
extern "C" {
#endif

/* Flags for flux_reactor_run()
 */
enum {
    FLUX_REACTOR_NOWAIT = 1,  /* run loop once without blocking */
    FLUX_REACTOR_ONCE = 2,    /* same as above but block until at least */
                              /*     one event occurs */
};

flux_reactor_t *flux_reactor_create (int flags);
void flux_reactor_destroy (flux_reactor_t *r);
void flux_reactor_incref (flux_reactor_t *r);
void flux_reactor_decref (flux_reactor_t *r);

int flux_reactor_run (flux_reactor_t *r, int flags);

void flux_reactor_stop (flux_reactor_t *r);
void flux_reactor_stop_error (flux_reactor_t *r);

double flux_reactor_now (flux_reactor_t *r);
void flux_reactor_now_update (flux_reactor_t *r);
double flux_reactor_time (void);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_REACTOR_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_WATCHER_H
#define _FLUX_CORE_WATCHER_H


#ifdef __cplusplus
extern "C" {
#endif

typedef void (*flux_watcher_f)(flux_reactor_t *r,
                               flux_watcher_t *w,
                               int revents,
                               void *arg);

/* Set the watcher priority.  The range is [-2:2] (default 0).
 * Higher priority watchers run first.
 * This is a no-op if the underlying watcher doesn't support it.
 * If the priority is out of range, the max or min value is set.
 * The priority should only be set when the watcher is stopped.
 * Currently only the check watcher supports it.
 */
void flux_watcher_set_priority (flux_watcher_t *w, int priority);

void flux_watcher_start (flux_watcher_t *w);
void flux_watcher_stop (flux_watcher_t *w);
void flux_watcher_ref (flux_watcher_t *w);
void flux_watcher_unref (flux_watcher_t *w);
void flux_watcher_destroy (flux_watcher_t *w);
double flux_watcher_next_wakeup (flux_watcher_t *w);
bool flux_watcher_is_active (flux_watcher_t *w);
bool flux_watcher_is_referenced (flux_watcher_t *w);

/* flux_t handle
 */

flux_watcher_t *flux_handle_watcher_create (flux_reactor_t *r,
                                            flux_t *h,
                                            int events,
                                            flux_watcher_f cb,
                                            void *arg);
flux_t *flux_handle_watcher_get_flux (flux_watcher_t *w);

/* file descriptor
 */

flux_watcher_t *flux_fd_watcher_create (flux_reactor_t *r,
                                        int fd, int events,
                                        flux_watcher_f cb,
                                        void *arg);
int flux_fd_watcher_get_fd (flux_watcher_t *w);

/* timer
 */

flux_watcher_t *flux_timer_watcher_create (flux_reactor_t *r,
                                           double after,
                                           double repeat,
                                           flux_watcher_f cb,
                                           void *arg);

void flux_timer_watcher_reset (flux_watcher_t *w, double after, double repeat);

void flux_timer_watcher_again (flux_watcher_t *w);

/* periodic
 */

typedef double (*flux_reschedule_f) (flux_watcher_t *w, double now, void *arg);

flux_watcher_t *flux_periodic_watcher_create (flux_reactor_t *r,
                                             double offset,
                                             double interval,
                                             flux_reschedule_f reschedule_cb,
                                             flux_watcher_f cb,
                                             void *arg);

void flux_periodic_watcher_reset (flux_watcher_t *w,
                                  double next_wakeup,
                                  double interval,
                                  flux_reschedule_f reschedule_cb);


/* prepare/check/idle
 */

flux_watcher_t *flux_prepare_watcher_create (flux_reactor_t *r,
                                             flux_watcher_f cb,
                                             void *arg);

flux_watcher_t *flux_check_watcher_create (flux_reactor_t *r,
                                           flux_watcher_f cb,
                                           void *arg);

flux_watcher_t *flux_idle_watcher_create (flux_reactor_t *r,
                                          flux_watcher_f cb,
                                          void *arg);

/* signal
 */

flux_watcher_t *flux_signal_watcher_create (flux_reactor_t *r,
                                            int signum,
                                            flux_watcher_f cb,
                                            void *arg);

int flux_signal_watcher_get_signum (flux_watcher_t *w);

/* stat
 */

flux_watcher_t *flux_stat_watcher_create (flux_reactor_t *r,
                                          const char *path,
                                          double interval,
                                          flux_watcher_f cb,
                                          void *arg);
int flux_stat_watcher_get_rstat (flux_watcher_t *w,
                                 struct stat *stat,
                                 struct stat *prev);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_WATCHER_H */

// vi:ts=4 sw=4 expandtab
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_MSG_HANDLER_H
#define _FLUX_CORE_MSG_HANDLER_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct flux_msg_handler flux_msg_handler_t;

typedef void (*flux_msg_handler_f)(flux_t *h, flux_msg_handler_t *mh,
                                   const flux_msg_t *msg, void *arg);

flux_msg_handler_t *flux_msg_handler_create (flux_t *h,
                                             const struct flux_match match,
                                             flux_msg_handler_f cb, void *arg);

void flux_msg_handler_destroy (flux_msg_handler_t *mh);

void flux_msg_handler_start (flux_msg_handler_t *mh);
void flux_msg_handler_stop (flux_msg_handler_t *mh);

/* By default, only messages from FLUX_ROLE_OWNER are delivered to handler.
 * Use _allow_rolemask() add roles, _deny_rolemask() to remove them.
 * (N.B. FLUX_ROLE_OWNER cannot be denied)
 */
void flux_msg_handler_allow_rolemask (flux_msg_handler_t *mh,
                                      uint32_t rolemask);
void flux_msg_handler_deny_rolemask (flux_msg_handler_t *mh,
                                     uint32_t rolemask);

struct flux_msg_handler_spec {
    int typemask;
    const char *topic_glob;
    flux_msg_handler_f cb;
    uint32_t rolemask;
};
#define FLUX_MSGHANDLER_TABLE_END { 0, NULL, NULL, 0 }

int flux_msg_handler_addvec_ex (flux_t *h,
                                const char *service_name,
                                const struct flux_msg_handler_spec tab[],
                                void *arg,
                                flux_msg_handler_t **hp[]);

int flux_msg_handler_addvec (flux_t *h,
                             const struct flux_msg_handler_spec tab[],
                             void *arg,
                             flux_msg_handler_t **msg_handlers[]);
void flux_msg_handler_delvec (flux_msg_handler_t *msg_handlers[]);

/* Requeue any unmatched messages, if handle was cloned.
 */
int flux_dispatch_requeue (flux_t *h);

// accessor for start/stop/ref/unref
flux_watcher_t *flux_get_handle_watcher (flux_t *h);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_MSG_HANDLER_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_CONNECTOR_H
#define _FLUX_CORE_CONNECTOR_H

#ifdef __cplusplus
extern "C" {
#endif

/**
 ** Only handle implementation stuff below.
 ** Flux_t handle users should not use these interfaces.
 */
typedef flux_t *(connector_init_f)(const char *uri,
                                   int flags,
                                   flux_error_t *errp);

struct flux_handle_ops {
    int         (*setopt)(void *impl,
                          const char *option,
                          const void *val,
                          size_t len);
    int         (*getopt)(void *impl,
                          const char *option,
                          void *val,
                          size_t len);
    int         (*pollfd)(void *impl);
    int         (*pollevents)(void *impl);
    int         (*send)(void *impl, const flux_msg_t *msg, int flags);
    flux_msg_t* (*recv)(void *impl, int flags);
    int         (*reconnect)(void *impl);

    void        (*impl_destroy)(void *impl);

    // added in v0.56.0
    int         (*send_new)(void *impl, flux_msg_t **msg, int flags);

    // added in v0.56.0
    void        *_pad[4]; // reserved for future use
};

flux_t *flux_handle_create (void *impl,
                            const struct flux_handle_ops *ops,
                            int flags);
void flux_handle_destroy (flux_t *hp);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_CONNECTOR_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2021 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_MSGLIST_H
#define _FLUX_CORE_MSGLIST_H

#ifdef __cplusplus
extern "C" {
#endif

/* message lists
 * - takes a ref on 'msg' upon append
 * - drops ref on 'msg' on delete / list destroy
 */
struct flux_msglist *flux_msglist_create (void);
void flux_msglist_destroy (struct flux_msglist *l);

int flux_msglist_push (struct flux_msglist *l, const flux_msg_t *msg);
int flux_msglist_append (struct flux_msglist *l, const flux_msg_t *msg);
void flux_msglist_delete (struct flux_msglist *l); // (at cursor) iteration safe
const flux_msg_t *flux_msglist_pop (struct flux_msglist *l);

const flux_msg_t *flux_msglist_first (struct flux_msglist *l);
const flux_msg_t *flux_msglist_next (struct flux_msglist *l);
const flux_msg_t *flux_msglist_last (struct flux_msglist *l);

int flux_msglist_count (struct flux_msglist *l);

/* These functions are for integration of flux_msglist into an event loop.
 * The pollfd file descriptor becomes readable when a poll event has been
 * raised (edge triggered).  This indicates that the pollevents mask has been
 * updated.  The mask cnosists of POLLIN | POLLOUT | POLLERR.  N.B. POLLOUT
 * is always ready in the current implementation.
 * Both functions return -1 on error with errno set.
 */
int flux_msglist_pollevents (struct flux_msglist *l);
int flux_msglist_pollfd (struct flux_msglist *l);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_MSGLIST_H */

/*
 * vi:ts=4 sw=4 expandtab
 */

/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_REQUEST_H
#define _FLUX_CORE_REQUEST_H

#ifdef __cplusplus
extern "C" {
#endif

/* Decode a request message with optional string payload.
 * If topic is non-NULL, assign the request topic string.
 * If s is non-NULL, assign the string payload or set to NULL if none
 * exists.  Returns 0 on success, or -1 on failure with errno set.
 */
int flux_request_decode (const flux_msg_t *msg,
                         const char **topic,
                         const char **s);

/* Decode a request message with required json payload.  These functions use
 * jansson unpack style variable arguments for decoding the JSON object
 * payload directly.  Returns 0 on success, or -1 on failure with errno set.
 */
int flux_request_unpack (const flux_msg_t *msg,
                         const char **topic,
                         const char *fmt,
                         ...);

/* Decode a request message with optional raw payload.
 * If topic is non-NULL, assign the request topic string.
 * Data and len must be non-NULL, and will be assigned the payload.
 * If there is no payload, they will be assigned NULL and zero.
 * Returns 0 on success, or -1 on failure with errno set.
 */
int flux_request_decode_raw (const flux_msg_t *msg,
                             const char **topic,
                             const void **data,
                             size_t *len);

/* Encode a request message with optional string payload.
 * If s is non-NULL, assign the string payload.
 */
flux_msg_t *flux_request_encode (const char *topic, const char *s);

/* Encode a request message with optional raw payload.
 * If data is non-NULL, assign the raw payload.
 * Otherwise there will be no payload.
 */
flux_msg_t *flux_request_encode_raw (const char *topic,
                                     const void *data,
                                     size_t len);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_REQUEST_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_RESPONSE_H
#define _FLUX_CORE_RESPONSE_H

#ifdef __cplusplus
extern "C" {
#endif

/* Decode a response message, with optional string payload.
 * If topic is non-NULL, assign the response topic string.
 * If s is non-NULL, assign the string payload if one exists or set to
 * NULL is none exists.  If response includes a nonzero errnum, errno
 * is set to the errnum value and -1 is returned with no assignments
 * to topic or s.  Returns 0 on success, or -1 on failure with
 * errno set.
 */
int flux_response_decode (const flux_msg_t *msg,
                          const char **topic,
                          const char **s);

/* Decode a response message, with optional raw payload.
 * If topic is non-NULL, assign the response topic string.
 * Data and len must be non-NULL and will be assigned the payload and length.
 * If there is no payload, they will be assigned NULL and zero.
 * If response includes a nonzero errnum, errno is set to the errnum value
 * and -1 is returned with no assignments to topic, data, or len.
 * Returns 0 on success, or -1 on failure with errno set.
 */
int flux_response_decode_raw (const flux_msg_t *msg,
                              const char **topic,
                              const void **data,
                              size_t *len);

/* If failed response includes an error string payload, assign to 'errstr',
 * otherwise fail.
 * Returns 0 on success, or -1 on failure with errno set.
 */
int flux_response_decode_error (const flux_msg_t *msg, const char **errstr);


/* Encode a message with optional string payload 's'.
 */
flux_msg_t *flux_response_encode (const char *topic, const char *s);

/* Encode a response message with optional raw payload.
 */
flux_msg_t *flux_response_encode_raw (const char *topic,
                                      const void *data,
                                      size_t len);

/* Encode an error response with 'errnum' (must be nonzero) and
 * if non-NULL, an error string payload.
 */
flux_msg_t *flux_response_encode_error (const char *topic,
                                        int errnum,
                                        const char *errstr);

/* Derive a response message from a request message, setting 'errnum' to
 * the specified value (0 = success).
 */
flux_msg_t *flux_response_derive (const flux_msg_t *request, int errnum);

/* Create a response to the provided request message with optional
 * string payload.
 */
int flux_respond (flux_t *h, const flux_msg_t *request, const char *s);

/* Create a response to the provided request message with json payload, using
 * jansson pack style variable arguments for encoding the JSON object
 * payload directly.
 */
int flux_respond_pack (flux_t *h,
                       const flux_msg_t *request,
                       const char *fmt,
                       ...);


/* Create a response to the provided request message with optional raw payload.
 */
int flux_respond_raw (flux_t *h,
                      const flux_msg_t *request,
                      const void *data,
                      int len);

/* Create an error response to the provided request message with optional
 * error string payload (if errstr is non-NULL).  If errnum is zero, EINVAL
 * is substituted.
 */
int flux_respond_error (flux_t *h,
                        const flux_msg_t *request,
                        int errnum,
                        const char *errstr);


#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_RESPONSE_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2016 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_CONTROL_H
#define _FLUX_CORE_CONTROL_H

#ifdef __cplusplus
extern "C" {
#endif

flux_msg_t *flux_control_encode (int type, int status);

int flux_control_decode (const flux_msg_t *msg, int *type, int *status);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_CONTROL_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_RPC_H
#define _FLUX_CORE_RPC_H

#ifdef __cplusplus
extern "C" {
#endif

enum {
    FLUX_RPC_NORESPONSE = 1,
    FLUX_RPC_STREAMING = 2,
};

flux_future_t *flux_rpc (flux_t *h,
                         const char *topic,
                         const char *s,
                         uint32_t nodeid,
                         int flags);

flux_future_t *flux_rpc_pack (flux_t *h,
                              const char *topic,
                              uint32_t nodeid,
                              int flags,
                              const char *fmt,
                              ...);

flux_future_t *flux_rpc_vpack (flux_t *h,
                               const char *topic,
                               uint32_t nodeid,
                               int flags,
                               const char *fmt,
                               va_list ap);

flux_future_t *flux_rpc_raw (flux_t *h,
                             const char *topic,
                             const void *data,
                             size_t len,
                             uint32_t nodeid,
                             int flags);

flux_future_t *flux_rpc_message (flux_t *h,
                                 const flux_msg_t *msg,
                                 uint32_t nodeid,
                                 int flags);

int flux_rpc_get (flux_future_t *f, const char **s);

int flux_rpc_get_unpack (flux_future_t *f, const char *fmt, ...);

int flux_rpc_get_raw (flux_future_t *f, const void **data, size_t *len);

/* Accessor for RPC matchtag (see RFC 6).
 */
uint32_t flux_rpc_get_matchtag (flux_future_t *f);

/* Accessor for original nodeid target of flux_rpc()
 */
uint32_t flux_rpc_get_nodeid (flux_future_t *f);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_RPC_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_EVENT_H
#define _FLUX_CORE_EVENT_H

#ifdef __cplusplus
extern "C" {
#endif

enum event_flags {
    FLUX_EVENT_PRIVATE = 1,
};

/* Event subscribe/unsubscribe.
 */
int flux_event_subscribe (flux_t *h, const char *topic);
int flux_event_unsubscribe (flux_t *h, const char *topic);
flux_future_t *flux_event_subscribe_ex (flux_t *h,
                                        const char *topic,
                                        int flags);
flux_future_t *flux_event_unsubscribe_ex (flux_t *h,
                                          const char *topic,
                                          int flags);

/* Decode an event message with optional string payload.
 * If topic is non-NULL, assign the event topic string.
 * If s is non-NULL, assign string payload or set to NULL if none
 * exists.  Returns 0 on success, or -1 on failure with errno set.
 */
int flux_event_decode (const flux_msg_t *msg,
                       const char **topic,
                       const char **s);

/* Decode an event message with required JSON payload.  These functions use
 * jansson unpack style variable arguments for decoding the JSON object
 * payload directly.  Returns 0 on success, or -1 on failure with errno set.
 */
int flux_event_unpack (const flux_msg_t *msg,
                       const char **topic,
                       const char *fmt, ...);

/* Encode an event message with optional string payload.
 * If s is non-NULL, it is copied to the message payload.
 * Returns message or NULL on failure with errno set.
 */
flux_msg_t *flux_event_encode (const char *topic, const char *s);

/* Encode an event message with JSON payload.  These functions use
 * jansson pack style variable arguments for encoding the JSON object
 * payload directly.  Returns message or NULL on failure with errno set.
 */
flux_msg_t *flux_event_pack (const char *topic, const char *fmt, ...);

/* Encode an event message with raw payload.
 */
flux_msg_t *flux_event_encode_raw (const char *topic,
                                   const void *data,
                                   size_t len);

/* Decode an event message, with optional raw payload.
 * If topic is non-NULL, assign the event topic string.
 * Data and len must be non-NULL and will be assigned the payload and length.
 * If there is no payload, they will be assigned NULL and zero.
 * Returns 0 on success, or -1 on failure with errno set.
 */
int flux_event_decode_raw (const flux_msg_t *msg,
                           const char **topic,
                           const void **data,
                           size_t *len);

/* Publish an event with optional string payload.
 * The future is fulfilled once the event has been assigned a sequence number,
 * and does not indicate that the event has yet reached all subscribers.
 */
flux_future_t *flux_event_publish (flux_t *h,
                                   const char *topic,
                                   int flags,
                                   const char *s);

/* Publish an event with JSON payload.
 */
flux_future_t *flux_event_publish_pack (flux_t *h,
                                        const char *topic,
                                        int flags,
                                        const char *fmt,
                                        ...);

/* Publish an event with optional raw payload.
 */
flux_future_t *flux_event_publish_raw (flux_t *h,
                                       const char *topic,
                                       int flags,
                                       const void *data,
                                       size_t len);

/* Obtain the event sequence number from the fulfilled
 * flux_event_publish() future.
 */
int flux_event_publish_get_seq (flux_future_t *f, int *seq);

#ifdef __cplusplus
}
#endif

#endif /* !FLUX_CORE_EVENT_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_MODULE_H
#define _FLUX_CORE_MODULE_H


#ifdef __cplusplus
extern "C" {
#endif

/* Module states, for embedding in keepalive messages (rfc 5)
 */
enum {
    FLUX_MODSTATE_INIT           = 0,
    FLUX_MODSTATE_RUNNING        = 1,
    FLUX_MODSTATE_FINALIZING     = 2,
    FLUX_MODSTATE_EXITED         = 3,
};

/* Mandatory symbols for modules
 */
#define MOD_NAME(x) const char *mod_name = x
typedef int (mod_main_f)(flux_t *h, int argc, char *argv[]);

/* Test and optionally clear module debug bit from within a module, as
 * described in RFC 5.  Return true if 'flag' bit is set.  If clear=true,
 * clear the bit after testing.  The flux-module(1) debug subcommand
 * manipulates these bits externally to set up test conditions.
 */
bool flux_module_debug_test (flux_t *h, int flag, bool clear);

/* Set module state to RUNNING.  This transition occurs automatically when the
 * reactor is entered, but this function can set the state to RUNNING early,
 * e.g. if flux module load must complete before the module enters the reactor.
 * Returns 0 on success, -1 on error with errno set.
 */
int flux_module_set_running (flux_t *h);

#ifdef __cplusplus
}
#endif

#endif /* !FLUX_CORE_MODULE_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_ATTR_H
#define _FLUX_CORE_ATTR_H

/* broker attributes
 *
 * Brokers have configuration attributes.
 * Values are local to a particular broker rank.
 * Some may be overridden on the broker command line with -Sattr=val.
 * The following commands are available for manipulating attributes
 * on the running system:
 *   flux lsattr [-v]
 *   flux setattr name value
 *   flux getattr name
 * In addition, the following functions may be used to get/set broker
 * attributes programmatically.
 */

#ifdef __cplusplus
extern "C" {
#endif

/* Get the value for attribute 'name' from the local broker.
 * Returns value on success, NULL on failure with errno set.
 * This function performs a synchronous RPC to the broker if the
 * attribute is not found in cache, thus may block for the round-trip
 * communication.
 */
const char *flux_attr_get (flux_t *h, const char *name);

/* Set the value for attribute 'name' from the local broker.
 * Returns value on success, NULL on failure with errno set.
 * This function performs a synchronous RPC to the broker,
 * thus blocks for the round-trip communication.
 */
int flux_attr_set (flux_t *h, const char *name, const char *val);

/* hotwire flux_attr_get()'s cache for testing */
int flux_attr_set_cacheonly (flux_t *h, const char *name, const char *val);

/* Iterate over the attribute names that are stored in the local
 * attribute cache.
 */
const char *flux_attr_cache_first (flux_t *h);
const char *flux_attr_cache_next (flux_t *h);

/* Get "rank" attribute, and convert to an unsigned integer.
 * Returns 0 on success, or -1 on failure with errno set.
 */
int flux_get_rank (flux_t *h, uint32_t *rank);

/* Get "size" attribute, and convert to an unsigned integer.
 * Returns 0 on success, or -1 on failure with errno set.
 */
int flux_get_size (flux_t *h, uint32_t *size);

/* Look up hostname of broker rank, by consulting "hostlist" attribute.
 * This function always returns a printable string, though it may be "(null)".
 */
const char *flux_get_hostbyrank (flux_t *h, uint32_t rank);

/* Find the lowest numbered broker rank running on 'host', by consulting
 * the "hostlist" attribute.
 * Returns rank on success, -1 on failure with errno set.
 */
int flux_get_rankbyhost (flux_t *h, const char *host);

/* Return a list/set of hosts/ranks in Hostlist/Idset form given 'targets'
 * in Idset/Hostlist form. Caller must free returned value.
 *
 * Returns NULL on failure with error message in errp->text (if errp != NULL).
 *
 * NOTES:
 *  - The source of the mapping is the rank-ordered broker 'hostlist' attribute.
 *  - An Idset (RFC 22) is a set (unordered, no duplicates)
 *  - A Hostlist (RFC 29) is a list (ordered, may be duplicates)
 *  - If there are multiple ranks per host, this function can only map
 *    hostnames to the first rank found on the host.
 *
 */
char *flux_hostmap_lookup (flux_t *h,
                           const char *targets,
                           flux_error_t *errp);

/* Look up the broker.starttime attribute on rank 0.
 * The instance uptime is flux_reactor_now() - starttime.
 * N.B. if the instance has been restarted, this value is the most
 * recent restart time.
 */
int flux_get_instance_starttime (flux_t *h, double *starttime);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_ATTR_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_FLOG_H
#define _FLUX_CORE_FLOG_H


#ifdef __cplusplus
extern "C" {
#endif

typedef void (*flux_log_f)(const char *buf, int len, void *arg);

/* Set log appname for handle instance.
 * Value will be truncated after FLUX_MAX_APPNAME bytes.
 */
void flux_log_set_appname (flux_t *h, const char *s);

/* Set log procid for handle instance.
 * Value will be truncated after FLUX_MAX_PROCID bytes.
 */
void flux_log_set_procid (flux_t *h, const char *s);

/* Log a message at the specified level, as defined for syslog(3).
 *
 * Flux handle is optional, if set to NULL output to stderr.
 */
int flux_vlog (flux_t *h, int level, const char *fmt, va_list ap);
int flux_log (flux_t *h, int level, const char *fmt, ...)
              __attribute__ ((format (printf, 3, 4)));

/* Log a message at LOG_ERR level, appending a colon, space, and error string.
 * The system 'errno' is assumed to be valid.
 *
 * Flux handle is optional, if set to NULL output to stderr.
 */
void flux_log_verror (flux_t *h, const char *fmt, va_list ap);
void flux_log_error (flux_t *h, const char *fmt, ...)
                 __attribute__ ((format (printf, 2, 3)));

#define FLUX_LOG_ERROR(h) \
    (void)flux_log_error ((h), "%s::%d[%s]", __FILE__, __LINE__, __FUNCTION__)

/* Redirect log messages to flux_log_f in this handle instance.
 */
void flux_log_set_redirect (flux_t *h, flux_log_f fun, void *arg);

/* Convert errno to string.
 * Flux errno space includes POSIX errno + zeromq errors.
 */
const char *flux_strerror (int errnum);

/* Flux log function compatible with libutil llog interface
 */
void flux_llog (void *arg,
                const char *file,
                int line,
                const char *func,
                const char *subsys,
                int level,
                const char *fmt,
                va_list ap);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_FLOG_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_CONF_H
#define _FLUX_CORE_CONF_H


#ifdef __cplusplus
extern "C" {
#endif

enum flux_conf_flags {
    FLUX_CONF_INSTALLED=0,
    FLUX_CONF_INTREE=1,
    FLUX_CONF_AUTO=2,
};

/* Retrieve builtin (compiled-in) configuration value by name.
 * If flags=INSTALLED, installed paths are used.
 * If flags=INTREE, source/build tree paths are used.
 * If flags=AUTO, a heuristic is employed internally to select paths.
 * This function returns NULL with errno=EINVAL on invalid name.
 */
const char *flux_conf_builtin_get (const char *name,
                                   enum flux_conf_flags flags);


typedef struct flux_conf flux_conf_t;

/* Create/copy/incref/decref config object
 */
flux_conf_t *flux_conf_create (void);
flux_conf_t *flux_conf_copy (const flux_conf_t *conf);
const flux_conf_t *flux_conf_incref (const flux_conf_t *conf);
void flux_conf_decref (const flux_conf_t *conf);

/* Decode config-reload request, setting 'conf' to a config object
 * owned by 'msg'.
 */
int flux_conf_reload_decode (const flux_msg_t *msg, const flux_conf_t **conf);

/* Parse TOML config in 'path' and return a new flux_conf_t on success.
 * If path is a directory, then parse all files matching *.toml in path.
 */
flux_conf_t *flux_conf_parse (const char *path, flux_error_t *error);

/* Get/set config object cached in flux_t handle, with destructor.
 * Re-setting the object decrefs the old one.
 */
const flux_conf_t *flux_get_conf (flux_t *h);
int flux_set_conf (flux_t *h, const flux_conf_t *conf);

/* Access config object.
 * If error is non-NULL, it is filled with error details on failure.
 */
int flux_conf_vunpack (const flux_conf_t *conf,
                       flux_error_t *error,
                       const char *fmt,
                       va_list ap);

int flux_conf_unpack (const flux_conf_t *conf,
                      flux_error_t *error,
                      const char *fmt,
                      ...);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_CONF_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2017 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_FUTURE_H
#define _FLUX_CORE_FUTURE_H

#ifdef __cplusplus
extern "C" {
#endif

/* Interfaces useful for all classes that return futures.
 * See flux_future_then(3).
 */

typedef void (*flux_continuation_f)(flux_future_t *f, void *arg);

int flux_future_then (flux_future_t *f,
                      double timeout,
                      flux_continuation_f cb,
                      void *arg);

int flux_future_wait_for (flux_future_t *f, double timeout);

bool flux_future_is_ready (flux_future_t *f);

void flux_future_reset (flux_future_t *f);

void flux_future_destroy (flux_future_t *f);

void *flux_future_aux_get (flux_future_t *f, const char *name);
int flux_future_aux_set (flux_future_t *f,
                         const char *name,
                         void *aux,
                         flux_free_f destroy);

/* Functions primarily used by implementors of classes that return futures.
 * See flux_future_create(3).
 */

typedef void (*flux_future_init_f)(flux_future_t *f, void *arg);

flux_future_t *flux_future_create (flux_future_init_f cb, void *arg);

int flux_future_get (flux_future_t *f, const void **result);

void flux_future_fulfill (flux_future_t *f, void *result, flux_free_f free_fn);
void flux_future_fulfill_error (flux_future_t *f,
                                int errnum,
                                const char *errstr);

int flux_future_fulfill_with (flux_future_t *f, flux_future_t *p);

void flux_future_fatal_error (flux_future_t *f, int errnum, const char *errstr);

/* Convenience macro */
#define future_strerror(__f, __errno) \
    (flux_future_has_error ((__f)) ? \
     flux_future_error_string ((__f)) : \
     flux_strerror ((__errno)))

bool flux_future_has_error (flux_future_t *f);
const char *flux_future_error_string (flux_future_t *f);

void flux_future_set_flux (flux_future_t *f, flux_t *h);
flux_t *flux_future_get_flux (flux_future_t *f);

void flux_future_set_reactor (flux_future_t *f, flux_reactor_t *r);
flux_reactor_t *flux_future_get_reactor (flux_future_t *f);

void flux_future_incref (flux_future_t *f);
void flux_future_decref (flux_future_t *f);

/* Composite future implementation
 */
flux_future_t *flux_future_wait_all_create (void);
flux_future_t *flux_future_wait_any_create (void);

int flux_future_push (flux_future_t *cf, const char *name, flux_future_t *f);

const char * flux_future_first_child (flux_future_t *cf);
const char * flux_future_next_child (flux_future_t *cf);

flux_future_t *flux_future_get_child (flux_future_t *cf, const char *name);

/* Future chaining
 */

/* Similar to flux_future_then(3), but return a future that can subsequently
 *  be "continued" from the continuation function `cb` via
 *  flux_future_continue(3) upon successful fulfillment of future `f`.
 *
 * The continuation `cb` is only called on success of future `f`. If `f`
 *  is fulfilled with an error, then that error is immediately passed
 *  to  future returned by this function, unless `flux_future_or_then(3)`
 *  has been used.
 */
flux_future_t *flux_future_and_then (flux_future_t *f,
                                     flux_continuation_f cb,
                                     void *arg);

/* Like flux_future_and_then(3), but run the continuation `cb` when
 *  future `f` is fulfilled with an error.
 */
flux_future_t *flux_future_or_then (flux_future_t *f,
                                    flux_continuation_f cb,
                                    void *arg);

/* Set the next future for the chained future `prev` to `f`.
 *  This function steals a reference to `f` and thus flux_future_destroy()
 *  should not be called on `f`. (However, flux_future_destroy() should
 *  still be called on `prev`)
 */
int flux_future_continue (flux_future_t *prev, flux_future_t *f);

/*  Set the next future for the chained future `prev` to be fulfilled
 *   with an error `errnum` and an optional error string.
 */
void flux_future_continue_error (flux_future_t *prev,
                                 int errnum,
                                 const char *errstr);

/*  Fulfill the next future in the chain immediately with a result.
 */
int flux_future_fulfill_next (flux_future_t *prev,
                              void *result,
                              flux_free_f free_fn);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_FUTURE_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_BARRIER_H
#define _FLUX_CORE_BARRIER_H

#ifdef __cplusplus
extern "C" {
#endif

/* Execute a barrier across 'nprocs' processes.
 * The 'name' must be unique across the Flux instance, or
 * if running in a Flux/slurm job, may be NULL.
 */
flux_future_t *flux_barrier (flux_t *h, const char *name, int nprocs);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_BARRIER_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2018 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_SERVICE_H
#define _FLUX_CORE_SERVICE_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 *  Register service `name` with the broker for this handle. On success
 *   request messages sent to "name.*" will be routed to this handle
 *   until `flux_service_unregister()` is called for `name`, or upon
 *   disconnect.
 *
 *  On success, the returned future will be fulfilled with no error, o/w
 *   the future is fulfilled with errnum set appropriately:
 *
 *   EINVAL - Invalid service name
 *   EEXIST - Service already registered under this name
 *   ENOENT - Unable to lookup route to requesting sender
 *
 */
flux_future_t *flux_service_register (flux_t *h, const char *name);

/*
 *  Unregister a previously registered service `name` for this handle.
 *
 *  On success, the returned future is fulfilled with no error, o/w
 *   the future is fulfilled with errnum set appropriately:
 *
 *  ENOENT - No such service registered as `name`
 *  EINVAL - Sender does not match current owner of service
 *
 */
flux_future_t *flux_service_unregister (flux_t *h, const char *name);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_SERVICE_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_VERSION_H
#define _FLUX_CORE_VERSION_H

#ifdef __cplusplus
extern "C" {
#endif

/* Flux uses semantic versioning: <major>.<minor>.<patch>
 */

/* The VERSION_STRING may include a "-N-hash" suffix from git describe
 * if this snapshot is not tagged.  This is not reflected in VERSION_PATCH.
 */
#define FLUX_CORE_VERSION_STRING    "0.73.0"
#define FLUX_CORE_VERSION_MAJOR     0
#define FLUX_CORE_VERSION_MINOR     73
#define FLUX_CORE_VERSION_PATCH     0

/* The version in 3 bytes, for numeric comparison.
 */
#define FLUX_CORE_VERSION_HEX       ((FLUX_CORE_VERSION_MAJOR << 16) | \
                                     (FLUX_CORE_VERSION_MINOR << 8) | \
                                     (FLUX_CORE_VERSION_PATCH << 0))


/* These functions return the compiled-in versions.
 * Useful for determining the version of dynamically linked libflux-core.
 */

/* Returns FLUX_CORE_VERSION_STRING.
 */
const char *flux_core_version_string (void);

/* If major is non-NULL set it to FLUX_CORE_VERSION_MAJOR.
 * If minor is non-NULL set it to FLUX_CORE_VERSION_MINOR.
 * If patch is non-NULL set it to FLUX_CORE_VERSION_PATCH.
 * Returns FLUX_CORE_VERSION_HEX.
 */
int flux_core_version (int *major, int *minor, int *patch);


#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_VERSION_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */

/************************************************************\
 * Copyright 2019 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef FLUX_CORE_PLUGIN_H
#define FLUX_CORE_PLUGIN_H

#ifdef __cplusplus
extern "C" {
#endif

enum {
    FLUX_PLUGIN_RTLD_LAZY =      1,  /* Lazy function binding                */
    FLUX_PLUGIN_RTLD_NOW =       2,  /* Immediate function binding           */
    FLUX_PLUGIN_RTLD_GLOBAL =    4,  /* Load with RTLD_GLOBAL                */
    FLUX_PLUGIN_RTLD_DEEPBIND =  8,  /* Load with RTLD_DEEPBIND if available */
};

typedef struct flux_plugin flux_plugin_t;
typedef struct flux_plugin_arg flux_plugin_arg_t;

typedef int (*flux_plugin_f) (flux_plugin_t *p,
                              const char *topic,
                              flux_plugin_arg_t *args,
                              void *data);

typedef int (*flux_plugin_init_f) (flux_plugin_t *p);

struct flux_plugin_handler {
    const char *topic;
    flux_plugin_f cb;
    void *data;
};

/*  Create and destroy a flux_plugin_t handle
 */
flux_plugin_t * flux_plugin_create (void);
void flux_plugin_destroy (flux_plugin_t *p);

/*  Get and set plugin flags. Flags currently only apply to load_dso()
 */
int flux_plugin_get_flags (flux_plugin_t *p);
int flux_plugin_set_flags (flux_plugin_t *p, int flags);

/*  Returns the last error from a plugin. Only valid if
 *   the last call returned an error.
 */
const char * flux_plugin_strerror (flux_plugin_t *p);

/*  Set a name for plugin 'p'. Overrides any existing name.
 */
int flux_plugin_set_name (flux_plugin_t *p, const char *name);

const char * flux_plugin_get_name (flux_plugin_t *p);

const char * flux_plugin_get_uuid (flux_plugin_t *p);

const char * flux_plugin_get_path (flux_plugin_t *p);

/*  Add a handler for topic 'topic' for the plugin 'p'.
 *  The topic string may be a glob to cause 'cb' to be invoked for
 *  a set of topic strings called by the host.
 */
int flux_plugin_add_handler (flux_plugin_t *p,
                             const char *topic,
                             flux_plugin_f cb,
                             void *arg);

/*  Remove handler associated with exact topic glob `topic`
 */
int flux_plugin_remove_handler (flux_plugin_t *p, const char *topic);

/*  Return handler that exactly matches topic glob `topic`.
 */
flux_plugin_f flux_plugin_get_handler (flux_plugin_t *p, const char *topic);

/*  Return handler that would match topic string `topic`, i.e. return
 *   the first handler in the list of handlers which would match topic
 *   string.
 */
flux_plugin_f flux_plugin_match_handler (flux_plugin_t *p, const char *topic);

/*  Convenience function to register a table of handlers along with
 *   a plugin name for the plugin 'p'.
 */
int flux_plugin_register (flux_plugin_t *p,
                          const char *name,
                          const struct flux_plugin_handler t[]);

/*  Associate auxiliary data with the plugin handle 'p'. If free_fn is
 *   set then this function will be called on the data at plugin
 *   destruction.
 *
 *  If key == NULL, val != NULL, stores val for destruction, but it
 *   cannot be retrieved with flux_plugin_aux_get ().
 *  If key != NULL, val == NULL, destroys currently stored val.
 *  For a duplicate key, current val is destroyed and new value stored.
 */
int flux_plugin_aux_set (flux_plugin_t *p,
                         const char *key,
                         void *val,
                         flux_free_f free_fn);

/*  Get current auxiliary data under `key`.
 */
void * flux_plugin_aux_get (flux_plugin_t *p, const char *key);

/*  Delete auxiliary data by value.
 */
void flux_plugin_aux_delete (flux_plugin_t *p, const void *val);

/*  Set optional JSON string as load-time config for plugin 'p'.
 */
int flux_plugin_set_conf (flux_plugin_t *p, const char *json_str);

/*  Get the current JSON string value of config for plugin 'p'.
 *  Returns NULL on failure.
 */
const char *flux_plugin_get_conf (flux_plugin_t *p);

/*  Read configuration for plugin 'p' using jansson style unpack args */
int flux_plugin_conf_unpack (flux_plugin_t *p, const char *fmt, ...);

/*  Create/destroy containers for marshalling read-only arguments
 *   and results between caller and plugin.
 */
flux_plugin_arg_t *flux_plugin_arg_create ();
void flux_plugin_arg_destroy (flux_plugin_arg_t *args);

const char *flux_plugin_arg_strerror (flux_plugin_arg_t *args);

/*  Flags for flux_plugin_arg_get/set/pack/unpack
 */
enum {
    FLUX_PLUGIN_ARG_IN =  0,    /* Operate on input args    */
    FLUX_PLUGIN_ARG_OUT = 1,    /* Operate on output args   */
    FLUX_PLUGIN_ARG_REPLACE = 2 /* Replace args for set/pack */
};

/*  Get/set arguments in plugin arg object using JSON encoded strings
 */
int flux_plugin_arg_set (flux_plugin_arg_t *args,
                         int flags,
                         const char *json_str);
int flux_plugin_arg_get (flux_plugin_arg_t *args,
                         int flags,
                         char **json_str);

/*  Pack/unpack arguments into plugin arg object using jansson pack style args
 */
int flux_plugin_arg_pack (flux_plugin_arg_t *args,
                          int flags,
                          const char *fmt, ...);
int flux_plugin_arg_vpack (flux_plugin_arg_t *args,
                           int flags,
                           const char *fmt,
                           va_list ap);

int flux_plugin_arg_unpack (flux_plugin_arg_t *args,
                            int flags,
                            const char *fmt,
                            ...);
int flux_plugin_arg_vunpack (flux_plugin_arg_t *args,
                             int flags,
                             const char *fmt,
                             va_list ap);

/*  Call first plugin callback matching 'name', passing optional plugin
 *   arguments in 'args'.
 *
 *  Returns 0 if no callback was found for `name`, -1 if callback was
 *   called with return value < 0, and 1 if callback was called with
 *   return value >= 0.
 */
int flux_plugin_call (flux_plugin_t *p,
                      const char *name,
                      flux_plugin_arg_t *args);

/*  Load a plugin from a shared object found in 'path'
 *
 *  Once the shared object is loaded, flux_plugin_init() is run from which
 *   DSO should register itself.
 *
 *  Returns -1 on failure to load plugin, or failure of flux_plugin_init().
 */
int flux_plugin_load_dso (flux_plugin_t *p, const char *path);

#ifdef __cplusplus
}
#endif

#endif /* !FLUX_CORE_PLUGIN_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2021 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_SYNC_H
#define _FLUX_CORE_SYNC_H

#ifdef __cplusplus
extern "C" {
#endif

/* Synchronize future to the system heartbeat.
 * Set minimum > 0. to establish a minimum time between fulfillments.
 * Use a continuation timeout to establish a maximum time between fulfillments.
 */
flux_future_t *flux_sync_create (flux_t *h, double minimum);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_SYNC_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2021 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_DISCONNECT_H
#define _FLUX_CORE_DISCONNECT_H

#ifdef __cplusplus
extern "C" {
#endif

/* Return true if disconnect request msg1 came from same sender as
 * msg2 and has appropriate authorization
 */
bool flux_disconnect_match (const flux_msg_t *msg1, const flux_msg_t *msg2);

/* Remove all messages in 'l' with the same sender as 'msg'.
 * Return 0 or the number of messages removed.
 */
int flux_msglist_disconnect (struct flux_msglist *l, const flux_msg_t *msg);

/* Return true if cancel request msg1 came from same sender as msg2,
 * has appropriate authorization, and references the matchtag in
 * msg2 */
bool flux_cancel_match (const flux_msg_t *msg1, const flux_msg_t *msg2);

/* Respond to and remove the first message in 'l' that matches 'msg'.
 * The sender must match 'msg', and the matchtag must match the one in
 * the cancel request payload.
 */
int flux_msglist_cancel (flux_t *h,
                         struct flux_msglist *l,
                         const flux_msg_t *msg);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_DISCONNECT_H */

/*
 * vi:ts=4 sw=4 expandtab
 */
/************************************************************\
 * Copyright 2021 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_STATS_H
#define _FLUX_CORE_STATS_H

/* Metric types:
 * Counter - An integer value that will, on the backend (brubeck) send the
 *           count and reset to 0 at each flush. It calculates the change
 *           from the value sent at the previous flush.
 *           An example of where to use a counter is the builtin msgcounters
 *           that are part of each flux_t handle. The counts will continually
 *           increase and brubeck will handle calculating the count sent in
 *           the interval.
 * Gauge   - An integer that takes an arbitrary value and maintains its
 *           value until it is set again. Gauges can also take incremental
 *           values in the form of a + or - in front of the value which
 *           increments the previously stored value.
 *           An example of where to use a gauge is to track the current
 *           size of the broker's content-cache. At each point, the cache's
 *           sizes are independent of each other.
 * Timing  - A double value which represents the time taken for a given
 *           task in ms.
 *           An example of where to use a timer is timing the length of
 *           asynchronous loads in the broker's content-cache. The cache
 *           entry can keep track of when the load was started and then
 *           calculate and send the time taken once the entry is loaded.
 */

/* Update (or create) and store 'count' for 'name' to be sent on the
 * next flush.
 */
void flux_stats_count (flux_t *h, const char *name, ssize_t count);

/* Update (or create) and store 'value' for 'name' to be sent on the
 * next flush.
 */
void flux_stats_gauge_set (flux_t *h, const char *name, ssize_t value);

/* Update (or create) and increment 'value' for 'name' to be sent on the
 * next flush. If'name' was not previously stored, then the value is stored
 * directly (i.e. assumed 0 previous value).
 */
void flux_stats_gauge_inc (flux_t *h, const char *name, ssize_t inc);


/* Update (or create) and store 'ms' for 'name' to be sent on the
 * next flush.
 */
void flux_stats_timing (flux_t *h, const char *name, double ms);

/* Update the internal aggregation period over which metrics accumulate
 * before being set. A 'period' of '0' indicates the metrics should be
 * sent immediately. The default aggregation period is 1s.
 */
void flux_stats_set_period (flux_t *h, double period);

/* Set the prefix to be prepended to all metrics sent from the handle.
 * The prefix has a max limit of 127 characters. The default prefix is
 * flux.{{rank}}.
 */
void flux_stats_set_prefix (flux_t *h, const char *fmt, ...);

/* Check whether stats collection is enabled on the flux handle.
 * If 'metric' is non-NULL check if it is currently being tracked.
 */
bool flux_stats_enabled (flux_t *h, const char *metric);

#endif

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */

#endif /* !_FLUX_CORE_FLUX_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2014 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_KVS_H
#define _FLUX_CORE_KVS_H


/************************************************************\
 * Copyright 2017 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_KVS_DIR_H
#define _FLUX_CORE_KVS_DIR_H

#ifdef __cplusplus
extern "C" {
#endif

/* The flux_kvsdir_t represents an unordered list of directory entries.
 * It is also overloaded as a container for a flux_t handle, a snapshot
 * reference, and a namespace placeholder.
 */

typedef struct flux_kvsdir flux_kvsdir_t;
typedef struct flux_kvsitr flux_kvsitr_t;

/* Create/destroy/copy a flux_kvsdir_t.
 *
 * flux_kvsdir_create() creates a new object from 'json_str', an encoded
 * RFC 11 dir object.  'key' is the full key path associated with the
 * directory.  Optional: 'handle', is a flux_t handle, and 'rootref' is
 * a snapshot reference.
 *
 * flux_kvsdir_incref() increments an internal reference count that is
 * decremented by each call to flux_kvsdir_destroy().  Resources
 * are not freed until the reference count reaches zero.  The object is
 * initially created with a reference count of one.
 */
flux_kvsdir_t *flux_kvsdir_create (flux_t *handle,
                                   const char *rootref,
                                   const char *key,
                                   const char *json_str);
void flux_kvsdir_destroy (flux_kvsdir_t *dir);

flux_kvsdir_t *flux_kvsdir_copy (const flux_kvsdir_t *dir);
void flux_kvsdir_incref (flux_kvsdir_t *dir);


/* flux_kvsitr_t is an iterator for walking the list of names in a
 * flux_kvsdir_t.  flux_kvsitr_next() returns NULL when the last
 * item is reached.
 */
flux_kvsitr_t *flux_kvsitr_create (const flux_kvsdir_t *dir);
void flux_kvsitr_destroy (flux_kvsitr_t *itr);
const char *flux_kvsitr_next (flux_kvsitr_t *itr);
void flux_kvsitr_rewind (flux_kvsitr_t *itr);

/* Get the number of keys in a directory.
 */
int flux_kvsdir_get_size (const flux_kvsdir_t *dir);

/* Test whether 'name' exists in 'dir'.
 * It is expected to be a single name, not fully qualified key path.
 */
bool flux_kvsdir_exists (const flux_kvsdir_t *dir, const char *name);

/* Test whether 'name' exists in 'dir' and is itself a directory.
 */
bool flux_kvsdir_isdir (const flux_kvsdir_t *dir, const char *name);

/* Test whether 'name' exists in 'dir' and is a symbolic link.
 */
bool flux_kvsdir_issymlink (const flux_kvsdir_t *dir, const char *name);

/* Access the original 'key', 'json_str', 'handle', and 'rootref' parameters
 * passed to flux_kvsdir_create ()
 */
const char *flux_kvsdir_key (const flux_kvsdir_t *dir);
void *flux_kvsdir_handle (const flux_kvsdir_t *dir);
const char *flux_kvsdir_rootref (const flux_kvsdir_t *dir);

/* Construct a fully-qualified key from flux_kvsdir_key() + "." + key.
 * Caller must free.
 */
char *flux_kvsdir_key_at (const flux_kvsdir_t *dir, const char *key);


#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_KVS_DIR_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2017 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_KVS_LOOKUP_H
#define _FLUX_CORE_KVS_LOOKUP_H

#ifdef __cplusplus
extern "C" {
#endif

flux_future_t *flux_kvs_lookup (flux_t *h,
                                const char *ns,
                                int flags,
                                const char *key);
flux_future_t *flux_kvs_lookupat (flux_t *h,
                                  int flags,
                                  const char *key,
                                  const char *treeobj);

int flux_kvs_lookup_get (flux_future_t *f, const char **value);
int flux_kvs_lookup_get_unpack (flux_future_t *f, const char *fmt, ...);
int flux_kvs_lookup_get_raw (flux_future_t *f, const void **data, size_t *len);
int flux_kvs_lookup_get_treeobj (flux_future_t *f, const char **treeobj);
int flux_kvs_lookup_get_dir (flux_future_t *f, const flux_kvsdir_t **dir);
int flux_kvs_lookup_get_symlink (flux_future_t *f,
                                 const char **ns,
                                 const char **target);

const char *flux_kvs_lookup_get_key (flux_future_t *f);

/* Cancel a FLUX_KVS_WATCH "stream".
 * Once the cancel request is processed, an ENODATA error response is sent,
 * thus the user should continue to reset and consume responses until an
 * error occurs, after which it is safe to destroy the future.
 */
int flux_kvs_lookup_cancel (flux_future_t *f);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_KVS_LOOKUP_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2018 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_KVS_GETROOT_H
#define _FLUX_CORE_KVS_GETROOT_H

#ifdef __cplusplus
extern "C" {
#endif

/* Request the current KVS root hash for namespace 'ns'. */
flux_future_t *flux_kvs_getroot (flux_t *h, const char *ns, int flags);

/* Decode KVS root hash response.
 *
 * treeobj - get the hash as an RFC 11 "dirref" object.
 * blobref - get the raw hash as an RFC 10 "blobref".
 * sequence - get the commit sequence number
 * owner - get the userid of the namespace owner
 */
int flux_kvs_getroot_get_treeobj (flux_future_t *f, const char **treeobj);
int flux_kvs_getroot_get_blobref (flux_future_t *f, const char **blobref);
int flux_kvs_getroot_get_sequence (flux_future_t *f, int *seq);
int flux_kvs_getroot_get_owner (flux_future_t *f, uint32_t *owner);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_KVS_GETROOT_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2017 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_KVS_TXN_H
#define _FLUX_CORE_KVS_TXN_H


#ifdef __cplusplus
extern "C" {
#endif

typedef struct flux_kvs_txn flux_kvs_txn_t;

flux_kvs_txn_t *flux_kvs_txn_create (void);
void flux_kvs_txn_destroy (flux_kvs_txn_t *txn);

int flux_kvs_txn_put (flux_kvs_txn_t *txn,
                      int flags,
                      const char *key,
                      const char *value);

int flux_kvs_txn_vpack (flux_kvs_txn_t *txn,
                        int flags,
                        const char *key,
                        const char *fmt,
                        va_list ap);

int flux_kvs_txn_pack (flux_kvs_txn_t *txn,
                       int flags,
                       const char *key,
                       const char *fmt,
                       ...);

int flux_kvs_txn_put_raw (flux_kvs_txn_t *txn,
                          int flags,
                          const char *key,
                          const void *data,
                          size_t len);

int flux_kvs_txn_put_treeobj (flux_kvs_txn_t *txn,
                              int flags,
                              const char *key,
                              const char *treeobj);

int flux_kvs_txn_mkdir (flux_kvs_txn_t *txn,
                        int flags,
                        const char *key);

int flux_kvs_txn_unlink (flux_kvs_txn_t *txn,
                         int flags,
                         const char *key);

int flux_kvs_txn_symlink (flux_kvs_txn_t *txn,
                          int flags,
                          const char *key,
                          const char *ns,
                          const char *target);

int flux_kvs_txn_clear (flux_kvs_txn_t *txn);

bool flux_kvs_txn_is_empty (flux_kvs_txn_t *txn);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_KVS_TXN_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2017 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_KVS_COMMIT_H
#define _FLUX_CORE_KVS_COMMIT_H

#ifdef __cplusplus
extern "C" {
#endif

/* FLUX_KVS_TXN_COMPACT will currently consolidate appends to the same
 * key.  For example, an append of "A" to the key "foo" and the append
 * "B" to the key "foo" maybe consolidated into a single append of
 * "AB".
 *
 * Compacting transactions means that certain ordered lists of
 * operations will be illegal to compact and result in an error.  Most
 * notably, if a key has data appended to it, then is overwritten in
 * the same transaction, a compaction of appends is not possible.
 *
 * FLUX_KVS_SYNC will ensure all data flushed to the backing store and
 * the root reference is checkpointed.  It effectively performs a:
 *
 * content.flush on rank 0
 * checkpoint on the new root reference from the commit
 *
 * FLUX_KVS_SYNC only works against the primary KVS namespace.  If any
 * part of the content.flush or checkpoint fails an error will be
 * returned and the entire commit will fail.  For example, if a
 * content backing store is not loaded, ENOSYS will returned from this
 * commit.
 */
enum kvs_commit_flags {
    FLUX_KVS_NO_MERGE = 1, /* disallow commits to be mergeable with others */
    FLUX_KVS_TXN_COMPACT = 2, /* try to combine ops on same key within txn */
    FLUX_KVS_SYNC = 4, /* flush and checkpoint after commit is done */
};

flux_future_t *flux_kvs_commit (flux_t *h,
                                const char *ns,
                                int flags,
                                flux_kvs_txn_t *txn);

/* accessors can be used for commit futures */
int flux_kvs_commit_get_treeobj (flux_future_t *f, const char **treeobj);
int flux_kvs_commit_get_rootref (flux_future_t *f, const char **rootref);
int flux_kvs_commit_get_sequence (flux_future_t *f, int *rootseq);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_KVS_COMMIT_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2018 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_KVS_COPY_H
#define _FLUX_CORE_KVS_COPY_H

#ifdef __cplusplus
extern "C" {
#endif

/* Create a copy of 'srckey' at 'dstkey'.  Read from / write to the
 * specified namespaces.  If a namespace is not specified (i.e. NULL),
 * the default namespace will be used, or if set, the namespace from
 * the FLUX_KVS_NAMESPACE environment variable.
 *
 * Due to the hash-tree design of the KVS, dstkey is by definition a
 * "deep copy" (or writable snapshot) of all content below srckey.
 * The copy operation has a low overhead since it only copies a single
 * directory entry.
 *
 * Returns future on success, NULL on failure with errno set.
 */
flux_future_t *flux_kvs_copy (flux_t *h,
                              const char *srcns,
                              const char *srckey,
                              const char *dstns,
                              const char *dstkey,
                              int commit_flags);

/* Move 'srckey' to 'dstkey'.  Read from / write to the
 * specified namespaces.  If a namespace is not specified (i.e. NULL),
 * the default namespace will be used, or if set, the namespace from
 * the FLUX_KVS_NAMESPACE environment variable.
 *
 * This is a copy followed by an unlink on 'srckey'.  The copy and
 * unlink are not atomic.
 *
 * Returns future on success, NULL on failure with errno set.
 */
flux_future_t *flux_kvs_move (flux_t *h,
                              const char *srcns,
                              const char *srckey,
                              const char *dstns,
                              const char *dstkey,
                              int commit_flags);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_KVS_COPY_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */

#ifdef __cplusplus
extern "C" {
#endif

#define KVS_PRIMARY_NAMESPACE "primary"

enum kvs_op {
    FLUX_KVS_READDIR = 1,
    FLUX_KVS_READLINK = 2,
    FLUX_KVS_WATCH = 4,
    FLUX_KVS_WAITCREATE = 8,
    FLUX_KVS_TREEOBJ = 16,
    FLUX_KVS_APPEND = 32,
    FLUX_KVS_WATCH_FULL = 64,
    FLUX_KVS_WATCH_UNIQ = 128,
    FLUX_KVS_WATCH_APPEND = 256,
    FLUX_KVS_STREAM = 512
};

/* Namespace
 * - namespace create only creates the namespace on rank 0.  Other
 *   ranks initialize against that namespace the first time they use
 *   it.
 * - namespace remove marks the namespace for removal on all ranks.
 *   Garbage collection will happen in the background and the
 *   namespace will official be removed.  The removal is "eventually
 *   consistent".
 */
flux_future_t *flux_kvs_namespace_create (flux_t *h,
                                          const char *ns,
                                          uint32_t owner,
                                          int flags);
flux_future_t *flux_kvs_namespace_create_with (flux_t *h,
                                               const char *ns,
                                               const char *rootref,
                                               uint32_t owner,
                                               int flags);
flux_future_t *flux_kvs_namespace_remove (flux_t *h, const char *ns);

/* Synchronization:
 * Process A commits data, then gets the store version V and sends it to B.
 * Process B waits for the store version to be >= V, then reads data.
 */
int flux_kvs_get_version (flux_t *h, const char *ns, int *versionp);
int flux_kvs_wait_version (flux_t *h, const char *ns, int version);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_KVS_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2018 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_JOB_H
#define _FLUX_CORE_JOB_H


#ifdef __cplusplus
extern "C" {
#endif

enum job_submit_flags {
    FLUX_JOB_PRE_SIGNED = 1,    // 'jobspec' is already signed
    FLUX_JOB_DEBUG = 2,
    FLUX_JOB_WAITABLE = 4,      // flux_job_wait() will be used on this job
    FLUX_JOB_NOVALIDATE = 8,    // don't validate jobspec (instance owner only)
};

enum job_event_watch_flags {
    FLUX_JOB_EVENT_WATCH_WAITCREATE = 1, // wait for path to exist
};

enum job_lookup_flags {
    /* return special fields as decoded JSON objects instead of strings
     * - currently works for jobspec and R
     */
    FLUX_JOB_LOOKUP_JSON_DECODE = 1,
    /* get current value of special fields by applying eventlog
     * updates for those fields
     * - currently works for jobspec and R
     */
    FLUX_JOB_LOOKUP_CURRENT = 2,
};

enum job_urgency {
    FLUX_JOB_URGENCY_MIN = 0,
    FLUX_JOB_URGENCY_HOLD = FLUX_JOB_URGENCY_MIN,
    FLUX_JOB_URGENCY_DEFAULT = 16,
    FLUX_JOB_URGENCY_MAX = 31,
    FLUX_JOB_URGENCY_EXPEDITE = FLUX_JOB_URGENCY_MAX,
};

enum job_queue_priority {
    FLUX_JOB_PRIORITY_MIN = 0,
    FLUX_JOB_PRIORITY_MAX = 4294967295,
};

// N.B. value is duplicated in python bindings
#define FLUX_JOBID_ANY 0xFFFFFFFFFFFFFFFF // ~(uint64_t)0

typedef enum {
    FLUX_JOB_STATE_NEW                    = 1,
    FLUX_JOB_STATE_DEPEND                 = 2,
    FLUX_JOB_STATE_PRIORITY               = 4,
    FLUX_JOB_STATE_SCHED                  = 8,
    FLUX_JOB_STATE_RUN                    = 16,
    FLUX_JOB_STATE_CLEANUP                = 32,
    FLUX_JOB_STATE_INACTIVE               = 64,   // captive end state
} flux_job_state_t;

#define FLUX_JOB_NR_STATES 7

/* Virtual states, for convenience.
 */
enum {
    /* FLUX_JOB_STATE_DEPEND | FLUX_JOB_STATE_PRIORITY | FLUX_JOB_STATE_SCHED */
    FLUX_JOB_STATE_PENDING    = 14,
    /* FLUX_JOB_STATE_RUN | FLUX_JOB_STATE_CLEANUP */
    FLUX_JOB_STATE_RUNNING    = 48,
    /* FLUX_JOB_STATE_PENDING | FLUX_JOB_STATE_RUNNING */
    FLUX_JOB_STATE_ACTIVE     = 62,
};

/* Result of a job
 */
typedef enum {
    FLUX_JOB_RESULT_COMPLETED = 1,
    FLUX_JOB_RESULT_FAILED = 2,
    FLUX_JOB_RESULT_CANCELED = 4,
    FLUX_JOB_RESULT_TIMEOUT = 8,
} flux_job_result_t;

typedef uint64_t flux_jobid_t;

/*  Parse a jobid from NULL-terminated string 's' in any supported encoding.
 *  Returns 0 on success, -1 on failure.
 */
int flux_job_id_parse (const char *s, flux_jobid_t *id);

/*  Encode a jobid into encoding "type", writing the result to buffer
 *   buf of size bufsz.
 *  Supported encoding types include:
 *   "dec", "hex", "kvs", "dothex", "words", "f58", or "f58plain"
 *  Returns 0 on success, -1 on failure with errno set:
 *   EPROTO: Invalid encoding type
 *   EINVAL: Invalid other argument
 */
int flux_job_id_encode (flux_jobid_t id, const char *type,
                        char *buf, size_t bufsz);

/* Convert state to string.  'fmt' may be:
 * "s" - lower case short name
 * "S" - upper case short name
 * "l" - lower case long name
 * "L" - upper case long name
 * This function always returns a valid string, though it may
 * be something like "(unknown)".
 */
const char *flux_job_statetostr (flux_job_state_t state, const char *fmt);

/* Convert state string in any of the forms produced by flux_job_statetostr()
 * back to state.  Returns 0 on success, -1 on failure with errno set.
 */
int flux_job_strtostate (const char *s, flux_job_state_t *state);

const char *flux_job_resulttostr (flux_job_result_t result, const char *fmt);

int flux_job_strtoresult (const char *s, flux_job_result_t *result);

/* Submit a job to the system.
 * 'jobspec' should be RFC 14 jobspec.
 * 'urgency' should be a value from 0 to 31 (16 if not instance owner).
 * 'flags' should be 0 for now.
 * The system assigns a jobid and returns it in the response.
 */
flux_future_t *flux_job_submit (flux_t *h, const char *jobspec,
                                int urgency, int flags);

/* Parse jobid from response to flux_job_submit() request.
 * Returns 0 on success, -1 on failure with errno set - and an extended
 * error message may be available with flux_future_error_string().
 */
int flux_job_submit_get_id (flux_future_t *f, flux_jobid_t *id);

/* Wait for jobid to enter INACTIVE state.
 * If jobid=FLUX_JOBID_ANY, wait for the next waitable job.
 * Fails with ECHILD if there is nothing to wait for.
 */
flux_future_t *flux_job_wait (flux_t *h, flux_jobid_t id);
int flux_job_wait_get_status (flux_future_t *f,
                              bool *success,
                              const char **errstr);
int flux_job_wait_get_id (flux_future_t *f, flux_jobid_t *id);

FLUX_DEPRECATED(flux_future_t *flux_job_list (flux_t *,
                                              int,
                                              const char *,
                                              uint32_t,
                                              int));

FLUX_DEPRECATED(flux_future_t *flux_job_list_inactive (flux_t *,
                                                       int,
                                                       double,
                                                       const char *));

/* Similar to flux_job_list(), but retrieve job info for a single
 * job id */
flux_future_t *flux_job_list_id (flux_t *h,
                                 flux_jobid_t id,
                                 const char *attrs_json_str);

/* Raise an exception for job.
 * Severity is 0-7, with severity=0 causing the job to abort.
 * Note may be NULL or a human readable message.
 */
flux_future_t *flux_job_raise (flux_t *h, flux_jobid_t id,
                               const char *type, int severity,
                               const char *note);

/* Cancel a job.
 * Reason may be NULL or a human readable message.
 */
flux_future_t *flux_job_cancel (flux_t *h, flux_jobid_t id, const char *reason);

/* Deliver a signal to a job.
 */
flux_future_t *flux_job_kill (flux_t *h, flux_jobid_t id, int signum);

/* Change job urgency.
 */
flux_future_t *flux_job_set_urgency (flux_t *h, flux_jobid_t id, int urgency);

/* Write KVS path to 'key' relative to job directory for job 'id'.
 * If key=NULL, write the job directory.
 * Returns string length on success, or -1 on failure.
 */
int flux_job_kvs_key (char *buf, int bufsz, flux_jobid_t id, const char *key);

/* Same as above but construct key relative to job guest directory,
 * and if FLUX_KVS_NAMESPACE is set, assume guest is the root directory.
 */
int flux_job_kvs_guest_key (char *buf,
                            int bufsz,
                            flux_jobid_t id,
                            const char *key);


/* Write KVS job namespace name to to buffer 'buf'.
 * Returns string length on success or < 0 on failure.
 */
int flux_job_kvs_namespace (char *buf,
                            int bufsz,
                            flux_jobid_t id);

/* Job eventlog watch functions
 * - path specifies optional alternate eventlog path
 */
flux_future_t *flux_job_event_watch (flux_t *h, flux_jobid_t id,
                                     const char *path, int flags);
int flux_job_event_watch_get (flux_future_t *f, const char **event);
int flux_job_event_watch_cancel (flux_future_t *f);

/*  Wait for job to reach its terminal state and fetch the job result
 *   along with other ancillary information from the job eventlog.
 */
flux_future_t *flux_job_result (flux_t *h, flux_jobid_t id, int flags);

/*  Get the job result "payload" as a JSON string
 */
int flux_job_result_get (flux_future_t *f,
                         const char **json_str);

/*  Decode and unpack the result payload from future `f`.
 *  The result object contains the following information:
 *
 *   {
 *     "id":i,                 jobid
 *     "result:i,              flux_job_result_t
 *     "t_submit":f,           timestamp of job submit event
 *     "t_run":f,              timestamp of job alloc event
 *     "t_cleanup":f,          timestamp of job finish event
 *     "waitstatus"?i,         wait status (if job started)
 *     "exception_occurred":b, true if job exception occurred
 *     "exception_severity"?i, exception severity (if exception)
 *     "exception_type"?s,     exception type (if exception)
 *     "exception_note"?s      exception note (if exception)
 *   }
 *
 */
int flux_job_result_get_unpack (flux_future_t *f, const char *fmt, ...);


/*  Get remaining time in floating point seconds for the current job or
 *  enclosing instance (i.e., if the current process is associated with
 *  a flux instance, but is not part of a parallel job).
 *
 *  Returns 0 on success with timeleft assigned to the remaining time.
 *  If there is no expiration in the current context (e.g. the job has
 *  no timelimit), then timeleft is set to infinity. If the job is not
 *  in RUN state, or the job has expired, then timeleft is set to 0.
 *
 *  Returns -1 with error string assigned to 'errp' on failure.
 */
int flux_job_timeleft (flux_t *h, flux_error_t *errp, double *timeleft);

/*  Unwrap signed data to a NUL terminated string, e.g. J -> jobspec.
 *
 *  If verify is true, then fail if signing mechanism is invalid or
 *   signing user does not match current uid. On failure, error.text
 *   is filled in with an error message. (errno not necessarily
 *   guaranteed to be valid).
 *
 *  Works when flux-core is built with or without flux-security
 *
 *  Caller must free returned value if non-NULL.
 *
 *  Predominantly used by flux-core internally and associated
 *  libraries/tools.
 */
char *flux_unwrap_string (const char *in,
                          bool verify,
                          uint32_t *userid,
                          flux_error_t *error);


/* Convert the waitstatus from a job `finish` event to an exit code.
 * If the job exited with nonzero status, then place an appropriate error
 * message in errp->text.
 */
int flux_job_waitstatus_to_exitcode (int waitstatus, flux_error_t *errp);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_JOB_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2021 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_JOBSPEC1_H
#define _FLUX_CORE_JOBSPEC1_H


typedef struct flux_jobspec1 flux_jobspec1_t;
typedef flux_error_t flux_jobspec1_error_t;

/* Remove the value in the jobspec's attributes section at the given path,
 * where "." is treated as a path separator.
 * It is not an error if 'path' does not exist.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_attr_del (flux_jobspec1_t *jobspec, const char *path);

/* Set the value in the jobspec's attributes section at the given path,
 * where "." is treated as a path separator.  'fmt' should be a jansson
 * pack-style string corresponding to the remaining arguments.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_attr_pack (flux_jobspec1_t *jobspec,
                             const char *path,
                             const char *fmt,
                             ...);

/* Unpack the values in the jobspec's attributes section at the given path,
 * where "." is treated as a path separator.  'fmt' should be a jansson
 * unpack-style string corresponding to the remaining args.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_attr_unpack (flux_jobspec1_t *jobspec,
                               const char *path,
                               const char *fmt,
                               ...);

/* Check the validity of only the attributes section of a jobspec, sufficient
 * if the jobspec object was created by flux_jobspec1_from_command(), then
 * modified with the other jobspec1 functions.
 * Return 0 on success, -1 on error with errno set.
 * On error, write an error message written to 'error', if non-NULL.
 */
int flux_jobspec1_attr_check (flux_jobspec1_t *jobspec,
                              flux_jobspec1_error_t *error);

/* Check the validity of the full jobspec, which may be necessary if the
 * jobspec object was created by flux_jobspec1_decode().
 * Return 0 on success, -1 on error with errno set.
 * On error, write an error message written to 'error', if non-NULL.
 */
int flux_jobspec1_check (flux_jobspec1_t *jobspec,
                         flux_jobspec1_error_t *error);

/* Remove the variable 'name' from the environment.
 * This function succeeds if 'name' does not exist.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_unsetenv (flux_jobspec1_t *jobspec, const char *name);

/* Add the variable 'name' to the environment with the value 'value'.
 * If 'name' exists in the environment and 'overwrite' is nonzero, change
 * value to 'value'.  If 'name' exists and 'overwrite' is zero, do not
 * change the value (and return success).
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_setenv (flux_jobspec1_t *jobspec,
                           const char *name,
                           const char *value,
                           int overwrite);

/* Redirect job stdin from the KVS to a file system path given by 'path'.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_set_stdin (flux_jobspec1_t *jobspec, const char *path);

/* Redirect job stdout from the KVS to a file system path given by 'path'.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_set_stdout (flux_jobspec1_t *jobspec, const char *path);

/* Redirect job stderr from the KVS to a file system path given by 'path'.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_set_stderr (flux_jobspec1_t *jobspec, const char *path);

/* Set the working directory of a jobspec.
 * Return 0 on success, -1 on error with errno set.
 */
int flux_jobspec1_set_cwd (flux_jobspec1_t *jobspec, const char *cwd);

/* Encode a jobspec to a string, e.g. for usage with flux_job_submit().
 * 'flags' should be 0.  The returned string must be released with free().
 * Return NULL on error with errno set.
 */
char *flux_jobspec1_encode (flux_jobspec1_t *jobspec, size_t flags);

/* Decode a string to jobspec.  No validation is performed on the content.
 * The returned jobspec must be released with flux_jobspec1_destroy().
 * Return NULL on error with errno set.
 * On error, write an error message to 'error', if non-NULL.
 */
flux_jobspec1_t *flux_jobspec1_decode (const char *s,
                                       flux_jobspec1_error_t *error);


/* Create and return a minimum viable V1 Jobspec.
 * The jobspec must be released with flux_jobspec1_destroy()'
 * The jobspec will have stdin, stdout, stderr all directed to the KVS.
 * 'argc' and 'argv' define the command and its arguments.
 * 'env' should be an environ(7)-style array, or NULL for empty.
 * 'tasks' should be the number of tasks to launch
 * 'cores_per_task' should be the number of cores per task to allocate
 * 'gpus_per_task' should be the number of gpus per task to allocate
 * 'nodes' should be the number of nodes to spread the allocated cores
 * and gpus across. If 0, the scheduler will determine the node allocation.
 * Return NULL on error with errno set.
 */
flux_jobspec1_t *flux_jobspec1_from_command (int argc,
                                             char **argv,
                                             char **env,
                                             int ntasks,
                                             int cores_per_task,
                                             int gpus_per_task,
                                             int nnodes,
                                             double duration);

/* Free a jobspec. */
void flux_jobspec1_destroy (flux_jobspec1_t *jobspec);

#endif /* _FLUX_CORE_JOBSPEC1_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
/************************************************************\
 * Copyright 2018 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _FLUX_CORE_SUBPROCESS_H
#define _FLUX_CORE_SUBPROCESS_H



/************************************************************\
 * Copyright 2018 Lawrence Livermore National Security, LLC
 * (c.f. AUTHORS, NOTICE.LLNS, COPYING)
 *
 * This file is part of the Flux resource manager framework.
 * For details, see https://github.com/flux-framework.
 *
 * SPDX-License-Identifier: LGPL-3.0
\************************************************************/

#ifndef _SUBPROCESS_COMMAND_H
#define _SUBPROCESS_COMMAND_H


#ifdef __cplusplus
extern "C" {
#endif

/*
 *  flux_cmd_t: An object that defines a command to be run, either
 *   remotely or as a child of the current process. Includes cmdline
 *   arguments, environment, and working directory. A flux_cmd_t is
 *   used to create Flux subprocesses.
 */
typedef struct flux_command flux_cmd_t;

/*
 *  Create a cmd object, from which subprocesses can be created
 */
flux_cmd_t * flux_cmd_create (int argc, char *argv[], char **env);

/*
 *  Create a copy of a cmd object.
 */
flux_cmd_t * flux_cmd_copy (const flux_cmd_t *cmd);

/*
 *  Destroy and free command object `cmd`
 */
void flux_cmd_destroy (flux_cmd_t *cmd);

/*
 *  Append formatted string to argv of `cmd`.
 */
int flux_cmd_argv_appendf (flux_cmd_t *cmd,
                           const char *fmt, ...)
                           __attribute__ ((format (printf, 2, 3)));

/*
 *  Append string to argv of `cmd`.
 */
int flux_cmd_argv_append (flux_cmd_t *cmd, const char *arg);

/*
 *  Delete the nth argument in cmd's argv
 */
int flux_cmd_argv_delete (flux_cmd_t *cmd, int n);

/*
 *  Insert arg before the nth argument in cmd's argv
 */
int flux_cmd_argv_insert (flux_cmd_t *cmd, int n, const char *arg);

/*
 *  Return the current argument count for `cmd`.
 */
int flux_cmd_argc (const flux_cmd_t *cmd);

/*
 *  Return the current argument at index n (range 0 to argc - 1)
 */
const char *flux_cmd_arg (const flux_cmd_t *cmd, int n);

/*
 *  Return a copy of the current cmd as a string. Caller must free
 */
char *flux_cmd_stringify (const flux_cmd_t *cmd);

/*
 *  Set a single environment variable (name) to formatted string `fmt`.
 *   If `overwrite` is non-zero then overwrite any existing setting for `name`.
 */
int flux_cmd_setenvf (flux_cmd_t *cmd,
                      int overwrite,
                      const char *name,
                      const char *fmt,
                      ...)
                      __attribute__ ((format (printf, 4, 5)));

/*
 *  Unset environment variable `name` in the command object `cmd`.
 *   If `name` is a glob pattern, unset all matching variables.
 */
void flux_cmd_unsetenv (flux_cmd_t *cmd, const char *name);

/*
 *  Return current value for environment variable `name` as set in
 *   command object `cmd`. If environment variable is not set then NULL
 *   is returned.
 */
const char *flux_cmd_getenv (const flux_cmd_t *cmd, const char *name);

/*
 *  Set/get the working directory for the command `cmd`.
 */
int flux_cmd_setcwd (flux_cmd_t *cmd, const char *cwd);
const char *flux_cmd_getcwd (const flux_cmd_t *cmd);

/*
 *  Request a channel for communication between process and caller.
 *   Callers can write to the subprocess via flux_subprocess_write()
 *   and read from it via flux_subprocess_read(), which is typically
 *   called from a callback set in 'on_channel_out'.
 *
 *  The `name` argument is also used as the name of the environment variable
 *   in the subprocess environment that is set to the file descriptor number
 *   of the process side of the socketpair. E.g. name = "FLUX_PMI_FD" would
 *   result in the environment variable "FLUX_PMI_FD=N" set in the process
 *   environment.
 */
int flux_cmd_add_channel (flux_cmd_t *cmd, const char *name);

/*
 *  Set generic string options for command object `cmd`. As with environment
 *   variables, this function adds the option `var` with value `val` to
 *   the options array for this command. This can be used to enable optional
 *   behavior for executed processes (e.g. setpgrp(2))
 *
 *  String options, note that name indicates the 'name' argument used
 *  in flux_cmd_add_channel() above.
 *
 *  "BUFSIZE" option
 *
 *   By default, stdio and channels use an internal buffer of 4 megs.
 *   The buffer size can be adjusted with this option.
 *
 *   - name + "_BUFSIZE" - set buffer size on channel name
 *   - stdin_BUFSIZE - set buffer size on stdin
 *   - stdout_BUFSIZE - set buffer size on stdout
 *   - stderr_BUFSIZE - set buffer size on stderr
 *
 *   The BUFSIZE string may be a floating point quantity scaled by
 *   an optional suffix from the set 'kKMG'.
 *
 *  "LINE_BUFFER" option
 *
 *    By default, the 'on_output' callback
 *    is called when a line of data is available (with the exception
 *    with data after a subprocess has exited).  By setting this
 *    option to "false", the output callback will be called whenever any amount
 *    of data is available on the stream.  These options can also be set to
 *    "true" to keep default behavior of line buffering.
 *
 *    - name + "_LINE_BUFFER" - configuring line buffering on channel name
 *    - stdout_LINE_BUFFER - configure line buffering for stdout
 *    - stderr_LINE_BUFFER - configure line buffering for stderr
 */
int flux_cmd_setopt (flux_cmd_t *cmd, const char *var, const char *val);
const char *flux_cmd_getopt (flux_cmd_t *cmd, const char *var);

#ifdef __cplusplus
}
#endif

#endif /* !_SUBPROCESS_COMMAND_H */

// vi: ts=4 sw=4 expandtab

#ifdef __cplusplus
extern "C" {
#endif

/*
 *  flux_subprocess_t: A subprocess is an instantiation of a command
 *   as a remote or local process. A subprocess has a state (e.g.
 *   initialized, starting, running, exited, completed), a PID, and
 *   a rank if running remotely.
 */
typedef struct flux_subprocess flux_subprocess_t;

/*
 * Subprocess states, on changes, will lead to calls to
 * on_state_change below.
 *
 * Possible state changes:
 *
 * init -> running
 * running -> exited
 * any state -> failed
 */
typedef enum {
    FLUX_SUBPROCESS_INIT,         /* initial state */
    FLUX_SUBPROCESS_RUNNING,      /* exec(2) has been called */
    FLUX_SUBPROCESS_EXITED,       /* process has exited */
    FLUX_SUBPROCESS_FAILED,       /* exec failure or other non-child error */
    FLUX_SUBPROCESS_STOPPED,      /* process was stopped */
} flux_subprocess_state_t;

/*
 * Subprocess flags
 */
enum {
    /* flux_local_exec(): let parent stdin, stdout, stderr, carry to
     * child.  Do not create "stdin", "stdout", or "stderr" channels.
     * Subsequently, flux_subprocess_write()/close()/read()/read_line()
     * will fail on streams of "stdin", "stdout", or "stderr".
     */
    FLUX_SUBPROCESS_FLAGS_STDIO_FALLTHROUGH = 1,
    /* flux_local_exec(): do not call setpgrp() before exec(2) */
    FLUX_SUBPROCESS_FLAGS_NO_SETPGRP = 2,
    /* flux_local_exec(): use fork(2)/exec(2) even if posix_spawn(3)
     * available */
    FLUX_SUBPROCESS_FLAGS_FORK_EXEC = 4,
    /* flux_rexec(): In order to improve performance, do not locally
     * copy and buffer output from the remote subprocess.  Immediately
     * call output callbacks.  Users should call
     * flux_subprocess_read() to retrieve the data.  If
     * flux_subprocess_read() is not called, data will be lost.  Data
     * will not be NUL terminated.  flux_subprocess_read() should be
     * called only once.  If called more than once, the same data is
     * returned.  Use of other read functions will result in a EPERM
     * error.
     */
    FLUX_SUBPROCESS_FLAGS_LOCAL_UNBUF = 8,
};

/*
 *  Typedefs for subprocess hooks and callbacks:
 *
 */
typedef void (*flux_subprocess_f) (flux_subprocess_t *p);
typedef void (*flux_subprocess_output_f) (flux_subprocess_t *p,
                                          const char *stream);
typedef void (*flux_subprocess_state_f) (flux_subprocess_t *p,
                                         flux_subprocess_state_t state);
typedef void (*flux_subprocess_credit_f) (flux_subprocess_t *p,
                                          const char *stream,
                                          int bytes);
typedef void (*flux_subprocess_hook_f) (flux_subprocess_t *p, void *arg);

/*
 *  Functions for event-driven subprocess handling:
 *
 *  When output callbacks are called, flux_subprocess_read(),
 *  flux_subprocess_read_line() and similar functions should be used
 *  to read buffered data.  If this is not done, it can lead to
 *  excessive callbacks and code "spinning".
 *
 *  The first call to on_credit will contain the full buffer size.
 *
 */
typedef struct {
    flux_subprocess_f on_completion;    /* Process exited and all I/O
                                         * complete, will not be
                                         * called if FAILED state reached.
                                         */
    flux_subprocess_state_f on_state_change;  /* Process state change        */
    flux_subprocess_output_f on_channel_out; /* Read from channel when ready */
    flux_subprocess_output_f on_stdout; /* Read of stdout is ready           */
    flux_subprocess_output_f on_stderr; /* Read of stderr is ready           */
    flux_subprocess_credit_f on_credit; /* Write buffer space available      */
} flux_subprocess_ops_t;

/*
 *  flux_subprocess_hooks_t: Hook functions to execute at pre-defined
 *  points.  Hooks can only be executed on local processes.
 */
typedef struct {
    flux_subprocess_hook_f pre_exec;
    void *pre_exec_arg;
    flux_subprocess_hook_f post_fork;
    void *post_fork_arg;
} flux_subprocess_hooks_t;

/*
 *  llog-compatible callback
 */
typedef void (*subprocess_log_f)(void *arg,
                                 const char *file,
                                 int line,
                                 const char *func,
                                 const char *subsys,
                                 int level,
                                 const char *fmt,
                                 va_list args);


/*
 *  Subprocesses:
 */

/*
 *  Asynchronously create a new subprocess described by command object
 *   `cmd`.  flux_local_exec() create a new subprocess locally.
 *   flux_rexec() creates a new subprocess on Flux rank
 *   `rank`. Callbacks in `ops` structure that are non-NULL will be
 *   called to process state changes, I/O, and completion.
 *
 *  'rank' can be set to FLUX_NODEID_ANY or FLUX_NODEID_UPSTREAM.
 *
 *  This function may return NULL (with errno set) on invalid
 *   argument(s) (EINVAL), or failure of underlying Flux messaging
 *   calls. Otherwise, a valid subprocess object is returned, though
 *   there is no guarantee the subprocess has started running anywhere
 *   by the time the call returns.
 *
 */
flux_subprocess_t *flux_local_exec (flux_reactor_t *r,
                                    int flags,
                                    const flux_cmd_t *cmd,
                                    const flux_subprocess_ops_t *ops);

flux_subprocess_t *flux_local_exec_ex (flux_reactor_t *r,
                                       int flags,
                                       const flux_cmd_t *cmd,
                                       const flux_subprocess_ops_t *ops,
                                       const flux_subprocess_hooks_t *hooks,
                                       subprocess_log_f log_fn,
                                       void *log_data);

flux_subprocess_t *flux_rexec (flux_t *h,
                               int rank,
                               int flags,
                               const flux_cmd_t *cmd,
                               const flux_subprocess_ops_t *ops);

flux_subprocess_t *flux_rexec_ex (flux_t *h,
                                  const char *service_name,
                                  int rank,
                                  int flags,
                                  const flux_cmd_t *cmd,
                                  const flux_subprocess_ops_t *ops,
                                  subprocess_log_f log_fn,
                                  void *log_data);


/* Start / stop a read stream temporarily on local processes.  This
 * may be useful for flow control.
 */
void flux_subprocess_stream_start (flux_subprocess_t *p, const char *stream);
void flux_subprocess_stream_stop (flux_subprocess_t *p, const char *stream);

/*
 *  Write data to "stream" stream of subprocess `p`.  'stream' can be
 *  "stdin" or the name of a stream specified with flux_cmd_add_channel().
 *
 *  Returns the total amount of data successfully buffered or -1 on error
 *  with errno set. Note: this function will not return a short write. If
 *  all `len` bytes cannot fit in the destination buffer, then no bytes
 *  will be written and -1 will be returned with errno=ENOSPC.
 */
int flux_subprocess_write (flux_subprocess_t *p,
                           const char *stream,
                           const char *buf,
                           size_t len);

/*
 *  Close "stream" stream of subprocess `p` and schedule EOF to be sent.
 *  'stream' can be "stdin" or the name of a stream specified with
 *  flux_cmd_add_channel().
 */
int flux_subprocess_close (flux_subprocess_t *p, const char *stream);

/*
 *  Read unread data from stream `stream`.  'stream' can be "stdout",
 *   "stderr", or the name of a stream specified with flux_cmd_add_channel().
 *
 *   Returns length of data on success and -1 on error with errno set.
 *   Buffer of data is returned in bufp.  Buffer is guaranteed to be
 *   NUL terminated unless the FLUX_SUBPROCESS_FLAGS_LOCAL_UNBUF flag
 *   has been specified.  User shall not free returned pointer.
 *
 *   In most cases, a length of 0 indicates that the subprocess has
 *   closed this stream.  A length of 0 could be returned if read
 *   functions are called multiple times within a single output
 *   callback, so it is generally recommended to call this function
 *   once per output callback.  flux_subprocess_read_stream_closed()
 *   can always be used to verify if the stream is in fact closed.
 */
int flux_subprocess_read (flux_subprocess_t *p,
                          const char *stream,
                          const char **bufp);

/*
 *  Read line of unread data from stream `stream`.  'stream' can be
 *   "stdout", "stderr", or the name of a stream specified with
 *   flux_cmd_add_channel().
 *
 *   Returns length of data on success and -1 on error with errno set.
 *   Buffer with line is returned in bufp.  Buffer will include
 *   newline character and is guaranteed to be NUL terminated.  If no
 *   line is available, returns length of zero.  User shall not free
 *   returned pointer.
 *
 *   A length of zero may be returned if the stream is closed OR if
 *   the stream is line buffered and a line is not yet available. Use
 *   flux_subprocess_read_stream_closed() to distinguish between the
 *   two.
 *
 *   This function may return an incomplete line when:
 *
 *   1) the stream has closed and the last output is not a line
 *   2) a single line of output exceeds the size of an internal output
 *      buffer (see BUFSIZE option).
 */
int flux_subprocess_read_line (flux_subprocess_t *p,
                               const char *stream,
                               const char **bufp);

/* Identical to flux_subprocess_read_line(), but does not return
 * trailing newline.
 */
int flux_subprocess_read_trimmed_line (flux_subprocess_t *p,
                                       const char *stream,
                                       const char **bufp);

/* Determine if the read stream has is closed / received an EOF.  This
 * function can be useful if you are reading lines via
 * flux_subprocess_read_line() or flux_subprocess_read_trimmed_line()
 * in output callbacks.  Those functions will return length 0 when no
 * lines are available, making it difficult to determine if the stream
 * has been closed and there is any non-newline terminated data left
 * available for reading with flux_subprocess_read().
 */
bool flux_subprocess_read_stream_closed (flux_subprocess_t *p,
                                         const char *stream);

/* flux_subprocess_getline() is a special case function
 * that behaves identically to flux_subprocess_read_line() but handles
 * several common special cases.  It requires the stream of data to be
 * line buffered (by default on, see LINE_BUFFER under
 * flux_cmd_setopt()).
 *
 * - if the stream of data has internally completed (i.e. the
 *   subprocess has closed the stream / EOF has been received) but the
 *   last data on the stream does not terminate in a newline
 *   character, this function will return that last data without the
 *   trailing newline.
 * - if the stream has been closed / reached EOF, 0 will be returned.
 * - if the stream is not line buffered, NULL and errno = EPERM will
 *   be returned.
 */
int flux_subprocess_getline (flux_subprocess_t *p,
                             const char *stream,
                             const char **bufp);

/*
 *  Create RPC to send signal `signo` to subprocess `p`.
 *  This call returns a flux_future_t. Use flux_future_then(3) to register
 *   a continuation callback when the kill operation is complete, or
 *   flux_future_wait_for(3) to block until the kill operation is complete.
 */
flux_future_t *flux_subprocess_kill (flux_subprocess_t *p, int signo);

/*
 *  Remove a reference to subprocess object `p`. The subprocess object
 *   is destroyed once the last reference is removed.  This call
 *   silently deso nothing if called within a hook.
 */
void flux_subprocess_destroy (flux_subprocess_t *p);

/*  Return current state value of subprocess.  Note this may differ
 *  than state returned in on_state_change callback, as a subprocess
 *  may have already transitioned past that point (e.g. the callback
 *  received a transition change to RUNNING, but the child subprocess
 *  has already EXITED).
 */
flux_subprocess_state_t flux_subprocess_state (flux_subprocess_t *p);

/*  Return string value of state of subprocess
 */
const char *flux_subprocess_state_string (flux_subprocess_state_t state);

/*  Return true if subprocess p is still active, i.e. it is waiting to
 *  start, still running, or waiting for eof on all streams.
 */
bool flux_subprocess_active (flux_subprocess_t *p);

int flux_subprocess_rank (flux_subprocess_t *p);

/* Returns the errno causing the FLUX_SUBPROCESS_FAILED state to be reached.
 */
int flux_subprocess_fail_errno (flux_subprocess_t *p);

/* Returns error message describing why FLUX_SUBPROCESS_FAILED state was
 * reached.  If error message was not set, will return strerror() of
 * errno returned from flux_subprocess_fail_errno().
 */
const char *flux_subprocess_fail_error (flux_subprocess_t *p);

/* Returns exit status as returned from wait(2).  Works only for
 * FLUX_SUBPROCESS_EXITED state. */
int flux_subprocess_status (flux_subprocess_t *p);

/* Returns exit code if processes exited normally.  Works only for
 * FLUX_SUBPROCESS_EXITED state. */
int flux_subprocess_exit_code (flux_subprocess_t *p);

/* Returns signal if process terminated via signal.  Works only for
 * FLUX_SUBPROCESS_EXITED state. */
int flux_subprocess_signaled (flux_subprocess_t *p);

pid_t flux_subprocess_pid (flux_subprocess_t *p);

/*  Return the command object associated with subprocess `p`.
 */
flux_cmd_t *flux_subprocess_get_cmd (flux_subprocess_t *p);

/*  Return the reactor object associated with subprocess `p`.
 */
flux_reactor_t * flux_subprocess_get_reactor (flux_subprocess_t *p);

/*
 *  Set arbitrary context `ctx` with name `name` on subprocess object `p`.
 *
 *  Returns 0 on success
 */
int flux_subprocess_aux_set (flux_subprocess_t *p,
                             const char *name,
                             void *ctx,
                             flux_free_f free);

/*
 *  Return pointer to any context associated with `p` under `name`. If
 *   no such context exists, then NULL is returned.
 */
void *flux_subprocess_aux_get (flux_subprocess_t *p, const char *name);

/*
 *  Take/drop a reference on a subprocess output channel `name` (e.g. "stdout"
 *   or "stderr"). EOF will not be produced from this channel the reference
 *   count drops to zero.
 */
void flux_subprocess_channel_incref (flux_subprocess_t *p, const char *name);
void flux_subprocess_channel_decref (flux_subprocess_t *p, const char *name);

#ifdef __cplusplus
}
#endif

#endif /* !_FLUX_CORE_SUBPROCESS_H */

// vi: ts=4 sw=4 expandtab

#endif /* !_FLUX_CORE_H */

/*
 * vi:tabstop=4 shiftwidth=4 expandtab
 */
//flux_msg_handler_f
extern "Python" void message_handler_wrapper(flux_t *, flux_msg_handler_t *, const flux_msg_t *, void *);

//flux_watcher_f
extern "Python" void timeout_handler_wrapper(flux_reactor_t *, flux_watcher_t *, int, void *);
extern "Python" void fd_handler_wrapper(flux_reactor_t *, flux_watcher_t *, int, void *);
extern "Python" void signal_handler_wrapper(flux_reactor_t *, flux_watcher_t *, int, void *);

//flux_continuation_f
extern "Python" void continuation_callback(flux_future_t *, void *);

//flux_future_init_f
extern "Python" void init_callback(flux_future_t *, void *);
