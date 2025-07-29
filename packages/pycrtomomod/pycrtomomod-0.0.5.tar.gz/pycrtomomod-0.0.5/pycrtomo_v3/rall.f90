!> \file rall.f90
!> \brief Read all parameters for the inversion.
!> \details The file formats are as follows (comments after the vertical bar):
!>      - grid file (delem):
!>          \verbatim
!>      1209           3          49  | nr of nodes, nr of element types, bandwidth of FE matrix)
!>         8        1140           4  | element type description, nr of elements, nr of nodes per element:)
!>        12          30           2  | ... element 5: triangles, 8: quadrilaterals (e.g., rectangles!))
!>        11         106           2  | ...        11: mixed boundary, 12: von Neumann boundary )
!>         1      -5.000       0.000  | node nr, x value, z value
!>         2      -3.596       0.000  | ...
!>         3      -2.465       0.000  | ...
!>         :           :           :  | ... 1206 more
!>        50   51    2    1           | edge node numbers of first element of type 8 (rectangle)
!>        51   52    3    2           | counter-clockwise notation starting at bottom left
!>         :    :    :    :           | ... 1138 more
!>         2    1                     | edge node numbers of first element of type 12 (line boundary)
!>         :    :                     | ... 29 more
!>         1   50                     | edge node numbers of first element of type 11 (line boundary)
!>         :    :                     | ... 105 more
!>         1                          | boundary element numbers to build a closed surface
!>         :                          | ... 135 more
!>          \endverbatim
!>      - electrode file (delectr):
!>          \verbatim
!>         31    | total number of electrodes
!>        564    | node number of 1st electrodes
!>          :    | ... 30 more
!>          \endverbatim
!>       These are the nicely ordered version of the grid and electrode file. They can be transformed into the corresponding high speed versions with the <I> CutMcK </I> command.
!>      - measurement file (dstrom):
!>          \verbatim
!>          812                       | nr of measurements
!>        10002 40003   283.1  0.00   | encoded current electr, encoded volt electr,...
!>        10002 50004   61.42  0.00   | recorded voltages and phase.
!>        10002 60005   6.364  0.00   | encoding: C1*10000+C2 same with P1 P2
!>          \endverbatim
!>
!> @author Andreas Kemna
!> @date 03/01/1995, last change 08/20/2007

