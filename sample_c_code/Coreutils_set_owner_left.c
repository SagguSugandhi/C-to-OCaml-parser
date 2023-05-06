typedef int uid_t;
typedef int gid_t;

int set_owner(char const *dst_name, int dest_desc, uid_t uid, gid_t gid,
              int fchown_dest_desc_uid_gid, int chown_dst_name_uid_gid,
              int chown_failure_ok_x, int x_require_preserve, int errno)
{
    int r = 1;
    if (dest_desc != -1)
    {
        if (fchown_dest_desc_uid_gid == 0)
        {
            return r;
        }
    }
    else
    {
        if (chown_dst_name_uid_gid == 0)
        {
            return r;
        }
    }

    if (!chown_failure_ok_x)
    {
        if (x_require_preserve)
        {
            return r;
        }
    }

    return r;
}
