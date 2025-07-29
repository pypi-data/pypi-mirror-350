SUBROUTINE chold(a,p,n,ierr,lverb)
!!$c-----------------------------------------------------------------
!!$c
!!$c                      Cholesky Decomposition
!!$c                      **********************
!!$c
!!$c This subroutine calculates the lower triangular matrix L which,
!!$c when multiplied by its own transpose, gives the symmetric 
!!$c matrix A. From Numerical recipies (Press et al 2003)
!!$c 
!!$c Changed and put into this format by R. Martin 2010
!!$c
!!$c**********          NOTE           ***************************
!!$c chold In this form needs only the upper triangular part of a
!!$c and stores L in the lower part.
!!$c P contains the diagonal entries (EVs)
!!$c**************************************************************
!!$c INPUT VARIABLES:
!!$c
!!$c   a(n,n) Symmetric positive definite nxn matrix
!!$c          to be decomposed
!!$c          Upper part still contains A and lower part is filled with L
!!$c   p(n)   Eigenvalues of a 
!!$c   ierr   Error code:  ierr=0 - no errors; ierr=1 - matrix a
!!$c          is not positive definite
!!$c NO EXTERNAL REFERENCES:
!!$c------------------------------------------------------------
  USE ompmod

  IMPLICIT none

  INTEGER,INTENT (IN)                             :: n
  REAL (KIND(0D0)), DIMENSION (n,n),INTENT(INOUT) :: a
  REAL (KIND(0D0)), DIMENSION (n),INTENT(OUT)     :: p
  LOGICAL,INTENT(IN)                              :: lverb
  INTEGER, INTENT (OUT)                           :: ierr
  INTEGER                                         :: i,k,j,count

  ierr = 0
  count = 0

  DO j = 1, n

     count = count + 1
     
     IF (lverb) WRITE (*,'(A,t25,F6.2,A)',ADVANCE='no')&
          ACHAR(13)//'Factorization',REAL( count * (100./n)),'%'
     DO k = 1, j - 1
        DO i = j, n
           a(i,j) = a(i,j) - a(i,k) * a(j,k)
        END DO
     END DO

     IF (a(j,j) <= 0) THEN
        PRINT*,'CHOLD:: - not positive definite', j,a(j,j)
        ierr = -j
        STOP
     END IF
     
     p(j) = DSQRT(a(j,j))
     a(j,j) = p(j)
     DO i = j + 1, n
        a(i,j) = a(i,j) / p(j)
     END DO
  END DO

END SUBROUTINE chold