SUBROUTINE rall(kanal,delem,delectr,dstrom,drandb,&
     dsigma,dvolt,dsens,dstart,dd0,dm0,dfm0,lagain)

    !    Unterprogramm zum Einlesen der benoetigten Variablen.
    !    Andreas Kemna 01-Mar-1995
    !    Letzte Aenderung 20-Aug-2007
    !....................................................................

    USE make_noise
    USE variomodel
    USE femmod
    USE datmod
    USE invmod
    USE cjgmod
    USE sigmamod
    USE electrmod
    USE modelmod
    USE elemmod
    USE wavenmod
    USE randbmod
    USE errmod
    USE konvmod
    USE pathmod
    USE get_ver, ONLY:version

    IMPLICIT NONE

    ! EIN-/AUSGABEPARAMETER:

    !> FID number
    INTEGER (KIND = 4) ::     kanal

    !> grid file
    CHARACTER (80) :: delem

    !> electrodes file
    CHARACTER (80) :: delectr

    !> configurations file
    CHARACTER (80) :: dstrom

    !> complex resistivity model file
    CHARACTER (80) :: dsigma

    !> measurements file
    CHARACTER (80) :: dvolt

    !> sensitivities file
    CHARACTER (80) :: dsens

    !> starting model file
    CHARACTER (80) :: dstart
    CHARACTER (80) :: dd0
    CHARACTER (80) :: dm0
    CHARACTER (80) :: dfm0
    CHARACTER (80) :: drandb

    !> run another inversion?
    LOGICAL ::     lagain
    LOGICAL ::     lsto

    ! check whether the file format is crtomo konform or not..
    LOGICAL ::    crtf

    ! check whether a file exists..
    LOGICAL ::    exi

    ! decoupling.dat exists?
    ! LOGICAL ::    decexi
    !!! INTEGER(KIND = 4), DIMENSION(:, :),ALLOCATABLE :: edecoup
    !!! REAL(KIND(0D0)), DIMENSION(:),ALLOCATABLE :: edecstr
    !!! INTEGER (KIND = 4) ::  decanz

    !!!$.....................................................................

    !!!$     PROGRAMMINTERNE PARAMETER:

    !!!$     Indexvariable
    INTEGER (KIND = 4) ::     i

    !!!$     Pi
    REAL(KIND(0D0))   ::     pi

    !!!$     diff+<
    REAL(KIND(0D0)),DIMENSION(:),ALLOCATABLE   :: dum,dum2
    REAL(KIND(0D0))                            :: dum3
    INTEGER(KIND = 4),DIMENSION(:),ALLOCATABLE :: idum,ic,ip
    INTEGER (KIND = 4) ::  nanz0,j,j0
    !!!$     diff+>

    !!!$     ak Inga
    INTEGER (KIND = 4) ::  elec1,elec2,elec3,elec4
    !!!$.....................................................................

    pi = dacos(-1d0)

    !!!$     'crtomo.cfg' EINLESEN
    fetxt = 'crtomo.cfg'
    errnr = 3
    !!!$#################DEFAULTS ########################
    !!!$###  switches
    !!!$     ro        lsr    = .false.
    !!!$     ro        lpol   = .true.
    !!!$     ro        lfphai = .true.
    !!!$     ro        lrho0  = .false.
    !!!$     akERT2003
    !!!$     ak        ld!!!$    = .true.
    !!!$     ak        lsr    = .false.
    !!!$     ak        lpol   = .false.
    !!!$     Sonstiges
    !!!$     diff+<
    lsr    = .FALSE.
    lpol   = .FALSE.
    lindiv = .FALSE.
    !!!$     ak
    !!!$     'dstart'
    lstart = .FALSE.
    dstart = ' '
    !!!$     ak        lstart = .true.
    !!!$     ak        dstart = '..\..\strasbrg\9610\plane45\mod\rho0.dat'
    ltri   = 0
    lsto = .FALSE.            !default--
    !!!$     "Force negative phase" ?
    !!!$     sandra        lphi0 = .true.
    lphi0 = .FALSE.
    !!!$     ak        lphi0 = .false.
    !!!$     "ratio-dataset" ?
    lratio = .FALSE.
    !!!$     ak        lratio = .true.
    !!!$     final phase improvement setzt phase zueruck auf homogenes modell
    lffhom = .FALSE.
    !!!$     Daten Rauschen vom Fehlermodell entkoppeln ?
    lnse2 = .FALSE.
    !!!$     Regularisierung mit prior modell?
    lprior = .FALSE.
    !!!$######values..
    !!!$     FIXED PARAMETER
    !!!$     Slash

    !!!$ BETA MGS
    betamgs = 1d0
    WRITE (*,'(/a)',ADVANCE='no')'OS identification:'
    IF (INDEX ( version(5), 'Msys') /= 0) THEN
        PRINT*,' MS-OS'
        slash = '\'  !' \ is escape char for syntax highlights
    ELSE
        PRINT*,' Linux-OS'
        slash = '/'
    END IF

    !  CALL CALL get_environment_variable('DELIMITER',slash) ! seems a special C extension
    !!!$     Minimale "L1-ratio" (Grenze der "robust inversion")
    l1min = 1d0
    !!!$     ak        l1min = 1.2d0
    nrmsdm = 1d0
    !!!$     Art der Ruecktransformation
    !!!$     ak        swrtr = 1
    !!!$     Minimaler Quotient zweier aufeinanderfolgender Daten-RMS-Werte
    !!!$     ak Default
    !!!$     ak        mqrms = 1d-2
    !!!$     ak ERT 2002-2003 synth
    mqrms = 2d-2
    !!!$     ak        mqrms = 2d-2
    !!!$     ak Tank
    !!!$     ak        mqrms = 2d-2
    !!!$     ak MMAJ
    !!!$     ak        mqrms = 5d-2
    !!!$     CG-Epsilon
    eps = 1d-4
    !!!$     Mindest-step-length
    stpmin = 1d-3
    !!!$     Minimale stepsize (bdpar)
    bdmin = 1d-3
    !!!$     Regularisierungsparameter
    !!!$     ak Default
    nlam   = 30
    !!!$     ak Default
    fstart = 0.5d0
    fstop  = 0.9d0
    lamfix = 0.0D0
    llamf = 0
    !!!$     ak MMAJ
    !!!$     ak        fstart = 0.2d0
    !!!$     ak        fstop  = 0.8d0
    !!!$     ak Strasbrg/Werne/Grimberg
    !!!$     ak        fstart = 0.5d0
    !!!$     ak        fstop  = 0.8d0
    iseedpri = 0; modl_stdn = 0.; iseed = 1
    mswitch = 0
    !!!$#########################################################
    !!!$     Read in input values..

    fetxt = 'rall -> mswitch'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=98) mswitch

    98 fetxt = 'rall -> grid file'
    CALL read_comments(fpcfg)
    READ (fpcfg,'(a)',END=1001,err=999) delem
    CALL clear_string (delem)

    fetxt = 'rall -> electrode file'
    CALL read_comments(fpcfg)
    READ (fpcfg,'(a)',END=1001,err=999) delectr
    CALL clear_string (delectr)

    fetxt = 'rall -> meaurement file'
    CALL read_comments(fpcfg)
    READ (fpcfg,'(a)',END=1001,err=999) dstrom
    CALL clear_string (dstrom)

    fetxt = 'rall -> directory for inversion results'
    CALL read_comments(fpcfg)
    READ (fpcfg,'(a)',END=1001,err=999) ramd
    CALL clear_string (ramd)

    !!$! checks if dir exists and if not, create it
    !#if defined (__INTEL_COMPILER)
    !!$! check for the intel compiler..
    !#define macro_1  INQUIRE ( DIRECTORY=TRIM(ramd),EXIST= crtf)
    !#else
    !!$! other compilers go here
    !!$! here we may put #elif defined (__GFORTRAN__) as well
    !#define macro_1  INQUIRE ( FILE=TRIM(ramd),EXIST= crtf)
    !#endif
    ! ifort uses DIRECTORY for folders, so this is to be used than..
    ! INQUIRE ( DIRECTORY=TRIM(ramd),EXIST= crtf)

    !!$! workaround for compability issues with ifort..
    fetxt = TRIM(ramd)//slash//'tmp.check'
    crtf = .FALSE.
    !!$ test if you can open a file in the directory..
    OPEN (fprun,FILE=TRIM(fetxt),STATUS='replace',ERR=97)
    !!$ if you can, the directory exits and you can remove it safely
    CLOSE(fprun,STATUS='delete')
    !!$ set this switch to circumvent mkdir
    PRINT*,'writing inversion results into '//TRIM(ramd)
    crtf = .TRUE.
    97 IF (.NOT.crtf) THEN
        PRINT*,'Creating inversion directory '//TRIM(ramd)
        CALL SYSTEM ('mkdir '//TRIM(ramd))
    END IF
    fetxt = 'rall -> Difference inversion ?'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) ldiff

    fetxt = 'rall -> Diff. measurements'
    CALL read_comments(fpcfg)
    ! read measurement data for time 0
    READ (fpcfg,'(a)',END=1001,err=999) dd0
    CALL clear_string (dd0)

    fetxt = 'rall -> Diff. model (prior)'
    CALL read_comments(fpcfg)
    ! read model time 0
    READ (fpcfg,'(a)',END=1001,err=999) dm0
    CALL clear_string (dm0)

    fetxt = 'rall -> Diff. model response of prior'
    CALL read_comments(fpcfg)
    ! read forward response of model
    READ (fpcfg,'(a)',END=1001,err=999) dfm0
    CALL clear_string (dfm0)

    IF (dm0 /= '') THEN
        INQUIRE(FILE=TRIM(dm0),EXIST=lstart) ! prior model ?
        IF (lstart) THEN       ! set the starting model
            dstart = dm0
            PRINT*,'+ read prior:',ACHAR(9)//TRIM(dm0)
        ELSE
            PRINT*,'- omit prior (NO FILE):',ACHAR(9)//TRIM(dm0)
            dm0 = ''
        END IF
    END IF
    IF (lstart.AND.ldiff.AND.((dd0 == ''.AND.dfm0 == ''))) THEN
        PRINT*,'Prior model regularization !'
        lprior = .TRUE.        ! reference model regu only if there is no
        ldiff = .FALSE.        ! time difference inversion
    END IF
    !!!$     diff+>
    fetxt = 'trying noise model seed'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=99) iseedpri,modl_stdn
    !     hier landet man nur, wenn man iseed und modl_stdn angenommen hat
    !      lnse2 = .NOT.lprior       ! kein prior?
    !     Daten Rauschen unabhängig vom Fehlermodell?
    lnsepri = lstart          ! if we have seed and std we assume to add noise to prior
    PRINT*,'Prior model noise !'
    99 fetxt = 'rall -> Gitter nx'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) nx
    fetxt = 'rall -> (lamfix) Gitter nz'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) nz
    fetxt = 'rall -> Anisotropie /x'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) alfx
    fetxt = 'rall -> Anistotropie /y'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) alfz

    fetxt = 'rall -> Maximale Iterationen'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) itmax
    !!!$     ak        READ (fpcfg,*,end=1001,err=999) nrmsdm

    fetxt = 'rall -> DC/IP Inversion'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) ldc
    !!!$     ak        READ (fpcfg,*,end=1001,err=999) lsr

    fetxt = 'rall -> Robuste Inversion'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) lrobust
    IF (lrobust) PRINT*,'## Robust inversion ##'
    !!!$     ak        READ (fpcfg,*,end=1001,err=999) lpol

    fetxt = 'rall -> Finale Phasen Inversion'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) lfphai
    !!!$     ak        READ (fpcfg,*,end=1001,err=999) lindiv

    fetxt = 'rall -> Relativer Fehler Widerstand'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) stabw0

    fetxt = 'rall -> Absoluter Fehler Widerstand'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) stabm0

    fetxt = 'rall -> Phasenfehlerparameter A1'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) stabpA1

    fetxt = 'rall -> Phasenfehlerparameter B'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) stabpB

    fetxt = 'rall -> Relative Fehler Phasen'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) stabpA2

    fetxt = 'rall -> Absoluter Fehler Phasen (mRad)'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) stabp0

    fetxt = 'rall -> Homogenes Startmodell?'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) lrho0

    fetxt = 'rall -> rho_0'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) bet0

    fetxt = 'rall -> phase_0'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) pha0

    fetxt = 'rall -> Noch eine Inversion'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) lagain

    fetxt = 'rall -> 2D oder 2.5D ?'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) swrtr

    fetxt = 'rall -> weitere Quelle?'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) lsink

    fetxt = 'rall -> Nummer der Quelle'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) nsink

    fetxt = 'rall -> Randbedingungen ?'
    CALL read_comments(fpcfg)
    READ (fpcfg,*,END=1001,err=999) lrandb2

    fetxt = 'rall -> Datei mit Randwerten'
    CALL read_comments(fpcfg)
    READ (fpcfg,'(a80)',END=1001,err=999) drandb

    fetxt = 'triangularization switch'
    CALL read_comments(fpcfg)
    READ (fpcfg,'(I2)',END=100,err=100) ltri

    IF (BTEST(ltri,5)) THEN
        llamf = 1
        fetxt = 'rall -> fixed lam value'
        CALL read_comments(fpcfg)
        READ (fpcfg,*,END=104,err=104) lamfix
        GOTO 105
        104  lamfix = 1.0           ! default value for MGS
        BACKSPACE(fpcfg)

        105  PRINT*,'Fixing Lambda =', lamfix
        ltri = ltri - 2**5

        IF (BTEST(ltri,6)) THEN
            llamf = llamf + 2
            PRINT*,'NEW:: COOLING lambdas during inv'
            ltri = ltri - 2**6
        END IF
    END IF

    IF (ltri > 15) THEN ! exception for wrong ltri switch
        PRINT*,'WARNING, fix lambda switch has changed'
        PRINT*,'check ltri value (>15):',ltri
        STOP
    END IF

    lsto = (ltri == 15)

    GOTO 101

    100 BACKSPACE (fpcfg)

    101 IF (lsto) THEN
        PRINT*,'Stochastische Regularisierung'
        !     eps = eps*1d-2
    END IF
    IF (ltri > 4 .AND. ltri < 15) THEN
        fetxt = 'rall -> beta value'
        CALL read_comments(fpcfg)
        READ (fpcfg,*,END=102,err=102) betamgs
        GOTO 103
        102  betamgs = 0.1          ! default value for MGS
        BACKSPACE (fpcfg)

        103  PRINT*,'Regularisation with support stabilizer beta =',betamgs
    END IF

    IF (itmax == 0) PRINT*,' ####### Only precalcs, itmax==0 ###########'

    !!!$     check if the final phase should start with homogenous model
    lffhom = (stabp0 < 0)
    IF (lffhom) stabp0 = -stabp0

    !!!$ check if there is crt.noisemod containig noise info
    fetxt = 'crt.noisemod'
    INQUIRE(FILE=TRIM(fetxt),EXIST=lnse2)

    lnse = ( stabw0 < 0 )     ! couple error and noise model
    IF (lnse) THEN
        stabw0 = -stabw0 ! reset standard deviation to positive val
        IF (lnse2) PRINT*,'overriding seperate noise model'
        lnse2 = .FALSE.        ! overrides the lnse2 switch
        !!!$     copy error model into noise model
        nstabw0 = stabw0
        nstabm0 = stabm0
        nstabpA1 = stabpA1
        nstabpA2 = stabpA2
        nstabp0 = stabp0

        fetxt = 'rall -> seed'

        CALL read_comments(fpcfg)
        READ (fpcfg,*,END=106,err=106) iseed
        GOTO 107
        106  iseed = 1              ! default value for PRS
        BACKSPACE(fpcfg)
        WRITE (*,'(a)')' Rauschen Gekoppelt an Fehlermodell '
    END IF

    107 IF (lnse2) THEN
        fetxt = 'get noise model from crt.noisemod'
        CALL get_noisemodel(iseed,nstabw0,nstabm0,nstabpA1,&
             nstabpB,nstabpA2,nstabp0,errnr)

        IF (errnr /= 0) GOTO 999

        WRITE (*,'(a,I7)',ADVANCE='no')&
              'Entkoppeltes Daten Rauschen:: seed:',iseed

        lnse = .TRUE.          ! add noise
    END IF

    IF (lnse) THEN
        fetxt = 'write out noise model'
        CALL write_noisemodel(iseed,nstabw0,nstabm0,&
            nstabpA1,nstabpB,nstabpA2,nstabp0,errnr)
        IF (errnr /= 0) GOTO 999
    END IF


    IF ((nx<=0.OR.nz<=0).AND.ltri==0) ltri=1 ! at least L1-smoothness

    !!!$     Ggf. Fehlermeldungen
    IF (ltri==0.AND.(nx.LT.2.OR.nz.LT.2)) THEN
        fetxt = ' '
        errnr = 89
        GOTO 999
        !!!$  else if (alfx.le.0d0.or.alfz.le.0d0) then
        !!!$  fetxt = ' '
    !!!$  errnr = 96
    !!!$  goto 999
    ELSE IF (itmax<0.OR.itmax.GE.100) THEN
        fetxt = ' '
        errnr = 61
        GOTO 999
    ELSE IF (nrmsdm.LT.1d-12) THEN
        fetxt = ' '
        errnr = 62
        GOTO 999
        !!!$     else if (nlam.lt.0) then
        !!!$     fetxt = ' '
        !!!$     errnr = 83
        !!!$     goto 999
        !!!$     else if (fstart.gt.1d0.or.fstop.gt.1d0.or.
        !!!$     1           fstart.le.0d0.or.fstop.le.0d0.or.
        !!!$     1           fstart.gt.fstop) then
        !!!$     fetxt = ' '
        !!!$     errnr = 98
        !!!$     goto 999
    ELSE IF (stabw0.LE.0d0.OR.stabm0.LT.0d0) THEN
        fetxt = ' '
        errnr = 104
        GOTO 999
    ELSE IF (.NOT.ldc.AND.lfphai.AND.&
        ((stabp0.LT.0d0.OR.stabpA2.LT.0d0).OR. &
        ((stabp0 == 0d0).AND.(stabpA2 == 0d0).AND.(stabpA1 == 0d0)))) THEN
        fetxt = ' '
        errnr = 105
        GOTO 999
    ELSE IF (lrho0.AND.(bet0.LE.0d0.OR.&
        (.NOT.ldc.AND.dabs(pha0).GT.1d3*pi))) THEN
        fetxt = ' '
        errnr = 91
        GOTO 999
        !!!$     else if (mqrms.lt.0d0.or.mqrms.ge.1d0) then
        !!!$     fetxt = ' '
        !!!$     errnr = 64
        !!!$     goto 999
        !!!$     else if (lrobust.and.l1min.lt.1d0) then
        !!!$     fetxt = ' '
        !!!$     errnr = 90
        !!!$     goto 999
    END IF

