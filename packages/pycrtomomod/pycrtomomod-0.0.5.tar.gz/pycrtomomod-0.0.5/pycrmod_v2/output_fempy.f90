module output_fempy
    ! modeling output of CRMod
    ! this module is used for the _no_fs version that tries to not touch the file system

    ! four point spreads
    integer(kind=4),dimension(:),allocatable,public :: out_ab
    integer(kind=4),dimension(:),allocatable,public :: out_mn
    real(kind=8),dimension(:),allocatable,public :: out_rmag
    real(kind=8),dimension(:),allocatable,public :: out_rpha_mrad

    ! node potential values
    real(kind=8),dimension(:),allocatable,public :: out_sx
    real(kind=8),dimension(:),allocatable,public :: out_dy
    real(kind=8),dimension(:),allocatable,public :: out_potmag
    real(kind=8),dimension(:),allocatable,public :: out_potrpha

    ! sensitivities
    real(kind=8),dimension(:,:),allocatable,public :: out_sens_rmag

    contains

end module output_fempy
