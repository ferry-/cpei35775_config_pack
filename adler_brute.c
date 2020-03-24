#include "zlib/adler32.c"
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <math.h>

#define BASE 65521U     /* largest prime smaller than 65536 */
#define NMAX 5552
/* NMAX is the largest n such that 255n(n+1)/2 + (n+1)(BASE-1) <= 2^32-1 */

#define DO1(buf,i)  {adler += (buf)[i]; sum2 += adler;}
#define DO2(buf,i)  DO1(buf,i); DO1(buf,i+1);
#define DO4(buf,i)  DO2(buf,i); DO2(buf,i+2);
#define DO8(buf,i)  DO4(buf,i); DO4(buf,i+4);
#define DO16(buf)   DO8(buf,0); DO8(buf,8);

#define MOD(a) a %= BASE
#define MOD28(a) a %= BASE
#define MOD63(a) a %= BASE

inline uLong adler32_short(uLong adler, const Bytef *buf, z_size_t len) {
	unsigned long sum2;
	unsigned n;

	/* split Adler-32 into component sums */
	sum2 = (adler >> 16) & 0xffff;
	adler &= 0xffff;

	/* do length NMAX blocks -- requires just one modulo operation */
    while (len >= NMAX) {
        len -= NMAX;
        n = NMAX / 16;          /* NMAX is divisible by 16 */
        do {
            DO16(buf);          /* 16 sums unrolled */
            buf += 16;
        } while (--n);
        MOD(adler);
        MOD(sum2);
    }

    /* do remaining bytes (less than NMAX, still just one modulo) */
    if (len) {                  /* avoid modulos if none remaining */
        while (len >= 16) {
            len -= 16;
            DO16(buf);
            buf += 16;
        }
        while (len--) {
            adler += *buf++;
            sum2 += adler;
        }
        MOD(adler);
        MOD(sum2);
    }

    /* return recombined sums */
    return adler | (sum2 << 16);
}	

int main(int argc, char **argv) {
	FILE *f = fopen(argv[1], "rb");
	fseek(f, 0, SEEK_END);
	long len = ftell(f);
	rewind(f);

	uint8_t *buf = malloc(len);
	assert( fread(buf, 1, len, f) == len );

	fclose(f);

	printf("read %ld bytes\n", len);
	const uint64_t chk_sum = 0x20a85587;
	int64_t best_diff = 0xFFFFFFFF;
	int64_t best_adler = 0;
	int64_t best_sum = 0;
	for(uint64_t val = 0; val <= 0xFFFFFFFF; val++) {
		if(!(val & 0x000FFFFF)) {
			printf("at 0x%lx00000\n", val >> 20);
		}
		int64_t sum = adler32_short(val, buf, len);
		int64_t diff = abs( (int64_t)chk_sum - (int64_t)sum);

		if(diff < best_diff) {
			best_diff = diff;
			best_adler = val;
			best_sum = sum;
			printf("better: v=%lx, diff=%lx, ch=%lx\n", val, diff, sum);
		}
		if(diff == 0) {
			break;
		}
	}
	printf("better: v=%lx, diff=%lx, ch=%lx\n", best_adler, best_diff, best_sum);
	return 0;
}