!!$ RM >>
!!!$ assign all the logical switches and settings for the inversion
  lelerr = .NOT.lfphai.AND..NOT.ldc ! complex inversion only

!!!$     (mswitch) Mega switch testing..
  lsens = BTEST(mswitch,0)  ! +1 ueberdeckung schreiben
  lcov1 = BTEST(mswitch,1)  ! +2 posterior modell covariance matrix 1
  lres  = BTEST(mswitch,2)  ! +4 rsolution matrix berechnen
  lcov2 = BTEST(mswitch,3)  ! +8 posterior modell covariance matrix 2

  lgauss = BTEST (mswitch,4) ! +16 solve ols with Gauss elemination

  lelerr = BTEST (mswitch,5).OR.lelerr ! +32 overwrites previous lelerr

  IF (lelerr) PRINT*,'## using complex error ellipses ##'

  lphi0 = BTEST (mswitch,7) ! +128 forcing negative phase

  lsytop = BTEST (mswitch,8) ! +256 disables sy top check of
  !     no flow boundary electrodes for enhanced beta calculation (bsytop).
  !     This is useful for including topographical effects and should be used

  lvario = BTEST (mswitch,9) ! +512 calculate variogram

  lverb = BTEST (mswitch,10) ! +1024 Verbose output CG, daten, bnchbar..

  lverb_dat = BTEST (mswitch,11) ! +2048 writing out full resolution, covariance and cm0

  IF (lverb) WRITE(*,'(/a/)')' #  ## VERBOSE ## #'

  lres = (lres.OR.lcov2)    ! compute mcm2 on top of resolution
  lcov1 = (lres.OR.lcov1)   ! compute resolution by taking mcm1
