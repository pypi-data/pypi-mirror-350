!> \file ompmod.f90
!> \brief variable declarations for OpenMP
!> @author Roland Martin 

MODULE ompmod

  IMPLICIT none

  INTEGER,PUBLIC :: TID ! Thread ID
  INTEGER,PUBLIC :: NTHREADS ! Total number of threads
  INTEGER,PUBLIC,PARAMETER :: CHUNK_0=256
  INTEGER,PUBLIC,PARAMETER :: CHUNK_1=2*CHUNK_0
  INTEGER,PUBLIC,PARAMETER :: CHUNK_2=2*CHUNK_1
  INTEGER,PUBLIC,PARAMETER :: CHUNK_3=2*CHUNK_2

  ! chunk pieces for guided scheduling of do loops
  
!!$  !$OMP PARALLEL SHARED(a,b,CHUNK) PRIVATE (i)
!!$  a = 1.
!!$  !$OMP DO SCHEDULE(STATIC, chunk)

!!$  DO i = 1, n
!!$    a(i) = a(i) + b(i)
!!$  END DO

!!$  !$OMP END PARALLEL

END MODULE ompmod
