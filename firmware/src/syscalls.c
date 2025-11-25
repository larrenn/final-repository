#include <errno.h>
#include <sys/stat.h>

// Минимальные системные вызовы для embedded
void _exit(int status) {
    while(1); // Бесконечный цикл при выходе
}

int _close(int file) {
    return -1;
}

int _fstat(int file, struct stat *st) {
    st->st_mode = S_IFCHR;
    return 0;
}

int _isatty(int file) {
    return 1;
}

int _lseek(int file, int ptr, int dir) {
    return 0;
}

int _read(int file, char *ptr, int len) {
    return 0;
}

int _write(int file, char *ptr, int len) {
    // Для Renode - вывод через UART/semihosting
    return len;
}

int _getpid(void) {
    return 1;
}

int _kill(int pid, int sig) {
    errno = EINVAL;
    return -1;
}

void *_sbrk(int incr) {
    extern char end; // Определяется линкером
    static char *heap_end = 0;
    char *prev_heap_end;

    if (heap_end == 0) {
        heap_end = &end;
    }
    prev_heap_end = heap_end;
    heap_end += incr;
    return prev_heap_end;
}
