!> \file datmod.f90
!> \brief variable delarations for the <I> data</I> part of the inversion
!> @author Roland Martin
!> @date 07/27/2010

MODULE datmod
! 'dat.fin'
!
! Original version by 
! Andreas Kemna                                            07-Oct-1993
!
! Modified F90 module by Roland Martin
!                                       Letzte Aenderung   27-07-2010
!.....................................................................
! Anzahl der Messwerte
  INTEGER (KIND = 4),PUBLIC                             :: nanz
! Nummern der Stromelektroden
  INTEGER (KIND = 4), DIMENSION(:),ALLOCATABLE, PUBLIC  :: strnr
! Stromwerte
  REAL (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC    :: strom
! Nummern der Spannungselektroden
  INTEGER (KIND = 4), DIMENSION(:),ALLOCATABLE, PUBLIC  :: vnr
! Spannungswerte
  COMPLEX (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC :: volt
! Scheinbare Leitfaehigkeiten
  COMPLEX (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC :: sigmaa
! storage
  COMPLEX (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC :: sgmaa2
! Konfigurationsfaktoren
  REAL (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC    :: kfak
! Wichtungsvektor der Phasen
  REAL (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC    :: wmatdp
! Wichtungsvektor der Widerstaende
  REAL (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC    :: wmatdr
! Wichtungsvektor der Komplexen Fehlerellipsen
  REAL (KIND(0D0)), DIMENSION(:),ALLOCATABLE, PUBLIC    :: wmatd_cri
! parameters of resistance error model (dR=stabw0*R+stabm0)
  REAL (KIND(0D0)), PUBLIC                              :: stabw0,stabm0
! parameters of phase error model
! (dp=stabA1*R^stabpB+stabpA2*|P|+stabpA3)
  REAL (KIND(0D0)), PUBLIC                              :: stabp0,stabpA1
  REAL (KIND(0D0)), PUBLIC                              :: stabpB,stabpA2
! Schalter ob 'individual error' (.true.) oder 'uniform weighting'
! (.false.)
  LOGICAL, PUBLIC                                       :: lindiv
! Schalter ob ratio-dataset (.true.)
  LOGICAL, PUBLIC                                       :: lratio
! Schalter ob Polaritaeten gecheckt werden sollen (.true.)
  LOGICAL, PUBLIC                                       :: lpol
! Daten Verrauschen? lnse2 entkoppelt Rauschen und Fehlermodell
  LOGICAL, PUBLIC                                       :: lnse,lnse2
! Initialer Seed der Pseudo Random Sequence (PRS)
  INTEGER (KIND = 4), PUBLIC                            :: iseed
! Noise error model ...
! ... of resistance error model (dnR=nstabw0*nR+nstabm0)
  REAL (KIND(0D0)), PUBLIC                              :: nstabw0,nstabm0
! ... of phase error model 
! (dnp=nstabA1*dnR^nstabpB+nstabpA2*nP+nstabp0)
  REAL (KIND(0D0)), PUBLIC                              :: nstabpB,nstabpA1
  REAL (KIND(0D0)), PUBLIC                              :: nstabpA2,nstabp0
! Anzahl der nicht beruecksichtigten Messwerte
  INTEGER (KIND = 4), PUBLIC                            :: npol

END MODULE datmod
