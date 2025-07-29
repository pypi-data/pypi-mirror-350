# 0 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 0 "<command-line>" 2
# 1 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
# 20 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
struct hostlist *hostlist_create (void);

void hostlist_destroy (struct hostlist *hl);





struct hostlist *hostlist_decode (const char *s);




char *hostlist_encode (struct hostlist *hl);




struct hostlist *hostlist_copy (const struct hostlist *hl);





int hostlist_append (struct hostlist *hl, const char *hosts);







int hostlist_append_list (struct hostlist *hl1, struct hostlist *hl2);





const char * hostlist_nth (struct hostlist * hl, int n);
# 68 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
int hostlist_find (struct hostlist * hl, const char *hostname);
# 82 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
struct hostlist_hostname *hostlist_hostname_create (const char *hostname);




void hostlist_hostname_destroy (struct hostlist_hostname *hn);
# 97 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
int hostlist_find_hostname (struct hostlist *hl, struct hostlist_hostname *hn);






int hostlist_delete (struct hostlist * hl, const char *hosts);




int hostlist_count (struct hostlist * hl);







void hostlist_sort (struct hostlist * hl);




void hostlist_uniq (struct hostlist *hl);
# 132 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
const char * hostlist_first (struct hostlist *hl);
# 142 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
const char * hostlist_last (struct hostlist *hl);
# 152 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
const char * hostlist_next (struct hostlist *hl);
# 161 "/__w/flux-python/flux-python/src/_hostlist_clean.h"
const char * hostlist_current (struct hostlist *hl);





int hostlist_remove_current (struct hostlist *hl);
