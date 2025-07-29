subroutine parfit(fa,fb,fc,fmin,smin)

!!!$     Unterprogramm fittet Parabel durch die drei Punkte (0,fa), (0.5,fb)
!!!$     und (1,fc) und liefert Abszisse des Minimums in 'step', falls Minimum
!!!$     zwischen 0 und 1 existiert und Minimum < fmin. Sonst geeignete lineare
!!!$     Interpolation auf fmin.
!!!$     (Formel aus 'Numerical Recipes' (S. 395, eq. (10.2.1)))

!!!$     Andreas Kemna                                            28-May-1996
!!!$     Letzte Aenderung   22-Sep-1998

!!!$.....................................................................

  USE konvmod,ONLY:step

  IMPLICIT none


!!!$.....................................................................

!!!$     EIN-/AUSGABEPARAMETER:

!!!$     Funktionswerte, Grenzwerte
  REAL (KIND(0D0))  :: fa,fb,fc,fmin,smin

!!!$.....................................................................

!!!$     PROGRAMMINTERNE PARAMETER:

!!!$     x-Werte
  REAL (KIND(0D0))  :: a,b,c

!!!$     Hilfsvariablen
  REAL (KIND(0D0))  :: bma,bmc,fbmfc,fbmfa,zaehler,nenner

!!!$.....................................................................

  a = 0d0
  b = 0.5d0
  c = 1d0

  if (fa.gt.fb) then

     if (fb.le.fc) then

        if (fb.le.fmin) then
           if (fa.lt.fmin.and.fc.gt.fa) then

!!!$     Zwischen 'fb' und 'fc' linear auf fmin interpolieren
              step = b + (c-b)*(fmin-fb)/(fc-fb)
           else 

!!!$     Zwischen 'fa' und 'fb' linear auf fmin interpolieren
              step = a + (b-a)*(fmin-fa)/(fb-fa)
           end if
        else

!!!$     Parabolische Interpolation auf Minimum
           bma     = b-a
           fbmfc   = fb-fc
           bmc     = b-c
           fbmfa   = fb-fa
           zaehler = bma*bma*fbmfc - bmc*bmc*fbmfa
           nenner  = bma*fbmfc - bmc*fbmfa
           step    = b - zaehler/(2d0*nenner)
        end if

     else if (fb.gt.fc) then

        if (fb.le.fmin) then

!!!$     Zwischen 'fa' und 'fb' linear auf fmin interpolieren
           step = a + (b-a)*(fmin-fa)/(fb-fa)
        else if (fc.le.fmin) then

!!!$     Zwischen 'fb' und 'fc' linear auf fmin interpolieren
           step = b + (c-b)*(fmin-fb)/(fc-fb)
        else

!!!$     Full step-length
           step = c
        end if

     end if

  else if (fa.lt.fb) then

     if (fb.ge.fc) then

        if (fb.ge.fmin) then
           if (fa.gt.fmin.and.fc.lt.fa) then

!!!$     Zwischen 'fb' und 'fc' linear auf fmin interpolieren
              step = b + (c-b)*(fmin-fb)/(fc-fb)
           else 

!!!$     Zwischen 'fa' und 'fb' linear auf fmin interpolieren
              step = a + (b-a)*(fmin-fa)/(fb-fa)
           end if
        else

!!!$     Parabolische Interpolation auf Maximum
           bma     = b-a
           fbmfc   = fb-fc
           bmc     = b-c
           fbmfa   = fb-fa
           zaehler = bma*bma*fbmfc - bmc*bmc*fbmfa
           nenner  = bma*fbmfc - bmc*fbmfa
           step    = b - zaehler/(2d0*nenner)
        end if

     else if (fb.lt.fc) then

        if (fb.ge.fmin) then

!!!$     Zwischen 'fa' und 'fb' linear auf fmin interpolieren
           step = a + (b-a)*(fmin-fa)/(fb-fa)
        else if (fc.ge.fmin) then

!!!$     Zwischen 'fb' und 'fc' linear auf fmin interpolieren
           step = b + (c-b)*(fmin-fb)/(fc-fb)
        else

!!!$     Full step-length
           step = c
        end if

     end if

  else if (fa.eq.fb) then

     if (fb.gt.fc) then

        if (fb.lt.fmin) then

!!!$     Parabolische Interpolation auf Maximum
           bma     = b-a
           fbmfc   = fb-fc
           bmc     = b-c
           fbmfa   = fb-fa
           zaehler = bma*bma*fbmfc - bmc*bmc*fbmfa
           nenner  = bma*fbmfc - bmc*fbmfa
           step    = b - zaehler/(2d0*nenner)
        else if (fc.le.fmin) then

!!!$     Zwischen 'fb' und 'fc' linear auf fmin interpolieren
           step = b + (c-b)*(fmin-fb)/(fc-fb)
        else

!!!$     Full step-length
           step = c
        end if

     else if (fb.lt.fc) then

        if (fb.gt.fmin) then

!!!$     Parabolische Interpolation auf Minimum
           bma     = b-a
           fbmfc   = fb-fc
           bmc     = b-c
           fbmfa   = fb-fa
           zaehler = bma*bma*fbmfc - bmc*bmc*fbmfa
           nenner  = bma*fbmfc - bmc*fbmfa
           step    = b - zaehler/(2d0*nenner)
        else if (fc.ge.fmin) then

!!!$     Zwischen 'fb' und 'fc' linear auf fmin interpolieren
           step = b + (c-b)*(fmin-fb)/(fc-fb)
        else

!!!$     Full step-length
           step = c
        end if

     else if (fb.eq.fc) then

!!!$     Mindest-step-length
        step = smin
     end if

  end if

!!!$     Genzen einhalten (wegen Möglichkeit der linearen "Extrapolation")
  step = dmax1(smin,step)
  step = dmin1(c,step)

  return
end subroutine parfit
