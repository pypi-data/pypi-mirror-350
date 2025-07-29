!> \file elem8.f90
!> \brief form functions of quadrilateral area elements (e.g., rectangles)
!> \details Kemna (1995): The stiffness matrix contribution of a quadrilateral element \f$ G^{(j)}\f$ consisting of 4 individual triangles with a linear approach, \f$ G^{(j_1)},..., G^{(j_4)}\f$ is \f$ \sigma_j S^{(j)} \f$, where
!> \f[ S^{(j)} = \sum_{m=1}^4 \left( S_1^{(j_m)} + k^2 S_2^{(j_m)} \right) \f]
!> This requires the four triangles to have the identical conductivities \f$ \sigma \f$. 
!>
!> By analogy with <I> elem3 </I>, the  global \f$ n_k \times n_k \f$ stiffness matrix \f$ S^{(j)} \f$ with the node values \f$ \tilde \phi_{i_1 (j)}, ,..., \tilde \phi_{i_5 (j)} \f$ can be transformed into a \f$ 5 \times 5 \f$ matrix \f$ S^{'(j)} \f$:
!> \f[ (s^{'(j)})_{\kappa \lambda} = (s^{(j)})_{m n} \f]
!> with \f$ m=i_\kappa(j) \f$ and \f$ n=i_\lambda (j) \f$, \f$ \kappa, \lambda \in \{ 1,...,5 \} \f$ 
!> \image html elem8_sketch.png "Assembled quadrilateral element"
!> The node \f$ i_5 (j) \f$ is an internal node of the quadrilateral element in the above figure. Generally, due to the underlying extremum prinviple, it is possible to substitude internal node values by the corresponding element boundary values (Schwarz 1991). This means that prior to solving the Finite Element equation, \f$ \tilde \phi_{i_5(j)} \f$ can be eliminated. The process is named <I> condensation </I> and involves the transformation into \f$ S_*^{'(j)} \f$. The assembled quadrilateral element contribution yields
!> \f[ (s_*^{'(j)})_{\kappa\lambda} = (s^{'(j)})_{\kappa\lambda} - \frac{(s^{'(j)})_{\kappa 5}} (s^{'(j)})_{5 \lambda}{(s^{'(j)})_{55}} \f]
!> with \f$ \kappa, \lambda \in \{ 1,...,5 \}  \f$. The corresponding transformation to the globals stiffness matrix requires the coordinates of the four nodes and their values, \f$ \tilde \phi_{i_1(j)}, ..., \tilde \phi_{i_5(j)} \f$, and the base matrices \f$ U_1,...,U_4 \f$ of the triangle elements. Finally, \f$ \sigma \S_*^{(j)} \f$ is the total contribution of the quadrilateral element to the FE stiffness matrix.

!> @author Andreas Kemna
!> @date 10/11/1993, last change 1/26/1998

subroutine elem8(kelmas,kelve,kwert,max_nr_element_nodes)

!     Unterprogramm liefert die Elementmatrix 'kelmas(4,4)' und den Element-
!     vektor 'kelve(4)' fuer ein zusammengesetztes Viereckelement
!     (vier Teildreiecke mit linearem Ansatz) ( Elementtyp Nr.8 ).

!     Andreas Kemna                                            11-Oct-1993
!     Letzte Aenderung   26-Jan-1998

!.....................................................................

  USE elemmod,only:xk,yk
  USE errmod

  IMPLICIT none


!.....................................................................
!> element contribution after condensation
  REAL(KIND(0D0)),DIMENSION(max_nr_element_nodes,max_nr_element_nodes) :: kelmas

!> element vector after condensation
  REAL(KIND(0D0)),DIMENSION(max_nr_element_nodes)       :: kelve

!> wave number
  REAL(KIND(0D0))                        :: kwert

!> unused
  INTEGER (KIND = 4)                     :: max_nr_element_nodes

!.....................................................................

!     PROGRAMMINTERNE PARAMETER:

!     Hilfskoordinaten
  REAL (KIND(0D0))    ::     xkdum(5),ykdum(5)

!     Beteiligte Knoten des zusammengesetzten Elements am Teildreieck
  INTEGER (KIND = 4)  ::     ik(3)

!     Elementmatrizen vor der Kondensation
  REAL (KIND(0D0))    ::     elmas(5,5),elmam(5,5)

!     Elementvektor vor der Kondensation
  REAL (KIND(0D0))    ::     elve(5)

!     Indexvariablen
  INTEGER (KIND = 4)  ::     i,j,k

!     Grundelementmatrizen
  INTEGER (KIND = 4)  ::     s1(3,3),s2(3,3),s3(3,3),s4(3,3)

!     Grundelementvektor
  INTEGER (KIND = 4)  ::     sb(3)

!     Hilfsvariablen
  REAL (KIND(0D0))    ::     x21,x31,y21,y31,det,a,b,c,a1,a2

!.....................................................................

  data s1/1,-1,0,-1,1,0,0,0,0/
  data s2/2,-1,-1,-1,0,1,-1,1,0/
  data s3/1,0,-1,0,0,0,-1,0,1/
  data s4/2,1,1,1,2,1,1,1,2/
  data sb/1,1,1/

!     Elementmatrix bzw. -vektor des zusammengesetzten Elements gleich
!     Null setzen
  do i=1,5
     elve(i) = 0d0

     do j=1,5
        elmas(i,j) = 0d0
        elmam(i,j) = 0d0
     end do
  end do

!     Hilfskoordinaten bestimmen
  a1 = xk(3)-xk(1)
  a2 = xk(4)-xk(2)

!     Ggf. Fehlermeldung
  if (dabs(a1).le.1d-12.or.dabs(a2).le.1d-12) then
     fetxt = ' '
!     ak            write(fetxt(1:20),'(g20.5)') dabs(a1)
!     ak            write(fetxt(26:45),'(g20.5)') dabs(a2)
     errnr = 26
     goto 1000
  end if

  a1 = (yk(3)-yk(1))/a1
  a2 = (yk(4)-yk(2))/a2

!     Ggf. Fehlermeldung
  if (dabs(a1-a2).le.1d-12) then
     fetxt = ' '
!     ak            write(fetxt(1:20),'(g20.5)') dabs(a1-a2)
     errnr = 26
     goto 1000
  end if

  xkdum(5) = (a1*xk(1)-yk(1)-a2*xk(2)+yk(2))/(a1-a2)
  ykdum(5) = yk(1)+a1*(xkdum(5)-xk(1))

!     Restlichen Koordinaten umspeichern
  do i=1,4
     xkdum(i) = xk(i)
     ykdum(i) = yk(i)
  end do

!     Beitraege der Teilelemente aufaddieren
  do k=1,4

!     Beteiligte Knotenpunkte definieren
     if (k.eq.1) then
        ik(1) = 1
        ik(2) = 2
        ik(3) = 5
     else if (k.eq.2) then
        ik(1) = 2
        ik(2) = 3
        ik(3) = 5
     else if (k.eq.3) then
        ik(1) = 5
        ik(2) = 3
        ik(3) = 4
     else if (k.eq.4) then
        ik(1) = 1
        ik(2) = 5
        ik(3) = 4
     end if

     x21 = xkdum(ik(2)) - xkdum(ik(1))
     x31 = xkdum(ik(3)) - xkdum(ik(1))
     y21 = ykdum(ik(2)) - ykdum(ik(1))
     y31 = ykdum(ik(3)) - ykdum(ik(1))
     det = x21*y31 - x31*y21

!     Ggf. Fehlermeldung
     if (det.le.1d-12) then
        fetxt = ' '
        write(fetxt(1:20),'(g20.5)') det
        errnr = 26
        goto 1000
     end if

     a =   (x31*x31 + y31*y31) / det
     b = - (x31*x21 + y31*y21) / det
     c =   (x21*x21 + y21*y21) / det

     do i=1,3
        elve(ik(i)) = elve(ik(i)) + det * dble(sb(i)) / 6d0

        do j=1,3
           elmas(ik(i),ik(j)) = elmas(ik(i),ik(j)) + &
                (a*dble(s1(i,j)) + b*dble(s2(i,j)) + &
                c*dble(s3(i,j))) / 2d0
           elmam(ik(i),ik(j)) = elmam(ik(i),ik(j)) + &
                det * dble(s4(i,j)) / 2.4d1
        end do
     end do
  end do

!     Kondensationsschritt
  do i=1,5
     do j=1,5
        elmas(i,j) = elmas(i,j) + kwert*kwert*elmam(i,j)
     end do
  end do

  do i=1,4
     kelve(i) = elve(i) - elmas(i,5)*elve(5)/elmas(5,5)

     do j=1,4
        kelmas(i,j) = elmas(i,j) - elmas(i,5)*elmas(5,j)/elmas(5,5)
     end do
  end do

  errnr = 0
  return

!:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

!     Fehlermeldungen

1000 return

end subroutine elem8
