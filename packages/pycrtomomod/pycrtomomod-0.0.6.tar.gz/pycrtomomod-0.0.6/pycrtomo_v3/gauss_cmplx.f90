SUBROUTINE Gauss_cmplx (a,n,e_flag)    ! Invert matrix by Gauss method

  IMPLICIT NONE
  INTEGER(KIND(4))                                :: n
  COMPLEX(KIND(0D0)),DIMENSION(n,n),INTENT(INOUT) :: a
  COMPLEX(KIND(0D0)),DIMENSION(:), ALLOCATABLE    :: temp
  COMPLEX(KIND(0D0))                              :: c,d 
  INTEGER(KIND(4))                                :: i,j,e_flag
  

  ALLOCATE (temp(n),STAT=e_flag)
  IF (e_flag/=0) THEN
     print*,'error alllocating temp(',n,')=',n*16/(1024**3),' GB'
     RETURN
  END IF
  
  DO i = 1,n
     WRITE (*,'(A,1X,F6.2,A)',ADVANCE='no')ACHAR(13)//ACHAR(9)//ACHAR(9)//&
          'gauss/ ',REAL( i * (100./n)),'%'

     e_flag = -i

     IF (ABS(a(i,i)) < EPSILON(DBLE(d))) RETURN

     d = DCMPLX(1.)/a(i,i)
     temp = a(:,i)
     DO j = 1, n
        c = a(i,j) * d
        a(:,j) = a(:,j) - temp * c
        a(i,j) = c
     END DO
     a(:,i) = temp * (-d)
     a(i,i) = d
  END DO

  e_flag=0
  
END SUBROUTINE Gauss_cmplx
