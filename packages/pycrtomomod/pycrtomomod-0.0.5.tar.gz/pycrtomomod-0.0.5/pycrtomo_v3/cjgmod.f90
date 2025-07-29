!> \file cjgmod.f90
!> \brief variable delarations for the conjugate gradient (CG) solver in <I>cg_mod</I>
!> @author Roland Martin
!> @date 07/27/2010

MODULE cjgmod
!! ------------------------------------------------------------------
! Module for the data of Conjugate gradient to solve Linear systems
! Copyright by Andreas Kemna   2010
! Edited first by Roland Martin                          27-07-2010
! -------------------------------------------------------------------
  USE datmod,ONLY:nanz
  USE modelmod,ONLY:manz

  IMPLICIT none
!!! COMPLEX CASE
!! auxiliary vector stores product of A*(Ap)
  COMPLEX(KIND(0D0)),ALLOCATABLE,DIMENSION(:),PUBLIC  :: ap
! Right hand side (RHS) vector
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE  :: bvec
! residual vector
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE  :: rvec
! intermediate vector (stores Ap)
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE  :: pvec

!!! DC CASE
!c assist vectors
  REAL(KIND(0D0)),ALLOCATABLE,DIMENSION(:),PUBLIC     :: apdc
! dc real valued version ov RHS
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: bvecdc
! residual vector dc
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: rvecdc
! intermediate vector (stores Ap) dc
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: pvecdc

!! variables for every case
! CG residuals
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: cgres
! storage
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: cgres2
! preconditioning factors
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE     :: cgfac
! CG Epsilon
  REAL(KIND(0D0)),PUBLIC                              :: eps
! maximum number of CG steps
  INTEGER (KIND = 4),PUBLIC                           :: ncgmax
! actual number of CG steps..
  INTEGER (KIND = 4),PUBLIC                           :: ncg

  PUBLIC :: con_cjgmod ! constructor
  PUBLIC :: des_cjgmod ! destructor

CONTAINS 


  SUBROUTINE con_cjgmod (mycase,errtxt,errnr) ! constructor of cjgmod
    INTEGER (KIND=4),INTENT (IN) :: mycase ! mycase can have 3 values
!! 0:  allocate global cgres and bvec which should be called from update
    CHARACTER (*),INTENT(INOUT)  :: errtxt
    INTEGER (KIND=4),INTENT(OUT) :: errnr

    SELECT CASE (mycase)
    CASE (1) !global variables
       errtxt = 'allocation problem cgres'
       ALLOCATE (cgres(ncgmax+1),STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'allocation problem cgres2'
       ALLOCATE (cgres2(ncgmax+1),STAT=errnr)
       IF (errnr /= 0) RETURN
!!  CJG aux vectors and update
       errtxt = 'allocation problem bvec'
       ALLOCATE (bvec(manz),STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'allocation problem cgfac'
       ALLOCATE (cgfac(manz),STAT=errnr)
       IF (errnr /= 0) RETURN
    CASE (2)! ERT or FPI
! getting further CJG variables
       errtxt = 'allocation problem pvecdc'
       ALLOCATE (pvecdc(manz),STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'allocation problem bvecdc'
       ALLOCATE (bvecdc(manz),STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'allocation problem rvecdc'
       ALLOCATE (rvecdc(manz),STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'allocation problem apdc'
       ALLOCATE (apdc(nanz),STAT=errnr)
    CASE(3) ! COMPLEX _only_
       errtxt = 'allocation problem rvec'
       ALLOCATE (rvec(manz),STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'allocation problem pvec'
       ALLOCATE (pvec(manz),STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'allocation problem ap'
       ALLOCATE (ap(nanz),STAT=errnr)
    END SELECT

  END SUBROUTINE con_cjgmod

  SUBROUTINE des_cjgmod (mycase,errtxt,errnr) ! destructor of cjgmod
    INTEGER (KIND=4),INTENT (IN) :: mycase
    CHARACTER (*),INTENT(INOUT)  :: errtxt
    INTEGER (KIND=4),INTENT(OUT) :: errnr

    SELECT CASE (mycase)
    CASE (1) !global variables
       errtxt = 'deallocation problem cgres'
       DEALLOCATE (cgres,STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'deallocation problem cgres2'
       DEALLOCATE (cgres2,STAT=errnr)
       IF (errnr /= 0) RETURN
!!  CJG aux vectors and update
       errtxt = 'deallocation problem bvec'
       DEALLOCATE (bvec,STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'deallocation problem bvec'
       DEALLOCATE (cgfac,STAT=errnr)
       IF (errnr /= 0) RETURN
    CASE (2)! ERT or FPI
! getting further CJG variables
       errtxt = 'deallocation problem pvecdc'
       DEALLOCATE (pvecdc,STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'deallocation problem bvecdc'
       DEALLOCATE (bvecdc,STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'deallocation problem rvecdc'
       DEALLOCATE (rvecdc,STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'deallocation problem apdc'
       DEALLOCATE (apdc,STAT=errnr)
    CASE(3) ! COMPLEX _only_
       errtxt = 'deallocation problem rvec'
       DEALLOCATE (rvec,STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'deallocation problem pvec'
       DEALLOCATE (pvec,STAT=errnr)
       IF (errnr /= 0) RETURN
       errtxt = 'deallocation problem ap'
       DEALLOCATE (ap,STAT=errnr)
    END SELECT

  END SUBROUTINE des_cjgmod

END MODULE cjgmod
