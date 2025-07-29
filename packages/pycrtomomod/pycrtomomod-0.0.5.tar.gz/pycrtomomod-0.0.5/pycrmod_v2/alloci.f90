!> \file alloci.f90
!> \brief Memory allocation module
!> @author Andreas Kemna
!> @date 01/24/1997, last change 11/13/1997

MODULE alloci
!!$Andreas Kemna                                            24-Jan-1997
!!$                                      Letzte Aenderung   13-Nov-1997
!!$COMPLEX CASE
!> FE stiffness matrix
  COMPLEX (KIND(0D0)), DIMENSION(:), ALLOCATABLE, PUBLIC     :: a
!> potential values of all electrode locations in wave number space
  COMPLEX (KIND(0D0)), DIMENSION(:,:,:), ALLOCATABLE, PUBLIC :: kpot
!> potential values of alle electrodes in real space
  COMPLEX (KIND(0D0)), DIMENSION(:,:), ALLOCATABLE, PUBLIC   :: hpot
!> sensitivities
  COMPLEX (KIND(0D0)), DIMENSION(:,:), ALLOCATABLE, PUBLIC   :: sens
!> coverages
  REAL (KIND(0D0)), DIMENSION(:), ALLOCATABLE, PUBLIC   :: csens
!!$DC-CASE
!> FE stiffness matrix, DC case
  REAL (KIND(0D0)), DIMENSION(:), ALLOCATABLE, PUBLIC        :: adc
!> potential values of all electrode locations in wave number space, DC case
  REAL (KIND(0D0)), DIMENSION(:,:,:),ALLOCATABLE, PUBLIC     :: kpotdc
!> potential values of alle electrodes in real space, DC case
  REAL (KIND(0D0)), DIMENSION(:,:),ALLOCATABLE, PUBLIC       :: hpotdc
!> sensitivities
  REAL (KIND(0D0)), DIMENSION(:,:),ALLOCATABLE, PUBLIC       :: sensdc
!> real symmetric data covariance
  REAL (KIND(0D0)), DIMENSION(:,:), ALLOCATABLE, PUBLIC      :: cov_d
!> regularization matrix
  REAL (KIND(0D0)), DIMENSION(:,:),ALLOCATABLE, PUBLIC       :: smatm
!> PSR fields
  REAL (KIND(0D0)), DIMENSION(:), ALLOCATABLE, PUBLIC        :: rnd_r,rnd_p
!> real symmetric matrix to compute general inverses
  REAL (KIND(0D0)), DIMENSION(:,:), ALLOCATABLE, PUBLIC   :: ata
!> general symmetric transpose matrix (regularized) to compute general inverses
  REAL (KIND(0D0)), DIMENSION(:,:), ALLOCATABLE, PUBLIC   :: ata_reg
!> inverse matrix (may be resolution matrix or the MCM)
  REAL (KIND(0D0)), DIMENSION(:,:), ALLOCATABLE, PUBLIC   :: cov_m
END MODULE alloci
