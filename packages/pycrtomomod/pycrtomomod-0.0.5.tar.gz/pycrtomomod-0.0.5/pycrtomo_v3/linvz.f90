SUBROUTINE linvz(a,p,n)
!!$c-----------------------------------------------------------------
!!$c
!!$c                Inverse of a Lower Triangular Matrix
!!$c                ************************************
!!$c
!!$c This subroutine finds the inverse of factorized Lower triangular
!!$c 
!!$c from Numerical recipies (Press et al 2003)
!!$c 
!!$c Changed and put into this format by R. Martin 2010
!!$c
!!$c
!!!$ in order to find the inverse of A we still need to compute 
!!!$ (L^-1)^T L^-1 , since
!!!$ (L^-1)^T L^-1 L L^T = I
!!!$
!!$c INPUT VARIABLES:
!!$c
!!$c   u(n,n)  Upper triangular matrix from chold
!!$c           which stores the inverse of A^-1 = (L^-1)^T L^-1
!!$c           in the upper part..
!!$c   p(n)    Eigenvalues of former A
!!$c   n       leading dimension 
!!$c-----------------------------------------------------------------
  IMPLICIT none
  
  INTEGER,INTENT (IN)                  :: n
  COMPLEX (KIND(0D0)), DIMENSION (n,n) :: a
  COMPLEX (KIND(0D0)), DIMENSION (n)   :: p
  COMPLEX (KIND(0D0))                  :: s
  INTEGER                              :: k,i,j


  DO i= 1 , n
     WRITE (*,'(A,t25,F6.2,A)',ADVANCE='no')&
          ACHAR(13)//'/ ',REAL( (i) * (100./n)),'%'

     a(i,i) = 1. / p(i)! main diagonal of L^-1

     DO j = i+1 , n

        s = 0.

        DO k = i , j-1

           s = s - a(j,k) * a(k,i)

        END DO

        a(j,i) = s / p(j) ! filling lower triangle of L^-1
        
        a(i,j) = 0. ! upper triangle eq zero for sum

     END DO

  END DO

!!$ --------------- own part -------------------
!!$ this part makes the inverse of A by MATMUL 
!!$ of L^-T L-^1 into the
!!$ upper part of a
!!$ --------------------------------------------

  DO i = 1, n
     WRITE (*,'(A,t25,F6.2,A)',ADVANCE='no')&
          ACHAR(13)//'/ ',REAL( (n-i) * (100./n)),'%'

     a(i,i) = a(i,i) * a(i,i) 

     DO k = i+1 , n

        a(i,i) = a(i,i) + a(k,i) * a(k,i) ! main diagonal

     END DO

     DO j = i + 1, n ! fills upper triangle with (L^-1)^T L^-1
        
        DO k = j, n

           a(i,j) = a(i,j) + a(k,i) * a(k,j) 

        END DO
     END DO

  END DO

END SUBROUTINE linvz
    
