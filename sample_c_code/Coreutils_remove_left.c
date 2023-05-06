int cache_fstatat(int fd, char const *file, int st_size, int st_ino, int flag,
                  int *errno, int *fstatat)
{
    if (st_size == -1 && *fstatat != 0)
        st_size = -1 - *errno;
    if (0 <= st_size)
        return 0;
    *errno = -1 - st_size;
    return -1;
}
