#include <stdio.h>
#include <stdlib.h>

void allocateMemory(int **buffer, size_t size)
{	
    *buffer = malloc(sizeof(int*));
}

int main(){
    int *int_ptr = NULL;
    allocateMemory(&int_ptr, sizeof(int));
    *int_ptr = 3;
    return 0;
}