!!!$
  lsens = .TRUE.            ! default immer coverages schreiben..
!!!$
  IF (lratio) THEN
     lrho0  = .TRUE.
     lstart = .FALSE.
     lphi0  = .FALSE.
     lpol   = .FALSE.
  END IF
!!!$     diff-        if (lstart) lrho0=.false.

  IF (lstart.OR.ldiff) lrho0=.FALSE.
!!!$     ak
  IF (ldiff) THEN
     ldc  = .TRUE.
     lpol = .FALSE.
  END IF
!!!$     diff+>
!!!$     ak        if (ldc.or.stabp0.ge.stabw0) lfphai=.false.
  IF (ldc) lfphai=.FALSE.
!!!$ << RM

!!!$ append path string (saved in ramd) and prepare
!!!$ output file names
  lnramd = INDEX(ramd,' ')-1
  dsigma = ramd(1:lnramd)//slash(1:1)//'rho.dat'
  dvolt  = ramd(1:lnramd)//slash(1:1)//'volt.dat'
  dsens  = ramd(1:lnramd)//slash(1:1)//'coverage.mag'

!!!$     Elementeinteilung einlesen
  IF (lverb) WRITE (*,'(a)',ADVANCE='no')ACHAR(13)//'reading grid'
  CALL relem(kanal,delem)
  IF (errnr.NE.0) GOTO 999

    !!! MW: read in decoupling
    INQUIRE(FILE=TRIM("decouplings.dat"),EXIST=decexi)
    IF (decexi) THEN
        WRITE(*,*) "Found decoupling file"

        OPEN(kanal, file=TRIM('decouplings.dat'),status='old')
        READ(kanal,*) decanz
        WRITE(*,*) "number of decouplings: ", decanz
        ALLOCATE (edecoup(decanz, 2),stat=errnr)
        ALLOCATE (edecstr(decanz),stat=errnr)
        DO j=1,decanz
            READ(kanal, *) edecoup(j, 1), edecoup(j, 2), edecstr(j)
            WRITE(*,*) "Input: ", edecoup(j, 1), edecoup(j, 2), edecstr(j)
        END DO

        CLOSE(kanal)
    ELSE
        decanz = 0
    END IF
    !!! decoupling end

    !!! MW: electrode capacitances
    INQUIRE(FILE=TRIM("electrode_capacitances.dat"), EXIST=elec_caps_file_exists)
    IF (elec_caps_file_exists) THEN
        WRITE(*,*) "Found electrode capacitances file"
        OPEN(kanal, file=TRIM('electrode_capacitances.dat'), status='old')
        READ(kanal,*) nr_elec_capacitances
        WRITE(*,*) "number of electrode capacitances: ", nr_elec_capacitances
        ALLOCATE (electrode_capacitances(nr_elec_capacitances), stat=errnr)
        DO j=1,nr_elec_capacitances
            READ(kanal, *) electrode_capacitances(j)
            WRITE(*,*) "Capacitance: ", j, electrode_capacitances(j)
        END DO
        CLOSE(kanal)
    ELSE
        nr_elec_capacitances = 0
    END IF
    !!! electrode capacitances end

  IF (ltri/=0) THEN
     manz = elanz           ! wichtig an dieser stelle..
     lvario = lvario.OR.lsto
  ELSE
