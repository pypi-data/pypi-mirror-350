# 0 "/__w/flux-python/flux-python/src/_idset_clean.h"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 0 "<command-line>" 2
# 1 "/__w/flux-python/flux-python/src/_idset_clean.h"
# 23 "/__w/flux-python/flux-python/src/_idset_clean.h"
enum idset_flags {
    IDSET_FLAG_AUTOGROW = 1,
    IDSET_FLAG_BRACKETS = 2,
    IDSET_FLAG_RANGE = 4,
    IDSET_FLAG_INITFULL = 8,
    IDSET_FLAG_COUNT_LAZY = 16,

};

typedef struct {
    char text[160];
} idset_error_t;
# 45 "/__w/flux-python/flux-python/src/_idset_clean.h"
struct idset *idset_create (size_t size, int flags);
void idset_destroy (struct idset *idset);




size_t idset_universe_size (const struct idset *idset);




struct idset *idset_copy (const struct idset *idset);





char *idset_encode (const struct idset *idset, int flags);




struct idset *idset_decode (const char *s);
# 76 "/__w/flux-python/flux-python/src/_idset_clean.h"


 ;
# 87 "/__w/flux-python/flux-python/src/_idset_clean.h"
struct idset *idset_decode_ex (const char *s,
                               ssize_t len,
                               ssize_t size,
                               int flags,
                               idset_error_t *error);





bool idset_decode_empty (const char *s, ssize_t len);







int idset_decode_info (const char *s,
                       ssize_t len,
                       size_t *count,
                       unsigned int *maxid,
                       idset_error_t *error);






int idset_decode_add (struct idset *idset,
                      const char *s,
                      ssize_t len,
                      idset_error_t *error);






int idset_decode_subtract (struct idset *idset,
                           const char *s,
                           ssize_t len,
                           idset_error_t *error);





int idset_set (struct idset *idset, unsigned int id);
int idset_range_set (struct idset *idset, unsigned int lo, unsigned int hi);





int idset_clear (struct idset *idset, unsigned int id);
int idset_range_clear (struct idset *idset, unsigned int lo, unsigned int hi);




bool idset_test (const struct idset *idset, unsigned int id);




unsigned int idset_first (const struct idset *idset);




unsigned int idset_next (const struct idset *idset, unsigned int id);




unsigned int idset_last (const struct idset *idset);




unsigned int idset_prev (const struct idset *idset, unsigned int id);




size_t idset_count (const struct idset *idset);




bool idset_empty (const struct idset *idset);




bool idset_equal (const struct idset *a, const struct idset *);




struct idset *idset_union (const struct idset *a, const struct idset *b);




int idset_add (struct idset *a, const struct idset *b);




struct idset *idset_difference (const struct idset *a, const struct idset *b);




int idset_subtract (struct idset *a, const struct idset *b);
# 212 "/__w/flux-python/flux-python/src/_idset_clean.h"
struct idset *idset_intersect (const struct idset *a, const struct idset *b);



bool idset_has_intersection (const struct idset *a, const struct idset *b);






int idset_alloc (struct idset *idset, unsigned int *val);
void idset_free (struct idset *idset, unsigned int val);
int idset_free_check (struct idset *idset, unsigned int val);
