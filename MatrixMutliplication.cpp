#include <bits/stdc++.h>
#include <chrono>
using namespace std;

// Edit MACROs here, according to your Matrix Dimensions for mat1[SIZE][SIZE] and mat2[SIZE][SIZE]
#define SIZE 1000

void mulMat(unsigned long int **mat1, unsigned long int **mat2) {
    unsigned long int** rslt = new unsigned long int*[SIZE];

    for (unsigned long int i = 0; i < SIZE; i++)
        rslt[i] = new unsigned long int[SIZE];

    // std::cout<< "Multiplication of given two matrices is:" << endl;

    for (unsigned long int i = 0; i < SIZE; i++) {
        for (unsigned long int j = 0; j < SIZE; j++) {
            rslt[i][j] = 0;

            for (unsigned long int k = 0; k < SIZE; k++) {
                rslt[i][j] += mat1[i][k] * mat2[k][j];
            }
            // std::cout<< rslt[i][j] <<" ";
        }
        // std::cout<<"\n";
    }
}


int main()
{
    // Square Matrices
    // SIZE = 4, SIZE = 4 and SIZE = 4, SIZE = 4 (Update these values in MACROs)
    std::cout<< "Multiplication of given two matrices with size: " << SIZE << "x" << SIZE << endl;
    unsigned long int** mat1 = new unsigned long int*[SIZE];
    unsigned long int** mat2 = new unsigned long int*[SIZE];

    for (unsigned long int i = 0; i < SIZE; i++)
        mat1[i] = new unsigned long int[SIZE];

    for (unsigned long int i = 0; i < SIZE; i++)
        mat2[i] = new unsigned long int[SIZE];
        /*
    // Rectangular Matrices
    // SIZE = 3, SIZE = 4 and SIZE = 4, SIZE = 3 (Update these values in MACROs)
    unsigned long int mat1[SIZE][SIZE] = {
            {1, 1, 1, 1},
            {2, 2, 2, 2},
            {3, 3, 3, 3}
    };
 
    unsigned long int mat2[SIZE][SIZE] = {
            {1, 1, 1},
            {2, 2, 2},
            {3, 3, 3},
            {4, 4, 4}
    };
    */

    for (unsigned long int i = 0; i < SIZE; i++)
        for (unsigned long int j = 0; j < SIZE; j++)
            mat1[i][j] = j + 1;

    for (unsigned long int i = 0; i < SIZE; i++)
        for (unsigned long int j = 0; j < SIZE; j++)
            mat2[i][j] = j + 1;
 
    auto start = chrono::high_resolution_clock::now();
    // unsync the I/O of C and C++.
    ios_base::sync_with_stdio(false);

    mulMat(mat1, mat2);

    auto end = chrono::high_resolution_clock::now();
 
     // Calculating total time taken by the program.
    double time_taken = 
      chrono::duration_cast<chrono::nanoseconds>(end - start).count();
  
    time_taken *= 1e-9;
  
    cout << "Time taken by program is : " << fixed 
         << time_taken << setprecision(9);
    cout << " sec" << endl;
    return 0;
}