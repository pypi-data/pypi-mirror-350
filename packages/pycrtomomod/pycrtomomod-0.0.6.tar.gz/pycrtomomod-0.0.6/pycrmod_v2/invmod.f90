!> \file invmod.f90
!> \brief variable delarations for the inversion algorithm
!> \details Replacement of former 'inv.fin' 
!> @author Andreas Kemna
!> @date 04/02/1994, last change 07/27/2010
MODULE invmod
!!$c  'inv.fin'
!!$c
!!$c Original version by 
!!$c Andreas Kemna                                            02-Apr-1994
!!$c
!!$c Modified F90 module by Roland Martin
!!$c                                       Letzte Aenderung   27-07-2010
!!$c 
!!$c.....................................................................
!!!$ Datenvektor
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: dat
!!$c Parametervektor
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: par
!!$c Verbesserungsvektor
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: dpar
!!$ storage
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: dpar2
!!$c data vector for difference inversion
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: d0
!!$c parameter vector for diff inv
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: m0
!!$c model vector for diff inv
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: fm0
!!!$ >> RM ref model regu
!!$c parameter vector for reference model regularization
  COMPLEX(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE   :: m_ref
!!!$ << RM ref model regu
!!!$ the reference vector is of the same length as par or m0
!!$c data weighting (data covariance) matrix (diag)
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE      :: wmatd
!!$c storage
  REAL(KIND(0D0)),PUBLIC,DIMENSION(:),ALLOCATABLE      :: wmatd2
!!$c parameter variance
  REAL(KIND(0D0)),PUBLIC                               :: par_vari
!!$c Hilfsfeld, bestimmt welche Daten beruecksichtigt (=1) bzw. nicht
!!$c beruecksichtigt (=0) werden
  INTEGER(KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE    :: wdfak
!!$c Schalter ob reine Phaseninversion durchgefuehrt werden soll
  LOGICAL(KIND = 4),PUBLIC                             :: lfpi
!!!$ Auxiliary field accounts for if the background value is used as
!!$ hard reference regularization, i.e. RTR m + I(m - m0), where 
!!!$ each entry of m0 is multiplied with wmfak to cancel values out
  INTEGER (KIND = 4),PUBLIC,DIMENSION(:),ALLOCATABLE   :: wmfak

END MODULE invmod
