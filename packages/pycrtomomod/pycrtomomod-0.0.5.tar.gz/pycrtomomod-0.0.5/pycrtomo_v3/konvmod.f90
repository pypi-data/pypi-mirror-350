MODULE konvmod
!!!$'konv.fin'
!!!$ Andreas Kemna                                          01-Mar-1995
!!!$                                      
!!!$ Last changed       RM                                  Jul-2010
!!!$
!!!$.....................................................................
!!!$Regularisierungsparameter
  REAL(KIND(0D0)), PUBLIC ::     lam

!!!$Maximaler Regularisierungsparameter
  REAL(KIND(0D0)), PUBLIC ::     lammax

!!$ >> RM
!!!$ Post CRI regularization parameter
  REAL(KIND(0D0)), PUBLIC ::     lam_cri
!!$ Starting regularization parameter (CRI)
  REAL(KIND(0D0)), PUBLIC ::     lamnull_cri
!!$ Starting regularization parameter (FPI)
  REAL(KIND(0D0)), PUBLIC ::     lamnull_fpi
!!$ << RM

!!$ >> RM
!!!$ Reference model regularization lambda (currently its a factor for lam)
  REAL(KIND(0D0)), PUBLIC ::     lam_ref
!!!$ switch if we want the absolute or just the gradient regularized
  INTEGER, PUBLIC         ::     lam_ref_sw
!!! << RM

!!!$Fester Regularisierungsparameter
  REAL(KIND(0D0)), PUBLIC ::     lamfix

!!!$Schrittweitenfaktor, maximale Anzahl der Schritte
  REAL(KIND(0D0)), PUBLIC ::     dlam,dlalt
  INTEGER(KIND = 4),PUBLIC ::     nlam

!!!$Parameter "a", "initial/final step factor"
  REAL(KIND(0D0)), PUBLIC ::     alam
  REAL(KIND(0D0)), PUBLIC ::     fstart
  REAL(KIND(0D0)), PUBLIC ::     fstop

!!!$Step-length der Modellverbesserung
  REAL(KIND(0D0)), PUBLIC ::     step

!!!$Step-length der vorherigen Iteration
  REAL(KIND(0D0)), PUBLIC ::     stpalt

!!!$Mindest-step-length
  REAL(KIND(0D0)), PUBLIC ::     stpmin

!!!$Schalter zur Steuerung der Regularisierung und der step-length-Wahl
  LOGICAL,PUBLIC  ::     llam,lstep,ldlami,ldlamf
!!!$wenn llamf >0 ist wird ein fixes Lambda gesetzt, llamf = BTEST(llamf,1) fuer lambda 
!!!$ cooling 
  INTEGER,PUBLIC  ::     llamf
!!!$Schalter ob volle step-length angebracht werden soll
  LOGICAL,PUBLIC  ::     lfstep

!!!$Daten-RMS
  REAL(KIND(0D0)), PUBLIC ::     nrmsd

!!!$Daten-RMS der vorherigen Iteration
  REAL(KIND(0D0)), PUBLIC ::     rmsalt

!!!$Daten-RMS des vorherigen "Regularisierungsschritts"
  REAL(KIND(0D0)), PUBLIC ::     rmsreg

!!!$Daten-Misfit insgesamt (in der objective function),
!!!$Misfit der Betraege, Misfit der Phasen
  REAL(KIND(0D0)), PUBLIC ::     rmssum,betrms,pharms

!!!$Roughness
  REAL(KIND(0D0)), PUBLIC ::     rough

!!!$Minimaler Daten-RMS
  REAL(KIND(0D0)), PUBLIC ::     nrmsdm

!!!$Minimaler Quotient zweier aufeinanderfolgender Daten-RMS-Werte
!!!$bzw. zwischen tatsaechlichem und minimalem Daten-RMS
  REAL(KIND(0D0)), PUBLIC ::     mqrms

!!!$Minimale "L1-ratio" (Grenze der "robust inversion")
  REAL(KIND(0D0)), PUBLIC ::     l1min

