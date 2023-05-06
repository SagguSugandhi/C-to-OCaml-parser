int cache_fstatat(int fd, char const *file, int st_size, int st_ino, int flag,
                  int *errno, int *fstatat)
{
    if (st_size == -1 && *fstatat != 0)
    {
        st_size = -2;
        st_ino = *errno;
    }
    if (0 <= st_size)
        return 0;
    *errno = (int)st_ino;
    return -1;
}