!!!$     Modelleinteilung gemaess Elementeinteilung belegen
     manz = nx*nz           ! nur für strukturierte gitter
  END IF


  CALL bnachbar          ! blegt nachbar
  CALL besp_elem


  IF (lstart .OR. ldiff .OR. lprior) THEN
     ALLOCATE (m0(manz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation m0'
        errnr = 94
        GOTO 999
     END IF
  END IF
!!$  lvario = lvario.OR. &       ! if already set or
!!$       (itmax == 0).AND.(lstart.OR.lprior) ! analyse any prior

  IF (lvario) CALL set_vario (nx,alfx,alfz,esp_mit,esp_med) ! nx is than
  !     the variogram and covariance function type, see variomodel.f90

  IF (manz.NE.elanz) THEN
     fetxt = 'manz /= elanz .. is not implemented yet'
     errnr = 50
     GOTO 999
  END IF
  !     !$ get memory for mnr..
  ALLOCATE (mnr(elanz),stat=errnr)
  IF (errnr /= 0) THEN
     fetxt = 'Error memory allocation mnr failed'
     errnr = 94
     GOTO 999
  END IF
  !     !$ set mnr.. this may be altered if we have zonal approach..
  DO i=1,elanz
     mnr(i) = i
  END DO
  !     !$ all the model mapping is than beased on a new numbering..
  !     !$ zonal approach ?

!!!$     Maximale Anzahl an CG-steps setzen
!!!$     ak        ncgmax = manz
!!!$  ncgmax = manz / 2         ! useful for small scale model variations
  ncgmax = manz         ! useful for small scale model variations
  !     for normal smooth and damping we usually need fewer CG iterations;
  !     because the model variations are of bigger scale size
  IF (ltri < 5) ncgmax = ncgmax / 10
!!!$     Elektrodenverteilung und Daten einlesen sowie Wellenzahlwerte
!!!$     bestimmen

  CALL relectr(kanal,delectr)
  IF (errnr.NE.0) GOTO 999

  IF (lsink) THEN
     IF (nsink > sanz) THEN
        PRINT*,'Sink node > grid nodes'
        errnr = 3
        GOTO 999
     END IF
     WRITE(*,'(/A,I5,2F12.3/)')'Fictious sink @ node ',&
          nsink,sx(snr(nsink)),sy(snr(nsink))
!!!$         WRITE(fpinv,'(A,I5,2F12.3)')'Fictious sink @ node ',
!!!$     1        nsink,sx(snr(nsink)),sy(snr(nsink))
  END IF

  CALL rdati (kanal,dstrom)
  IF (errnr.NE.0) GOTO 999



!!$>> RM
  fetxt = 'crt.lamnull'
  INQUIRE(FILE=TRIM(fetxt),EXIST=exi)
  IF (exi) THEN
!!!$ Overwriting lamfix with crt.lamnull content
     WRITE (*,'(/a)')'overwriting lamfix with content of '//TRIM(fetxt)
     OPEN(kanal,FILE=TRIM(fetxt),ACCESS='sequential',STATUS='old')
     READ(kanal,*,END=1001,ERR=999)lamnull_cri
     PRINT*,'++ Lambda_0(CRI) = ',REAL(lamnull_cri)
     READ(kanal,*,END=30,ERR=30)lamnull_fpi
     PRINT*,'++ Lambda_0(FPI) = ',REAL(lamnull_fpi)
     GOTO 31
30   lamnull_fpi = 0d0
     IF (BTEST(llamf,0)) lamnull_fpi = lamfix ! in case of llamf we possibly
!!!$ do not want lam0 search at the beginning of FPI
31   CLOSE(kanal)
     PRINT*
  ELSE IF (BTEST(llamf,0)) THEN
     WRITE (*,'(/a,G12.4/)')'Presetting lamnull with lamfix ',REAL(lamfix)
     lamnull_cri = lamfix
     lamnull_fpi = lamfix
  ELSE IF (nz == -1) THEN
     lamnull_cri = DBLE(MAX(manz,nanz))
     WRITE (*,'(/a,G12.4/)')'+++ Lambda_0(CRI) =',REAL(lamnull_cri)
     lamnull_fpi = 0d0
  ELSE IF (nz < 0) THEN
     lamnull_cri = ABS(DBLE(nz))
     WRITE (*,'(/a,G12.4/)')'+++ Lambda_0(CRI) =',REAL(lamnull_cri)
     lamnull_fpi = 0d0
  ELSE
     WRITE (*,'(/a/)')'+++ Found no presettings for lambda_0 (default)'
     lamnull_cri = 0d0
     lamnull_fpi = 0d0
  END IF
  PRINT*,'Saving lamba presettings -> '//TRIM(fetxt)
  OPEN (kanal,FILE=TRIM(fetxt),ACCESS='sequential',STATUS='replace')
  WRITE (kanal,*)lamnull_cri
  WRITE (kanal,*)lamnull_fpi
  CLOSE (kanal)

!!$<< RM


  IF (ldc) THEN
     WRITE (*,'(/a/)')'++ (DC) Setting magnitude error'
     wmatd = wmatdr
  ELSE

     IF (lelerr) THEN
        WRITE (*,'(/a/)')'++ (CRI) Setting complex error ellipse'
        wmatd = wmatd_cri
     ELSE
        WRITE (*,'(/a/)')'++ (CRI) Setting complex error of magnitude'
        wmatd = wmatdr
     END IF
  END IF

  IF (swrtr.EQ.0) THEN
     lsr    = .FALSE.
     kwnanz = 1
     ALLOCATE (kwn(kwnanz),kwnwi(kwnanz),stat=errnr)
     IF (errnr /= 0) THEN
        fetxt = 'Error memory allocation kwn'
        errnr = 94
        GOTO 999
     END IF
     kwn = 0d0; kwnwi = 0D0
     DO i=1,typanz
        IF (typ(i) == 11) THEN
           fetxt = 'in 2D keine gemischten RB'
           PRINT*,TRIM(fetxt)
           errnr = 110
           GOTO 999
        END IF
     END DO
     IF (.NOT.lrandb2) THEN
        WRITE (*,'(//a,t33,a)')'2D without Dirichlet nodes','setting k=1e-6'
        kwn = 1d-6  ! make sure A is still pos definite
     END IF
  ELSE
     CALL rwaven()
     IF (errnr.NE.0) GOTO 999
  END IF

!!!$     read boundary values
  IF (lrandb2) THEN
     CALL rrandb(kanal,drandb)
     IF (errnr.NE.0) GOTO 999
  END IF

    !!!$     diff+<
    IF (ldiff) THEN
        ALLOCATE (d0(nanz),fm0(nanz),stat=errnr)
        IF (errnr /= 0) THEN
            fetxt = 'Error memory allocation diff data '
            errnr = 94
            GOTO 999
        END IF
        OPEN(kanal,file=TRIM(dd0),status='old')
        READ(kanal,*) nanz0
        READ(kanal,*,err=999) elec1
        BACKSPACE(kanal)

        elec3=elec1-10000      ! are we still positive?
        ! testen, welches Format benutzt wird
        ! crtf == True  - benutze 10002 40003 Format für Elektrodenkennungen
        crtf=(elec3 > 0)       ! crtomo konform?

        ALLOCATE (dum(nanz0),dum2(nanz0),idum(nanz0),&
            ic(nanz0),ip(nanz0),stat=errnr)
        IF (errnr /= 0) THEN
            fetxt = 'Error memory allocation dum'
            errnr = 94
            GOTO 999
        END IF

        ! read time 0 data
        DO j=1,nanz0
            IF (crtf) THEN
                READ(kanal,*) ic(j),ip(j),dum(j)
            ELSE
                READ(kanal,*) elec1,elec2,elec3,elec4,dum(j)
                ic(j) = elec1*10000 + elec2
                ip(j) = elec3*10000 + elec4
            END IF
        END DO
        CLOSE(kanal)

        ! read forward response of time-0 model
        OPEN(kanal,file=TRIM(dfm0),status='old')
        READ(kanal,*)
        DO j=1,nanz0
            ! read current and voltage electrodes (ignored later on) as i,i
            ! read dum2 == magnitudes
            ! read idum == bool switch indicating invalid forward responses
            !      i.e. because of sign problems with R (remember: we do not
            !      switch any electrodes to correct signs)
            READ(kanal,*) i,i,dum2(j),idum(j)
        END DO
        CLOSE(kanal)

        !
        j0 = 0
        i  = 0
        10   i  = i+1
        j = j0
        20   j = j+1
        !
        IF (strnr(i).EQ.ic(j).AND.vnr(i).EQ.ip(j).AND.idum(j).EQ.1) THEN
            !!!$     nur falls jede Messkonfiguration nur einmal!
            !!!$     j0     = j
            d0(i)  = dcmplx(-dlog(dum(j)),0d0)
            fm0(i) = dcmplx(-dlog(dum2(j)),0d0)
        ELSE IF (j.LT.nanz0) THEN
            GOTO 20
        ELSE
            WRITE(fprun,'(i7,1x,i7,a12)',err=999)strnr(i),vnr(i),' : discarded'

            nanz = nanz-1
            DO j=i,nanz
                strnr(j) = strnr(j+1)
                vnr(j)   = vnr(j+1)
                dat(j)   = dat(j+1)
                wmatd(j) = wmatd(j+1)
                IF (lfphai) wmatdp(j)=wmatdp(j+1)
                !!!$     nicht notwendig, da Werte eh alle 1
                !!!$     wdfak(j) = wdfak(j+1)
            END DO
            i = i-1
        END IF
        IF (i.LT.nanz) GOTO 10

        ! read start model
        OPEN(kanal,file=TRIM(dm0),status='old')
        READ(kanal,*)
        DO j=1,elanz
            READ(kanal,*) dum3,dum3,dum3
            m0(mnr(j)) = dcmplx(-dlog(1d1)*dum3,0d0)
        END DO
        CLOSE(kanal)
        DEALLOCATE (dum,dum2,idum,ic,ip)
    END IF ! ldiff
    !!!$     diff+>

    errnr = 0

    RETURN

    !!!$:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    !!!$     Fehlermeldungen

    999 RETURN

    1001 errnr = 2
        RETURN

END SUBROUTINE rall