!!!$"L1-ratio"
  REAL(KIND(0D0)), PUBLIC ::     l1rat

!!!$Norm des Verbesserungsvektors (stepsize)
  REAL(KIND(0D0)), PUBLIC ::     bdpar

!!!$Minimale step size 
  REAL(KIND(0D0)), PUBLIC ::     bdmin

!!!$Felddimensionen in x- und z-Richtung
  INTEGER(KIND = 4),PUBLIC ::     nx,nz

!!!$Maximale Anzahl der Iterationen
  INTEGER(KIND = 4),PUBLIC ::     itmax

!!!$Iterationsindex
  INTEGER(KIND = 4),PUBLIC ::     it

!!!$Index des Regularisierungsschritts
  INTEGER(KIND = 4),PUBLIC ::     itr

!!!$Parameter zur Glaettung in x- und z-Richtung
!!!$(=0 bedeutet keine Glaettung in der jeweiligen Richtung)
  REAL(KIND(0D0)), PUBLIC ::     alfx,alfz
!!!$MGS beta
  REAL(KIND(0D0)), PUBLIC ::     betamgs

!!!$Schalter ob "robust inversion" durchgefuehrt werden soll
  LOGICAL,PUBLIC  ::     lrobust

!!$cdiff+<
!!!$Schalter ob "difference inversion" durchgefuehrt werden soll
  LOGICAL,PUBLIC  ::     ldiff
!!$cdiff+>
!!!$Schalter ob positive Phasen auf Null korrigiert werden sollen
  LOGICAL,PUBLIC  ::     lphi0
!!!$Schalter ob "final phase improvement" durchgefuehrt werden soll
  LOGICAL,PUBLIC  ::     lfphai
!!!$Schalter ob "final phase improvement" mit homogenem phasenwert startet
  LOGICAL,PUBLIC  ::     lffhom
!!$c	triang>
!!!$Schalter für die Triangularisierungsinversion
  INTEGER(KIND = 4),PUBLIC :: ltri
!!$c	triang<	
!!!$Schalter ob prior model vorhanden
  LOGICAL,PUBLIC  :: lprior
!!!$ >> RM ref model regu
!!!$switch is true for reference model regularization (DAMPING)
  LOGICAL,PUBLIC  :: lw_ref
!!!$ << RM ref model regu
!!!$Schalter ob prior model verrauschen
  LOGICAL,PUBLIC  :: lnsepri
!!!$Schalter ob Summe der Sensitivitaeten aller Messungen ausgegeben
!!!$werden soll
  LOGICAL,PUBLIC  :: lsens
!!!$Schalter fuer Resolution matrix
  LOGICAL,PUBLIC  :: lres
!!!$Schalter fuer posterior cov
  LOGICAL,PUBLIC  :: lcov1
!!!$Schalter fuer posterior cov
  LOGICAL,PUBLIC  :: lcov2
!!!$Mega schalter, wird binaer getestet
  INTEGER(KIND = 4),PUBLIC :: mswitch
!!!$Schalter für ols Loeser
  LOGICAL,PUBLIC  :: lgauss
!!!$Schalter ob experimentelles variogram berechnet werden soll
  LOGICAL,PUBLIC  :: lvario
!!!$ Verbose output switch
  LOGICAL,PUBLIC  :: lverb
!!!$ Verbose output of full resoultion, cm0, cm0_inv, full covariance, etc..
  LOGICAL,PUBLIC  :: lverb_dat
!!!$ lsytop = .NOT.BTEST (mswitch,8)  disables sy top check of 
!!$ no flow boundary electrodes for enhanced beta calculation (bsytop). 
!!$  This is useful for including topographical effects and should be used
  LOGICAL,PUBLIC  ::     lsytop
!!!$ switch to regard error ellipses in complex plane 
!!!$ is srt false as default if we have FPI but may be overwritten with
!!!$ mswitch + 32 setting it to true
  LOGICAL, PUBLIC ::     lelerr

END MODULE konvmod
